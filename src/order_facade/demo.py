"""
Script de demostración del patrón Facade para gestión de pedidos.

Este script demuestra el uso práctico del patrón Facade implementado
en el sistema de gestión de pedidos, mostrando diferentes escenarios
y casos de uso.
"""

import sys
import os
from typing import Dict, List

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from order_facade import OrderFacade, OrderResult
from order_facade.services.notifications import NotificationChannel


def print_separator(title: str = "") -> None:
    """Imprime un separador visual."""
    print("\n" + "=" * 60)
    if title:
        print(f"  {title}")
        print("=" * 60)


def print_result(result: OrderResult, scenario: str) -> None:
    """Imprime el resultado de un pedido de forma formateada."""
    print(f"\n🎯 Escenario: {scenario}")
    print("-" * 40)

    if result.success:
        print("✅ Estado: EXITOSO")
        order_id_short = result.order_id[:8] if result.order_id else "N/A"
        print(f"📦 ID del Pedido: {order_id_short}...")
        print(f"💳 ID Transacción: {result.transaction_id}")
        print(f"🚚 Número de Seguimiento: {result.tracking_number}")
        print(f"💰 Total Pagado: ${result.total_amount:.2f}")
        print(f"📅 Entrega Estimada: {result.estimated_delivery}")
    else:
        print("❌ Estado: FALLIDO")
        order_id_short = result.order_id[:8] if result.order_id else "N/A"
        print(f"📦 ID del Pedido: {order_id_short}...")
        print(f"⚠️  Razón: {result.reason}")
        if result.transaction_id:
            print(f"💳 ID Transacción: {result.transaction_id}")


def demo_successful_orders(facade: OrderFacade) -> List[OrderResult]:
    """Demuestra pedidos exitosos."""
    print_separator("DEMO 1: PEDIDOS EXITOSOS")

    # Configurar información de pago válida (Visa)
    payment_info_visa = {
        "card_number": "4111111111111111",
        "cvv": "123",
        "expiry": "12/27",
        "cardholder": "Juan Pérez",
    }

    # Configurar información de pago válida (MasterCard)
    payment_info_mc = {
        "card_number": "5555555555554444",
        "cvv": "456",
        "expiry": "08/26",
        "cardholder": "María García",
    }

    # Dirección de envío
    shipping_address = {
        "street": "Av. Arequipa 1234",
        "city": "Lima",
        "zip_code": "15001",
        "country": "Perú",
    }

    # Escenario 1: Pedido estándar con Visa
    print("\n🛒 Realizando pedido estándar...")
    result1 = facade.place_order(
        customer_id="customer_001",
        sku="MONITOR-27",
        qty=1,
        payment_info=payment_info_visa,
        unit_price=299.99,
        shipping_address=shipping_address,
        shipping_type="standard",
    )
    print_result(result1, 'Pedido Estándar - Monitor 27"')

    # Escenario 2: Pedido express con MasterCard
    print("\n🛒 Realizando pedido express...")
    result2 = facade.place_order(
        customer_id="customer_002",
        sku="LAPTOP-15",
        qty=1,
        payment_info=payment_info_mc,
        unit_price=899.99,
        shipping_type="express",
    )
    print_result(result2, 'Pedido Express - Laptop 15"')

    # Escenario 3: Pedido múltiple
    print("\n🛒 Realizando pedido de múltiples unidades...")
    result3 = facade.place_order(
        customer_id="customer_003",
        sku="SMARTPHONE-X",
        qty=2,
        payment_info=payment_info_visa,
        unit_price=649.99,
        shipping_type="premium",
    )
    print_result(result3, "Pedido Premium - 2x Smartphone X")

    return [result1, result2, result3]


def demo_failed_orders(facade: OrderFacade) -> None:
    """Demuestra diferentes tipos de fallos en pedidos."""
    print_separator("DEMO 2: MANEJO DE ERRORES")

    # Escenario 1: Stock insuficiente
    print("\n🛒 Intentando pedido con stock insuficiente...")
    result1 = facade.place_order(
        customer_id="customer_004",
        sku="WASHER-7KG",  # Solo hay 2 en stock
        qty=5,  # Pidiendo más de lo disponible
        payment_info={"card_number": "4111111111111111", "cvv": "123"},
        unit_price=499.99,
    )
    print_result(result1, "Error - Stock Insuficiente")

    # Escenario 2: Pago rechazado (American Express)
    print("\n🛒 Intentando pedido con pago rechazado...")
    payment_declined = {
        "card_number": "3782822463100005",  # Amex - será rechazada
        "cvv": "1234",
        "expiry": "12/25",
    }

    result2 = facade.place_order(
        customer_id="customer_005",
        sku="TABLET-10",
        qty=1,
        payment_info=payment_declined,
        unit_price=299.99,
    )
    print_result(result2, "Error - Pago Rechazado")

    # Escenario 3: Producto inexistente
    print("\n🛒 Intentando pedido de producto inexistente...")
    result3 = facade.place_order(
        customer_id="customer_006",
        sku="NONEXISTENT-PRODUCT",
        qty=1,
        payment_info={"card_number": "4111111111111111", "cvv": "123"},
        unit_price=99.99,
    )
    print_result(result3, "Error - Producto No Existe")


def demo_order_management(
    facade: OrderFacade, successful_orders: List[OrderResult]
) -> None:
    """Demuestra las funciones de gestión de pedidos."""
    print_separator("DEMO 3: GESTIÓN DE PEDIDOS")

    if successful_orders:
        order = successful_orders[0]

        # Consultar estado del pedido
        order_id_safe = order.order_id or "N/A"
        order_id_short = order_id_safe[:8] if order_id_safe != "N/A" else "N/A"
        print(f"\n📋 Consultando estado del pedido {order_id_short}...")
        status = facade.get_order_status(order_id_safe)

        if status:
            print("✅ Información del pedido encontrada:")
            print(f"   Cliente: {status['customer_id']}")
            print(f"   Producto: {status['sku']} x {status['qty']}")
            print(f"   Total: ${status['total_amount']:.2f}")
            print(f"   Estado: {status['status']}")

            if "shipping_status" in status:
                print(f"   Estado del envío: {status['shipping_status']['status']}")

        # Demostrar cancelación de pedido
        print(f"\n🚫 Cancelando pedido {order_id_short}...")
        cancel_success = facade.cancel_order(order_id_safe, "customer_001")

        if cancel_success:
            print("✅ Pedido cancelado exitosamente")
        else:
            print("❌ Error cancelando el pedido")


def demo_customer_history(facade: OrderFacade) -> None:
    """Demuestra el historial de pedidos por cliente."""
    print_separator("DEMO 4: HISTORIAL DE CLIENTES")

    # Obtener historial del cliente 1
    print("\n📊 Historial de pedidos - Cliente 001:")
    history = facade.get_order_history("customer_001")

    if history:
        for i, order in enumerate(history, 1):
            print(
                f"   {i}. Pedido {order['order_id'][:8]}... - {order['sku']} x {order['qty']}"
            )
            print(
                f"      Total: ${order['total_amount']:.2f} - Estado: {order['status']}"
            )
    else:
        print("   No hay pedidos en el historial")

    # Obtener historial del cliente 2
    print("\n📊 Historial de pedidos - Cliente 002:")
    history2 = facade.get_order_history("customer_002")

    if history2:
        for i, order in enumerate(history2, 1):
            print(
                f"   {i}. Pedido {order['order_id'][:8]}... - {order['sku']} x {order['qty']}"
            )
            print(
                f"      Total: ${order['total_amount']:.2f} - Estado: {order['status']}"
            )
    else:
        print("   No hay pedidos en el historial")


def demo_system_statistics(facade: OrderFacade) -> None:
    """Demuestra las estadísticas del sistema."""
    print_separator("DEMO 5: ESTADÍSTICAS DEL SISTEMA")

    stats = facade.get_system_stats()

    print("\n📈 Estadísticas Generales:")
    print(f"   Pedidos exitosos: {stats['total_successful_orders']}")
    print(f"   Pedidos fallidos: {stats['total_failed_orders']}")
    print(f"   Tasa de éxito: {stats['success_rate_percentage']:.2f}%")

    print("\n📦 Estado del Inventario:")
    inventory = stats["inventory_status"]
    for sku, quantity in inventory.items():
        status = "⚠️  BAJO STOCK" if quantity <= 2 else "✅ DISPONIBLE"
        print(f"   {sku}: {quantity} unidades - {status}")

    print("\n🚚 Carriers Disponibles:")
    carriers = stats["available_carriers"]
    for carrier_type, info in carriers.items():
        print(
            f"   {carrier_type.capitalize()}: {info['name']} ({info['days']} días, ${info['cost']:.2f})"
        )

    print("\n📧 Estadísticas de Notificaciones:")
    notif_stats = stats["notification_stats"]
    if notif_stats["total"] > 0:
        print(f"   Total de notificaciones enviadas: {notif_stats['total']}")
        print("   Por canal:")
        for channel, count in notif_stats["by_channel"].items():
            print(f"     {channel}: {count}")
    else:
        print("   No hay notificaciones registradas")


def demo_notification_preferences(facade: OrderFacade) -> None:
    """Demuestra la configuración de preferencias de notificación."""
    print_separator("DEMO 6: PREFERENCIAS DE NOTIFICACIÓN")

    print("\n🔔 Configurando preferencias de notificación...")

    # Configurar preferencias para diferentes clientes
    facade.notifications.set_customer_preferences(
        "customer_001", [NotificationChannel.EMAIL, NotificationChannel.SMS]
    )

    facade.notifications.set_customer_preferences(
        "customer_002", [NotificationChannel.EMAIL, NotificationChannel.PUSH]
    )

    print("✅ Preferencias configuradas para clientes")

    # Enviar notificación de prueba
    print("\n📧 Enviando notificación de prueba...")
    result = facade.notifications.send_bulk_notification(
        ["customer_001", "customer_002", "customer_003"],
        "¡Oferta especial! 20% de descuento en todos los productos electrónicos.",
        NotificationChannel.EMAIL,
    )

    print(f"   Enviadas: {result['sent']}")
    print(f"   Fallidas: {result['failed']}")


def interactive_demo() -> OrderFacade:
    """Demostración interactiva del sistema."""
    print_separator("DEMOSTRACIÓN INTERACTIVA")

    facade = OrderFacade()

    print("\n¡Bienvenido a la demostración interactiva del Order Facade!")
    print("\nEste sistema demuestra el patrón Facade orquestando:")
    print("• 📦 Servicio de Inventario")
    print("• 💳 Gateway de Pagos")
    print("• 🚚 Servicio de Envíos")
    print("• 📧 Servicio de Notificaciones")

    input("\nPresiona Enter para continuar...")

    # Demo 1: Pedidos exitosos
    successful_orders = demo_successful_orders(facade)
    input("\nPresiona Enter para continuar con los errores...")

    # Demo 2: Manejo de errores
    demo_failed_orders(facade)
    input("\nPresiona Enter para continuar con la gestión...")

    # Demo 3: Gestión de pedidos
    demo_order_management(facade, successful_orders)
    input("\nPresiona Enter para ver el historial...")

    # Demo 4: Historial de clientes
    demo_customer_history(facade)
    input("\nPresiona Enter para ver las estadísticas...")

    # Demo 5: Estadísticas del sistema
    demo_system_statistics(facade)
    input("\nPresiona Enter para configurar notificaciones...")

    # Demo 6: Preferencias de notificación
    demo_notification_preferences(facade)

    print_separator("FIN DE LA DEMOSTRACIÓN")
    print("\n🎉 ¡Demostración completada exitosamente!")
    print("\n✨ Beneficios del patrón Facade demostrados:")
    print("• Interfaz simplificada para operaciones complejas")
    print("• Ocultación de la complejidad de múltiples subsistemas")
    print("• Manejo centralizado de errores y rollbacks")
    print("• Facilidad para testing y mantenimiento")
    print("• Desacoplamiento entre cliente y subsistemas")

    return facade


def automated_demo() -> OrderFacade:
    """Demostración automatizada sin interacción del usuario."""
    print_separator("DEMOSTRACIÓN AUTOMATIZADA DEL PATRÓN FACADE")

    facade = OrderFacade()

    print("\n🚀 Ejecutando demostración automatizada...")
    print("Mostrando el patrón Facade en acción...")

    # Ejecutar todas las demos automáticamente
    successful_orders = demo_successful_orders(facade)
    demo_failed_orders(facade)
    demo_order_management(facade, successful_orders)
    demo_customer_history(facade)
    demo_system_statistics(facade)
    demo_notification_preferences(facade)

    print_separator("RESUMEN DE LA DEMOSTRACIÓN")

    # Estadísticas finales
    final_stats = facade.get_system_stats()
    print(f"\n📊 Resumen Final:")
    print(
        f"• Pedidos procesados exitosamente: {final_stats['total_successful_orders']}"
    )
    print(f"• Pedidos con errores: {final_stats['total_failed_orders']}")
    print(f"• Tasa de éxito del sistema: {final_stats['success_rate_percentage']:.1f}%")
    print(f"• Notificaciones enviadas: {final_stats['notification_stats']['total']}")

    return facade


def main() -> None:
    """Función principal del script de demostración."""
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        facade = interactive_demo()
    else:
        facade = automated_demo()

    print("\n" + "=" * 60)
    print("  PATRÓN FACADE - DEMOSTRACIÓN COMPLETADA")
    print("=" * 60)
    print("\n📚 Para más información:")
    print("• README.md - Documentación completa")
    print("• tests/ - Casos de prueba exhaustivos")
    print("• src/order_facade/ - Código fuente comentado")
    print("\n💻 Para ejecutar tests:")
    print("  pytest tests/ -v")
    print("\n🔧 Para ejecutar demo interactivo:")
    print("  python -m src.order_facade.demo --interactive")

    # Evitar el warning de mypy sobre falta de return
    return


if __name__ == "__main__":
    main()
