# src/notifiers/discord_notifier.py
"""
💬 Notificador para Discord usando webhooks
"""

import requests
from datetime import datetime
from typing import Optional
from src.notifiers.base import BaseNotifier
from src.config.settings import settings
from src.config.constants import (
    DISCORD_EMBED_COLOR,
    DISCORD_MAX_DESCRIPTION_LENGTH,
    UNVIME_LOGO_URL
)


class DiscordNotifier(BaseNotifier):
    """
    Notificador que envía mensajes a Discord mediante webhooks.
    
    Requiere configurar DISCORD_WEBHOOK_URL en .env
    """
    
    def __init__(self, webhook_url: Optional[str] = None):
        """
        Inicializa el notificador de Discord.
        
        Args:
            webhook_url: URL del webhook (opcional, usa la de config por defecto)
        """
        super().__init__("Discord")
        self.webhook_url = webhook_url or settings.discord_webhook_url
    
    def is_configured(self) -> bool:
        """
        Verifica si Discord está configurado.
        
        Returns:
            True si el webhook está configurado
        """
        return self.webhook_url is not None and self.webhook_url != ""
    
    def enviar(self, mensaje: str) -> bool:
        """
        Envía un mensaje a Discord.
        
        Args:
            mensaje: Mensaje en formato markdown
            
        Returns:
            True si se envió exitosamente
        """
        if not self.is_configured():
            self.logger.error("Discord webhook no configurado")
            return False
        
        try:
            # Adaptar formato para Discord
            mensaje_adaptado = self._adaptar_formato_discord(mensaje)
            
            # Crear payload
            payload = self._crear_payload(mensaje_adaptado)
            
            # Enviar
            self.logger.info("Enviando notificación a Discord...")
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            
            self.logger.info("✅ Notificación enviada exitosamente a Discord")
            return True
            
        except requests.exceptions.Timeout:
            self.logger.error("⏱️ Timeout al conectar con Discord")
            return False
            
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"❌ Error HTTP al enviar a Discord: {e}")
            if hasattr(e.response, 'text'):
                self.logger.debug(f"Respuesta del servidor: {e.response.text}")
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Error inesperado: {e}", exc_info=True)
            return False
    
    def _crear_payload(self, mensaje: str) -> dict:
        """
        Crea el payload JSON para Discord.
        
        Args:
            mensaje: Mensaje adaptado para Discord
            
        Returns:
            Diccionario con el payload
        """
        # Truncar si es muy largo
        if len(mensaje) > DISCORD_MAX_DESCRIPTION_LENGTH:
            mensaje = mensaje[:DISCORD_MAX_DESCRIPTION_LENGTH - 50] + "\n\n... (mensaje truncado)"
            self.logger.warning("Mensaje truncado por límite de Discord")
        
        return {
            "username": "Pregón",
            "avatar_url": "https://i.imgur.com/8osiyMR.png",
            "embeds": [
                {
                    "title": "📅 Calendario Académico UNViMe - Próxima Semana",
                    "description": mensaje,
                    "color": DISCORD_EMBED_COLOR,
                    "footer": {
                        "text": f"Pregon Bot • {datetime.now().strftime('%d/%m/%Y %H:%M')}"
                    },
                    "thumbnail": {
                        "url": UNVIME_LOGO_URL
                    }
                }
            ]
        }
    
    def _adaptar_formato_discord(self, mensaje: str) -> str:
        """
        Adapta el formato markdown para Discord.
        
        Args:
            mensaje: Mensaje original
            
        Returns:
            Mensaje adaptado
        """
        # Discord usa markdown similar, solo quitamos el título principal
        # ya que va en el campo "title" del embed
        lineas = mensaje.split('\n')
        resultado = []
        
        for linea in lineas:
            # Saltar el título principal
            if linea.strip().startswith('📅 **EVENTOS'):
                continue
            resultado.append(linea)
        
        return '\n'.join(resultado)