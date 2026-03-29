"""Orders router — receive WhatsApp orders, track status."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime
from auto_sme.store import orders as _orders_db, products as _products_db

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
    status: str = "pending"
    created_at: datetime

def process_order(customer_phone: str, items: List[dict], customer_name: Optional[str] = None) -> dict:
    """Create order and deduct stock atomically (in-memory for MVP)."""
    total = sum(item["quantity"] * item["unit_price"] for item in items)
    new_order = {
        "id": str(uuid.uuid4()),
        "customer_phone": customer_phone,
        "customer_name": customer_name,
        "items": items,
        "total_amount": total,
        "status": "pending",
        "created_at": datetime.utcnow(),
    }
    _orders_db.append(new_order)

    # Deduct stock for each item
    for item in items:
        prod_id = item["product_id"]
        qty = item["quantity"]
        for prod in _products_db:
            if prod["id"] == prod_id:
                prod["stock"] = max(0, prod["stock"] - qty)
                break

    return new_order

@router.post("", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    new_order = process_order(
        customer_phone=order.customer_phone,
        items=[item.model_dump() for item in order.items],
        customer_name=order.customer_name
    )
    return new_order

@router.get("", response_model=List[Order])
async def list_orders():
    return _orders_db

@router.patch("/{order_id}/status")
async def update_order_status(order_id: str, status: str = "confirmed"):
    for order in _orders_db:
        if order["id"] == order_id:
            order["status"] = status
            return order
    raise HTTPException(status_code=404, detail="Order not found")