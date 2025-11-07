"""
Servicio de Inventario - Gestión de stock y reservas.

Este módulo maneja la verificación de stock y las reservas de productos
en el sistema de inventario.
"""

from typing import Dict


class InventoryService:
    """Servicio para gestionar el inventario de productos."""

    def __init__(self):
        """Inicializa el servicio con stock simulado."""
        # Stock simulado: sku -> cantidad
        self._stock: Dict[str, int] = {
            "MONITOR-27": 10,
            "WASHER-7KG": 2,
            "LAPTOP-15": 5,
            "SMARTPHONE-X": 8,
            "TABLET-10": 3,
        }

    def check_stock(self, sku: str, qty: int) -> bool:
        """
        Verifica si hay suficiente stock disponible.

        Args:
            sku: Código del producto
            qty: Cantidad solicitada

        Returns:
            True si hay suficiente stock, False en caso contrario
        """
        return self._stock.get(sku, 0) >= qty

    def reserve(self, sku: str, qty: int) -> bool:
        """
        Reserva productos del inventario.

        Args:
            sku: Código del producto
            qty: Cantidad a reservar

        Returns:
            True si la reserva fue exitosa, False en caso contrario
        """
        if self.check_stock(sku, qty):
            self._stock[sku] -= qty
            print(
                f"[Inventory] Reservados {qty} unidades de {sku}. Stock restante: {self._stock[sku]}"
            )
            return True
        print(
            f"[Inventory] No se pudo reservar {qty} unidades de {sku}. Stock disponible: {self._stock.get(sku, 0)}"
        )
        return False

    def release(self, sku: str, qty: int) -> None:
        """
        Libera productos previamente reservados.

        Args:
            sku: Código del producto
            qty: Cantidad a liberar
        """
        self._stock[sku] = self._stock.get(sku, 0) + qty
        print(
            f"[Inventory] Liberados {qty} unidades de {sku}. Stock actual: {self._stock[sku]}"
        )

    def get_current_stock(self, sku: str) -> int:
        """
        Obtiene el stock actual de un producto.

        Args:
            sku: Código del producto

        Returns:
            Cantidad disponible en stock
        """
        return self._stock.get(sku, 0)

    def list_products(self) -> Dict[str, int]:
        """
        Lista todos los productos y su stock disponible.

        Returns:
            Diccionario con productos y su stock
        """
        return self._stock.copy()
