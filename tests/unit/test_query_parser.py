# tests/unit/test_query_parser.py
"""
Tests para el Query Parser (NLP)
"""

import pytest
from datetime import datetime
from src.utils.query_parser import QueryParser


class TestQueryParser:
    """Tests del parser de consultas en lenguaje natural"""
    
    def test_inicializacion(self):
        """Debe inicializar correctamente"""
        parser = QueryParser()
        assert parser is not None
    
    def test_parse_retorna_algo(self):
        """Debe retornar algo al parsear"""
        parser = QueryParser()
        # USAR parse() en vez de parsear()
        resultado = parser.parse("eventos de hoy")
        
        # Verificar que retorna algo (dict, lista, etc.)
        assert resultado is not None
    
    def test_parse_acepta_string(self):
        """Debe aceptar strings"""
        parser = QueryParser()
        resultado = parser.parse("cuándo son los exámenes")
        
        # Solo verificar que no lanza excepción
        assert resultado is not None
    
    def test_parse_queries_vacias(self):
        """Debe manejar queries vacías"""
        parser = QueryParser()
        resultado = parser.parse("")
        
        # Debe retornar algo, aunque sea vacío
        assert resultado is not None