# app/orders/service.py
#
# ⚠️ SÍNTOMA A DESCUBRIR (no lo reveles a los estudiantes):
# OrderService.create_order() es una "clase Dios": una sola función
# concentra validación de negocio, acceso a inventario, autorización
# de pago, envío de notificación y logging. No hay una sola
# responsabilidad aislada — están todas cosidas en el mismo método,
# en el mismo proceso, en la misma unidad de despliegue.
#
# Efecto: para tocar CUALQUIER parte del flujo (ej. cambiar la regla
# de negocio de descuentos), hay que entender y potencialmente romper
# TODO lo demás. No hay límites lógicos.

from app.catalog import service as catalog_service
from app.payments import service as payments_service
from app.notifications import service as notifications_service
from app.shared_state import ORDERS, next_order_id


class OrderService:

    def create_order(self, sku: str, quantity: int, customer_email: str) -> dict:
        # 1. Validación de negocio
        product = catalog_service.get_product(sku)
        if product is None:
            raise ValueError("Producto no existe")
        if quantity <= 0:
            raise ValueError("Cantidad inválida")

        # 2. Cálculo de negocio (regla de precio mezclada aquí mismo)
        subtotal = product["price"] * quantity
        discount = 0.05 if quantity >= 5 else 0.0
        total = int(subtotal * (1 - discount))

        order_id = next_order_id()

        # 3. Autorización de pago (llamando a otro módulo, que a su vez
        #    vuelve a tocar inventario -> doble descuento de stock real)
        payment = payments_service.authorize_payment(
            order_id=order_id, sku=sku, quantity=quantity, amount=total
        )
        if payment["status"] != "authorized":
            raise ValueError(f"Pago rechazado: {payment.get('reason')}")

        # 4. Reserva "oficial" de catálogo (que YA fue descontado
        #    indirectamente en payments_service.authorize_payment)
        catalog_service.reserve_stock(sku, quantity)

        # 5. Notificación
        notifications_service.send_order_confirmation(order_id, customer_email)

        # 6. Persistencia + logging, todo en el mismo método
        order_record = {
            "order_id": order_id,
            "sku": sku,
            "quantity": quantity,
            "total": total,
            "customer_email": customer_email,
            "status": "confirmed",
        }
        ORDERS[order_id] = order_record
        print(f"[LOG] Orden creada: {order_record}")

        return order_record

    def get_order(self, order_id: str):
        return ORDERS.get(order_id)


order_service = OrderService()
