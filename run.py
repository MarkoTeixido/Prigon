# run.py
"""
🚀 Script principal de ejecución de Pregon
Sistema de calendario académico UNViMe con IA

IMPORTANTE:
- Para desarrollo local: ejecutar este script
- Para producción (Railway): usar entry points en /entrypoints/
"""

import sys
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

from src.utils.logger import setup_logger

logger = setup_logger("Main")


def mostrar_banner():
    """Muestra el banner de bienvenida"""
    print("="*70)
    print("🤖 PREGON - Sistema de Calendario Académico UNViMe")
    print("="*70)
    print()


def mostrar_menu():
    """Muestra el menú principal"""
    print("Selecciona qué ejecutar:")
    print()
    print("1. Bot de Discord (interactivo con IA)")
    print("2. Webhook de WhatsApp (servidor)")
    print("3. MCP Server (Model Context Protocol)")
    print("4. Scheduler (notificaciones automáticas)")
    print("5. Salir")
    print()
    print("="*70)


def run_discord():
    """Ejecuta el bot de Discord"""
    logger.info("🚀 Iniciando bot de Discord...")
    
    try:
        from src.integrations.discord_bot import PregonDiscordBot
        from src.config.settings import settings
        
        if not settings.discord_bot_token:
            logger.error("❌ DISCORD_BOT_TOKEN no configurado")
            logger.error("💡 Configura la variable en .env")
            return
        
        bot = PregonDiscordBot()
        bot.run(settings.discord_bot_token)
        
    except KeyboardInterrupt:
        logger.info("⚠️ Bot detenido")
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)


def run_whatsapp():
    """Ejecuta el webhook de WhatsApp"""
    logger.info("📱 Iniciando webhook de WhatsApp...")
    
    try:
        from src.integrations.whatsapp_webhook import app
        from src.config.settings import settings
        
        if not settings.twilio_account_sid:
            logger.error("❌ Credenciales de Twilio no configuradas")
            logger.error("💡 Configura TWILIO_ACCOUNT_SID y TWILIO_AUTH_TOKEN en .env")
            return
        
        port = int(os.getenv('PORT', 5000))
        logger.info(f"🚀 Servidor iniciado en puerto {port}")
        logger.info("📡 Endpoint: /webhook")
        
        app.run(host='0.0.0.0', port=port, debug=False)
        
    except KeyboardInterrupt:
        logger.info("⚠️ Servidor detenido")
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)


async def run_mcp():
    """Ejecuta el servidor MCP"""
    from src.mcp.server import main as mcp_main
    
    logger.info("="*70)
    logger.info("🔌 PREGON - MCP SERVER")
    logger.info("="*70)
    logger.info("")
    logger.info("Servidor MCP iniciado. Esperando conexiones...")
    logger.info("")
    
    await mcp_main()


def run_scheduler():
    """Ejecuta el scheduler"""
    logger.info("⏰ Iniciando scheduler...")
    
    try:
        from src.services.calendario_service import CalendarioService
        import time
        from datetime import datetime
        
        service = CalendarioService()
        
        logger.info("📅 Ejecutando cada 24 horas")
        logger.info("⏸️ Presiona Ctrl+C para detener")
        
        while True:
            try:
                ahora = datetime.now()
                logger.info(f"⏰ Ejecutando: {ahora.strftime('%Y-%m-%d %H:%M:%S')}")
                
                service.ejecutar()
                
                logger.info("✅ Completado. Próxima ejecución en 24h")
                time.sleep(86400)
                
            except Exception as e:
                logger.error(f"❌ Error: {e}", exc_info=True)
                logger.info("⏳ Reintentando en 1 hora...")
                time.sleep(3600)
        
    except KeyboardInterrupt:
        logger.info("⚠️ Scheduler detenido")
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)


def main():
    """Punto de entrada principal"""
    mostrar_banner()
    
    # Detectar si estamos en entorno no-interactivo
    if not sys.stdin.isatty():
        logger.warning("⚠️ Entorno no-interactivo detectado")
        logger.warning("💡 Para producción, usa los entry points en /entrypoints/")
        logger.warning("   Ejemplo: python entrypoints/discord_service.py")
        sys.exit(1)
    
    while True:
        mostrar_menu()
        
        try:
            opcion = input("Selecciona una opción (1-5): ").strip()
        except EOFError:
            logger.error("❌ No se puede leer input (entorno no-interactivo)")
            logger.error("💡 Usa los entry points en /entrypoints/ para producción")
            sys.exit(1)
        
        if opcion == "1":
            run_discord()
            break
        
        elif opcion == "2":
            run_whatsapp()
            break
        
        elif opcion == "3":
            asyncio.run(run_mcp())
            break
        
        elif opcion == "4":
            run_scheduler()
            break
        
        elif opcion == "5":
            print("👋 ¡Hasta luego!")
            sys.exit(0)
        
        else:
            print("❌ Opción inválida. Intenta de nuevo.\n")


if __name__ == "__main__":
    main()