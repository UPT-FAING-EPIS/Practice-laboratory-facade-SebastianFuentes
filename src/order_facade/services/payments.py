"""
Servicio de Pagos - Procesamiento de transacciones financieras.

Este módulo maneja el procesamiento de pagos y validación de tarjetas
de crédito en el sistema.
"""

import uuid
from dataclasses import dataclass
from typing import Dict, Optional
from decimal import Decimal


@dataclass
class PaymentReceipt:
    """Recibo de pago con información de la transacción."""

    success: bool
    transaction_id: str = ""
    message: str = ""
    amount: Optional[Decimal] = None
    timestamp: Optional[str] = None


class PaymentGateway:
    """Gateway de pagos para procesar transacciones financieras."""

    def __init__(self):
        """Inicializa el gateway con configuración simulada."""
        # Simulación de diferentes tipos de tarjetas y sus comportamientos
        self._card_behaviors = {
            "4": "visa_success",  # Visa - éxito
            "5": "mastercard_success",  # MasterCard - éxito
            "3": "amex_decline",  # Amex - rechazada
            "6": "discover_decline",  # Discover - rechazada
        }

    def charge(self, payment_info: Dict, amount: float) -> PaymentReceipt:
        """
        Procesa un cargo a la tarjeta de crédito.

        Args:
            payment_info: Información de pago (card_number, cvv, etc.)
            amount: Monto a cobrar

        Returns:
            PaymentReceipt con el resultado de la transacción
        """
        card_number = payment_info.get("card_number", "")

        # Validaciones básicas
        if not card_number:
            return PaymentReceipt(success=False, message="Número de tarjeta requerido")

        if amount <= 0:
            return PaymentReceipt(
                success=False, message="El monto debe ser mayor a cero"
            )

        if len(card_number) < 15:
            return PaymentReceipt(success=False, message="Número de tarjeta inválido")

        # Simulación de validación y riesgo
        first_digit = card_number[0]
        behavior = self._card_behaviors.get(first_digit, "unknown")

        if behavior in ["visa_success", "mastercard_success"]:
            transaction_id = str(uuid.uuid4())
            card_type = "Visa" if first_digit == "4" else "MasterCard"
            print(
                f"[Payment] Cargo exitoso: ${amount:.2f} en tarjeta {card_type} ****{card_number[-4:]}"
            )
            return PaymentReceipt(
                success=True,
                transaction_id=transaction_id,
                amount=Decimal(str(amount)),
                message=f"Pago procesado exitosamente con {card_type}",
            )
        else:
            print(f"[Payment] Pago rechazado para tarjeta ****{card_number[-4:]}")
            return PaymentReceipt(
                success=False,
                message="Pago rechazado - Fondos insuficientes o tarjeta bloqueada",
            )

    def refund(self, transaction_id: str, amount: float) -> PaymentReceipt:
        """
        Procesa un reembolso.

        Args:
            transaction_id: ID de la transacción original
            amount: Monto a reembolsar

        Returns:
            PaymentReceipt con el resultado del reembolso
        """
        if not transaction_id:
            return PaymentReceipt(
                success=False, message="ID de transacción requerido para reembolso"
            )

        refund_id = str(uuid.uuid4())
        print(
            f"[Payment] Reembolso procesado: ${amount:.2f} (TX: {transaction_id[:8]}...)"
        )
        return PaymentReceipt(
            success=True,
            transaction_id=refund_id,
            amount=Decimal(str(amount)),
            message="Reembolso procesado exitosamente",
        )

    def validate_card(self, payment_info: Dict) -> bool:
        """
        Valida la información básica de la tarjeta.

        Args:
            payment_info: Información de pago

        Returns:
            True si la tarjeta es válida, False en caso contrario
        """
        card_number = payment_info.get("card_number", "")
        cvv = payment_info.get("cvv", "")
        expiry = payment_info.get("expiry", "")

        # Validaciones básicas
        if len(card_number) < 15 or len(card_number) > 19:
            return False

        if len(cvv) < 3 or len(cvv) > 4:
            return False

        if not expiry or len(expiry) != 5:  # MM/YY format
            return False

        return True
