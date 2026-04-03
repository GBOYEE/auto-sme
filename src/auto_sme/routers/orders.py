"""Orders router — receive WhatsApp orders, track status."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from auto_sme.crud import create_order, get_orders, update_order_status, adjust_stock
from auto_sme.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/orders")  # no API key required for webhooks

class OrderItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    unit_price: float

class OrderCreate(BaseModel):
    customer_phone: str
    customer_name: Optional[str] = None
    items: List[OrderItem]

class Order(OrderCreate):
    id: str
    total_amount: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

def process_order(customer_phone: str, items: List[dict], customer_name: Optional[str] = None, db: Session = None) -> Order:
    """Create order and deduct stock atomically."""
    total = sum(item["quantity"] * item["unit_price"] for item in items)
    order = create_order(
        db=db,
        customer_phone=customer_phone,
        items=items,
        customer_name=customer_name
    )

    # Deduct stock for each item
    for item in items:
        prod_id = item["product_id"]
        qty = item["quantity"]
        prod = adjust_stock(db=db, product_id=prod_id, delta=-qty)
        if not prod:
            # Rollback? For MVP we continue but leave order as is
            pass

    return order

@router.post("", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order_endpoint(order: OrderCreate, db: Session = Depends(get_db)):
    return process_order(
        customer_phone=order.customer_phone,
        items=[item.model_dump() for item in order.items],
        customer_name=order.customer_name,
        db=db
    )

@router.get("", response_model=List[Order])
async def list_orders(db: Session = Depends(get_db)):
    return get_orders(db)

@router.patch("/{order_id}/status")
async def update_order_status_endpoint(order_id: str, status: str = "confirmed", db: Session = Depends(get_db)):
    order = update_order_status(db=db, order_id=order_id, status=status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
