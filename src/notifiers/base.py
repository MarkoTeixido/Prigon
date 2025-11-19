# src/notifiers/base.py
"""
📬 Clase base abstracta para notificadores
Implementa el patrón Strategy para diferentes canales de notificación
"""

from abc import ABC, abstractmethod
from typing import List
from src.models.evento import Evento
from src.utils.logger import setup_logger


class BaseNotifier(ABC):
    """
    Clase abstracta que define la interfaz para todos los notificadores.
    
    Cada canal de notificación (Discord, WhatsApp, Email, etc.) debe:
    - Implementar enviar()
    - Implementar is_configured()
    """
    
    def __init__(self, nombre: str):
        """
        Inicializa el notificador.
        
        Args:
            nombre: Nombre del notificador (para logs)
        """
        self.nombre = nombre
        self.logger = setup_logger(f"Notifier.{nombre}")
    
    @abstractmethod
    def enviar(self, mensaje: str) -> bool:
        """
        Envía una notificación.
        
        Args:
            mensaje: Mensaje a enviar (formato markdown)
            
        Returns:
            True si se envió exitosamente, False en caso contrario
        """
        pass
    
    @abstractmethod
    def is_configured(self) -> bool:
        """
        Verifica si el notificador está correctamente configurado.
        
        Returns:
            True si está configurado, False en caso contrario
        """
        pass
    
    def enviar_resumen(self, eventos: List[Evento]) -> bool:
        """
        Envía un resumen de eventos.
        Formatea los eventos y los envía.
        
        Args:
            eventos: Lista de eventos a notificar
            
        Returns:
            True si se envió exitosamente
        """
        if not self.is_configured():
            self.logger.warning(f"{self.nombre} no está configurado correctamente")
            return False
        
        if not eventos:
            self.logger.info("No hay eventos para notificar")
            mensaje = self._formatear_sin_eventos()
        else:
            self.logger.info(f"Preparando notificación de {len(eventos)} eventos")
            mensaje = self._formatear_eventos(eventos)
        
        return self.enviar(mensaje)
    
    def _formatear_eventos(self, eventos: List[Evento]) -> str:
        """
        Formatea una lista de eventos en un mensaje legible.
        
        Args:
            eventos: Lista de eventos
            
        Returns:
            Mensaje formateado
        """
        from datetime import datetime
        from src.config.constants import EMOJIS_CATEGORIAS
        
        # Agrupar por categoría
        por_categoria = {}
        for evento in eventos:
            cat = evento.categoria
            if cat not in por_categoria:
                por_categoria[cat] = []
            por_categoria[cat].append(evento)
        
        # Construir mensaje
        lineas = ["📅 **EVENTOS DE LA PRÓXIMA SEMANA - UNViMe**\n"]
        
        for categoria, eventos_cat in sorted(por_categoria.items()):
            emoji = EMOJIS_CATEGORIAS.get(categoria, '📌')
            nombre_categoria = categoria.replace('_', ' ').upper()
            
            lineas.append(f"\n**{emoji} {nombre_categoria}**")
            
            for evento in sorted(eventos_cat, key=lambda e: e.fecha):
                lineas.append(f"  • {evento.fecha_legible()} - {evento.titulo}")
        
        lineas.append("\n---")
        lineas.append(f"_Actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}_")
        
        return "\n".join(lineas)
    
    def _formatear_sin_eventos(self) -> str:
        """
        Formatea el mensaje cuando no hay eventos.
        
        Returns:
            Mensaje formateado
        """
        from datetime import datetime
        
        return (
            "📭 **No hay eventos programados para la próxima semana**\n\n"
            f"_Actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}_"
        )
    
    def __str__(self) -> str:
        """Representación en string del notificador"""
        estado = "✅ Configurado" if self.is_configured() else "❌ No configurado"
        return f"{self.nombre} ({estado})"