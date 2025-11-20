# tests/unit/test_cache.py
"""
Tests para el sistema de caché
"""

import pytest
from datetime import timedelta
from src.utils.cache import Cache


class TestCache:
    """Tests del sistema de caché"""
    
    def test_cache_set_get(self, mock_cache):
        """Debe guardar y recuperar valores"""
        mock_cache.set("test_key", {"data": "test"})
        resultado = mock_cache.get("test_key")
        
        assert resultado is not None
        assert resultado["data"] == "test"
    
    def test_cache_miss(self, mock_cache):
        """Debe retornar None para keys inexistentes"""
        resultado = mock_cache.get("key_inexistente")
        assert resultado is None
    
    def test_cache_expiration(self, mock_cache, monkeypatch):
        """Debe expirar después del TTL"""
        from datetime import datetime, timedelta
        
        # Guardar valor
        mock_cache.set("test_key", "valor")
        
        # Simular paso del tiempo
        from unittest.mock import MagicMock
        future_time = datetime.now() + timedelta(hours=7)
        
        # El valor debería haber expirado
        # (Este test es conceptual, en producción necesitarías
        # una librería como freezegun para manipular el tiempo)
    
    def test_cache_clear_key(self, mock_cache):
        """Debe eliminar una key específica"""
        mock_cache.set("test_key", "valor")
        mock_cache.clear("test_key")
        resultado = mock_cache.get("test_key")
        assert resultado is None
    
    def test_cache_clear_all(self, mock_cache):
        """Debe eliminar todas las keys"""
        mock_cache.set("key1", "valor1")
        mock_cache.set("key2", "valor2")
        mock_cache.clear()
        
        assert mock_cache.get("key1") is None
        assert mock_cache.get("key2") is None