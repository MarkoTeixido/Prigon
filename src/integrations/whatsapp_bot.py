# src/integrations/whatsapp_bot.py
"""
📱 Bot interactivo de WhatsApp para Pregon
Maneja respuestas de usuarios y comandos
"""

from typing import Dict, Optional
from src.integrations.calendar_manager import CalendarManager
from src.ai.chatbot import CalendarioChatbot
from src.notifiers.whatsapp_notifier import WhatsAppNotifier
from src.utils.logger import setup_logger


class WhatsAppBot:
    """
    Bot conversacional de WhatsApp que responde a comandos
    y permite interacción con el calendario.
    """
    
    def __init__(self):
        self.logger = setup_logger("WhatsAppBot")
        self.notifier = WhatsAppNotifier()
        self.chatbot = CalendarioChatbot()
        self.calendar_manager = CalendarManager()
        
        # Comandos disponibles
        self.comandos = {
            'eventos': self._cmd_eventos,
            'calendario': self._cmd_calendario,
            'ayuda': self._cmd_ayuda,
            'help': self._cmd_ayuda,
        }
    
    def procesar_mensaje(self, mensaje: str, numero_remitente: str) -> str:
        """
        Procesa un mensaje entrante de WhatsApp.
        
        Args:
            mensaje: Texto del mensaje
            numero_remitente: Número de teléfono del remitente
            
        Returns:
            Respuesta a enviar
        """
        mensaje_lower = mensaje.lower().strip()
        
        self.logger.info(f"Mensaje de {numero_remitente}: {mensaje}")
        
        # Verificar si es un comando
        for comando, handler in self.comandos.items():
            if mensaje_lower.startswith(comando):
                return handler(mensaje)
        
        # Si no es comando, usar IA para responder
        return self._responder_con_ia(mensaje)
    
    def _cmd_eventos(self, mensaje: str) -> str:
        """Comando: EVENTOS - Muestra eventos de la semana"""
        eventos = self.chatbot.obtener_eventos_semana()
        
        if not eventos:
            return "ℹ️ No hay eventos próximos programados."
        
        # Usar el método del notificador para formatear
        from src.notifiers.whatsapp_notifier import WhatsAppNotifier
        notifier = WhatsAppNotifier()
        return notifier._construir_mensaje_interactivo(eventos)
    
    def _cmd_calendario(self, mensaje: str) -> str:
        """Comando: CALENDARIO - Genera links para agregar eventos"""
        eventos = self.chatbot.obtener_eventos_semana()
        
        if not eventos:
            return "ℹ️ No hay eventos próximos para agregar."
        
        # Generar mensaje con links
        mensaje = self.calendar_manager.generar_mensaje_whatsapp_seleccionable(eventos)
        return mensaje
    
    def _cmd_ayuda(self, mensaje: str) -> str:
        """Comando: AYUDA - Muestra comandos disponibles"""
        return """
🤖 *COMANDOS DISPONIBLES*

📅 *EVENTOS*
Muestra los eventos de la próxima semana

🔗 *CALENDARIO*
Genera links para agregar eventos a tu Google Calendar

❓ *AYUDA*
Muestra este mensaje

💬 *Pregunta libre*
Escribe cualquier pregunta sobre el calendario y te responderé con IA

Ejemplos:
• "¿Cuándo son los exámenes en diciembre?"
• "¿Hay feriados en julio?"
• "Dame todas las fechas importantes"
"""
    
    def _responder_con_ia(self, pregunta: str) -> str:
        """Responde usando IA"""
        try:
            respuesta = self.chatbot.responder_sync(pregunta)
            return respuesta
        except Exception as e:
            self.logger.error(f"Error usando IA: {e}", exc_info=True)
            return (
                "❌ Lo siento, tuve un problema procesando tu mensaje. "
                "Usa *AYUDA* para ver los comandos disponibles."
            )