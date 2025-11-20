# run_discord_bot.py
"""
🤖 Ejecutar Bot de Discord de Pregon
"""

from dotenv import load_dotenv
load_dotenv()

from src.integrations.discord_bot import run_discord_bot
from src.utils.logger import setup_logger

logger = setup_logger("Main")

if __name__ == "__main__":
    logger.info("="*70)
    logger.info("🤖 PREGON - BOT DE DISCORD")
    logger.info("="*70)
    
    run_discord_bot()