from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine("sqlite:///skillbid.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text)
    max_budget = Column(Float)
    status = Column(String, default="open")
    winner_agent = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Bid(Base):
    __tablename__ = "bids"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer)
    agent_name = Column(String)
    bid_amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer)
    from_wallet = Column(String)
    to_wallet = Column(String)
    amount = Column(Float)
    arc_tx_hash = Column(String, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

class AgentEarnings(Base):
    __tablename__ = "agent_earnings"
    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String, unique=True)
    total_earned = Column(Float, default=0.0)
    tasks_completed = Column(Integer, default=0)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()