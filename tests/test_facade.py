"""
Tests unitarios para el patrón Facade - Order Management System.

Este módulo contiene tests completos para validar el funcionamiento
del patrón Facade y todos sus subsistemas.
"""

import pytest
import sys
import os

# Agregar el directorio src al path para importar los módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from order_facade.facade import OrderFacade, OrderResult
from order_facade.services.inventory import InventoryService
from order_facade.services.payments import PaymentGateway, PaymentReceipt
from order_facade.services.shipping import ShippingService, ShipmentInfo
from order_facade.services.notifications import NotificationService, NotificationChannel
from decimal import Decimal


class MockPaymentGateway(PaymentGateway):
    """Mock del gateway de pagos para testing."""
    
    def __init__(self, should_succeed=True):
        super().__init__()
        self.should_succeed = should_succeed
        self.charged_amounts = []
    
    def charge(self, payment_info, amount):
        self.charged_amounts.append(amount)
        if self.should_succeed and payment_info.get("card_number", "").startswith("4"):
            return PaymentReceipt(
                success=True, 
                transaction_id="tx-test-123",
                message="Test payment successful"
            )
        return PaymentReceipt(
            success=False, 
            message="Test payment declined"
        )


class MockShippingService(ShippingService):
    """Mock del servicio de envíos para testing."""
    
    def __init__(self, should_succeed=True):
        super().__init__()
        self.should_succeed = should_succeed
        self.created_shipments = []
    
    def create_shipment(self, customer_id, items, shipping_address=None, shipping_type="standard"):
        self.created_shipments.append({
            "customer_id": customer_id,
            "items": items,
            "shipping_type": shipping_type
        })
        
        if self.should_succeed and items:
            return ShipmentInfo(
                success=True,
                shipment_id="ship-test-123",
                tracking_number="TRK12345678",
                eta_days=3,
                estimated_delivery="2025-11-10",
                message="Test shipment created"
            )
        return ShipmentInfo(
            success=False,
            message="Test shipping failed"
        )


class MockNotificationService(NotificationService):
    """Mock del servicio de notificaciones para testing."""
    
    def __init__(self):
        super().__init__()
        self.sent_messages = []
    
    def notify(self, customer_id, message, channel=NotificationChannel.EMAIL):
        self.sent_messages.append({
            "customer_id": customer_id,
            "message": message,
            "channel": channel
        })
        return True
    
    def send_order_notification(self, customer_id, notification_type, order_data, channels=None):
        self.sent_messages.append({
            "customer_id": customer_id,
            "type": notification_type,
            "data": order_data,
            "channels": channels or [NotificationChannel.EMAIL]
        })
        return {"email": "success"}


class TestInventoryService:
    """Tests para el servicio de inventario."""
    
    def test_check_stock_available(self):
        """Test verificación de stock disponible."""
        inventory = InventoryService()
        assert inventory.check_stock("MONITOR-27", 5) is True
        assert inventory.check_stock("MONITOR-27", 15) is False
        assert inventory.check_stock("NONEXISTENT", 1) is False
    
    def test_reserve_stock_success(self):
        """Test reserva exitosa de stock."""
        inventory = InventoryService()
        initial_stock = inventory.get_current_stock("MONITOR-27")
        
        result = inventory.reserve("MONITOR-27", 2)
        assert result is True
        assert inventory.get_current_stock("MONITOR-27") == initial_stock - 2
    
    def test_reserve_stock_insufficient(self):
        """Test reserva con stock insuficiente."""
        inventory = InventoryService()
        result = inventory.reserve("MONITOR-27", 20)  # Más del stock disponible
        assert result is False
    
    def test_release_stock(self):
        """Test liberación de stock."""
        inventory = InventoryService()
        initial_stock = inventory.get_current_stock("MONITOR-27")
        
        # Reservar y luego liberar
        inventory.reserve("MONITOR-27", 2)
        inventory.release("MONITOR-27", 2)
        
        assert inventory.get_current_stock("MONITOR-27") == initial_stock


class TestPaymentGateway:
    """Tests para el gateway de pagos."""
    
    def test_charge_success_visa(self):
        """Test cargo exitoso con tarjeta Visa."""
        gateway = PaymentGateway()
        payment_info = {"card_number": "4111111111111111", "cvv": "123"}
        
        receipt = gateway.charge(payment_info, 100.0)
        assert receipt.success is True
        assert receipt.transaction_id is not None
        assert "Visa" in receipt.message
    
    def test_charge_success_mastercard(self):
        """Test cargo exitoso con MasterCard."""
        gateway = PaymentGateway()
        payment_info = {"card_number": "5555555555554444", "cvv": "123"}
        
        receipt = gateway.charge(payment_info, 50.0)
        assert receipt.success is True
        assert "MasterCard" in receipt.message
    
    def test_charge_declined(self):
        """Test cargo rechazado."""
        gateway = PaymentGateway()
        payment_info = {"card_number": "3111111111111111", "cvv": "123"}  # Amex - rechazada
        
        receipt = gateway.charge(payment_info, 100.0)
        assert receipt.success is False
        assert "rechazado" in receipt.message
    
    def test_charge_invalid_card(self):
        """Test con tarjeta inválida."""
        gateway = PaymentGateway()
        payment_info = {"card_number": "123", "cvv": "123"}
        
        receipt = gateway.charge(payment_info, 100.0)
        assert receipt.success is False
        assert "inválido" in receipt.message


class TestShippingService:
    """Tests para el servicio de envíos."""
    
    def test_create_shipment_success(self):
        """Test creación exitosa de envío."""
        shipping = ShippingService()
        items = [{"sku": "MONITOR-27", "qty": 1}]
        
        shipment = shipping.create_shipment("customer-123", items)
        assert shipment.success is True
        assert shipment.shipment_id is not None
        assert shipment.tracking_number is not None
        assert shipment.eta_days > 0
    
    def test_create_shipment_no_items(self):
        """Test creación de envío sin productos."""
        shipping = ShippingService()
        
        shipment = shipping.create_shipment("customer-123", [])
        assert shipment.success is False
        assert "No hay productos" in shipment.message
    
    def test_calculate_shipping_cost(self):
        """Test cálculo de costo de envío."""
        shipping = ShippingService()
        items = [{"sku": "MONITOR-27", "qty": 1, "weight": 2}]
        
        cost_standard = shipping.calculate_shipping_cost(items, "standard")
        cost_express = shipping.calculate_shipping_cost(items, "express")
        
        assert cost_express > cost_standard
        assert cost_standard >= 10.0  # Costo mínimo


class TestNotificationService:
    """Tests para el servicio de notificaciones."""
    
    def test_simple_notification(self):
        """Test notificación simple."""
        notifications = NotificationService()
        
        result = notifications.notify("customer-123", "Test message")
        assert result is True
    
    def test_order_notification_templates(self):
        """Test notificaciones con plantillas."""
        notifications = NotificationService()
        order_data = {
            "order_id": "order-123",
            "amount": 100.0,
            "transaction_id": "tx-123"
        }
        
        result = notifications.send_order_notification(
            "customer-123", 
            "order_confirmed", 
            order_data
        )
        assert "success" in result.values()
    
    def test_notification_history(self):
        """Test historial de notificaciones."""
        notifications = NotificationService()
        
        notifications.notify("customer-123", "Message 1")
        notifications.notify("customer-123", "Message 2")
        notifications.notify("customer-456", "Message 3")
        
        history = notifications.get_notification_history("customer-123")
        assert len(history) == 2


class TestOrderFacade:
    """Tests para el Facade principal."""
    
    def test_place_order_success(self):
        """Test pedido exitoso completo."""
        # Configurar mocks
        inventory = InventoryService()
        payments = MockPaymentGateway(should_succeed=True)
        shipping = MockShippingService(should_succeed=True)
        notifications = MockNotificationService()
        
        facade = OrderFacade(inventory, payments, shipping, notifications)
        
        # Asegurar que hay stock
        inventory._stock["TEST-SKU"] = 10
        
        payment_info = {"card_number": "4111111111111111", "cvv": "123"}
        
        result = facade.place_order(
            "customer-123", 
            "TEST-SKU", 
            2, 
            payment_info, 
            50.0
        )
        
        assert result.success is True
        assert result.order_id is not None
        assert result.transaction_id == "tx-test-123"
        assert result.tracking_number == "TRK12345678"
        assert result.total_amount > Decimal("100")  # Productos + envío
        
        # Verificar que se llamaron todos los servicios
        assert len(payments.charged_amounts) == 1
        assert len(shipping.created_shipments) == 1
        assert len(notifications.sent_messages) >= 2  # Confirmación + envío
        
        # Verificar que se redujo el stock
        assert inventory.get_current_stock("TEST-SKU") == 8
    
    def test_place_order_insufficient_stock(self):
        """Test pedido con stock insuficiente."""
        inventory = InventoryService()
        inventory._stock["LOW-STOCK"] = 1
        
        facade = OrderFacade(inventory=inventory)
        payment_info = {"card_number": "4111111111111111", "cvv": "123"}
        
        result = facade.place_order("customer-123", "LOW-STOCK", 5, payment_info, 10.0)
        
        assert result.success is False
        assert "insuficiente" in result.reason.lower()
        assert inventory.get_current_stock("LOW-STOCK") == 1  # Stock no cambió
    
    def test_place_order_payment_declined(self):
        """Test pedido con pago rechazado."""
        inventory = InventoryService()
        inventory._stock["TEST-SKU"] = 10
        
        payments = MockPaymentGateway(should_succeed=False)
        notifications = MockNotificationService()
        
        facade = OrderFacade(inventory=inventory, payments=payments, notifications=notifications)
        
        payment_info = {"card_number": "3111111111111111", "cvv": "123"}  # Amex rechazada
        
        result = facade.place_order("customer-123", "TEST-SKU", 2, payment_info, 50.0)
        
        assert result.success is False
        assert "pago" in result.reason.lower()
        assert inventory.get_current_stock("TEST-SKU") == 10  # Stock liberado
        
        # Verificar notificación de falla
        payment_fail_notifications = [
            msg for msg in notifications.sent_messages 
            if msg.get("type") == "payment_failed"
        ]
        assert len(payment_fail_notifications) >= 1
    
    def test_place_order_shipping_failed(self):
        """Test pedido con falla en el envío."""
        inventory = InventoryService()
        inventory._stock["TEST-SKU"] = 10
        
        payments = MockPaymentGateway(should_succeed=True)
        shipping = MockShippingService(should_succeed=False)
        
        facade = OrderFacade(inventory=inventory, payments=payments, shipping=shipping)
        
        payment_info = {"card_number": "4111111111111111", "cvv": "123"}
        
        result = facade.place_order("customer-123", "TEST-SKU", 2, payment_info, 50.0)
        
        assert result.success is False
        assert "envío" in result.reason.lower()
        assert result.transaction_id == "tx-test-123"  # Pago se procesó
        assert inventory.get_current_stock("TEST-SKU") == 10  # Stock liberado por falla
    
    def test_cancel_order(self):
        """Test cancelación de pedido."""
        # Crear un pedido exitoso primero
        inventory = InventoryService()
        inventory._stock["TEST-SKU"] = 10
        
        payments = MockPaymentGateway(should_succeed=True)
        shipping = MockShippingService(should_succeed=True)
        notifications = MockNotificationService()
        
        facade = OrderFacade(inventory, payments, shipping, notifications)
        
        payment_info = {"card_number": "4111111111111111", "cvv": "123"}
        
        # Crear pedido
        result = facade.place_order("customer-123", "TEST-SKU", 2, payment_info, 50.0)
        assert result.success is True
        
        stock_after_order = inventory.get_current_stock("TEST-SKU")
        
        # Cancelar pedido
        cancel_result = facade.cancel_order(result.order_id, "customer-123")
        assert cancel_result is True
        
        # Verificar que el stock se restauró
        assert inventory.get_current_stock("TEST-SKU") > stock_after_order
    
    def test_get_order_status(self):
        """Test consulta de estado de pedido."""
        inventory = InventoryService()
        inventory._stock["TEST-SKU"] = 10
        
        facade = OrderFacade(inventory=inventory)
        payment_info = {"card_number": "4111111111111111", "cvv": "123"}
        
        # Crear pedido
        result = facade.place_order("customer-123", "TEST-SKU", 1, payment_info, 25.0)
        assert result.success is True
        
        # Consultar estado
        status = facade.get_order_status(result.order_id)
        assert status is not None
        assert status["order_id"] == result.order_id
        assert status["customer_id"] == "customer-123"
    
    def test_get_order_history(self):
        """Test historial de pedidos del cliente."""
        inventory = InventoryService()
        inventory._stock["TEST-SKU"] = 10
        
        facade = OrderFacade(inventory=inventory)
        payment_info = {"card_number": "4111111111111111", "cvv": "123"}
        
        # Crear múltiples pedidos
        result1 = facade.place_order("customer-123", "TEST-SKU", 1, payment_info, 25.0)
        result2 = facade.place_order("customer-123", "TEST-SKU", 2, payment_info, 25.0)
        
        # Obtener historial
        history = facade.get_order_history("customer-123")
        assert len(history) == 2
        
        order_ids = [order["order_id"] for order in history]
        assert result1.order_id in order_ids
        assert result2.order_id in order_ids
    
    def test_get_system_stats(self):
        """Test estadísticas del sistema."""
        facade = OrderFacade()
        
        stats = facade.get_system_stats()
        
        assert "total_successful_orders" in stats
        assert "total_failed_orders" in stats
        assert "success_rate_percentage" in stats
        assert "inventory_status" in stats
        assert "notification_stats" in stats
        assert "available_carriers" in stats


class TestIntegration:
    """Tests de integración completos."""
    
    def test_multiple_orders_different_customers(self):
        """Test múltiples pedidos de diferentes clientes."""
        facade = OrderFacade()
        payment_info = {"card_number": "4111111111111111", "cvv": "123", "expiry": "12/25"}
        
        # Pedidos de diferentes clientes
        result1 = facade.place_order("customer-1", "MONITOR-27", 1, payment_info, 200.0)
        result2 = facade.place_order("customer-2", "LAPTOP-15", 1, payment_info, 800.0)
        
        assert result1.success is True
        assert result2.success is True
        assert result1.order_id != result2.order_id
        
        # Verificar historiales separados
        history1 = facade.get_order_history("customer-1")
        history2 = facade.get_order_history("customer-2")
        
        assert len(history1) == 1
        assert len(history2) == 1
        assert history1[0]["order_id"] == result1.order_id
        assert history2[0]["order_id"] == result2.order_id
    
    def test_order_workflow_with_different_shipping_types(self):
        """Test flujo completo con diferentes tipos de envío."""
        facade = OrderFacade()
        payment_info = {"card_number": "4111111111111111", "cvv": "123"}
        
        # Pedido estándar
        result_standard = facade.place_order(
            "customer-1", "TABLET-10", 1, payment_info, 300.0, 
            shipping_type="standard"
        )
        
        # Pedido express
        result_express = facade.place_order(
            "customer-1", "SMARTPHONE-X", 1, payment_info, 500.0,
            shipping_type="express"
        )
        
        assert result_standard.success is True
        assert result_express.success is True
        
        # El envío express debería costar más
        assert result_express.total_amount > result_standard.total_amount


if __name__ == "__main__":
    # Ejecutar tests con pytest
    pytest.main([__file__, "-v", "--tb=short"])