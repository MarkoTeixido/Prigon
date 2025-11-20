# tests/unit/test_scraper_base.py
"""
Tests para BaseScraper
"""

import pytest
from src.scrapers.base import BaseScraper
from src.scrapers.unvime_scraper import UNVimeScraper


class TestBaseScraper:
    """Tests del scraper base"""
    
    def test_scraper_concreto_hereda_de_base(self):
        """UNVimeScraper debe heredar de BaseScraper"""
        scraper = UNVimeScraper()
        assert isinstance(scraper, BaseScraper)
    
    def test_scraper_tiene_logger(self):
        """Debe tener logger"""
        scraper = UNVimeScraper()
        assert hasattr(scraper, 'logger')
        assert scraper.logger is not None
    
    def test_scraper_implementa_descargar(self):
        """Debe implementar descargar_contenido"""
        scraper = UNVimeScraper()
        assert hasattr(scraper, 'descargar_contenido')
        assert callable(scraper.descargar_contenido)
    
    def test_scraper_implementa_extraer(self):
        """Debe implementar extraer_eventos"""
        scraper = UNVimeScraper()
        assert hasattr(scraper, 'extraer_eventos')
        assert callable(scraper.extraer_eventos)
    
    def test_scraper_hereda_metodos_abstractos(self):
        """Debe implementar todos los métodos abstractos"""
        scraper = UNVimeScraper()
        
        # Verificar que tiene los métodos requeridos
        assert hasattr(scraper, 'descargar_contenido')
        assert hasattr(scraper, 'extraer_eventos')
    
    def test_scraper_puede_descargar(self):
        """Debe poder descargar contenido"""
        scraper = UNVimeScraper()
        contenido = scraper.descargar_contenido()
        
        assert contenido is not None
        assert isinstance(contenido, str)
        assert len(contenido) > 0
    
    def test_scraper_puede_extraer(self):
        """Debe poder extraer eventos"""
        scraper = UNVimeScraper()
        contenido = scraper.descargar_contenido()
        eventos = scraper.extraer_eventos(contenido)
        
        assert eventos is not None
        assert isinstance(eventos, list)