# test_chatbot.py
"""
🧪 Test del chatbot conversacional
"""

from dotenv import load_dotenv
load_dotenv()

from src.ai.chatbot import CalendarioChatbot
from src.utils.logger import setup_logger

logger = setup_logger("TestChatbot")

def main():
    logger.info("🤖 Probando Chatbot del Calendario...")
    
    try:
        # Crear chatbot
        chatbot = CalendarioChatbot()
        
        logger.info("✅ Chatbot creado correctamente")
        
        # Obtener eventos de la semana
        logger.info("Obteniendo eventos de la próxima semana...")
        eventos = chatbot.obtener_eventos_semana()
        
        logger.info(f"Eventos obtenidos: {len(eventos)}")
        
        if not eventos:
            logger.warning("No se obtuvieron eventos")
            return
        
        # Test 1: Pregunta con eventos pre-cargados
        logger.info("\n" + "="*70)
        logger.info("TEST 1: ¿Qué eventos hay esta semana?")
        logger.info("="*70)
        
        respuesta1 = chatbot.responder_sync(
            "¿Qué eventos hay esta semana?",
            contexto_eventos=eventos
        )
        print(f"\n{respuesta1}\n")
        
        # Test 2: Pregunta sobre exámenes
        logger.info("\n" + "="*70)
        logger.info("TEST 2: ¿Cuándo son los próximos exámenes?")
        logger.info("="*70)
        
        respuesta2 = chatbot.responder_sync(
            "¿Cuándo son los próximos exámenes?",
            contexto_eventos=eventos
        )
        print(f"\n{respuesta2}\n")
        
        logger.info("="*70)
        logger.info("✅ Tests completados")
        logger.info("="*70)
        
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)

if __name__ == "__main__":
    main()