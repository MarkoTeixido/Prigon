# run_whatsapp_webhook.py
"""
🚀 Ejecutar servidor webhook de WhatsApp
"""

from dotenv import load_dotenv
load_dotenv()

from src.integrations.whatsapp_webhook import run_webhook_server
from src.utils.logger import setup_logger

logger = setup_logger("Main")

if __name__ == "__main__":
    logger.info("="*70)
    logger.info("📱 PREGON - WEBHOOK DE WHATSAPP")
    logger.info("="*70)
    logger.info("")
    logger.info("INSTRUCCIONES PARA DESARROLLO LOCAL:")
    logger.info("")
    logger.info("1. Mantén este servidor corriendo")
    logger.info("2. En otra terminal, ejecuta: ngrok http 5000")
    logger.info("3. Copia la URL de ngrok (https://xxxx.ngrok.io)")
    logger.info("4. Ve a Twilio Console → WhatsApp Sandbox")
    logger.info("5. Pega la URL: https://xxxx.ngrok.io/webhook")
    logger.info("")
    logger.info("="*70)
    
    run_webhook_server(port=5000)