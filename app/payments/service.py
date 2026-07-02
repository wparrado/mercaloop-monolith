# app/payments/service.py
#
# ⚠️ SÍNTOMA A DESCUBRIR (no lo reveles a los estudiantes):
# Esta función necesita saber si un producto sigue "disponible" para
# poder autorizar el pago. En vez de llamar a catalog.service.get_product(),
# alguien (con prisa, en algún sprint pasado) importó directamente el
# diccionario interno de catalog y lo empezó a leer Y ESCRIBIR aquí mismo.
#
# Efecto: payments/ y catalog/ ahora están acoplados a nivel de estructura
# de datos interna. Si mañana catalog/ cambia su modelo (por ejemplo, pasa
# "stock" a otro nombre, o migra a una base de datos real), este archivo
# se rompe sin que nadie en el equipo de pagos se entere hasta producción.

from app.shared_state import CATALOG_INVENTORY, PAYMENTS


def authorize_payment(order_id: str, sku: str, quantity: int, amount: int) -> dict:
    # Acceso directo al inventario de OTRO módulo. Debería ser:
    #   product = catalog.service.get_product(sku)
    product = CATALOG_INVENTORY.get(sku)

    if product is None:
        return {"status": "rejected", "reason": "producto inexistente"}

    # Y aquí, peor aún: escribe directamente sobre el estado de catalog,
    # como "pre-reserva" de pago, duplicando la responsabilidad que ya
    # tiene catalog.service.reserve_stock().
    if product["stock"] < quantity:
        return {"status": "rejected", "reason": "stock insuficiente"}

    product["stock"] -= quantity  # <-- mutación cruzada de módulo

    payment_record = {
        "order_id": order_id,
        "sku": sku,
        "amount": amount,
        "status": "authorized",
    }
    PAYMENTS[order_id] = payment_record
    return payment_record
