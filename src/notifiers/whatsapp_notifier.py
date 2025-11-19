# src/notifiers/whatsapp_notifier.py
"""
📱 Notificador para WhatsApp usando Twilio
"""

from typing import Optional
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from src.notifiers.base import BaseNotifier
from src.config.settings import settings


class WhatsAppNotifier(BaseNotifier):
    """
    Notificador que envía mensajes a WhatsApp mediante Twilio.
    
    Requiere configurar en .env:
    - TWILIO_ACCOUNT_SID
    - TWILIO_AUTH_TOKEN
    - TWILIO_WHATSAPP_FROM
    - TWILIO_WHATSAPP_TO
    
    Para desarrollo, puedes usar el sandbox gratuito de Twilio:
    https://www.twilio.com/console/sms/whatsapp/learn
    """
    
    def __init__(
        self,
        account_sid: Optional[str] = None,
        auth_token: Optional[str] = None,
        from_number: Optional[str] = None,
        to_number: Optional[str] = None
    ):
        """
        Inicializa el notificador de WhatsApp.
        
        Args:
            account_sid: Twilio Account SID (opcional, usa config)
            auth_token: Twilio Auth Token (opcional, usa config)
            from_number: Número de origen (opcional, usa config)
            to_number: Número destino (opcional, usa config)
        """
        super().__init__("WhatsApp")
        
        self.account_sid = account_sid or settings.twilio_account_sid
        self.auth_token = auth_token or settings.twilio_auth_token
        self.from_number = from_number or settings.twilio_whatsapp_from
        self.to_number = to_number or settings.twilio_whatsapp_to
        
        self.client = None
        if self.is_configured():
            try:
                self.client = Client(self.account_sid, self.auth_token)
                self.logger.info("Cliente de Twilio inicializado correctamente")
            except Exception as e:
                self.logger.error(f"Error inicializando cliente de Twilio: {e}")
    
    def is_configured(self) -> bool:
        """
        Verifica si WhatsApp/Twilio está configurado.
        
        Returns:
            True si todas las credenciales están presentes
        """
        return all([
            self.account_sid,
            self.auth_token,
            self.from_number,
            self.to_number
        ])
    
    def enviar(self, mensaje: str) -> bool:
        """
        Envía un mensaje por WhatsApp.
        
        Args:
            mensaje: Mensaje a enviar
            
        Returns:
            True si se envió exitosamente
        """
        if not self.is_configured():
            self.logger.error("WhatsApp/Twilio no está configurado")
            return False
        
        if not self.client:
            self.logger.error("Cliente de Twilio no inicializado")
            return False
        
        try:
            # Adaptar mensaje para WhatsApp (texto plano, sin markdown complejo)
            mensaje_adaptado = self._adaptar_formato_whatsapp(mensaje)
            
            self.logger.info(f"Enviando mensaje a WhatsApp: {self.to_number}")
            
            # 🔧 LOG DEBUG: Ver qué se está enviando
            self.logger.debug(f"From: {self.from_number}")
            self.logger.debug(f"To: {self.to_number}")
            self.logger.debug(f"Body length: {len(mensaje_adaptado)}")
            
            # Enviar mensaje
            message = self.client.messages.create(
                from_=self.from_number,
                to=self.to_number,
                body=mensaje_adaptado
            )
            
            self.logger.info(f"✅ Mensaje enviado exitosamente. SID: {message.sid}")
            self.logger.debug(f"Estado: {message.status}")
            
            return True
            
        except TwilioRestException as e:
            self.logger.error(f"❌ Error de Twilio: {e.msg}")
            self.logger.debug(f"Código: {e.code}, Status: {e.status}")
            
            # Debug adicional
            self.logger.debug(f"From number: '{self.from_number}'")
            self.logger.debug(f"To number: '{self.to_number}'")
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Error inesperado: {e}", exc_info=True)
            return False
    
    def _adaptar_formato_whatsapp(self, mensaje: str) -> str:
        """
        Adapta el mensaje para WhatsApp.
        WhatsApp soporta markdown limitado: *negrita*, _cursiva_, ~tachado~
        
        Args:
            mensaje: Mensaje original
            
        Returns:
            Mensaje adaptado para WhatsApp
        """
        # WhatsApp no soporta ** para negrita, usa *
        mensaje = mensaje.replace('**', '*')
        
        # Simplificar emojis complejos si es necesario
        # (WhatsApp soporta emojis bien, así que los dejamos)
        
        # Limitar longitud (WhatsApp tiene límite de ~1600 caracteres)
        MAX_LENGTH = 1600
        if len(mensaje) > MAX_LENGTH:
            mensaje = mensaje[:MAX_LENGTH - 50] + "\n\n... (mensaje truncado)"
            self.logger.warning("Mensaje truncado por límite de WhatsApp")
        
        return mensaje
    
    def verificar_estado(self) -> dict:
        """
        Verifica el estado de la conexión con Twilio.
        Útil para debugging.
        
        Returns:
            Diccionario con información de estado
        """
        if not self.is_configured():
            return {"configurado": False, "error": "Credenciales faltantes"}
        
        try:
            # Intentar obtener información de la cuenta
            account = self.client.api.accounts(self.account_sid).fetch()
            
            return {
                "configurado": True,
                "account_sid": account.sid,
                "status": account.status,
                "friendly_name": account.friendly_name
            }
            
        except Exception as e:
            return {
                "configurado": True,
                "error": str(e)
            }