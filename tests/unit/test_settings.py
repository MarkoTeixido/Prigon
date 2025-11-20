# tests/unit/test_settings.py
"""
Tests de la configuración del sistema
"""

import pytest
from src.config.settings import Settings


class TestSettings:
    """Tests de configuración"""
    
    def test_settings_singleton(self):
        """Settings debe ser singleton"""
        from src.config.settings import settings
        
        settings1 = settings
        settings2 = settings
        
        assert settings1 is settings2
    
    def test_calendar_url_existe(self):
        """URL del calendario debe estar configurada"""
        from src.config.settings import settings
        
        assert settings.calendar_url is not None
        assert "unvime.edu.ar" in settings.calendar_url.lower()
    
    def test_is_development(self):
        """Debe detectar modo desarrollo"""
        from src.config.settings import settings
        
        resultado = settings.is_development()
        assert isinstance(resultado, bool)
    
    def test_environment_field(self):
        """Debe tener campo environment"""
        from src.config.settings import settings
        
        assert hasattr(settings, 'environment')
        assert isinstance(settings.environment, str)
    
    def test_app_name_existe(self):
        """Debe tener nombre de app"""
        from src.config.settings import settings
        
        assert hasattr(settings, 'app_name')
        assert settings.app_name is not None
    
    def test_version_existe(self):
        """Debe tener versión"""
        from src.config.settings import settings
        
        assert hasattr(settings, 'version')
        assert settings.version is not None
    
    def test_log_level_valido(self):
        """Log level debe ser válido"""
        from src.config.settings import settings
        
        assert settings.log_level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    
    def test_google_credentials_path(self):
        """Debe tener path de credenciales"""
        from src.config.settings import settings
        
        assert hasattr(settings, 'google_credentials_path')