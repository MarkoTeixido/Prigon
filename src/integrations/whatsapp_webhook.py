# src/integrations/whatsapp_webhook.py
"""
🔌 Webhook para recibir mensajes de WhatsApp vía Twilio
Requiere Flask y ngrok para desarrollo local
"""

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from src.integrations.whatsapp_bot import WhatsAppBot
from src.utils.logger import setup_logger

app = Flask(__name__)
logger = setup_logger("WhatsAppWebhook")
bot = WhatsAppBot()


@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Endpoint que recibe mensajes de Twilio.
    
    Twilio envía POST a esta URL cuando llega un mensaje.
    """
    try:
        # Obtener datos del mensaje
        mensaje = request.form.get('Body', '')
        numero_remitente = request.form.get('From', '')
        
        logger.info(f"Mensaje recibido de {numero_remitente}: {mensaje}")
        
        # Procesar mensaje con el bot
        respuesta_texto = bot.procesar_mensaje(mensaje, numero_remitente)
        
        # Crear respuesta de Twilio
        resp = MessagingResponse()
        resp.message(respuesta_texto)
        
        logger.info(f"Respuesta enviada: {respuesta_texto[:50]}...")
        
        return str(resp)
        
    except Exception as e:
        logger.error(f"Error en webhook: {e}", exc_info=True)
        
        resp = MessagingResponse()
        resp.message("❌ Lo siento, hubo un error procesando tu mensaje.")
        return str(resp)


@app.route('/health', methods=['GET'])
def health():
    """Endpoint de salud para verificar que el servidor está corriendo"""
    return {'status': 'ok', 'service': 'Pregon WhatsApp Webhook'}


def run_webhook_server(port: int = 5000):
    """
    Inicia el servidor webhook.
    
    Args:
        port: Puerto donde escuchar (default: 5000)
    """
    logger.info(f"🚀 Iniciando webhook de WhatsApp en puerto {port}")
    logger.info("⚠️ IMPORTANTE: Necesitas exponer este servidor con ngrok")
    logger.info("   Ejecuta en otra terminal: ngrok http 5000")
    
    app.run(host='0.0.0.0', port=port, debug=False)