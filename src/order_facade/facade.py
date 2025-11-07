"""
Order Facade - Implementación del patrón Facade para gestión de pedidos.

Este módulo implementa el patrón Facade que orquesta múltiples subsistemas
(inventario, pagos, envíos, notificaciones) para simplificar el proceso
de creación de pedidos en sistemas empresariales.
"""

from .services.inventory import InventoryService
from .services.payments import PaymentGateway
from .services.shipping import ShippingService
from .services.notifications import NotificationService, NotificationChannel
from dataclasses import dataclass
from typing import Optional, Dict, List
from decimal import Decimal
import uuid


@dataclass
class OrderResult:
    """Resultado de una operación de pedido."""

    success: bool
    order_id: Optional[str] = None
    reason: Optional[str] = None
    transaction_id: Optional[str] = None
    shipment_id: Optional[str] = None
    tracking_number: Optional[str] = None
    total_amount: Optional[Decimal] = None
    estimated_delivery: Optional[str] = None


class OrderFacade:
    """
    Facade que proporciona una interfaz simplificada para gestionar pedidos.

    Este facade orquesta las operaciones de múltiples subsistemas:
    - Inventario: verificación y reserva de productos
    - Pagos: procesamiento de transacciones
    - Envíos: logística y seguimiento
    - Notificaciones: comunicación con clientes
    """

    def __init__(
        self,
        inventory: Optional[InventoryService] = None,
        payments: Optional[PaymentGateway] = None,
        shipping: Optional[ShippingService] = None,
        notifications: Optional[NotificationService] = None,
    ):
        """
        Inicializa el facade con los servicios de subsistemas.

        Args:
            inventory: Servicio de inventario (se crea uno por defecto si no se proporciona)
            payments: Gateway de pagos (se crea uno por defecto si no se proporciona)
            shipping: Servicio de envíos (se crea uno por defecto si no se proporciona)
            notifications: Servicio de notificaciones (se crea uno por defecto si no se proporciona)
        """
        self.inventory = inventory or InventoryService()
        self.payments = payments or PaymentGateway()
        self.shipping = shipping or ShippingService()
        self.notifications = notifications or NotificationService()

        # Estado interno para auditoría
        self._order_history: list[Dict] = []
        self._failed_orders: list[Dict] = []

    def place_order(
        self,
        customer_id: str,
        sku: str,
        qty: int,
        payment_info: Dict,
        unit_price: float,
        shipping_address: Optional[Dict] = None,
        shipping_type: str = "standard",
    ) -> OrderResult:
        """
        Procesa un pedido completo orquestando todos los subsistemas.

        Args:
            customer_id: ID único del cliente
            sku: Código del producto
            qty: Cantidad solicitada
            payment_info: Información de pago (tarjeta, etc.)
            unit_price: Precio unitario del producto
            shipping_address: Dirección de envío (opcional)
            shipping_type: Tipo de envío (standard, express, premium)

        Returns:
            OrderResult con el resultado de la operación
        """
        order_id = str(uuid.uuid4())

        print(f"\\n=== Procesando Pedido {order_id[:8]}... ===")
        print(f"Cliente: {customer_id}")
        print(f"Producto: {sku} x {qty}")
        print(f"Precio unitario: ${unit_price:.2f}")

        try:
            # 1. Validar y reservar inventario
            print(f"\\n[Paso 1] Verificando inventario...")
            if not self.inventory.check_stock(sku, qty):
                result = OrderResult(
                    success=False, order_id=order_id, reason="Stock insuficiente"
                )
                self._record_failed_order(order_id, result.reason or "Error desconocido", customer_id)
                return result

            reserved = self.inventory.reserve(sku, qty)
            if not reserved:
                result = OrderResult(
                    success=False,
                    order_id=order_id,
                    reason="No se pudo reservar el stock",
                )
                self._record_failed_order(order_id, result.reason or "Error desconocido", customer_id)
                return result

            # 2. Calcular total y procesar pago
            print(f"\\n[Paso 2] Procesando pago...")
            total_amount = Decimal(str(qty * unit_price))

            # Agregar costo de envío
            shipping_cost = self.shipping.calculate_shipping_cost(
                [{"sku": sku, "qty": qty, "weight": 1}], shipping_type
            )
            total_amount += Decimal(str(shipping_cost))

            print(f"Subtotal productos: ${qty * unit_price:.2f}")
            print(f"Costo envío: ${shipping_cost:.2f}")
            print(f"Total: ${total_amount:.2f}")

            receipt = self.payments.charge(payment_info, float(total_amount))
            if not receipt.success:
                # Revertir reserva de inventario
                self.inventory.release(sku, qty)
                result = OrderResult(
                    success=False,
                    order_id=order_id,
                    reason=f"Error en el pago: {receipt.message}",
                )
                self._record_failed_order(order_id, result.reason or "Error desconocido", customer_id)

                # Notificar falla en el pago
                self.notifications.send_order_notification(
                    customer_id,
                    "payment_failed",
                    {"order_id": order_id, "reason": receipt.message},
                )

                return result

            # 3. Crear envío
            print(f"\\n[Paso 3] Programando envío...")
            shipment = self.shipping.create_shipment(
                customer_id, [{"sku": sku, "qty": qty}], shipping_address, shipping_type
            )

            if not shipment.success:
                # Revertir inventario (simular reembolso)
                self.inventory.release(sku, qty)
                result = OrderResult(
                    success=False,
                    order_id=order_id,
                    reason=f"Error en el envío: {shipment.message}",
                    transaction_id=receipt.transaction_id,
                )
                self._record_failed_order(order_id, result.reason or "Error desconocido", customer_id)
                return result

            # 4. Notificar al cliente
            print(f"\\n[Paso 4] Enviando notificaciones...")
            notification_data = {
                "order_id": order_id,
                "amount": float(total_amount),
                "transaction_id": receipt.transaction_id,
                "tracking_number": shipment.tracking_number,
                "eta": shipment.estimated_delivery,
            }

            # Notificación de confirmación
            self.notifications.send_order_notification(
                customer_id,
                "order_confirmed",
                notification_data,
                [NotificationChannel.EMAIL, NotificationChannel.SMS],
            )

            # Notificación de envío
            self.notifications.send_order_notification(
                customer_id, "order_shipped", notification_data
            )

            # Crear resultado exitoso
            result = OrderResult(
                success=True,
                order_id=order_id,
                transaction_id=receipt.transaction_id,
                shipment_id=shipment.shipment_id,
                tracking_number=shipment.tracking_number,
                total_amount=total_amount,
                estimated_delivery=shipment.estimated_delivery,
            )

            # Registrar pedido exitoso
            self._record_successful_order(result, customer_id, sku, qty)

            print(f"\\n✅ Pedido {order_id[:8]}... procesado exitosamente!")
            print(f"Número de seguimiento: {shipment.tracking_number}")
            print(f"Entrega estimada: {shipment.estimated_delivery}")

            return result

        except Exception as e:
            # Manejo de errores inesperados
            print(
                f"\\n❌ Error inesperado procesando pedido {order_id[:8]}...: {str(e)}"
            )

            # Intentar revertir cambios
            try:
                self.inventory.release(sku, qty)
            except:
                pass

            result = OrderResult(
                success=False,
                order_id=order_id,
                reason=f"Error interno del sistema: {str(e)}",
            )
            self._record_failed_order(order_id, result.reason or "Error desconocido", customer_id)

            return result

    def cancel_order(self, order_id: str, customer_id: str) -> bool:
        """
        Cancela un pedido existente.

        Args:
            order_id: ID del pedido a cancelar
            customer_id: ID del cliente

        Returns:
            True si la cancelación fue exitosa
        """
        print(f"\\n=== Cancelando Pedido {order_id[:8]}... ===")

        # Buscar el pedido en el historial
        order = self._find_order_in_history(order_id)
        if not order:
            print(f"❌ Pedido {order_id[:8]}... no encontrado")
            return False

        try:
            # Cancelar envío
            if order.get("shipment_id"):
                self.shipping.cancel_shipment(order["shipment_id"])

            # Procesar reembolso
            if order.get("transaction_id") and order.get("total_amount"):
                refund_receipt = self.payments.refund(
                    order["transaction_id"], float(order["total_amount"])
                )
                print(f"Reembolso procesado: {refund_receipt.success}")

            # Restaurar inventario
            if order.get("sku") and order.get("qty"):
                self.inventory.release(order["sku"], order["qty"])

            # Notificar cancelación
            self.notifications.notify(
                customer_id,
                f"Tu pedido {order_id[:8]}... ha sido cancelado exitosamente. El reembolso será procesado en 3-5 días hábiles.",
            )

            print(f"✅ Pedido {order_id[:8]}... cancelado exitosamente")
            return True

        except Exception as e:
            print(f"❌ Error cancelando pedido: {str(e)}")
            return False

    def get_order_status(self, order_id: str) -> Optional[Dict]:
        """
        Obtiene el estado actual de un pedido.

        Args:
            order_id: ID del pedido

        Returns:
            Diccionario con información del pedido o None si no existe
        """
        order = self._find_order_in_history(order_id)
        if not order:
            return None

        # Si tiene tracking number, obtener estado del envío
        if order.get("tracking_number"):
            tracking_info = self.shipping.track_shipment(order["tracking_number"])
            order["shipping_status"] = tracking_info

        return order

    def get_order_history(self, customer_id: str) -> List[Dict]:
        """
        Obtiene el historial de pedidos de un cliente.

        Args:
            customer_id: ID del cliente

        Returns:
            Lista de pedidos del cliente
        """
        return [
            order
            for order in self._order_history
            if order["customer_id"] == customer_id
        ]

    def get_system_stats(self) -> Dict:
        """
        Obtiene estadísticas del sistema.

        Returns:
            Diccionario con estadísticas generales
        """
        total_orders = len(self._order_history)
        failed_orders = len(self._failed_orders)
        success_rate = (
            (total_orders / (total_orders + failed_orders)) * 100
            if (total_orders + failed_orders) > 0
            else 0
        )

        # Estadísticas de notificaciones
        notification_stats = self.notifications.get_notification_stats()

        return {
            "total_successful_orders": total_orders,
            "total_failed_orders": failed_orders,
            "success_rate_percentage": round(success_rate, 2),
            "inventory_status": self.inventory.list_products(),
            "notification_stats": notification_stats,
            "available_carriers": self.shipping.get_available_carriers(),
        }

    def _record_successful_order(
        self, result: OrderResult, customer_id: str, sku: str, qty: int
    ) -> None:
        """Registra un pedido exitoso en el historial."""
        order_record = {
            "order_id": result.order_id,
            "customer_id": customer_id,
            "sku": sku,
            "qty": qty,
            "transaction_id": result.transaction_id,
            "shipment_id": result.shipment_id,
            "tracking_number": result.tracking_number,
            "total_amount": result.total_amount,
            "estimated_delivery": result.estimated_delivery,
            "status": "completed",
            "timestamp": self._get_current_timestamp(),
        }
        self._order_history.append(order_record)

    def _record_failed_order(self, order_id: str, reason: str, customer_id: str) -> None:
        """Registra un pedido fallido."""
        failed_record = {
            "order_id": order_id,
            "customer_id": customer_id,
            "reason": reason,
            "timestamp": self._get_current_timestamp(),
        }
        self._failed_orders.append(failed_record)

    def _find_order_in_history(self, order_id: str) -> Optional[Dict]:
        """Busca un pedido en el historial."""
        for order in self._order_history:
            if order["order_id"] == order_id:
                return order
        return None

    def _get_current_timestamp(self) -> str:
        """Obtiene el timestamp actual."""
        from datetime import datetime

        return datetime.now().isoformat()
