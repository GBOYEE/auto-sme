"""SQLAlchemy models for AutoSME."""
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    stock = Column(Integer, default=0)
    low_stock_threshold = Column(Integer, default=10)
    created_at = Column(DateTime, default=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True)
    customer_phone = Column(String, nullable=False)
    customer_name = Column(String, nullable=True)
    items = Column(JSON, nullable=False)  # List[dict]
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    cron = Column(String, nullable=True)
    action = Column(String, nullable=False)
    payload = Column(JSON, nullable=True)  # dict
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

class OptOut(Base):
    __tablename__ = "optouts"

    phone = Column(String, primary_key=True)
    opted_out_at = Column(DateTime, default=datetime.utcnow)
