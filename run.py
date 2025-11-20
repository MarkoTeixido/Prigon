# run.py
"""
🚀 Script principal de ejecución de Pregon
"""

import sys
from dotenv import load_dotenv

load_dotenv()

def mostrar_menu():
    print("="*70)
    print("🤖 PREGON - Sistema de Calendario Académico UNViMe")
    print("="*70)
    print()
    print("Selecciona qué ejecutar:")
    print()
    print("1. Bot de Discord (interactivo)")
    print("2. Webhook de WhatsApp (servidor)")
    print("3. Notificaciones programadas (scheduler)")
    print("4. Salir")
    print()
    print("="*70)

def main():
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción (1-4): ").strip()
        
        if opcion == "1":
            from src.integrations.discord_bot import run_discord_bot
            run_discord_bot()
            break
        
        elif opcion == "2":
            from src.integrations.whatsapp_webhook import run_webhook_server
            run_webhook_server(port=5000)
            break
        
        elif opcion == "3":
            print("⚠️ Scheduler no implementado aún")
            continue
        
        elif opcion == "4":
            print("👋 ¡Hasta luego!")
            sys.exit(0)
        
        else:
            print("❌ Opción inválida. Intenta de nuevo.\n")

if __name__ == "__main__":
    main()