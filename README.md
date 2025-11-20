# 🎓 Pregon - Sistema de Calendario Académico UNViMe

> Sistema inteligente de notificaciones y gestión del calendario académico de la Universidad Nacional de Villa Mercedes

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Discord](https://img.shields.io/badge/Discord-Bot-7289DA.svg)](https://discord.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🌟 Características

- 🤖 **Bot de Discord** conversacional con IA (Google Gemini)
- 📱 **Integración WhatsApp** vía Twilio con comandos interactivos
- 📅 **Google Calendar** - Agrega eventos automáticamente
- 🔍 **Scraping inteligente** - Extrae 173+ eventos del calendario académico
- 💬 **NLP Query Parser** - Entiende preguntas en lenguaje natural
- 🎯 **Filtrado inteligente** - Por fecha, categoría, tipo de evento
- 📬 **Notificaciones programadas** - Discord + WhatsApp

---

## 🚀 Inicio Rápido

### **Requisitos Previos**

- Python 3.10+
- Cuenta de Discord con bot token
- Cuenta de Twilio (para WhatsApp)
- Google Gemini API key
- Credenciales de Google Calendar API

### **Instalación**

```bash
# 1. Clonar repositorio
git clone https://github.com/MarkoTeixido/Prigon.git
cd Prigon

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt
pip install -r requirements-ai.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Edita .env con tus credenciales

# 5. Ejecutar bot de Discord
python run_discord_bot.py