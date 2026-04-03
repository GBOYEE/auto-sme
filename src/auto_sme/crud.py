"""CRUD operations for AutoSME."""
from datetime import datetime
from typing import Optional, List
import uuid
from sqlalchemy.orm import Session
from .models import Product, Order, Task, OptOut

# Products
def create_product(db: Session, name: str, price: float, unit: str, stock: int = 0, low_stock_threshold: int = 10) -> Product:
    prod = Product(
        name=name,
        price=price,
        unit=unit,
        stock=stock,
        low_stock_threshold=low_stock_threshold,
        created_at=datetime.utcnow()
    )
    db.add(prod)
    db.commit()
    db.refresh(prod)
    return prod

def get_products(db: Session) -> List[Product]:
    return db.query(Product).all()

def adjust_stock(db: Session, product_id: str, delta: int) -> Optional[Product]:
    prod = db.query(Product).filter(Product.id == product_id).first()
    if not prod:
        return None
    prod.stock = max(0, prod.stock + delta)
    db.commit()
    db.refresh(prod)
    return prod

# Orders
def create_order(db: Session, customer_phone: str, items: List[dict], customer_name: Optional[str] = None) -> Order:
    total = sum(item["quantity"] * item["unit_price"] for item in items)
    order = Order(
        id=str(uuid.uuid4()),
        customer_phone=customer_phone,
        customer_name=customer_name,
        items=items,
        total_amount=total,
        status="pending",
        created_at=datetime.utcnow()
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def get_orders(db: Session) -> List[Order]:
    return db.query(Order).all()

def update_order_status(db: Session, order_id: str, status: str) -> Optional[Order]:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None
    order.status = status
    db.commit()
    db.refresh(order)
    return order

# Tasks
def create_task(db: Session, name: str, cron: str, action: str, payload: Optional[dict] = None) -> Task:
    import uuid
    task = Task(
        id=str(uuid.uuid4()),
        name=name,
        cron=cron,
        action=action,
        payload=payload or {},
        created_at=datetime.utcnow()
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_tasks(db: Session, status: Optional[str] = None) -> List[Task]:
    query = db.query(Task)
    if status == "active":
        # Simple filter: tasks with a cron string are considered active
        query = query.filter(Task.cron.isnot(None))
    return query.all()

# Opt-outs
def opt_out(db: Session, phone: str) -> OptOut:
    opt = OptOut(phone=phone, opted_out_at=datetime.utcnow())
    db.add(opt)
    db.commit()
    db.refresh(opt)
    return opt

def is_opted_out(db: Session, phone: str) -> bool:
    return db.query(OptOut).filter(OptOut.phone == phone).first() is not None
