# app/catalog/router.py
from fastapi import APIRouter, HTTPException
from app.catalog import service

router = APIRouter(prefix="/catalog", tags=["catalog"])


@router.get("/products")
def get_products():
    return service.list_products()


@router.get("/products/{sku}")
def get_product(sku: str):
    product = service.get_product(sku)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"sku": sku, **product}
