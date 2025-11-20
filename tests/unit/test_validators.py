# tests/unit/test_validators.py
"""
Tests para los validadores
"""

import pytest
from src.utils.validators import (
    validar_fecha,
    validar_email,
    validar_url,
    validar_categoria,
    validar_rango_fechas,
    sanitizar_texto
)


class TestValidadores:
    """Tests de funciones de validación"""
    
    def test_validar_fecha_correcta(self):
        """Debe validar fechas en formato correcto"""
        valida, fecha = validar_fecha("2025-12-15")
        assert valida is True
        assert fecha.year == 2025
        assert fecha.month == 12
        assert fecha.day == 15
    
    def test_validar_fecha_incorrecta(self):
        """Debe rechazar fechas inválidas"""
        valida, fecha = validar_fecha("2025-13-40")
        assert valida is False
        assert fecha is None
    
    def test_validar_email_correcto(self):
        """Debe validar emails correctos"""
        assert validar_email("test@example.com") is True
        assert validar_email("user.name@domain.co.uk") is True
    
    def test_validar_email_incorrecto(self):
        """Debe rechazar emails inválidos"""
        assert validar_email("invalido") is False
        assert validar_email("@example.com") is False
        assert validar_email("test@") is False
    
    def test_validar_url_correcta(self):
        """Debe validar URLs correctas"""
        assert validar_url("https://example.com") is True
        assert validar_url("http://test.com/path") is True
    
    def test_validar_url_incorrecta(self):
        """Debe rechazar URLs inválidas"""
        assert validar_url("not-a-url") is False
        assert validar_url("ftp://invalid") is False
    
    def test_validar_categoria_valida(self):
        """Debe validar categorías válidas"""
        assert validar_categoria("examen") is True
        assert validar_categoria("FERIADO") is True
        assert validar_categoria("Academico") is True
    
    def test_validar_categoria_invalida(self):
        """Debe rechazar categorías inválidas"""
        assert validar_categoria("invalida") is False
    
    def test_validar_rango_fechas_valido(self):
        """Debe validar rangos de fechas correctos"""
        assert validar_rango_fechas("2025-01-01", "2025-12-31") is True
    
    def test_validar_rango_fechas_invalido(self):
        """Debe rechazar rangos inválidos"""
        assert validar_rango_fechas("2025-12-31", "2025-01-01") is False
    
    def test_sanitizar_texto(self):
        """Debe limpiar texto correctamente"""
        texto = "  Hola   Mundo  <script>  "
        resultado = sanitizar_texto(texto)
        assert resultado == "Hola Mundo script"
        assert "<" not in resultado
        assert ">" not in resultado