# tests/integration/test_cache_scraper.py
"""
Tests de integración: Caché + Scraper
"""

import pytest
from src.scrapers.unvime_scraper import UNVimeScraper
from src.utils.cache import get_cache


@pytest.mark.integration
class TestCacheScraperIntegration:
    """Tests de integración Caché → Scraper"""
    
    def test_scraper_usa_cache(self):
        """
        Verificar que el scraper guarda en caché
        """
        # Limpiar caché primero
        cache = get_cache()
        cache.clear()
        
        # Primera descarga (debe hacer request)
        scraper = UNVimeScraper()
        html1 = scraper.descargar_contenido()
        
        # Verificar que guardó en caché
        cached = cache.get("calendario_html")
        assert cached is not None
        assert cached == html1
    
    def test_scraper_reutiliza_cache(self):
        """
        Verificar que el scraper reutiliza caché
        """
        scraper = UNVimeScraper()
        
        # Primera descarga
        html1 = scraper.descargar_contenido()
        
        # Segunda descarga (debe usar caché)
        html2 = scraper.descargar_contenido()
        
        # Deben ser iguales
        assert html1 == html2