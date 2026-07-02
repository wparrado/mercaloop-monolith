# app/payments/router.py
from fastapi import APIRouter
from app.shared_state import PAYMENTS

router = APIRouter(prefix="/payments", tags=["payments"])


@router.get("/{order_id}")
def get_payment(order_id: str):
    return PAYMENTS.get(order_id, {"status": "not_found"})
