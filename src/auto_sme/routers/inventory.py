"""Inventory router — product CRUD and stock adjustment."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
from datetime import datetime
from auto_sme.dependencies import verify_api_key
from auto_sme.crud import create_product, get_products, adjust_stock
from auto_sme.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/inventory", dependencies=[Depends(verify_api_key)])

class ProductCreate(BaseModel):
    name: str
    price: float
    unit: str
    stock: int = 0
    low_stock_threshold: int = 10

class Product(ProductCreate):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

@router.post("", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product_endpoint(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(
        db=db,
        name=product.name,
        price=product.price,
        unit=product.unit,
        stock=product.stock,
        low_stock_threshold=product.low_stock_threshold
    )

@router.patch("/{product_id}")
async def adjust_stock_endpoint(product_id: str, delta: int = 0, db: Session = Depends(get_db)):
    prod = adjust_stock(db=db, product_id=product_id, delta=delta)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return prod

@router.get("", response_model=List[Product])
async def list_products(db: Session = Depends(get_db)):
    return get_products(db)
