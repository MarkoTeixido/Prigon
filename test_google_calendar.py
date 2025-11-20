# test_google_calendar.py
"""
🧪 Test de integración con Google Calendar
"""

from dotenv import load_dotenv
load_dotenv()

from datetime import datetime, timedelta
from src.integrations.google_calendar_service import GoogleCalendarService
from src.models.evento import Evento
from src.utils.logger import setup_logger

logger = setup_logger("TestGoogleCalendar")

def main():
    logger.info("="*70)
    logger.info("🧪 PROBANDO GOOGLE CALENDAR API")
    logger.info("="*70)
    
    # Crear servicio
    logger.info("\n1️⃣ Inicializando servicio de Google Calendar...")
    calendar_service = GoogleCalendarService()
    
    # Crear evento de prueba
    logger.info("\n2️⃣ Creando evento de prueba...")
    evento_prueba = Evento(
        fecha=datetime.now() + timedelta(days=3),
        titulo="[TEST] Examen de Matemáticas - Pregon",
        categoria="examen"
    )
    
    # Agregar evento
    logger.info("\n3️⃣ Agregando evento al calendario...")
    resultado = calendar_service.agregar_evento(evento_prueba)
    
    if resultado:
        logger.info(f"\n✅ Evento agregado exitosamente!")
        logger.info(f"   📅 {resultado['evento']}")
        logger.info(f"   🔗 Link: {resultado['link']}")
    else:
        logger.error("\n❌ No se pudo agregar el evento")
    
    # Listar próximos eventos
    logger.info("\n4️⃣ Listando próximos eventos en tu calendario...")
    proximos = calendar_service.listar_proximos_eventos(5)
    
    logger.info(f"\nPróximos {len(proximos)} eventos:")
    for evento in proximos:
        fecha = evento['start'].get('dateTime', evento['start'].get('date'))
        logger.info(f"   • {fecha[:10]}: {evento['summary']}")
    
    logger.info("\n" + "="*70)
    logger.info("✅ Test completado")
    logger.info("="*70)

if __name__ == "__main__":
    main()