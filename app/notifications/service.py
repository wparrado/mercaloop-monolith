# app/notifications/service.py
from app.shared_state import NOTIFICATIONS_LOG


def send_order_confirmation(order_id: str, customer_email: str):
    message = f"[EMAIL a {customer_email}] Tu pedido {order_id} fue confirmado."
    NOTIFICATIONS_LOG.append(message)
    print(message)  # simula el envío
    return message
