<p align="center">
  <a href="https://github.com/MarkoTeixido/Prigon">
    <img src="https://i.imgur.com/8osiyMR.png" height="128"> 
  </a>
  <h2 align="center"><a href="https://github.com/MarkoTeixido/Prigon">Pregon</a></h2>
  <p align="center">Sistema inteligente de calendario académico para la Universidad Nacional de Villa Mercedes, potenciado por IA y MCP Server.<p>
  <p align="center">
    <a href="https://github.com/MarkoTeixido/Prigon">
    	<img src="https://img.shields.io/badge/%F0%9F%8E%93-Proyecto_Educativo-0a0a0a.svg?style=flat&colorA=0a0a0a" alt="proyecto" />
    </a>
    <a href="#-características">
    	<img src="https://img.shields.io/badge/%E2%9C%A8-Características-0a0a0a.svg?style=flat&colorA=0a0a0a" alt="características" />
    </a>
    <a href="#-tecnologías">
    	<img src="https://img.shields.io/badge/%F0%9F%9A%80-Stack-0a0a0a.svg?style=flat&colorA=0a0a0a" alt="stack" />
    </a>
    <a href="#-instalación">
    	<img src="https://img.shields.io/badge/%F0%9F%93%A6-Instalación-0a0a0a.svg?style=flat&colorA=0a0a0a" alt="instalación" />
    </a>
    <a href="LICENSE">
    	<img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="licencia" />
    </a>
  </p>
</p>

<br>

![](https://i.imgur.com/waxVImv.png)

## 📝 Sobre el Proyecto

**Pregon** es un sistema multicanal que automatiza la gestión del calendario académico de la UNViMe. Extrae, procesa y distribuye eventos académicos a través de Discord, WhatsApp y Google Calendar, potenciado por inteligencia artificial y una arquitectura MCP moderna.

### 🎯 Objetivo

Crear una plataforma que sea:
- **Inteligente**: IA conversacional con Google Gemini
- **Multicanal**: Discord, WhatsApp y Google Calendar
- **Moderna**: MCP Server (Model Context Protocol)
- **Automática**: Web scraping y notificaciones programadas
- **Profesional**: Código limpio, modular y bien documentado

### 🖼️ Preview

<p align="center">
   [agregar imagen - screenshot del bot en Discord]
</p>

<p align="center">
   [agregar imagen - screenshot del bot en WhatsApp]
</p>

![](https://i.imgur.com/waxVImv.png)

## ✨ Características

### 🤖 Inteligencia Artificial

- **Google Gemini 2.5 Flash**: Asistente conversacional inteligente
- **NLP Query Parser**: Entiende preguntas en lenguaje natural
- **Contexto Académico**: Comprende términos universitarios
- **Filtrado Inteligente**: Busca eventos por fecha, categoría y tipo
- **Respuestas Personalizadas**: Adapta el tono según el canal

### 🔌 MCP Server (Model Context Protocol)

- **Arquitectura Moderna**: Protocolo estándar para LLMs
- **6 Herramientas Disponibles**:
  - `get_eventos_semana`: Eventos de la próxima semana
  - `buscar_eventos`: Búsqueda con filtros avanzados
  - `get_proximos_examenes`: Exámenes próximos
  - `agregar_a_google_calendar`: Integración directa con Calendar
  - `generar_link_calendar`: Links públicos para agregar eventos
  - `enviar_recordatorio`: Notificaciones multicanal
- **Extensible**: Fácil agregar nuevas herramientas
- **Interoperable**: Compatible con cualquier LLM que soporte MCP

### 🤖 Bot de Discord

- **Comandos Interactivos**: `!eventos`, `!calendario`, `!ayuda`, etc.
- **Chat con IA**: `!pregunta <tu consulta>`
- **Embeds Profesionales**: Mensajes con formato rico
- **Reacciones Interactivas**: Navegación por menús
- **Modo Conversacional**: Mantiene contexto entre mensajes

### 📱 Bot de WhatsApp

- **Webhook Seguro**: Integración vía Twilio
- **Comandos Simples**: `EVENTOS`, `CALENDARIO`, `AYUDA`
- **IA Conversacional**: Responde preguntas naturales
- **Links Directos**: Agrega eventos a Google Calendar
- **Sandbox Compatible**: Testing sin costo

### 🔍 Web Scraping Inteligente

- **173+ Eventos Extraídos**: Calendario académico completo
- **BeautifulSoup + lxml**: Parsing robusto
- **Categorización Automática**: Exámenes, feriados, recesos, etc.
- **Rangos de Fechas**: Expande eventos multi-día
- **Caché Inteligente**: Evita scraping repetido (6 horas)
- **Validación de Datos**: Asegura integridad

### 📅 Google Calendar Integration

- **Creación Automática**: Agrega eventos directamente
- **Links Públicos**: URLs cortas con TinyURL
- **OAuth 2.0**: Autenticación segura
- **Zona Horaria**: Argentina/Buenos Aires
- **Batch Operations**: Múltiples eventos a la vez

### 🔔 Sistema de Notificaciones

- **Multicanal**: Discord + WhatsApp
- **Programables**: Scheduler automático
- **Personalizables**: Por tipo de evento
- **Recordatorios**: Antes de exámenes importantes
- **Manager Pattern**: Arquitectura extensible

![](https://i.imgur.com/waxVImv.png)

## 🏗️ Arquitectura

### 🔄 Diagrama General

<p align="center">
   [agregar imagen - diagrama de arquitectura]
</p>

```
┌─────────────────────────────────────────────────────────────┐
│                        USUARIOS                              │
│                                                               │
│   Discord    WhatsApp    Google Calendar    Otros LLMs      │
└────────┬──────────┬──────────────┬────────────────┬──────────┘
         │          │              │                │
         v          v              v                v
┌────────────────────────────────────────────────────────────┐
│                      PREGON SYSTEM                          │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Discord Bot  │  │WhatsApp Bot  │  │  MCP Server  │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │              │
│         └──────────────────┼──────────────────┘              │
│                            v                                 │
│                   ┌─────────────────┐                       │
│                   │  AI Chatbot     │                       │
│                   │  (Gemini 2.5)   │                       │
│                   └────────┬────────┘                       │
│                            │                                 │
│         ┌──────────────────┼──────────────────┐             │
│         v                  v                  v              │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐          │
│  │  Scraper   │   │  Calendar  │   │Notificaciones│        │
│  │  (UNViMe)  │   │  Service   │   │   Manager    │        │
│  └─────┬──────┘   └─────┬──────┘   └──────┬─────┘          │
│        │                 │                  │                │
│        v                 v                  v                │
│  ┌──────────────────────────────────────────────┐           │
│  │            Utils (Cache, Validators)         │           │
│  └──────────────────────────────────────────────┘           │
└──────────────────────────────────────────────────────────────┘
         │                 │                  │
         v                 v                  v
┌────────────────────────────────────────────────────────────┐
│                   SERVICIOS EXTERNOS                        │
│                                                              │
│   UNViMe Web    Google AI    Google Calendar    Twilio     │
└─────────────────────────────────────────────────────────────┘
```

### 📊 Flujo de una Consulta

```
Usuario en Discord
    │
    ├─> !pregunta "¿Cuándo son los exámenes de diciembre?"
    │
    v
Discord Bot
    │
    ├─> Sanitiza input
    ├─> Envía a Chatbot
    │
    v
AI Chatbot (Gemini)
    │
    ├─> Detecta intención: "buscar exámenes"
    ├─> Llama a MCP Server
    │
    v
MCP Server
    │
    ├─> Tool: get_proximos_examenes(dias=60)
    │
    v
EventosTools
    │
    ├─> Verifica caché
    ├─> Si no existe: scraping
    ├─> Filtra por categoría "examen"
    ├─> Filtra por rango de fechas
    │
    v
Scraper
    │
    ├─> Descarga HTML (si no está en caché)
    ├─> Extrae 173 eventos
    ├─> Guarda en caché (6h)
    │
    v
EventosTools
    │
    ├─> Retorna JSON estructurado
    │
    v
AI Chatbot
    │
    ├─> Procesa respuesta JSON
    ├─> Genera respuesta natural
    │
    v
Discord Bot
    │
    ├─> Formatea como Discord Embed
    ├─> Envía al usuario
    │
    v
Usuario ve:
    📝 Próximos Exámenes (Diciembre 2025)
    
    • 2/12 - Exámenes Generales
    • 9/12 - Exámenes Generales
    ...
```

![](https://i.imgur.com/waxVImv.png)

## 🚀 Tecnologías

### Backend/Core

| Tecnología | Versión | Uso |
|-----------|---------|-----|
| **Python** | 3.10+ | Lenguaje principal |
| **discord.py** | 2.3.2+ | SDK de Discord |
| **Flask** | 3.0.0+ | Webhook de WhatsApp |
| **Twilio** | 9.0.0+ | API de WhatsApp |
| **Google Generative AI** | 0.8.3+ | SDK de Gemini |
| **Google Calendar API** | 2.149.0+ | Integración con Calendar |
| **BeautifulSoup4** | 4.12.0+ | Web scraping |
| **lxml** | 5.3.0+ | Parser HTML rápido |
| **Requests** | 2.31.0+ | Cliente HTTP |
| **python-dotenv** | 1.0.0+ | Variables de entorno |

### MCP (Model Context Protocol)

| Componente | Estado | Descripción |
|-----------|--------|-------------|
| **MCP Server** | ✅ | Servidor con 6 herramientas |
| **EventosTools** | ✅ | Búsqueda y filtrado de eventos |
| **CalendarioTools** | ✅ | Integración con Google Calendar |
| **NotificacionesTools** | ✅ | Sistema de recordatorios |
| **Cache System** | ✅ | Optimización de consultas |
| **Validators** | ✅ | Validación de datos |

### Integraciones

| Servicio | API | Uso |
|----------|-----|-----|
| **UNViMe** | Web Scraping | Extracción de eventos |
| **Google Gemini** | AI API | Chatbot conversacional |
| **Google Calendar** | Calendar API v3 | Gestión de eventos |
| **Twilio** | WhatsApp API | Mensajería |
| **Discord** | Bot API | Chat interactivo |
| **TinyURL** | Shortening API | Acortar links |

### DevOps

| Herramienta | Uso |
|------------|-----|
| **Git/GitHub** | Control de versiones |
| **ngrok** | Túnel para desarrollo local |
| **Virtual Environment** | Aislamiento de dependencias |
| **Logging** | Sistema de logs estructurado |

![](https://i.imgur.com/waxVImv.png)

## 📦 Instalación

### Prerequisitos

- Python >= 3.10
- pip >= 23.x
- Cuenta de Discord con bot token
- Cuenta de Twilio (para WhatsApp)
- API Key de Google Gemini
- Credenciales de Google Calendar API

### Opción 1: Setup Rápido

```bash
# 1. Clonar repositorio
git clone https://github.com/MarkoTeixido/Prigon.git
cd Prigon

# 2. Crear entorno virtual
python -m venv venv

# Activar (Linux/macOS)
source venv/bin/activate

# Activar (Windows)
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt
pip install -r requirements-ai.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# 5. Ejecutar
python run.py
```

### Opción 2: Setup Detallado

<details>
<summary><b>Ver instrucciones paso a paso</b></summary>

#### 1. Clonar el Repositorio

```bash
git clone https://github.com/MarkoTeixido/Prigon.git
cd Prigon
```

#### 2. Crear Entorno Virtual

```bash
python -m venv venv
```

**Activar:**
- **Linux/macOS**: `source venv/bin/activate`
- **Windows**: `venv\Scripts\activate`

#### 3. Instalar Dependencias

```bash
# Core dependencies
pip install -r requirements.txt

# AI dependencies
pip install -r requirements-ai.txt

# Development tools (opcional)
pip install -r requirements-dev.txt
```

#### 4. Configurar Variables de Entorno

Crear archivo `.env`:

```env
# === DISCORD ===
DISCORD_BOT_TOKEN=tu_token_de_discord
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...

# === TWILIO (WhatsApp) ===
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=tu_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
TWILIO_WHATSAPP_TO=whatsapp:+54tu_numero

# === GOOGLE GEMINI ===
GEMINI_API_KEY=tu_api_key_de_gemini

# === GOOGLE CALENDAR ===
GOOGLE_CREDENTIALS_PATH=credentials/google_calendar.json
GOOGLE_TOKEN_PATH=credentials/token.json

# === CALENDARIO UNVIME ===
CALENDAR_URL=https://www.unvime.edu.ar/calendario/

# === CONFIGURACIÓN ===
ENVIRONMENT=development
LOG_LEVEL=INFO
```

#### 5. Obtener Credenciales

**Discord Bot:**
1. Ir a [Discord Developer Portal](https://discord.com/developers/applications)
2. Crear nueva aplicación
3. Ir a "Bot" → "Reset Token"
4. Copiar token
5. Habilitar "Message Content Intent"

**Twilio WhatsApp:**
1. Crear cuenta en [Twilio](https://www.twilio.com/try-twilio)
2. Ir a WhatsApp Sandbox
3. Copiar Account SID y Auth Token

**Google Gemini:**
1. Ir a [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Crear API Key
3. Copiar

**Google Calendar:**
1. Ir a [Google Cloud Console](https://console.cloud.google.com/)
2. Crear proyecto
3. Habilitar Google Calendar API
4. Crear credenciales OAuth 2.0
5. Descargar JSON a `credentials/google_calendar.json`

#### 6. Ejecutar

**Discord Bot:**
```bash
python run.py
# Seleccionar opción 1
```

**WhatsApp Webhook:**
```bash
# Terminal 1
python run.py
# Seleccionar opción 2

# Terminal 2
ngrok http 5000
# Copiar URL y configurar en Twilio
```

</details>

![](https://i.imgur.com/waxVImv.png)

## 🎮 Uso

### Discord Bot

Una vez el bot esté en tu servidor, usa estos comandos:

```
!pregunta <consulta>     - Pregunta al asistente IA
!eventos                 - Eventos de la próxima semana
!hoy                     - Eventos de hoy
!calendario              - Links para agregar eventos
!agregar menu            - Menú interactivo para agregar
!buscar <término>        - Buscar eventos específicos
!ayuda                   - Muestra todos los comandos
```

**Ejemplos:**
```
!pregunta ¿Cuándo son los exámenes de diciembre?
!buscar receso
!eventos
```

### WhatsApp Bot

Envía mensajes al número del sandbox:

```
EVENTOS      - Ver próximos eventos
CALENDARIO   - Links de Google Calendar
AYUDA        - Lista de comandos
<pregunta>   - Cualquier pregunta sobre el calendario
```

**Ejemplos:**
```
EVENTOS
¿Hay clases el 21 de noviembre?
¿Cuándo empiezan las clases en 2025?
```

### MCP Server (Programático)

```python
from src.mcp.server import get_mcp_server

# Obtener servidor
server = get_mcp_server()

# Listar herramientas
tools = server.list_tools()

# Ejecutar herramienta
response = await server.call_tool(
    "get_eventos_semana",
    {}
)

# Buscar eventos
response = await server.call_tool(
    "buscar_eventos",
    {
        "categoria": "examen",
        "desde": "2025-12-01",
        "hasta": "2025-12-31"
    }
)
```

![](https://i.imgur.com/waxVImv.png)

## 📊 Estructura del Proyecto

```
Prigon/
├── src/
│   ├── ai/                          # Chatbot con IA
│   │   ├── chatbot.py              # Integración con Gemini
│   │   └── prompts.py              # Prompts del sistema
│   │
│   ├── config/                      # Configuración
│   │   ├── constants.py            # Constantes del sistema
│   │   └── settings.py             # Settings con python-dotenv
│   │
│   ├── integrations/                # Integraciones externas
│   │   ├── discord_bot.py          # Bot de Discord
│   │   ├── whatsapp_webhook.py     # Webhook de WhatsApp
│   │   ├── google_calendar_service.py
│   │   └── calendar_link_generator.py
│   │
│   ├── mcp/                         # MCP Server ⭐
│   │   ├── server.py               # Servidor principal
│   │   └── tools/
│   │       ├── eventos.py          # Herramientas de eventos
│   │       ├── calendario.py       # Herramientas de calendar
│   │       └── notificaciones.py   # Herramientas de notificaciones
│   │
│   ├── models/                      # Modelos de datos
│   │   └── evento.py               # Modelo Evento (Pydantic)
│   │
│   ├── notifiers/                   # Sistema de notificaciones
│   │   ├── manager.py              # Manager pattern
│   │   ├── base.py                 # Clase base
│   │   ├── discord_notifier.py
│   │   └── whatsapp_notifier.py
│   │
│   ├── scrapers/                    # Web scraping
│   │   ├── base.py                 # Scraper base
│   │   └── unvime_scraper.py       # Scraper de UNViMe
│   │
│   ├── services/                    # Lógica de negocio
│   │   └── calendario_service.py   # Servicio principal
│   │
│   └── utils/                       # Utilidades
│       ├── cache.py                # Sistema de caché
│       ├── validators.py           # Validadores
│       ├── logger.py               # Logger estructurado
│       └── query_parser.py         # Parser NLP
│
├── credentials/                     # Credenciales (no en git)
│   ├── google_calendar.json
│   └── token.json
│
├── cache/                           # Caché de scraping
│   └── .gitkeep
│
├── logs/                            # Logs del sistema
│   └── .gitkeep
│
├── tests/                           # Tests (opcional)
│   └── test_mcp_server.py
│
├── .env                             # Variables de entorno (no en git)
├── .env.example                     # Template de .env
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt                 # Dependencias core
├── requirements-ai.txt              # Dependencias IA
├── requirements-dev.txt             # Dependencias desarrollo
└── run.py                           # Script principal
```

![](https://i.imgur.com/waxVImv.png)

## 🎓 Aprendizajes y Decisiones Técnicas

### ¿Por qué Python?

- Ecosistema rico para IA/ML
- Excelentes librerías de scraping
- APIs de bots bien soportadas
- Fácil prototipado rápido
- Gran comunidad

### ¿Por qué MCP Server?

- **Protocolo moderno** (2024-2025)
- **Interoperabilidad** con cualquier LLM
- **Arquitectura desacoplada** del chatbot
- **Reutilizable** en otros proyectos
- **Demuestra conocimiento** de tecnologías actuales

### ¿Por qué Gemini 2.5 Flash?

- Modelo de última generación
- API gratuita generosa
- Streaming nativo
- Excelente para español
- Bajo costo en producción

### ¿Por qué BeautifulSoup + lxml?

- Robusto para HTML mal formado
- Rápido (lxml parser)
- Fácil de debuggear
- No requiere JavaScript rendering
- Excelente documentación

### ¿Por qué Caché de 6 horas?

- El calendario académico **no cambia frecuentemente**
- Reduce carga en servidor de UNViMe
- Mejora velocidad de respuesta
- Ahorra ancho de banda
- 6h es balance perfecto entre freshness y performance

### ¿Por qué Multi-canal (Discord + WhatsApp)?

- **Alcance máximo**: Diferentes audiencias
- **Flexibilidad**: Usuarios eligen su plataforma
- **Aprendizaje**: Demostrar integración de múltiples APIs
- **Real-world**: Apps profesionales son multi-plataforma

![](https://i.imgur.com/waxVImv.png)

## 🚀 Roadmap Futuro

### Corto Plazo

- [ ] Tests automatizados (pytest)
- [ ] GitHub Actions (CI/CD)
- [ ] Docker containerización
- [ ] Deployment en Render/Railway

### Mediano Plazo

- [ ] Base de datos (SQLite) para usuarios
- [ ] Sistema de suscripciones
- [ ] Notificaciones programadas automáticas
- [ ] Panel web de administración
- [ ] API REST pública

### Largo Plazo

- [ ] Telegram bot
- [ ] App móvil nativa
- [ ] Multi-universidad (escalar a otras instituciones)
- [ ] Machine Learning para predecir fechas
- [ ] Real-time updates con WebSockets

![](https://i.imgur.com/waxVImv.png)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: AmazingFeature'`)
4. Push a la branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Coding Standards

- Seguir PEP 8
- Docstrings en español
- Type hints cuando sea posible
- Logs informativos
- Tests para nuevas features

![](https://i.imgur.com/waxVImv.png)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

![](https://i.imgur.com/waxVImv.png)

## 👨‍💻 Autor

**Marko Teixido**

- GitHub: [@MarkoTeixido](https://github.com/MarkoTeixido)
- Email: teixido.marko@gmail.com
- LinkedIn: [Marko Teixido](https://linkedin.com/in/markoteixido)
- Portfolio: [markoteixido.site](https://markoteixido.site)

---

<p align="center">
  Hecho con ❤️ para la comunidad de UNViMe
</p>

<p align="center">
  <sub>Si este proyecto te fue útil, dejá una ⭐ en GitHub</sub>
</p>