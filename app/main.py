# app/main.py
#
# Mercaloop: un único proceso FastAPI que sirve catálogo, pedidos,
# pagos y notificaciones. Un solo artefacto, un solo despliegue.
#
# ⚠️ SÍNTOMA A DESCUBRIR (Bloque 2 - "De la autopsia a la cirugía"):
# Cambiar el texto de WELCOME_MESSAGE de abajo -por trivial que sea-
# exige reconstruir la imagen Docker completa y redesplegar TODA la
# aplicación (catálogo, pedidos, pagos y notificaciones incluidos),
# aunque el cambio no tenga nada que ver con esos módulos.

from fastapi import FastAPI
from app.catalog.router import router as catalog_router
from app.orders.router import router as orders_router
from app.payments.router import router as payments_router

WELCOME_MESSAGE = "Bienvenido a Mercaloop API"

app = FastAPI(title="Mercaloop Monolith")

app.include_router(catalog_router)
app.include_router(orders_router)
app.include_router(payments_router)


@app.get("/")
def root():
    return {"message": WELCOME_MESSAGE}


@app.get("/health")
def health():
    return {"status": "ok"}
