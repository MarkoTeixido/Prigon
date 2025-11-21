#!/usr/bin/env python3
# entrypoints/discord_service.py
"""
🤖 Entry point para el servicio Discord Bot
Diseñado para ambientes de producción (Railway, Docker, etc.)
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from dotenv import load_dotenv
from src.utils.logger import setup_logger
from src.integrations.discord_bot import PregonDiscordBot
from src.config.settings import settings

# Cargar variables de entorno
load_dotenv()

logger = setup_logger("DiscordService")


def main():
    """
    Punto de entrada principal para el servicio Discord.
    
    Este servicio:
    - Valida configuración requerida
    - Inicia el bot de Discord
    - Maneja errores gracefully
    """
    logger.info("="*70)
    logger.info("🤖 PREGON - DISCORD BOT SERVICE")
    logger.info("="*70)
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Version: {settings.version}")
    logger.info("")
    
    # Validar token
    if not settings.discord_bot_token:
        logger.error("❌ ERROR: DISCORD_BOT_TOKEN no configurado")
        logger.error("💡 Configura la variable de entorno DISCORD_BOT_TOKEN")
        logger.error("🔗 Obtén tu token en: https://discord.com/developers/applications")
        sys.exit(1)
    
    try:
        logger.info("🚀 Iniciando bot de Discord...")
        logger.info("📡 Conectando a Discord Gateway...")
        
        bot = PregonDiscordBot()
        bot.run(settings.discord_bot_token)
        
    except KeyboardInterrupt:
        logger.info("⚠️ Bot detenido por usuario (Ctrl+C)")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"❌ Error crítico iniciando bot: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()