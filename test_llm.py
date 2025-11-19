# test_llm.py
"""
🧪 Test del cliente LLM
"""

from dotenv import load_dotenv
load_dotenv()

from src.ai.llm_client import get_llm_client
from src.utils.logger import setup_logger

logger = setup_logger("TestLLM")

def main():
    logger.info("🧪 Probando cliente LLM...")
    
    try:
        # Crear cliente (usará el configurado en .env)
        llm = get_llm_client()
        
        logger.info(f"Cliente creado: {llm.__class__.__name__}")
        
        # Test básico
        pregunta = "¿Qué es UNViMe?"
        logger.info(f"Pregunta: {pregunta}")
        
        respuesta = llm.chat_sync(
            mensaje=pregunta,
            contexto="Eres un asistente de la Universidad Nacional de Villa Mercedes (UNViMe)."
        )
        
        logger.info(f"Respuesta:\n{respuesta}")
        
        print("\n" + "="*70)
        print(f"PREGUNTA: {pregunta}")
        print("="*70)
        print(respuesta)
        print("="*70)
        
        logger.info("✅ Test completado")
        
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)

if __name__ == "__main__":
    main()