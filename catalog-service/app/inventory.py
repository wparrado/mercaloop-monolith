# catalog-service/app/inventory.py
#
# Copia PROPIA e independiente del inventario semilla.
#
# Deliberadamente NO importa nada de `app/shared_state.py` del monolito
# viejo (esa ruta ni siquiera existe en este proceso/paquete). Este
# diccionario vive solo en la memoria de este servicio nuevo. Los
# mismos datos semilla que el monolito se copiaron a mano una sola vez,
# al momento de "cortar" el módulo catalog con el patrón Strangler Fig -
# a partir de aquí, cada copia evoluciona en su propio proceso.

CATALOG_INVENTORY = {
    "PROD-001": {"name": "Teclado Mecánico", "price": 189000, "stock": 12},
    "PROD-002": {"name": "Mouse Ergonómico", "price": 79000, "stock": 30},
    "PROD-003": {"name": "Monitor 27\" 4K", "price": 1250000, "stock": 5},
    "PROD-004": {"name": "Webcam HD", "price": 145000, "stock": 18},
}


def list_products():
    return [
        {"sku": sku, **data}
        for sku, data in CATALOG_INVENTORY.items()
    ]


def get_product(sku: str):
    return CATALOG_INVENTORY.get(sku)
