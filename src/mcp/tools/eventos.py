# src/mcp/tools/eventos.py
"""
📅 Herramientas MCP para gestión de eventos
"""

import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from src.services.calendario_service import CalendarioService
from src.scrapers.unvime_scraper import UNVimeScraper
from src.utils.logger import setup_logger
from src.utils.validators import validar_fecha, validar_rango_fechas


class EventosTools:
    """
    Herramientas MCP para consultar y filtrar eventos del calendario.
    """
    
    def __init__(self):
        self.logger = setup_logger("EventosTools")
        self.scraper = UNVimeScraper()
    
    def _obtener_todos_eventos(self) -> List:
        """
        Obtiene todos los eventos del calendario.
        
        Returns:
            Lista de eventos
        """
        try:
            # Método correcto: descargar_contenido()
            contenido_html = self.scraper.descargar_contenido()
            
            # Luego extraer eventos
            eventos = self.scraper.extraer_eventos(contenido_html)
            
            return eventos
            
        except Exception as e:
            self.logger.error(f"Error obteniendo eventos: {e}", exc_info=True)
            return []
    
    async def get_eventos_semana(self) -> Dict:
        """
        Obtiene eventos de la próxima semana.
        
        Returns:
            Diccionario con eventos y metadata
        """
        try:
            # Obtener todos los eventos
            todos_eventos = self._obtener_todos_eventos()
            
            # Filtrar próxima semana
            hoy = datetime.now()
            una_semana = hoy + timedelta(days=7)
            
            eventos_semana = [
                ev for ev in todos_eventos
                if hoy <= ev.fecha <= una_semana
            ]
            
            # Ordenar por fecha
            eventos_semana.sort(key=lambda x: x.fecha)
            
            resultado = {
                "total": len(eventos_semana),
                "desde": hoy.strftime("%Y-%m-%d"),
                "hasta": una_semana.strftime("%Y-%m-%d"),
                "eventos": [
                    {
                        "id": idx,
                        "titulo": ev.titulo,
                        "fecha": ev.fecha.strftime("%Y-%m-%d"),
                        "dia_semana": ev.fecha.strftime("%A"),
                        "categoria": ev.categoria
                    }
                    for idx, ev in enumerate(eventos_semana, 1)
                ]
            }
            
            self.logger.info(f"Obtenidos {len(eventos_semana)} eventos de la semana")
            return resultado
            
        except Exception as e:
            self.logger.error(f"Error obteniendo eventos: {e}", exc_info=True)
            return {"error": str(e)}
    
    async def buscar_eventos(
        self,
        query: Optional[str] = None,
        categoria: Optional[str] = None,
        desde: Optional[str] = None,
        hasta: Optional[str] = None
    ) -> Dict:
        """
        Busca eventos con filtros.
        
        Args:
            query: Texto a buscar
            categoria: Categoría de evento
            desde: Fecha desde (YYYY-MM-DD)
            hasta: Fecha hasta (YYYY-MM-DD)
            
        Returns:
            Diccionario con eventos encontrados
        """
        # ✅ INICIALIZAR VARIABLE ANTES DEL TRY
        eventos_filtrados = []
        
        try:
            # ✅ VALIDAR FECHAS SI SE PROPORCIONAN
            if desde:
                valida, _ = validar_fecha(desde)
                if not valida:
                    return {"error": f"Fecha 'desde' inválida: {desde}. Usa formato YYYY-MM-DD"}
            
            if hasta:
                valida, _ = validar_fecha(hasta)
                if not valida:
                    return {"error": f"Fecha 'hasta' inválida: {hasta}. Usa formato YYYY-MM-DD"}
            
            if desde and hasta:
                if not validar_rango_fechas(desde, hasta):
                    return {"error": "El rango de fechas es inválido (desde debe ser <= hasta)"}
            
            # Obtener todos los eventos
            todos_eventos = self._obtener_todos_eventos()
            
            # Aplicar filtros
            eventos_filtrados = todos_eventos
            
            if query:
                eventos_filtrados = [
                    ev for ev in eventos_filtrados
                    if query.lower() in ev.titulo.lower()
                ]
            
            if categoria:
                eventos_filtrados = [
                    ev for ev in eventos_filtrados
                    if ev.categoria.lower() == categoria.lower()
                ]
            
            if desde:
                fecha_desde = datetime.strptime(desde, "%Y-%m-%d")
                eventos_filtrados = [
                    ev for ev in eventos_filtrados
                    if ev.fecha >= fecha_desde
                ]
            
            if hasta:
                fecha_hasta = datetime.strptime(hasta, "%Y-%m-%d")
                eventos_filtrados = [
                    ev for ev in eventos_filtrados
                    if ev.fecha <= fecha_hasta
                ]
            
            # Ordenar por fecha
            eventos_filtrados.sort(key=lambda x: x.fecha)
            
            resultado = {
                "total": len(eventos_filtrados),
                "filtros_aplicados": {
                    "query": query,
                    "categoria": categoria,
                    "desde": desde,
                    "hasta": hasta
                },
                "eventos": [
                    {
                        "id": idx,
                        "titulo": ev.titulo,
                        "fecha": ev.fecha.strftime("%Y-%m-%d"),
                        "dia_semana": ev.fecha.strftime("%A"),
                        "categoria": ev.categoria
                    }
                    for idx, ev in enumerate(eventos_filtrados, 1)
                ]
            }
            
            self.logger.info(f"Búsqueda: {len(eventos_filtrados)} eventos encontrados")
            return resultado
            
        except Exception as e:
            self.logger.error(f"Error buscando eventos: {e}", exc_info=True)
            return {"error": str(e)}
    
    async def get_proximos_examenes(self, dias: int = 30) -> Dict:
        """
        Obtiene los próximos exámenes.
        
        Args:
            dias: Número de días a futuro
            
        Returns:
            Diccionario con exámenes próximos
        """
        try:
            hoy = datetime.now()
            fecha_limite = hoy + timedelta(days=dias)
            
            # Obtener todos los eventos
            todos_eventos = self._obtener_todos_eventos()
            
            # Filtrar exámenes
            examenes = [
                ev for ev in todos_eventos
                if ev.categoria.lower() == "examen"
                and hoy <= ev.fecha <= fecha_limite
            ]
            
            # Ordenar por fecha
            examenes.sort(key=lambda x: x.fecha)
            
            resultado = {
                "total": len(examenes),
                "dias_busqueda": dias,
                "desde": hoy.strftime("%Y-%m-%d"),
                "hasta": fecha_limite.strftime("%Y-%m-%d"),
                "examenes": [
                    {
                        "id": idx,
                        "titulo": ex.titulo,
                        "fecha": ex.fecha.strftime("%Y-%m-%d"),
                        "dia_semana": ex.fecha.strftime("%A"),
                        "dias_restantes": (ex.fecha - hoy).days
                    }
                    for idx, ex in enumerate(examenes, 1)
                ]
            }
            
            self.logger.info(f"Encontrados {len(examenes)} exámenes en {dias} días")
            return resultado
            
        except Exception as e:
            self.logger.error(f"Error obteniendo exámenes: {e}", exc_info=True)
            return {"error": str(e)}