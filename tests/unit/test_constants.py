# tests/unit/test_constants.py
"""
Tests de constantes del sistema
"""

import pytest
from src.config.constants import (
    MESES_ESPANOL,
    PALABRAS_CLAVE_CATEGORIAS,
    CategoriaEvento,
    SCRAPING_TIMEOUT,
    USER_AGENT
)


class TestConstants:
    """Tests de constantes"""
    
    def test_meses_espanol_completo(self):
        """Debe tener los 12 meses"""
        assert len(MESES_ESPANOL) == 12
        assert "enero" in MESES_ESPANOL
        assert "diciembre" in MESES_ESPANOL
    
    def test_meses_numeros_correctos(self):
        """Debe mapear meses a números correctos"""
        assert MESES_ESPANOL["enero"] == 1
        assert MESES_ESPANOL["junio"] == 6
        assert MESES_ESPANOL["diciembre"] == 12
    
    def test_palabras_clave_categorias_existe(self):
        """Debe tener palabras clave para cada categoría"""
        assert "examen" in PALABRAS_CLAVE_CATEGORIAS
        assert "feriado" in PALABRAS_CLAVE_CATEGORIAS
        assert len(PALABRAS_CLAVE_CATEGORIAS) > 0
    
    def test_categoria_evento_enum(self):
        """Debe tener todas las categorías"""
        assert CategoriaEvento.EXAMEN is not None
        assert CategoriaEvento.ACADEMICO is not None
        assert CategoriaEvento.FERIADO is not None
    
    def test_scraping_timeout_valido(self):
        """Timeout debe ser positivo"""
        assert SCRAPING_TIMEOUT > 0
        assert isinstance(SCRAPING_TIMEOUT, int)
    
    def test_user_agent_definido(self):
        """User-Agent debe estar definido"""
        assert USER_AGENT is not None
        assert len(USER_AGENT) > 0
        assert isinstance(USER_AGENT, str)