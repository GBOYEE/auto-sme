"""Inventory router — product CRUD and stock adjustment."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime
from auto_sme.dependencies import verify_api_key
from auto_sme.store import products

router = APIRouter(prefix="/inventory", dependencies=[Depends(verify_api_key)])

class ProductCreate(BaseModel):
    name: str
    price: float
    unit: str
    stock: int = 0
    low_stock_threshold: int = 10

class Product(ProductCreate):
    id: str

@router.post("", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    new_prod = {
        "id": str(uuid.uuid4()),
        "name": product.name,
        "price": product.price,
        "unit": product.unit,
        "stock": product.stock,
        "low_stock_threshold": product.low_stock_threshold,
    }
    products.append(new_prod)
    return new_prod

@router.patch("/{product_id}")
async def adjust_stock(product_id: str, delta: int = 0):
    for prod in products:
        if prod["id"] == product_id:
            prod["stock"] = max(0, prod["stock"] + delta)
            return prod
    raise HTTPException(status_code=404, detail="Product not found")

@router.get("", response_model=List[Product])
async def list_products():
    return products