#!/usr/bin/env python3
# entrypoints/scheduler_service.py
"""
⏰ Entry point para el servicio Scheduler
Ejecuta notificaciones programadas automáticamente
"""

import sys
import os
import time
from pathlib import Path
from datetime import datetime

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from dotenv import load_dotenv
from src.utils.logger import setup_logger
from src.services.calendario_service import CalendarioService
from src.config.settings import settings

# Cargar variables de entorno
load_dotenv()

logger = setup_logger("SchedulerService")


def main():
    """
    Punto de entrada principal para el servicio Scheduler.
    
    Este servicio:
    - Ejecuta tareas programadas
    - Envía notificaciones automáticas
    - Mantiene el scraping actualizado
    """
    logger.info("="*70)
    logger.info("⏰ PREGON - SCHEDULER SERVICE")
    logger.info("="*70)
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Version: {settings.version}")
    logger.info("")
    
    try:
        service = CalendarioService()
        
        logger.info("🚀 Scheduler iniciado")
        logger.info("📅 Ejecutando cada 24 horas")
        logger.info("⏸️ Presiona Ctrl+C para detener")
        logger.info("")
        
        while True:
            try:
                ahora = datetime.now()
                logger.info(f"⏰ Ejecutando tarea programada: {ahora.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Ejecutar servicio
                service.ejecutar()
                
                logger.info("✅ Tarea completada exitosamente")
                logger.info("⏳ Próxima ejecución en 24 horas")
                logger.info("")
                
                # Dormir 24 horas (86400 segundos)
                time.sleep(86400)
                
            except Exception as e:
                logger.error(f"❌ Error en tarea programada: {e}", exc_info=True)
                logger.info("⏳ Reintentando en 1 hora...")
                time.sleep(3600)  # Reintentar en 1 hora si falla
        
    except KeyboardInterrupt:
        logger.info("⚠️ Scheduler detenido por usuario (Ctrl+C)")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"❌ Error crítico en scheduler: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()