# catalog-service/app/main.py
#
# Servicio independiente que reemplaza (a la Strangler Fig) SOLO el
# módulo catalog del monolito viejo: listar productos y consultar un
# producto por SKU. Corre en su propio proceso, puerto 8001.

from fastapi import FastAPI, HTTPException
from app import inventory

app = FastAPI(title="Mercaloop Catalog Service (nuevo)")

# Prefijo /catalog para que la forma de las rutas coincida con la que
# expone el monolito viejo (app/catalog/router.py) - así el gateway
# puede reenviar el path tal cual, sin reescribirlo.


@app.get("/catalog/products")
def get_products():
    return inventory.list_products()


@app.get("/catalog/products/{sku}")
def get_product(sku: str):
    product = inventory.get_product(sku)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"sku": sku, **product}


@app.get("/health")
def health():
    return {"status": "ok", "service": "catalog-service"}
