"""
Servicio de Notificaciones - Gestión de comunicaciones con clientes.

Este módulo maneja el envío de notificaciones por diferentes canales
como email, SMS y push notifications.
"""

from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum


class NotificationChannel(Enum):
    """Canales disponibles para notificaciones."""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"


class NotificationService:
    """Servicio de notificaciones multi-canal."""
    
    def __init__(self):
        """Inicializa el servicio con configuración de canales."""
        self._sent_notifications = []
        self._customer_preferences = {}
        
        # Plantillas de notificación
        self._templates = {
            "order_confirmed": {
                "subject": "Pedido Confirmado - #{order_id}",
                "message": "Tu pedido #{order_id} ha sido confirmado. Total: ${amount:.2f}. ID de transacción: {transaction_id}"
            },
            "order_shipped": {
                "subject": "Pedido Enviado - #{order_id}",
                "message": "Tu pedido #{order_id} ha sido enviado. Número de seguimiento: {tracking_number}. Entrega estimada: {eta}"
            },
            "order_delivered": {
                "subject": "Pedido Entregado - #{order_id}",
                "message": "Tu pedido #{order_id} ha sido entregado exitosamente. ¡Gracias por tu compra!"
            },
            "payment_failed": {
                "subject": "Error en el Pago - #{order_id}",
                "message": "No se pudo procesar el pago para tu pedido #{order_id}. Razón: {reason}"
            }
        }
    
    def notify(self, customer_id: str, message: str, 
               channel: NotificationChannel = NotificationChannel.EMAIL) -> bool:
        """
        Envía una notificación simple.
        
        Args:
            customer_id: ID del cliente
            message: Mensaje a enviar
            channel: Canal de notificación
            
        Returns:
            True si la notificación fue enviada exitosamente
        """
        try:
            notification = {
                "customer_id": customer_id,
                "message": message,
                "channel": channel.value,
                "timestamp": datetime.now().isoformat(),
                "status": "sent"
            }
            
            self._sent_notifications.append(notification)
            
            # Simular envío según el canal
            if channel == NotificationChannel.EMAIL:
                print(f"[Email] to {customer_id}: {message}")
            elif channel == NotificationChannel.SMS:
                print(f"[SMS] to {customer_id}: {message}")
            elif channel == NotificationChannel.PUSH:
                print(f"[Push] to {customer_id}: {message}")
            else:
                print(f"[In-App] to {customer_id}: {message}")
            
            return True
            
        except Exception as e:
            print(f"[Notification Error] Failed to send to {customer_id}: {str(e)}")
            return False
    
    def send_order_notification(self, customer_id: str, notification_type: str, 
                               order_data: Dict, channels: Optional[List[NotificationChannel]] = None) -> Dict:
        """
        Envía notificación usando plantillas predefinidas.
        
        Args:
            customer_id: ID del cliente
            notification_type: Tipo de notificación (order_confirmed, order_shipped, etc.)
            order_data: Datos del pedido para personalizar el mensaje
            channels: Canales a usar (si no se especifica, usa preferencias del cliente)
            
        Returns:
            Diccionario con resultados del envío por canal
        """
        if notification_type not in self._templates:
            return {"error": f"Tipo de notificación '{notification_type}' no válido"}
        
        template = self._templates[notification_type]
        
        # Personalizar mensaje con datos del pedido
        try:
            subject = template["subject"].format(**order_data)
            message = template["message"].format(**order_data)
        except KeyError as e:
            return {"error": f"Falta el campo requerido: {str(e)}"}
        
        # Determinar canales a usar
        if channels is None:
            channels = self._get_customer_notification_preferences(customer_id)
        
        results = {}
        
        # Enviar por cada canal
        for channel in channels:
            success = self.notify(customer_id, f"{subject}\n\n{message}", channel)
            results[channel.value] = "success" if success else "failed"
        
        return results
    
    def set_customer_preferences(self, customer_id: str, 
                                preferences: List[NotificationChannel]) -> None:
        """
        Establece las preferencias de notificación del cliente.
        
        Args:
            customer_id: ID del cliente
            preferences: Lista de canales preferidos
        """
        self._customer_preferences[customer_id] = preferences
        print(f"[Notifications] Preferencias actualizadas para {customer_id}: {[p.value for p in preferences]}")
    
    def get_notification_history(self, customer_id: str) -> List[Dict]:
        """
        Obtiene el historial de notificaciones de un cliente.
        
        Args:
            customer_id: ID del cliente
            
        Returns:
            Lista de notificaciones enviadas
        """
        return [n for n in self._sent_notifications if n["customer_id"] == customer_id]
    
    def send_bulk_notification(self, customer_ids: List[str], message: str,
                             channel: NotificationChannel = NotificationChannel.EMAIL) -> Dict:
        """
        Envía notificación masiva a múltiples clientes.
        
        Args:
            customer_ids: Lista de IDs de clientes
            message: Mensaje a enviar
            channel: Canal de notificación
            
        Returns:
            Diccionario con estadísticas del envío
        """
        results = {"sent": 0, "failed": 0, "details": []}
        
        for customer_id in customer_ids:
            success = self.notify(customer_id, message, channel)
            if success:
                results["sent"] += 1
            else:
                results["failed"] += 1
            
            results["details"].append({
                "customer_id": customer_id,
                "status": "sent" if success else "failed"
            })
        
        print(f"[Bulk Notification] Enviado: {results['sent']}, Fallidos: {results['failed']}")
        return results
    
    def _get_customer_notification_preferences(self, customer_id: str) -> List[NotificationChannel]:
        """
        Obtiene las preferencias de notificación del cliente.
        
        Args:
            customer_id: ID del cliente
            
        Returns:
            Lista de canales preferidos (por defecto: email)
        """
        return self._customer_preferences.get(
            customer_id, 
            [NotificationChannel.EMAIL]  # Canal por defecto
        )
    
    def get_notification_stats(self) -> Dict:
        """
        Obtiene estadísticas de notificaciones enviadas.
        
        Returns:
            Diccionario con estadísticas
        """
        total_notifications = len(self._sent_notifications)
        
        if total_notifications == 0:
            return {"total": 0, "by_channel": {}, "by_customer": {}}
        
        # Estadísticas por canal
        by_channel = {}
        by_customer = {}
        
        for notification in self._sent_notifications:
            channel = notification["channel"]
            customer = notification["customer_id"]
            
            by_channel[channel] = by_channel.get(channel, 0) + 1
            by_customer[customer] = by_customer.get(customer, 0) + 1
        
        return {
            "total": total_notifications,
            "by_channel": by_channel,
            "by_customer": by_customer
        }