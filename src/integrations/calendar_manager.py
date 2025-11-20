# src/integrations/calendar_manager.py
"""
📅 Gestor de eventos para Google Calendar
Permite a usuarios seleccionar qué eventos agregar
"""

from typing import List, Dict, Optional
from src.models.evento import Evento
from src.integrations.google_calendar_service import GoogleCalendarService
from src.integrations.calendar_link_generator import CalendarLinkGenerator
from src.utils.logger import setup_logger


class CalendarManager:
    """
    Gestor que permite a usuarios seleccionar y agregar eventos
    a su Google Calendar de forma individual o grupal.
    """
    
    def __init__(self):
        self.logger = setup_logger("CalendarManager")
        self.calendar_service = GoogleCalendarService()
        self.link_generator = CalendarLinkGenerator()
    
    def generar_opciones_seleccion(self, eventos: List[Evento]) -> Dict:
        """
        Genera opciones de selección para los eventos.
        
        Args:
            eventos: Lista de eventos disponibles
            
        Returns:
            Diccionario con eventos numerados y sus links
        """
        opciones = {
            'eventos': [],
            'links_individuales': {},
            'link_todos': None
        }
        
        for idx, evento in enumerate(eventos, 1):
            link = self.link_generator.generar_link(evento)
            
            opciones['eventos'].append({
                'numero': idx,
                'evento': evento,
                'titulo': evento.titulo,
                'fecha': evento.fecha_legible(),
                'categoria': evento.categoria,
                'link': link
            })
            
            opciones['links_individuales'][idx] = link
        
        # Generar link corto para "agregar todos" (usaremos el primero)
        # Nota: Google Calendar no permite agregar múltiples eventos en un solo link
        # Así que daremos instrucciones o links individuales
        
        return opciones
    
    def generar_mensaje_whatsapp_seleccionable(self, eventos: List[Evento]) -> str:
        """
        Genera mensaje de WhatsApp con opciones seleccionables.
        
        Args:
            eventos: Lista de eventos
            
        Returns:
            Mensaje formateado con links individuales
        """
        opciones = self.generar_opciones_seleccion(eventos)
        
        lineas = [
            "🎓 *CALENDARIO ACADÉMICO UNViMe*",
            "",
            "📅 *Próximos eventos:*",
            "",
            "👇 *Selecciona qué eventos agregar a tu calendario:*",
            ""
        ]
        
        # Agrupar por categoría
        eventos_por_cat = {}
        for opcion in opciones['eventos']:
            cat = opcion['categoria'].upper()
            if cat not in eventos_por_cat:
                eventos_por_cat[cat] = []
            eventos_por_cat[cat].append(opcion)
        
        emojis = {
            "ACADEMICO": "🎓",
            "EXAMEN": "📝",
            "FERIADO": "🎉",
            "INSTITUCIONAL": "🏛️",
            "RECESO": "🏖️",
            "OTRO": "📌"
        }
        
        # Agregar eventos con links
        for categoria, eventos_cat in eventos_por_cat.items():
            emoji = emojis.get(categoria, "📅")
            lineas.append(f"*{emoji} {categoria}*")
            
            for opcion in eventos_cat:
                fecha = opcion['evento'].fecha.strftime("%d/%m")
                lineas.append(f"• {fecha} - {opcion['titulo']}")
                lineas.append(f"  ➕ Agregar: {opcion['link'][:50]}...")
                lineas.append("")
        
        lineas.extend([
            "─────────────────────",
            "💡 *Cómo agregar eventos:*",
            "",
            "1️⃣ Haz click en el link del evento que quieras",
            "2️⃣ Se abrirá Google Calendar",
            "3️⃣ Click en 'Guardar'",
            "",
            "✅ Agrega solo los que necesites"
        ])
        
        return "\n".join(lineas)
    
    def generar_embed_discord_seleccionable(self, eventos: List[Evento]) -> Dict:
        """
        Genera estructura de embed de Discord con botones.
        
        Args:
            eventos: Lista de eventos
            
        Returns:
            Diccionario con estructura del embed
        """
        opciones = self.generar_opciones_seleccion(eventos)
        
        # Agrupar por categoría
        eventos_por_cat = {}
        for opcion in opciones['eventos']:
            cat = opcion['categoria'].upper()
            if cat not in eventos_por_cat:
                eventos_por_cat[cat] = []
            eventos_por_cat[cat].append(opcion)
        
        fields = []
        emojis = {
            "ACADEMICO": "🎓",
            "EXAMEN": "📝",
            "FERIADO": "🎉",
            "INSTITUCIONAL": "🏛️",
            "RECESO": "🏖️",
            "OTRO": "📌"
        }
        
        for categoria, eventos_cat in eventos_por_cat.items():
            emoji = emojis.get(categoria, "📅")
            
            # Crear texto con números
            texto_eventos = []
            for opcion in eventos_cat:
                fecha = opcion['evento'].fecha.strftime("%d/%m")
                numero = opcion['numero']
                texto_eventos.append(
                    f"{numero}️⃣ **{fecha}** - {opcion['titulo']}"
                )
            
            fields.append({
                'name': f"{emoji} {categoria}",
                'value': '\n'.join(texto_eventos),
                'inline': False
            })
        
        return {
            'title': '📅 Eventos de la Próxima Semana',
            'description': (
                '**Agrega eventos a tu Google Calendar:**\n\n'
                '• Reacciona con los números (1️⃣, 2️⃣, etc.)\n'
                '• O usa el comando: `!agregar <número>`\n'
                '• Para agregar todos: `!agregar todos`'
            ),
            'fields': fields,
            'color': 0x3498db,  # Azul
            'opciones': opciones
        }