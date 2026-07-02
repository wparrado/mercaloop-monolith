# app/catalog/service.py
#
# Esta es la capa de servicio "oficial" del catálogo.
# En teoría, cualquier otro módulo que necesite tocar inventario
# debería pasar por aquí. En la práctica... revisa app/payments/service.py.

from app.shared_state import CATALOG_INVENTORY


def list_products():
    return [
        {"sku": sku, **data}
        for sku, data in CATALOG_INVENTORY.items()
    ]


def get_product(sku: str):
    return CATALOG_INVENTORY.get(sku)


def reserve_stock(sku: str, quantity: int) -> bool:
    """Punto de entrada 'oficial' para reservar stock.
    Válida disponibilidad y descuenta. Nadie más debería tocar
    CATALOG_INVENTORY directamente."""
    product = CATALOG_INVENTORY.get(sku)
    if not product or product["stock"] < quantity:
        return False
    product["stock"] -= quantity
    return True
