# app/orders/router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.orders.service import order_service

router = APIRouter(prefix="/orders", tags=["orders"])


class CreateOrderRequest(BaseModel):
    sku: str
    quantity: int
    customer_email: str


@router.post("")
def create_order(payload: CreateOrderRequest):
    try:
        return order_service.create_order(
            sku=payload.sku,
            quantity=payload.quantity,
            customer_email=payload.customer_email,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{order_id}")
def get_order(order_id: str):
    order = order_service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return order
