# src/config/constants.py
"""
🔧 Constantes del proyecto Pregon
Define valores que NO cambian durante la ejecución
"""

from datetime import timedelta

# URLs
UNVIME_CALENDAR_URL = "https://www.unvime.edu.ar/calendario/"
UNVIME_LOGO_URL = "https://www.unvime.edu.ar/wp-content/uploads/2019/06/Logo-UNViMe-2019-Negro-Oscuro-600x600.png"

# Configuración de scraping
SCRAPING_TIMEOUT = 10  # segundos
USER_AGENT = "Pregon-Bot/1.0 (UNViMe Calendar Bot; +https://github.com/markgoddar/Pregon)"

# Configuración de eventos
DIAS_ANTICIPACION = 7  # Cuántos días adelante buscar eventos
TIMEDELTA_SEMANA = timedelta(days=DIAS_ANTICIPACION)

# Meses en español
MESES_ESPANOL = {
    'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
    'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
    'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
}

# Días de la semana en español
DIAS_SEMANA_ESPANOL = {
    'Monday': 'Lunes',
    'Tuesday': 'Martes',
    'Wednesday': 'Miércoles',
    'Thursday': 'Jueves',
    'Friday': 'Viernes',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}

# Categorías de eventos
class CategoriaEvento:
    """Categorías posibles para eventos"""
    ACADEMICO = 'academico'
    EXAMEN = 'examen'
    FERIADO = 'feriado'
    ADMINISTRATIVO = 'administrativo'
    RECESO = 'receso'
    INSTITUCIONAL = 'institucional'
    OTRO = 'evento'

# Emojis por categoría
EMOJIS_CATEGORIAS = {
    CategoriaEvento.ACADEMICO: '🎓',
    CategoriaEvento.EXAMEN: '📝',
    CategoriaEvento.FERIADO: '🎉',
    CategoriaEvento.ADMINISTRATIVO: '📋',
    CategoriaEvento.RECESO: '🏖️',
    CategoriaEvento.INSTITUCIONAL: '🏛️',
    CategoriaEvento.OTRO: '📌'
}

# Palabras clave para categorización
PALABRAS_CLAVE_CATEGORIAS = {
    CategoriaEvento.EXAMEN: ['examen', 'final', 'mesa', 'evaluación', 'exámenes'],
    CategoriaEvento.FERIADO: ['feriado', 'asueto', 'no laborable', 'día nacional', 'soberanía'],
    CategoriaEvento.ACADEMICO: ['inicio', 'comienzo', 'fin', 'cuatrimestre', 'clases'],
    CategoriaEvento.RECESO: ['receso', 'vacaciones'],
    CategoriaEvento.ADMINISTRATIVO: ['inscripción', 'inscripciones', 'preinscripción'],
    CategoriaEvento.INSTITUCIONAL: ['aniversario', 'fundación', 'día de', 'día del', 'navidad', 'inmaculada', 'claustro']
}

# Selectores CSS para scraping
CSS_SELECTORS = {
    'month_container': 'div.cal-month',
    'month_title': ['h2', 'h3', 'h4'],
    'event_item': 'div.cal-event-item',
    'event_date': 'span.cal-event-date',
    'event_title': 'span.cal-event-title'
}

# Configuración de Discord
DISCORD_EMBED_COLOR = 3447003  # Azul
DISCORD_MAX_DESCRIPTION_LENGTH = 2048
DISCORD_MAX_FIELD_VALUE_LENGTH = 1024

# Configuración de logging
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LOG_FILE = 'logs/pregon.log'
LOG_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5

# Cache
CACHE_DIR = '.cache'
CACHE_TTL_SECONDS = 3600  # 1 hora