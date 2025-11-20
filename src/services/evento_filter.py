# src/services/evento_filter.py
"""
🔍 Filtro inteligente de eventos
Selecciona eventos relevantes según la consulta parseada
"""

from typing import List
from datetime import datetime, timedelta
from src.models.evento import Evento
from src.utils.query_parser import QueryParser
from src.utils.logger import setup_logger


class EventoFilter:
    """
    Filtro inteligente que selecciona eventos relevantes
    según el contexto de la consulta.
    """
    
    def __init__(self):
        self.logger = setup_logger("EventoFilter")
        self.parser = QueryParser()
    
    def filtrar(self, consulta: str, todos_eventos: List[Evento]) -> List[Evento]:
        """
        Filtra eventos relevantes según la consulta.
        
        Args:
            consulta: Pregunta del usuario
            todos_eventos: Lista completa de eventos
            
        Returns:
            Lista filtrada de eventos relevantes
        """
        # Parsear consulta
        info = self.parser.parse(consulta)
        
        # Si no detectamos ningún filtro específico, devolver todo
        if not any([info['mes'], info['tipo_evento'], info['temporal']]):
            self.logger.info("Sin filtros específicos detectados, usando todos los eventos")
            return todos_eventos[:100]  # Límite de seguridad
        
        eventos_filtrados = todos_eventos.copy()
        
        # Filtrar por mes si se mencionó
        if info['mes']:
            eventos_filtrados = self._filtrar_por_mes(eventos_filtrados, info['mes'], info['año'])
            self.logger.info(f"Filtrados por mes {info['mes']}: {len(eventos_filtrados)} eventos")
        
        # Filtrar por tipo de evento si se mencionó
        if info['tipo_evento']:
            eventos_filtrados = self._filtrar_por_tipo(eventos_filtrados, info['tipo_evento'])
            self.logger.info(f"Filtrados por tipo '{info['tipo_evento']}': {len(eventos_filtrados)} eventos")
        
        # Filtrar por temporal si se mencionó
        if info['temporal']:
            eventos_filtrados = self._filtrar_por_temporal(eventos_filtrados, info['temporal'])
            self.logger.info(f"Filtrados por temporal '{info['temporal']}': {len(eventos_filtrados)} eventos")
        
        # Si después de filtrar no quedan eventos, devolver más contexto
        if not eventos_filtrados:
            self.logger.warning("Sin eventos después de filtrar, ampliando contexto")
            return self._fallback_filter(todos_eventos, info)
        
        # Ordenar por fecha
        eventos_filtrados.sort(key=lambda e: e.fecha)
        
        self.logger.info(f"Total eventos filtrados: {len(eventos_filtrados)}")
        
        return eventos_filtrados[:50]  # Máximo 50 eventos
    
    def _filtrar_por_mes(self, eventos: List[Evento], mes: int, año: int = None) -> List[Evento]:
        """Filtra eventos por mes (y opcionalmente año)"""
        if año:
            return [e for e in eventos if e.fecha.month == mes and e.fecha.year == año]
        else:
            return [e for e in eventos if e.fecha.month == mes]
    
    def _filtrar_por_tipo(self, eventos: List[Evento], tipo: str) -> List[Evento]:
        """Filtra eventos por tipo/categoría"""
        return [e for e in eventos if tipo.lower() in e.categoria.lower()]
    
    def _filtrar_por_temporal(self, eventos: List[Evento], temporal: str) -> List[Evento]:
        """Filtra eventos según referencia temporal"""
        hoy = datetime.now()
        
        filtros = {
            "today": lambda e: e.fecha.date() == hoy.date(),
            "tomorrow": lambda e: e.fecha.date() == (hoy + timedelta(days=1)).date(),
            "this_week": lambda e: hoy <= e.fecha <= hoy + timedelta(days=7),
            "next_week": lambda e: hoy + timedelta(days=7) <= e.fecha <= hoy + timedelta(days=14),
            "this_month": lambda e: e.fecha.month == hoy.month and e.fecha.year == hoy.year,
            "next_month": lambda e: e.fecha.month == (hoy.month % 12) + 1,
            "this_year": lambda e: e.fecha.year == hoy.year
        }
        
        filtro_fn = filtros.get(temporal)
        if filtro_fn:
            return [e for e in eventos if filtro_fn(e)]
        
        return eventos
    
    def _fallback_filter(self, eventos: List[Evento], info: dict) -> List[Evento]:
        """
        Filtro de fallback cuando el filtro principal no encuentra nada.
        Amplía el contexto gradualmente.
        """
        # Si buscaban un tipo específico, dar todos de ese tipo
        if info['tipo_evento']:
            return self._filtrar_por_tipo(eventos, info['tipo_evento'])
        
        # Si buscaban un mes, dar el mes completo más el siguiente
        if info['mes']:
            mes_siguiente = (info['mes'] % 12) + 1
            return [
                e for e in eventos 
                if e.fecha.month in [info['mes'], mes_siguiente]
            ]
        
        # Fallback final: próximos 90 días
        hoy = datetime.now()
        fecha_limite = hoy + timedelta(days=90)
        return [e for e in eventos if hoy <= e.fecha <= fecha_limite]