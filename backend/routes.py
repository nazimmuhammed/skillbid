from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db, Task, Bid, Transaction, AgentEarnings
from agents.orchestrator import Orchestrator
from payments.circle import send_payment, get_wallet_balance
from datetime import datetime
import uuid

router = APIRouter()
orchestrator = Orchestrator()

@router.post("/task")
async def submit_task(payload: dict, db: Session = Depends(get_db)):
    description = payload.get("description")
    max_budget = payload.get("max_budget", 0.01)

    # Save task to DB
    task = Task(description=description, max_budget=max_budget, status="bidding")
    db.add(task)
    db.commit()
    db.refresh(task)

    # Collect bids from all agents
    bids = orchestrator.collect_bids(description)

    # Save bids to DB
    for bid in bids:
        b = Bid(task_id=task.id, agent_name=bid["agent_name"], bid_amount=bid["bid_amount"])
        db.add(b)
    db.commit()

    # Pick winner
    winner = orchestrator.pick_winner(bids)
    winning_agent = orchestrator.get_agent(winner["agent_name"])

    # Execute task
    result = winning_agent.execute(description)

    # Send payment
    payment = send_payment("orchestrator", winner["agent_name"], winner["bid_amount"])

    # Save transaction
    tx = Transaction(
        task_id=task.id,
        from_wallet=winner["agent_name"],
        to_wallet=winner["agent_name"],
        amount=winner["bid_amount"],
        arc_tx_hash=payment.get("tx_hash"),
        status="confirmed"
    )
    db.add(tx)

    # Update agent earnings
    earnings = db.query(AgentEarnings).filter_by(agent_name=winner["agent_name"]).first()
    if not earnings:
        earnings = AgentEarnings(agent_name=winner["agent_name"], total_earned=0.0, tasks_completed=0)
        db.add(earnings)
    earnings.total_earned += winner["bid_amount"]
    earnings.tasks_completed += 1

    # Update task status
    task.status = "completed"
    task.winner_agent = winner["agent_name"]
    db.commit()

    return {
        "task_id": task.id,
        "description": description,
        "bids": bids,
        "winner": winner["agent_name"],
        "amount_paid": winner["bid_amount"],
        "tx_hash": payment.get("tx_hash"),
        "simulated": payment.get("simulated", True),
        "result": result
    }

@router.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).order_by(Task.created_at.desc()).limit(50).all()
    return [{"id": t.id, "description": t.description, "status": t.status, "winner": t.winner_agent, "created_at": str(t.created_at)} for t in tasks]

@router.get("/transactions")
def get_transactions(db: Session = Depends(get_db)):
    txs = db.query(Transaction).order_by(Transaction.created_at.desc()).limit(50).all()
    return [{"id": t.id, "task_id": t.task_id, "amount": t.amount, "tx_hash": t.arc_tx_hash, "status": t.status, "created_at": str(t.created_at)} for t in txs]

@router.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    agents = db.query(AgentEarnings).order_by(AgentEarnings.total_earned.desc()).all()
    return [{"agent": a.agent_name, "total_earned": a.total_earned, "tasks_completed": a.tasks_completed} for a in agents]

@router.get("/balances")
def get_balances():
    agents = ["orchestrator", "summarizer", "translator", "sentiment"]
    balances = {}
    for agent in agents:
        balances[agent] = get_wallet_balance(agent)
    return balances

@router.get("/bids/{task_id}")
def get_bids(task_id: int, db: Session = Depends(get_db)):
    bids = db.query(Bid).filter_by(task_id=task_id).all()
    return [{"agent": b.agent_name, "amount": b.bid_amount} for b in bids]