import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Use DATABASE_URL env if provided, else sqlite file
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./aml.db")

# For sqlite needed connect args
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    customer_id = Column(String)
    amount = Column(Float)
    counterparty_country = Column(String)
    is_international = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    risk_score = Column(Float)
    label = Column(String)
    reasons = Column(String)  # comma-separated

# create tables
Base.metadata.create_all(bind=engine)
