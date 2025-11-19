# src/config/settings.py
"""
⚙️ Configuración de Pregon
Manejo centralizado de variables de entorno y configuración
"""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, validator


class Settings(BaseSettings):
    """
    Configuración de la aplicación usando Pydantic.
    Lee automáticamente desde .env y variables de entorno.
    """
    
    # Configuración general
    app_name: str = Field(default="Pregon", description="Nombre de la aplicación")
    version: str = Field(default="2.0.0", description="Versión de la aplicación")
    environment: str = Field(default="production", description="Entorno (development/production)")
    
    # URLs
    calendar_url: str = Field(
        default="https://www.unvime.edu.ar/calendario/",
        description="URL del calendario académico"
    )
    
    # Discord Webhook (notificaciones automáticas)
    discord_webhook_url: Optional[str] = Field(
        default=None,
        description="URL del webhook de Discord para notificaciones"
    )
    
    # Discord Bot (conversacional)
    discord_bot_token: Optional[str] = Field(
        default=None,
        description="Token del bot de Discord para chat"
    )
    discord_guild_id: Optional[str] = Field(
        default=None,
        description="ID del servidor de Discord (opcional)"
    )
    
    # WhatsApp (Twilio)
    twilio_account_sid: Optional[str] = Field(default=None, description="Twilio Account SID")
    twilio_auth_token: Optional[str] = Field(default=None, description="Twilio Auth Token")
    twilio_whatsapp_from: Optional[str] = Field(
        default="whatsapp:+14155238886",
        description="Número de WhatsApp de Twilio (sandbox o propio)"
    )
    twilio_whatsapp_to: Optional[str] = Field(
        default=None,
        description="Número de WhatsApp destino (formato: whatsapp:+5491234567890)"
    )
    
    # IA / Gemini
    gemini_api_key: Optional[str] = Field(
        default=None,
        description="Google Gemini API Key (obtener en https://makersuite.google.com/app/apikey)"
    )
    
    # Configuración de Gemini
    llm_model_gemini: str = Field(
        default="gemini-2.0-flash-exp",
        description="Modelo de Gemini a usar"
    )
    llm_temperature: float = Field(
        default=0.3,
        description="Temperature del LLM (0-1, menor = más determinista)"
    )
    llm_max_tokens: int = Field(
        default=1000,
        description="Máximo de tokens en respuestas"
    )
    
    # Google Calendar
    google_credentials_path: str = Field(
        default="credentials/google_calendar.json",
        description="Ruta a credenciales de Google Calendar"
    )
    google_token_path: str = Field(
        default="credentials/token.json",
        description="Ruta al token de Google Calendar"
    )
    
    # Logging
    log_level: str = Field(default="INFO", description="Nivel de logging")
    log_to_file: bool = Field(default=True, description="Guardar logs en archivo")
    
    # Cache
    enable_cache: bool = Field(default=True, description="Habilitar sistema de caché")
    cache_ttl: int = Field(default=3600, description="Tiempo de vida del caché en segundos")
    
    # Configuración de Pydantic
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )
    
    @validator('discord_webhook_url')
    def validate_discord_webhook(cls, v):
        """Valida que el webhook de Discord sea válido si está configurado"""
        if v and not v.startswith('https://discord.com/api/webhooks/'):
            raise ValueError('Discord webhook URL inválida')
        return v
    
    @validator('log_level')
    def validate_log_level(cls, v):
        """Valida que el nivel de logging sea válido"""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'Log level debe ser uno de: {", ".join(valid_levels)}')
        return v.upper()
    
    def is_discord_webhook_enabled(self) -> bool:
        """Verifica si Discord webhook está configurado"""
        return self.discord_webhook_url is not None
    
    def is_discord_bot_enabled(self) -> bool:
        """Verifica si Discord bot está configurado"""
        return self.discord_bot_token is not None
    
    def is_whatsapp_enabled(self) -> bool:
        """Verifica si WhatsApp está configurado"""
        return all([
            self.twilio_account_sid,
            self.twilio_auth_token,
            self.twilio_whatsapp_to
        ])
    
    def is_ai_enabled(self) -> bool:
        """Verifica si Gemini está configurado"""
        return self.gemini_api_key is not None
    
    def is_google_calendar_enabled(self) -> bool:
        """Verifica si Google Calendar está configurado"""
        return Path(self.google_credentials_path).exists()
    
    def is_development(self) -> bool:
        """Verifica si está en modo desarrollo"""
        return self.environment.lower() == 'development'


# Instancia global de configuración
settings = Settings()


# Funciones helper para obtener rutas del proyecto
def get_project_root() -> Path:
    """Retorna la ruta raíz del proyecto"""
    return Path(__file__).parent.parent.parent


def get_logs_dir() -> Path:
    """Retorna la ruta del directorio de logs"""
    logs_dir = get_project_root() / 'logs'
    logs_dir.mkdir(exist_ok=True)
    return logs_dir


def get_cache_dir() -> Path:
    """Retorna la ruta del directorio de caché"""
    cache_dir = get_project_root() / '.cache'
    cache_dir.mkdir(exist_ok=True)
    return cache_dir


def get_credentials_dir() -> Path:
    """Retorna la ruta del directorio de credenciales"""
    cred_dir = get_project_root() / 'credentials'
    cred_dir.mkdir(exist_ok=True)
    return cred_dir