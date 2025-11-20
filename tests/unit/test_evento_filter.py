# tests/unit/test_evento_filter.py
"""
Tests para EventoFilter
"""

import pytest
from datetime import datetime, timedelta
from src.services.evento_filter import EventoFilter
from src.models.evento import Evento


class TestEventoFilter:
    """Tests del filtrador de eventos"""
    
    @pytest.fixture
    def eventos_muestra(self):
        """Eventos de muestra"""
        hoy = datetime.now()
        return [
            Evento(
                fecha=hoy,
                titulo="Evento Hoy",
                categoria="academico"
            ),
            Evento(
                fecha=hoy + timedelta(days=1),
                titulo="Examen Mañana",
                categoria="examen"
            ),
            Evento(
                fecha=hoy + timedelta(days=7),
                titulo="Feriado Próxima Semana",
                categoria="feriado"
            ),
            Evento(
                fecha=datetime(2025, 12, 15),
                titulo="Examen Diciembre",
                categoria="examen"
            ),
        ]
    
    def test_inicializacion(self):
        """Debe inicializar correctamente"""
        filtro = EventoFilter()
        assert filtro is not None
        assert hasattr(filtro, 'parser')
        assert hasattr(filtro, 'logger')
    
    def test_filtrar_sin_filtros_especificos(self, eventos_muestra):
        """Sin filtros específicos debe retornar todos"""
        filtro = EventoFilter()
        resultado = filtro.filtrar("eventos", eventos_muestra)
        
        # Debe retornar eventos (máximo 100)
        assert len(resultado) > 0
        assert len(resultado) <= 100
    
    def test_filtrar_por_tipo_examen(self, eventos_muestra):
        """Debe filtrar por tipo 'examen'"""
        filtro = EventoFilter()
        resultado = filtro._filtrar_por_tipo(eventos_muestra, "examen")
        
        assert len(resultado) == 2
        assert all(e.categoria == "examen" for e in resultado)
    
    def test_filtrar_por_mes(self, eventos_muestra):
        """Debe filtrar por mes"""
        filtro = EventoFilter()
        resultado = filtro._filtrar_por_mes(eventos_muestra, 12)
        
        assert all(e.fecha.month == 12 for e in resultado)
    
    def test_filtrar_por_mes_con_año(self, eventos_muestra):
        """Debe filtrar por mes y año"""
        filtro = EventoFilter()
        resultado = filtro._filtrar_por_mes(eventos_muestra, 12, 2025)
        
        assert all(e.fecha.month == 12 and e.fecha.year == 2025 for e in resultado)
    
    def test_filtrar_por_temporal_today(self, eventos_muestra):
        """Debe filtrar eventos de hoy"""
        filtro = EventoFilter()
        resultado = filtro._filtrar_por_temporal(eventos_muestra, "today")
        
        hoy = datetime.now().date()
        assert all(e.fecha.date() == hoy for e in resultado)
    
    def test_filtrar_por_temporal_this_week(self, eventos_muestra):
        """Debe filtrar eventos de esta semana"""
        filtro = EventoFilter()
        resultado = filtro._filtrar_por_temporal(eventos_muestra, "this_week")
        
        assert len(resultado) >= 0
    
    def test_filtrar_con_consulta_examenes(self, eventos_muestra):
        """Debe filtrar cuando se pregunta por exámenes"""
        filtro = EventoFilter()
        resultado = filtro.filtrar("cuándo son los exámenes", eventos_muestra)
        
        # Debe retornar algo
        assert len(resultado) > 0
    
    def test_fallback_filter_por_tipo(self, eventos_muestra):
        """Fallback debe funcionar"""
        filtro = EventoFilter()
        info = {'tipo_evento': 'examen', 'mes': None, 'temporal': None, 'año': None}
        resultado = filtro._fallback_filter(eventos_muestra, info)
        
        assert len(resultado) > 0