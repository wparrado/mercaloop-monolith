# app/shared_state.py
#
# "Base de datos" en memoria compartida por TODO el monolito.
# Cualquier módulo puede importar esto y leer/escribir directamente.
#
# (Nota para el facilitador: este es el punto de acoplamiento oculto #1.
#  No hay ninguna barrera que impida que payments/ toque el inventario
#  de catalog/ directamente, sin pasar por su capa de servicio.)

CATALOG_INVENTORY = {
    "PROD-001": {"name": "Teclado Mecánico", "price": 189000, "stock": 12},
    "PROD-002": {"name": "Mouse Ergonómico", "price": 79000, "stock": 30},
    "PROD-003": {"name": "Monitor 27\" 4K", "price": 1250000, "stock": 5},
    "PROD-004": {"name": "Webcam HD", "price": 145000, "stock": 18},
}

ORDERS = {}

PAYMENTS = {}

NOTIFICATIONS_LOG = []

_next_order_id = [1]


def next_order_id() -> str:
    order_id = f"ORD-{_next_order_id[0]:04d}"
    _next_order_id[0] += 1
    return order_id
