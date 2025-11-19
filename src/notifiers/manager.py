# src/notifiers/manager.py
"""
🎛️ Manager para coordinar múltiples notificadores
"""

from typing import List
from src.notifiers.base import BaseNotifier
from src.notifiers.discord_notifier import DiscordNotifier
from src.notifiers.whatsapp_notifier import WhatsAppNotifier
from src.models.evento import Evento
from src.utils.logger import setup_logger


class NotificationManager:
    """
    Coordina el envío de notificaciones a través de múltiples canales.
    
    Permite registrar diferentes notificadores y enviar a todos
    o solo a los configurados.
    """
    
    def __init__(self):
        """Inicializa el manager"""
        self.logger = setup_logger("NotificationManager")
        self.notificadores: List[BaseNotifier] = []
    
    def registrar(self, notificador: BaseNotifier) -> None:
        """
        Registra un notificador.
        
        Args:
            notificador: Instancia de un notificador
        """
        self.notificadores.append(notificador)
        estado = "✅" if notificador.is_configured() else "⚠️"
        self.logger.info(f"{estado} Notificador registrado: {notificador.nombre}")
    
    def registrar_todos(self) -> None:
        """
        Registra todos los notificadores disponibles automáticamente.
        """
        self.logger.info("Registrando todos los notificadores...")
        
        # Discord
        discord = DiscordNotifier()
        self.registrar(discord)
        
        # WhatsApp
        whatsapp = WhatsAppNotifier()
        self.registrar(whatsapp)
    
    def obtener_configurados(self) -> List[BaseNotifier]:
        """
        Obtiene solo los notificadores que están configurados.
        
        Returns:
            Lista de notificadores configurados
        """
        return [n for n in self.notificadores if n.is_configured()]
    
    def enviar_a_todos(self, eventos: List[Evento]) -> dict:
        """
        Envía notificaciones a través de todos los canales configurados.
        
        Args:
            eventos: Lista de eventos a notificar
            
        Returns:
            Diccionario con resultados por canal
        """
        configurados = self.obtener_configurados()
        
        if not configurados:
            self.logger.warning("⚠️ No hay notificadores configurados")
            return {"total": 0, "exitosos": 0, "fallidos": 0, "detalles": {}}
        
        self.logger.info(f"📤 Enviando notificaciones a {len(configurados)} canales...")
        
        resultados = {
            "total": len(configurados),
            "exitosos": 0,
            "fallidos": 0,
            "detalles": {}
        }
        
        for notificador in configurados:
            self.logger.info(f"Enviando a {notificador.nombre}...")
            
            try:
                exito = notificador.enviar_resumen(eventos)
                
                if exito:
                    resultados["exitosos"] += 1
                    resultados["detalles"][notificador.nombre] = "✅ Enviado"
                else:
                    resultados["fallidos"] += 1
                    resultados["detalles"][notificador.nombre] = "❌ Falló"
                    
            except Exception as e:
                self.logger.error(f"Error enviando a {notificador.nombre}: {e}")
                resultados["fallidos"] += 1
                resultados["detalles"][notificador.nombre] = f"❌ Error: {str(e)}"
        
        # Log resumen
        self.logger.info(
            f"📊 Resultados: {resultados['exitosos']}/{resultados['total']} exitosos"
        )
        
        return resultados
    
    def enviar_a_canal(self, nombre_canal: str, eventos: List[Evento]) -> bool:
        """
        Envía notificación a un canal específico.
        
        Args:
            nombre_canal: Nombre del notificador ('Discord', 'WhatsApp', etc.)
            eventos: Lista de eventos
            
        Returns:
            True si se envió exitosamente
        """
        for notificador in self.notificadores:
            if notificador.nombre.lower() == nombre_canal.lower():
                if not notificador.is_configured():
                    self.logger.warning(f"{nombre_canal} no está configurado")
                    return False
                
                return notificador.enviar_resumen(eventos)
        
        self.logger.error(f"Notificador '{nombre_canal}' no encontrado")
        return False
    
    def listar_notificadores(self) -> List[dict]:
        """
        Lista todos los notificadores registrados con su estado.
        
        Returns:
            Lista de diccionarios con información de cada notificador
        """
        return [
            {
                "nombre": n.nombre,
                "configurado": n.is_configured(),
                "estado": "✅ Listo" if n.is_configured() else "❌ No configurado"
            }
            for n in self.notificadores
        ]