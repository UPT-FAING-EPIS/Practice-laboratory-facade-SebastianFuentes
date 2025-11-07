"""
Order Facade - Implementación del patrón Facade para sistemas empresariales.

Este paquete implementa el patrón Facade para simplificar la interacción con múltiples
subsistemas en un proceso de pedido: inventario, pagos, envíos y notificaciones.

Autor: SebastianFuentesAvalos
Fecha: 2025-11-07
Licencia: MIT
"""

from .facade import OrderFacade, OrderResult

__version__ = "1.0.0"
__all__ = ["OrderFacade", "OrderResult"]
