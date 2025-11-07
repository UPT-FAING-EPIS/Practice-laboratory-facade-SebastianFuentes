"""
Servicio de Envíos - Gestión de logística y envíos.

Este módulo maneja la creación de envíos y cálculo de tiempos de entrega
para el sistema de logística.
"""

import uuid
from dataclasses import dataclass
from typing import List, Dict, Optional, Union
from datetime import datetime, timedelta


@dataclass
class ShipmentInfo:
    """Información de envío con detalles logísticos."""

    success: bool
    shipment_id: str = ""
    eta_days: int = 0
    message: str = ""
    tracking_number: str = ""
    carrier: str = ""
    estimated_delivery: Optional[str] = None


class ShippingService:
    """Servicio de envíos para gestionar la logística de productos."""

    def __init__(self) -> None:
        """Inicializa el servicio con configuración de carriers."""
        self._carriers: Dict[str, Dict[str, Union[str, int, float]]] = {
            "standard": {"name": "Correos Nacionales", "days": 5, "cost": 10.0},
            "express": {"name": "Express Delivery", "days": 3, "cost": 25.0},
            "premium": {"name": "Premium Logistics", "days": 1, "cost": 50.0},
        }

        # Zonas de cobertura simuladas
        self._coverage_zones = {
            "zone_1": ["Lima", "Callao", "Miraflores"],
            "zone_2": ["Arequipa", "Trujillo", "Chiclayo"],
            "zone_3": ["Cusco", "Huancayo", "Piura"],
        }

    def create_shipment(
        self,
        customer_id: str,
        items: List[Dict],
        shipping_address: Optional[Dict] = None,
        shipping_type: str = "standard",
    ) -> ShipmentInfo:
        """
        Crea un nuevo envío.

        Args:
            customer_id: ID del cliente
            items: Lista de productos a enviar
            shipping_address: Dirección de envío (opcional)
            shipping_type: Tipo de envío (standard, express, premium)

        Returns:
            ShipmentInfo con detalles del envío
        """
        # Validaciones básicas
        if not items:
            return ShipmentInfo(success=False, message="No hay productos para enviar")

        if not customer_id:
            return ShipmentInfo(success=False, message="ID de cliente requerido")

        # Validar tipo de envío
        if shipping_type not in self._carriers:
            shipping_type = "standard"

        carrier_info = self._carriers[shipping_type]

        # Generar IDs únicos
        shipment_id = str(uuid.uuid4())
        tracking_number = f"TRK{shipment_id[:8].upper()}"

        # Calcular fecha estimada de entrega
        days_value = carrier_info["days"]
        days = int(days_value) if isinstance(days_value, (int, float)) else 5
        delivery_date = datetime.now() + timedelta(days=days)

        # Simular zona de cobertura
        city = self._get_customer_city(customer_id, shipping_address)
        zone = self._get_shipping_zone(city)

        # Ajustar tiempo de entrega según la zona
        if zone == "zone_3":
            delivery_date += timedelta(days=1)  # Zona remota

        print(f"[Shipping] Envío creado: {tracking_number} via {carrier_info['name']}")
        print(f"[Shipping] Destino: {city} (Zona {zone[-1]})")
        print(f"[Shipping] Entrega estimada: {delivery_date.strftime('%Y-%m-%d')}")

        return ShipmentInfo(
            success=True,
            shipment_id=shipment_id,
            eta_days=days + (1 if zone == "zone_3" else 0),
            tracking_number=tracking_number,
            carrier=str(carrier_info["name"]),
            estimated_delivery=delivery_date.strftime("%Y-%m-%d"),
            message=f"Envío programado via {carrier_info['name']}",
        )

    def track_shipment(self, tracking_number: str) -> Dict:
        """
        Rastrea un envío existente.

        Args:
            tracking_number: Número de seguimiento

        Returns:
            Diccionario con información de rastreo
        """
        # Simulación de estados de envío
        statuses = [
            "Paquete recibido en centro de distribución",
            "En tránsito",
            "En reparto",
            "Entregado",
        ]

        import random

        current_status = random.choice(statuses)

        return {
            "tracking_number": tracking_number,
            "status": current_status,
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "location": "Centro de Distribución Lima",
        }

    def cancel_shipment(self, shipment_id: str) -> bool:
        """
        Cancela un envío.

        Args:
            shipment_id: ID del envío a cancelar

        Returns:
            True si la cancelación fue exitosa
        """
        print(f"[Shipping] Envío {shipment_id[:8]}... cancelado")
        return True

    def calculate_shipping_cost(
        self, items: List[Dict], shipping_type: str = "standard"
    ) -> float:
        """
        Calcula el costo de envío.

        Args:
            items: Lista de productos
            shipping_type: Tipo de envío

        Returns:
            Costo total de envío
        """
        carrier_data = self._carriers.get(shipping_type, self._carriers["standard"])
        cost_value = carrier_data["cost"]
        base_cost = float(cost_value) if isinstance(cost_value, (int, float)) else 10.0

        # Costo adicional por peso (simulado)
        weights = []
        for item in items:
            weight = item.get("weight", 1)
            weights.append(float(weight) if isinstance(weight, (int, float)) else 1.0)

        total_weight = sum(weights)
        weight_cost = max(0, (total_weight - 2) * 5)  # Costo extra por kg adicional

        return float(base_cost + weight_cost)

    def get_available_carriers(self) -> Dict:
        """
        Obtiene la lista de carriers disponibles.

        Returns:
            Diccionario con información de carriers
        """
        carriers_copy: Dict[str, Dict[str, Union[str, int, float]]] = (
            self._carriers.copy()
        )
        return carriers_copy

    def _get_customer_city(self, customer_id: str, address: Optional[Dict]) -> str:
        """Obtiene la ciudad del cliente (simulado)."""
        if address and "city" in address:
            city_value = address["city"]
            return str(city_value) if city_value else "Lima"

        # Simulación basada en customer_id
        cities = ["Lima", "Arequipa", "Trujillo", "Cusco", "Chiclayo"]
        return cities[hash(customer_id) % len(cities)]

    def _get_shipping_zone(self, city: str) -> str:
        """Determina la zona de envío basada en la ciudad."""
        for zone, cities in self._coverage_zones.items():
            if city in cities:
                return zone
        return "zone_2"  # Zona por defecto
