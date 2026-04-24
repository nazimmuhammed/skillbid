from agents.summarizer import SummarizerAgent
from agents.translator import TranslatorAgent
from agents.sentiment import SentimentAgent

class Orchestrator:
    def __init__(self):
        self.agents = [
            SummarizerAgent(),
            TranslatorAgent(),
            SentimentAgent()
        ]
    
    def collect_bids(self, task_description: str) -> list:
        bids = []
        for agent in self.agents:
            bid_amount = agent.get_bid(task_description)
            bids.append({
                "agent_name": agent.name,
                "bid_amount": bid_amount
            })
            print(f"  {agent.name} bids ${bid_amount}")
        return bids
    
    def pick_winner(self, bids: list) -> dict:
        # Cheapest bid wins
        winner = min(bids, key=lambda x: x["bid_amount"])
        print(f"  Winner: {winner['agent_name']} at ${winner['bid_amount']}")
        return winner
    
    def get_agent(self, agent_name: str):
        for agent in self.agents:
            if agent.name == agent_name:
                return agent
        return None
    
    def run(self, task_description: str) -> dict:
        print(f"\n Task: {task_description}")
        
        # Step 1: Collect bids
        print("\n Collecting bids...")
        bids = self.collect_bids(task_description)
        
        # Step 2: Pick winner
        print("\n Picking winner...")
        winner = self.pick_winner(bids)
        
        # Step 3: Execute task
        print(f"\n Executing task with {winner['agent_name']}...")
        winning_agent = self.get_agent(winner["agent_name"])
        result = winning_agent.execute(task_description)
        
        return {
            "task": task_description,
            "bids": bids,
            "winner": winner["agent_name"],
            "amount_paid": winner["bid_amount"],
            "result": result
        }