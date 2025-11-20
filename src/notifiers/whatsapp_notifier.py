# src/notifiers/whatsapp_notifier.py
"""
📱 Notificador de WhatsApp usando Twilio
Con botones interactivos para Google Calendar
"""

from typing import List, Optional
from twilio.rest import Client
from src.notifiers.base import BaseNotifier
from src.models.evento import Evento
from src.config.settings import settings


class WhatsAppNotifier(BaseNotifier):
    """
    Notificador que envía mensajes por WhatsApp usando Twilio.
    Incluye botones para agregar eventos a Google Calendar.
    """
    
    def __init__(self):
        super().__init__("WhatsApp")
        
        # Validar configuración
        if not self.is_configured():
            self.logger.error("❌ Configuración de Twilio incompleta en .env")
            self.enabled = False
            return
        
        try:
            # Inicializar cliente de Twilio
            self.client = Client(
                settings.twilio_account_sid,
                settings.twilio_auth_token
            )
            self.from_number = settings.twilio_whatsapp_from
            self.to_number = settings.twilio_whatsapp_to
            
            self.logger.info("Cliente de Twilio inicializado correctamente")
            self.enabled = True
            
        except Exception as e:
            self.logger.error(f"Error inicializando Twilio: {e}", exc_info=True)
            self.enabled = False
    
    def is_configured(self) -> bool:
        """
        Verifica si el notificador está configurado correctamente.
        
        Returns:
            True si todas las credenciales están configuradas
        """
        return all([
            settings.twilio_account_sid,
            settings.twilio_auth_token,
            settings.twilio_whatsapp_from,
            settings.twilio_whatsapp_to
        ])
    
    def enviar(self, eventos: List[Evento]) -> bool:
        """
        Envía notificación por WhatsApp con botones interactivos.
        
        Args:
            eventos: Lista de eventos a notificar
            
        Returns:
            True si se envió correctamente
        """
        if not self.enabled:
            self.logger.warning("Notificador de WhatsApp deshabilitado")
            return False
        
        if not eventos:
            self.logger.info("No hay eventos para notificar")
            return True
        
        try:
            # Construir mensaje con formato mejorado
            mensaje = self._construir_mensaje_interactivo(eventos)
            
            # Enviar mensaje
            message = self.client.messages.create(
                from_=self.from_number,
                body=mensaje,
                to=self.to_number
            )
            
            self.logger.info(f"✅ WhatsApp enviado. SID: {message.sid}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error enviando WhatsApp: {e}", exc_info=True)
            return False
    
    def enviar_con_calendario(self, eventos: List[Evento], link_calendario: str) -> bool:
        """
        Envía notificación con link para agregar a Google Calendar.
        
        Args:
            eventos: Lista de eventos
            link_calendario: URL para agregar eventos
            
        Returns:
            True si se envió correctamente
        """
        if not self.enabled:
            return False
        
        try:
            mensaje = self._construir_mensaje_interactivo(eventos)
            mensaje += f"\n\n🔗 *Agregar todos a tu calendario:*\n{link_calendario}"
            
            message = self.client.messages.create(
                from_=self.from_number,
                body=mensaje,
                to=self.to_number
            )
            
            self.logger.info(f"✅ WhatsApp con calendario enviado. SID: {message.sid}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error enviando WhatsApp: {e}", exc_info=True)
            return False
    
    def _construir_mensaje_interactivo(self, eventos: List[Evento]) -> str:
        """
        Construye mensaje con formato mejorado y emojis.
        
        Args:
            eventos: Lista de eventos
            
        Returns:
            Mensaje formateado
        """
        # Encabezado
        lineas = [
            "🎓 *CALENDARIO ACADÉMICO UNViMe* 🎓",
            "",
            f"📅 *Próximos {len(eventos)} eventos:*",
            ""
        ]
        
        # Agrupar eventos por categoría
        eventos_por_categoria = {}
        for evento in eventos:
            cat = evento.categoria.upper()
            if cat not in eventos_por_categoria:
                eventos_por_categoria[cat] = []
            eventos_por_categoria[cat].append(evento)
        
        # Emojis por categoría
        emojis = {
            "ACADEMICO": "🎓",
            "EXAMEN": "📝",
            "FERIADO": "🎉",
            "INSTITUCIONAL": "🏛️",
            "RECESO": "🏖️",
            "OTRO": "📌"
        }
        
        # Agregar eventos por categoría
        for categoria, eventos_cat in eventos_por_categoria.items():
            emoji = emojis.get(categoria, "📅")
            lineas.append(f"*{emoji} {categoria}*")
            
            for evento in eventos_cat:
                fecha = evento.fecha.strftime("%d/%m (%A)")
                lineas.append(f"• {fecha}: {evento.titulo}")
            
            lineas.append("")
        
        # Footer con instrucciones
        lineas.extend([
            "─────────────────────",
            "💡 *¿Quieres agregar estos eventos a tu Google Calendar?*",
            "",
            "Responde con: *CALENDARIO* y te enviaré los links"
        ])
        
        return "\n".join(lineas)