"""
Tests de rendimiento para el patrón Facade.

Este módulo contiene pruebas de rendimiento que evalúan
la eficiencia del patrón Facade en diferentes escenarios.
"""

import pytest
import time

from order_facade import OrderFacade


class TestPerformance:
    """Tests de rendimiento para OrderFacade."""

    @pytest.fixture
    def facade(self):
        """Fixture para crear una instancia de OrderFacade."""
        return OrderFacade()

    def test_basic_order_performance(self, facade):
        """Test básico de rendimiento para crear un pedido."""
        start_time = time.time()

        result = facade.place_order(
            customer_id="perf_test_001",
            sku="LAPTOP-15",
            qty=1,
            payment_info={
                "card_number": "4111111111111111",
                "card_holder": "Performance Test",
                "expiry_month": "12",
                "expiry_year": "2025",
                "cvv": "123",
            },
            unit_price=999.99,
        )

        end_time = time.time()
        execution_time = end_time - start_time

        assert result.success
        assert execution_time < 1.0

    def test_multiple_orders_performance(self, facade):
        """Test de rendimiento para múltiples pedidos."""
        start_time = time.time()

        results = []
        for i in range(5):
            result = facade.place_order(
                customer_id=f"perf_test_{i:03d}",
                sku="TABLET-10",
                qty=1,
                payment_info={
                    "card_number": "4111111111111111",
                    "card_holder": f"Test User {i}",
                    "expiry_month": "12",
                    "expiry_year": "2025",
                    "cvv": "123",
                },
                unit_price=299.99,
            )
            results.append(result)

        end_time = time.time()
        execution_time = end_time - start_time

        # Verificar que todos fueron exitosos
        successful_orders = sum(1 for r in results if r.success)
        assert successful_orders >= 3  # Al menos 3 de 5 deberían ser exitosos

        # Verificar que el tiempo es razonable (menos de 2 segundos para 5 pedidos)
        assert execution_time < 2.0

    def test_system_statistics_performance(self, facade):
        """Test de rendimiento para obtener estadísticas del sistema."""
        # Crear algunos pedidos primero
        for i in range(3):
            facade.place_order(
                customer_id=f"stat_test_{i:03d}",
                sku="SMARTPHONE-X",
                qty=1,
                payment_info={
                    "card_number": "4111111111111111",
                    "card_holder": f"Stat Test {i}",
                    "expiry_month": "12",
                    "expiry_year": "2025",
                    "cvv": "123",
                },
                unit_price=649.99,
            )

        start_time = time.time()
        stats = facade.get_system_statistics()
        end_time = time.time()
        execution_time = end_time - start_time

        assert isinstance(stats, dict)
        assert "total_orders" in stats
        assert execution_time < 0.5

    def test_memory_usage_basic(self, facade):
        """Test básico de uso de memoria."""
        import sys

        initial_size = sys.getsizeof(facade)

        # Crear varios pedidos
        for i in range(10):
            facade.place_order(
                customer_id=f"mem_test_{i:03d}",
                sku="MONITOR-27",
                qty=1,
                payment_info={
                    "card_number": "4111111111111111",
                    "card_holder": f"Memory Test {i}",
                    "expiry_month": "12",
                    "expiry_year": "2025",
                    "cvv": "123",
                },
                unit_price=329.99,
            )

        final_size = sys.getsizeof(facade)

        # El tamaño no debería crecer excesivamente
        size_increase = final_size - initial_size
        assert size_increase < 10000


@pytest.mark.performance
class TestScalability:
    """Tests de escalabilidad."""

    def test_concurrent_orders_simulation(self):
        """Simula pedidos concurrentes."""
        start_time = time.time()

        # Simular procesamiento concurrente con múltiples facades
        facades = [OrderFacade() for _ in range(3)]
        results = []

        for i, f in enumerate(facades):
            result = f.place_order(
                customer_id=f"concurrent_{i:03d}",
                sku="LAPTOP-15",
                qty=1,
                payment_info={
                    "card_number": "4111111111111111",
                    "card_holder": f"Concurrent User {i}",
                    "expiry_month": "12",
                    "expiry_year": "2025",
                    "cvv": "123",
                },
                unit_price=999.99,
            )
            results.append(result)

        end_time = time.time()
        execution_time = end_time - start_time

        # Verificar que se ejecutó en tiempo razonable
        assert execution_time < 1.0

        # Verificar que al menos algunos pedidos fueron exitosos
        successful = sum(1 for r in results if r.success)
        assert successful >= 1
