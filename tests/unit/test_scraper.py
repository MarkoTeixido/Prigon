# tests/unit/test_scraper.py
"""
Tests para el scraper de UNViMe
"""

import pytest
from datetime import datetime
from src.scrapers.unvime_scraper import UNVimeScraper


class TestUNVimeScraper:
    """Tests del scraper"""
    
    def test_extraer_eventos_desde_html(self, html_calendario_mock):
        """Debe extraer eventos del HTML"""
        scraper = UNVimeScraper()
        eventos = scraper.extraer_eventos(html_calendario_mock)
        
        assert len(eventos) > 0
        assert any(e.titulo == "Examen de Matemáticas" for e in eventos)
    
    def test_parsear_fecha_simple(self):
        """Debe parsear fecha simple (día solo)"""
        scraper = UNVimeScraper()
        fecha = scraper._parsear_fecha("15", 12, 2025)
        
        assert fecha.day == 15
        assert fecha.month == 12
        assert fecha.year == 2025
    
    def test_parsear_fecha_completa(self):
        """Debe parsear fecha con día/mes"""
        scraper = UNVimeScraper()
        fecha = scraper._parsear_fecha("15/12", 1, 2025)
        
        assert fecha.day == 15
        assert fecha.month == 12
        assert fecha.year == 2025
    
    def test_categorizar_por_titulo_examen(self):
        """Debe categorizar eventos de examen"""
        scraper = UNVimeScraper()
        categoria = scraper._categorizar_por_titulo("Examen de Matemáticas")
        assert categoria.lower() == "examen"
    
    def test_categorizar_por_titulo_feriado(self):
        """Debe categorizar feriados"""
        scraper = UNVimeScraper()
        categoria = scraper._categorizar_por_titulo("Día no laborable")
        assert categoria.lower() == "feriado"
    
    def test_parsear_rango_fechas(self):
        """Debe expandir rangos de fechas"""
        scraper = UNVimeScraper()
        eventos = scraper._parsear_linea_evento(
            "1/12 al 3/12",
            "Receso",
            12,
            2025
        )
        
        # Debe crear 3 eventos (1, 2 y 3 de diciembre)
        assert len(eventos) == 3
        assert eventos[0].fecha.day == 1
        assert eventos[1].fecha.day == 2
        assert eventos[2].fecha.day == 3