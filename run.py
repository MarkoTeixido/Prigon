# run.py
"""
🎓 Pregon - Sistema de Notificaciones UNViMe
Script principal de ejecución
"""

import sys
from src.services.calendario_service import CalendarioService
from src.utils.logger import setup_logger
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Logger principal
logger = setup_logger("Main")


def main():
    """Función principal"""
    try:
        # Crear e inicializar el servicio
        servicio = CalendarioService()
        
        # Ejecutar
        resultado = servicio.ejecutar()
        
        # Verificar resultado
        if resultado["exito"]:
            logger.info("\n🎉 ¡Ejecución exitosa!")
            
            # Mostrar resumen
            logger.info("\n📊 RESUMEN:")
            logger.info(f"   • Eventos totales extraídos: {resultado['eventos_totales']}")
            logger.info(f"   • Eventos de la próxima semana: {resultado['eventos_proximos']}")
            
            notif = resultado['notificaciones']
            logger.info(f"   • Notificaciones enviadas: {notif['exitosos']}/{notif['total']}")
            
            for canal, estado in notif['detalles'].items():
                logger.info(f"     {estado} {canal}")
            
            return 0
        else:
            logger.error(f"\n💥 Ejecución fallida: {resultado.get('error', 'Error desconocido')}")
            return 1
            
    except KeyboardInterrupt:
        logger.warning("\n⚠️ Ejecución cancelada por el usuario")
        return 130
        
    except Exception as e:
        logger.error(f"\n💥 Error crítico: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())