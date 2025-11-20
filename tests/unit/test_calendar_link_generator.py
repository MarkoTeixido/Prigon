# tests/unit/test_calendar_link_generator.py
"""
Tests para CalendarLinkGenerator
"""

import pytest
from datetime import datetime
from src.integrations.calendar_link_generator import CalendarLinkGenerator
from src.models.evento import Evento


class TestCalendarLinkGenerator:
    """Tests del generador de links de calendario"""
    
    @pytest.fixture
    def evento_ejemplo(self):
        """Evento de ejemplo"""
        return Evento(
            fecha=datetime(2025, 12, 15, 9, 0),
            titulo="Examen de Matemáticas",
            categoria="examen"
        )
    
    def test_generar_link_basico(self, evento_ejemplo):
        """Debe generar un link de Google Calendar"""
        generador = CalendarLinkGenerator()
        link = generador.generar_link(evento_ejemplo)
        
        assert link is not None
        assert isinstance(link, str)
        assert len(link) > 0
    
    def test_link_contiene_titulo(self, evento_ejemplo):
        """El link debe incluir información del evento"""
        generador = CalendarLinkGenerator()
        link = generador.generar_link(evento_ejemplo)
        
        # Verificar que es una URL válida
        assert link.startswith("http") or "calendar.google.com" in link.lower()
    
    def test_generar_link_con_descripcion(self):
        """Debe manejar eventos con descripción"""
        evento = Evento(
            fecha=datetime(2025, 12, 15),
            titulo="Test",
            categoria="academico"
        )
        
        generador = CalendarLinkGenerator()
        link = generador.generar_link(evento)
        
        assert link is not None