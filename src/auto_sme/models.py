"""SQLAlchemy models for AutoSME."""
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, MetaData
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
    product_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True)
    description = Column(String, nullable=False)
    type = Column(String, nullable=False)
    params = Column(String, nullable=True)  # JSON string
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

class OptOut(Base):
    __tablename__ = "optouts"

    phone = Column(String, primary_key=True)
    opted_out_at = Column(DateTime, default=datetime.utcnow)
