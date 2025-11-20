# test_calendar_links.py
"""
🧪 Test del generador de links de Google Calendar
"""

from dotenv import load_dotenv
load_dotenv()

from datetime import datetime, timedelta
from src.integrations.calendar_link_generator import CalendarLinkGenerator
from src.models.evento import Evento
from src.utils.logger import setup_logger

logger = setup_logger("TestCalendarLinks")

def main():
    logger.info("="*70)
    logger.info("🧪 PROBANDO GENERADOR DE LINKS DE GOOGLE CALENDAR")
    logger.info("="*70)
    
    # Crear eventos de prueba
    eventos = [
        Evento(
            fecha=datetime.now() + timedelta(days=2),
            titulo="Examen de Matemáticas",
            categoria="examen"
        ),
        Evento(
            fecha=datetime.now() + timedelta(days=5),
            titulo="Inicio del Segundo Cuatrimestre",
            categoria="academico"
        ),
        Evento(
            fecha=datetime.now() + timedelta(days=7),
            titulo="Día del Estudiante",
            categoria="feriado"
        ),
    ]
    
    # Crear generador
    generator = CalendarLinkGenerator()
    
    # Generar links
    logger.info("\n📅 Links generados:")
    logger.info("="*70)
    
    for evento in eventos:
        link = generator.generar_link(evento)
        logger.info(f"\n{evento.titulo}")
        logger.info(f"📆 {evento.fecha_legible()}")
        logger.info(f"🔗 {link[:80]}...")
    
    # Generar mensaje para WhatsApp
    logger.info("\n" + "="*70)
    logger.info("📱 Mensaje para WhatsApp:")
    logger.info("="*70)
    
    mensaje = generator.generar_mensaje_whatsapp(eventos)
    print(f"\n{mensaje}\n")
    
    logger.info("="*70)
    logger.info("✅ Test completado")
    logger.info("="*70)
    logger.info("\n💡 Copia uno de los links y ábrelo en tu navegador")
    logger.info("   Debería abrir Google Calendar con el evento pre-cargado")

if __name__ == "__main__":
    main()