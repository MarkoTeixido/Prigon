# src/services/calendario_service.py
"""
🎯 Servicio principal que orquesta todo el flujo de Pregon
"""

from datetime import datetime, timedelta
from typing import List
from src.models.evento import Evento
from src.scrapers.unvime_scraper import UNVimeScraper
from src.notifiers.manager import NotificationManager
from src.config.constants import TIMEDELTA_SEMANA
from src.utils.logger import setup_logger


class CalendarioService:
    """
    Servicio principal que coordina:
    1. Scraping del calendario
    2. Filtrado de eventos próximos
    3. Envío de notificaciones
    """
    
    def __init__(self):
        """Inicializa el servicio"""
        self.logger = setup_logger("CalendarioService")
        self.scraper = UNVimeScraper()
        self.notification_manager = NotificationManager()
        self.notification_manager.registrar_todos()
    
    def ejecutar(self) -> dict:
        """
        Ejecuta el flujo completo de Pregon.
        
        Returns:
            Diccionario con resultados de la ejecución
        """
        self.logger.info("=" * 70)
        self.logger.info("🚀 Iniciando Pregon - Sistema de Notificaciones UNViMe")
        self.logger.info("=" * 70)
        
        try:
            # Paso 1: Scrapear calendario
            self.logger.info("\n📅 PASO 1: Obteniendo eventos del calendario...")
            todos_eventos = self.scraper.obtener_eventos()
            
            # Paso 2: Filtrar eventos próximos
            self.logger.info("\n🔍 PASO 2: Filtrando eventos de la próxima semana...")
            eventos_proximos = self.filtrar_proxima_semana(todos_eventos)
            
            self.logger.info(f"   Eventos totales: {len(todos_eventos)}")
            self.logger.info(f"   Eventos próximos: {len(eventos_proximos)}")
            
            # Paso 3: Enviar notificaciones
            self.logger.info("\n📬 PASO 3: Enviando notificaciones...")
            resultados_envio = self.notification_manager.enviar_a_todos(eventos_proximos)
            
            # Resultado final
            resultado = {
                "exito": True,
                "eventos_totales": len(todos_eventos),
                "eventos_proximos": len(eventos_proximos),
                "notificaciones": resultados_envio
            }
            
            self.logger.info("\n" + "=" * 70)
            self.logger.info("✅ Proceso completado exitosamente")
            self.logger.info(f"   📊 {resultados_envio['exitosos']}/{resultados_envio['total']} notificaciones enviadas")
            self.logger.info("=" * 70)
            
            return resultado
            
        except Exception as e:
            self.logger.error(f"\n❌ Error durante la ejecución: {e}", exc_info=True)
            return {
                "exito": False,
                "error": str(e)
            }
    
    def filtrar_proxima_semana(self, eventos: List[Evento]) -> List[Evento]:
        """
        Filtra eventos que ocurren en los próximos 7 días.
        
        Args:
            eventos: Lista de todos los eventos
            
        Returns:
            Lista filtrada de eventos próximos
        """
        hoy = datetime.now()
        fecha_limite = hoy + TIMEDELTA_SEMANA
        
        eventos_filtrados = [
            evento for evento in eventos
            if hoy <= evento.fecha <= fecha_limite
        ]
        
        # Ordenar por fecha
        eventos_filtrados.sort(key=lambda e: e.fecha)
        
        self.logger.debug(f"Rango de fechas: {hoy.date()} a {fecha_limite.date()}")
        
        return eventos_filtrados
    
    def obtener_eventos_mes(self, mes: int, año: int = None) -> List[Evento]:
        """
        Obtiene eventos de un mes específico.
        
        Args:
            mes: Número de mes (1-12)
            año: Año (default: año actual)
            
        Returns:
            Lista de eventos del mes
        """
        año = año or datetime.now().year
        
        todos_eventos = self.scraper.obtener_eventos()
        
        eventos_mes = [
            evento for evento in todos_eventos
            if evento.mes == mes and evento.año == año
        ]
        
        eventos_mes.sort(key=lambda e: e.fecha)
        
        return eventos_mes