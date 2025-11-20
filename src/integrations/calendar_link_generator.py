# src/integrations/calendar_link_generator.py
"""
🔗 Generador de links de Google Calendar
Crea URLs para agregar eventos sin necesidad de OAuth
"""

from typing import List
from urllib.parse import quote
from datetime import datetime
import requests
from src.models.evento import Evento
from src.utils.logger import setup_logger


class CalendarLinkGenerator:
    """
    Genera links de Google Calendar para agregar eventos.
    
    Usa el formato público de Google Calendar que no requiere autenticación:
    https://calendar.google.com/calendar/render?action=TEMPLATE&...
    """
    
    def __init__(self):
        self.logger = setup_logger("CalendarLinkGenerator")
        self.base_url = "https://calendar.google.com/calendar/render"
    
    def generar_link(self, evento: Evento, acortar: bool = True) -> str:
        """
        Genera un link para agregar un evento individual.
        
        Args:
            evento: Evento a agregar
            acortar: Si es True, intenta acortar la URL
            
        Returns:
            URL de Google Calendar
        """
        # Formatear fechas (formato: YYYYMMDDTHHMMSS)
        fecha_inicio = evento.fecha.strftime("%Y%m%dT090000")  # 9:00 AM
        fecha_fin = evento.fecha.strftime("%Y%m%dT100000")     # 10:00 AM
        
        # Construir descripción más corta
        descripcion = f"Calendario UNViMe - {evento.categoria}"
        
        # Construir URL
        params = {
            'action': 'TEMPLATE',
            'text': evento.titulo,
            'dates': f"{fecha_inicio}/{fecha_fin}",
            'details': descripcion,
            'location': 'UNViMe',
            'ctz': 'America/Argentina/Buenos_Aires'
        }
        
        # Generar query string
        query_parts = [f"{k}={quote(str(v))}" for k, v in params.items()]
        url = f"{self.base_url}?{'&'.join(query_parts)}"
        
        # Intentar acortar si es para WhatsApp
        if acortar:
            url_corta = self._acortar_url(url)
            if url_corta:
                return url_corta
        
        return url
    
    def _acortar_url(self, url: str) -> str:
        """
        Acorta una URL usando un servicio gratuito.
        
        Args:
            url: URL larga a acortar
            
        Returns:
            URL corta o la original si falla
        """
        try:
            # Usar TinyURL (gratuito, sin API key)
            response = requests.get(
                f"http://tinyurl.com/api-create.php?url={quote(url)}",
                timeout=5
            )
            
            if response.status_code == 200:
                url_corta = response.text.strip()
                self.logger.debug(f"URL acortada: {url_corta}")
                return url_corta
            
        except Exception as e:
            self.logger.warning(f"No se pudo acortar URL: {e}")
        
        return url
    
    def generar_links_multiples(self, eventos: List[Evento]) -> List[dict]:
        """
        Genera links para múltiples eventos.
        
        Args:
            eventos: Lista de eventos
            
        Returns:
            Lista de diccionarios con evento y su link
        """
        resultados = []
        
        for evento in eventos:
            link = self.generar_link(evento, acortar=True)
            resultados.append({
                'evento': evento,
                'titulo': evento.titulo,
                'fecha': evento.fecha_legible(),
                'link': link
            })
        
        return resultados
    
    def generar_mensaje_whatsapp_seleccionable(self, eventos: List[Evento]) -> str:
        """
        Genera un mensaje de WhatsApp con links para agregar eventos.
        
        Args:
            eventos: Lista de eventos
            
        Returns:
            Mensaje formateado para WhatsApp
        """
        links = self.generar_links_multiples(eventos)
        
        lineas = [
            "📅 *AGREGAR EVENTOS A TU CALENDARIO*",
            "",
            "👇 *Click en los links para agregar:*",
            ""
        ]
        
        for idx, item in enumerate(links, 1):
            fecha = item['evento'].fecha.strftime("%d/%m")
            emoji = self._get_emoji(item['evento'].categoria)
            
            # Acortar título si es muy largo
            titulo = item['titulo']
            if len(titulo) > 40:
                titulo = titulo[:37] + "..."
            
            lineas.append(f"{emoji} *{idx}. {fecha}* - {titulo}")
            lineas.append(f"   {item['link']}")
            lineas.append("")
        
        lineas.extend([
            "─────────────────────",
            "💡 *Instrucciones:*",
            "1. Click en el link del evento",
            "2. Se abrirá Google Calendar",
            "3. Click en *Guardar* para agregarlo",
            "",
            "✅ Agrega solo los que necesites"
        ])
        
        return "\n".join(lineas)
    
    def _get_emoji(self, categoria: str) -> str:
        """Retorna emoji según categoría"""
        emojis = {
            "academico": "🎓",
            "examen": "📝",
            "feriado": "🎉",
            "institucional": "🏛️",
            "receso": "🏖️",
            "otro": "📌"
        }
        return emojis.get(categoria.lower(), "📅")