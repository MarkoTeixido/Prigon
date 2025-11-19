# src/scrapers/unvime_scraper.py
"""
🎓 Scraper específico para el calendario académico de UNViMe
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List
import re
from src.scrapers.base import BaseScraper
from src.models.evento import Evento
from src.config.settings import settings
from src.config.constants import (
    SCRAPING_TIMEOUT,
    USER_AGENT,
    MESES_ESPANOL,
    PALABRAS_CLAVE_CATEGORIAS,
    CategoriaEvento
)


class UNVimeScraper(BaseScraper):
    """
    Scraper para el calendario académico de la Universidad Nacional de Villa Mercedes.
    
    Extrae eventos de: https://www.unvime.edu.ar/calendario/
    
    Estructura HTML real:
    <div class="cal-grid">
      <div class="cal-month">
        <h3>Enero</h3>
        ...
      </div>
      <ul> <!-- Lista de eventos del mes -->
        <li>1 . Año nuevo</li>
        <li>1/1 al 2/2 . Receso</li>
      </ul>
    </div>
    """
    
    def __init__(self, url: str = None):
        """
        Inicializa el scraper de UNViMe.
        
        Args:
            url: URL del calendario (opcional, usa la de config por defecto)
        """
        super().__init__()
        self.url = url or settings.calendar_url
    
    def descargar_contenido(self) -> str:
        """
        Descarga el HTML de la página del calendario.
        
        Returns:
            Contenido HTML de la página
            
        Raises:
            requests.exceptions.RequestException: Si falla la descarga
        """
        self.logger.info(f"Descargando calendario desde: {self.url}")
        
        headers = {
            'User-Agent': USER_AGENT
        }
        
        response = requests.get(
            self.url,
            headers=headers,
            timeout=SCRAPING_TIMEOUT
        )
        response.raise_for_status()
        
        self.logger.info(f"Página descargada: {len(response.text)} caracteres")
        
        # Guardar para debug si estamos en desarrollo
        if settings.is_development():
            debug_file = 'debug_calendario.html'
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            self.logger.debug(f"HTML guardado en {debug_file}")
        
        return response.text
    
    def extraer_eventos(self, contenido: str) -> List[Evento]:
        """
        Extrae eventos del HTML del calendario.
        
        Estructura REAL:
        <div class="cal-month">
            <h3>Enero</h3>
            ...
            <div class="cal-event-list">
                <div class="cal-event-item categoria-X">
                    <span class="cal-event-date">1</span>
                    <span class="cal-event-title">. Año nuevo</span>
                </div>
            </div>
        </div>
        
        Args:
            contenido: HTML de la página
            
        Returns:
            Lista de objetos Evento
        """
        soup = BeautifulSoup(contenido, 'lxml')
        eventos = []
        año_actual = datetime.now().year
        
        # Buscar el contenedor principal
        cal_grid = soup.find('div', class_='cal-grid')
        if not cal_grid:
            self.logger.error("No se encontró div.cal-grid")
            return eventos
        
        # Buscar todos los meses
        meses_divs = cal_grid.find_all('div', class_='cal-month')
        self.logger.info(f"✅ Meses encontrados: {len(meses_divs)}")
        
        # Procesar cada mes
        for mes_div in meses_divs:
            # Extraer nombre del mes
            h3 = mes_div.find('h3')
            if not h3:
                continue
            
            mes_nombre = h3.get_text(strip=True).lower()
            mes_numero = MESES_ESPANOL.get(mes_nombre)
            
            if not mes_numero:
                self.logger.debug(f"Mes no reconocido: {mes_nombre}")
                continue
            
            self.logger.debug(f"📅 Procesando {mes_nombre.capitalize()} ({mes_numero})")
            
            # Buscar el div.cal-event-list DENTRO del mes
            event_list = mes_div.find('div', class_='cal-event-list')
            
            if not event_list:
                self.logger.debug(f"   No hay eventos en {mes_nombre}")
                continue
            
            # Buscar todos los cal-event-item
            items = event_list.find_all('div', class_='cal-event-item')
            self.logger.debug(f"   Eventos encontrados: {len(items)}")
            
            for item in items:
                try:
                    # Extraer fecha y título
                    fecha_span = item.find('span', class_='cal-event-date')
                    titulo_span = item.find('span', class_='cal-event-title')
                    
                    if not fecha_span or not titulo_span:
                        continue
                    
                    fecha_texto = fecha_span.get_text(strip=True)
                    titulo_texto = titulo_span.get_text(strip=True)
                    
                    # Limpiar título (quitar punto inicial)
                    if titulo_texto.startswith('.'):
                        titulo_texto = titulo_texto[1:].strip()
                    
                    # Parsear eventos (puede ser rango)
                    eventos_parseados = self._parsear_linea_evento(fecha_texto, titulo_texto, mes_numero, año_actual)
                    
                    for evento in eventos_parseados:
                        if evento:
                            eventos.append(evento)
                            self.logger.debug(f"   ✅ {evento}")
                            
                except Exception as e:
                    self.logger.warning(f"Error parseando evento: {e}")
                    continue
        
        self.logger.info(f"📋 Total eventos extraídos: {len(eventos)}")
        return eventos
    
    def _parsear_linea_evento(self, fecha_texto: str, titulo: str, mes_default: int, año: int) -> List[Evento]:
        """
        Parsea un evento que puede tener varios formatos de fecha:
        
        - "1" (solo día)
        - "1/1 al 2/2" (rango con mes)
        - "3/3 al 4/3" (rango)
        
        Args:
            fecha_texto: Texto de la fecha
            titulo: Descripción del evento
            mes_default: Mes por defecto
            año: Año del evento
            
        Returns:
            Lista de objetos Evento
        """
        eventos = []
        
        # Caso 1: Rango de fechas "1/1 al 2/2" o "3/3 al 4/3"
        if ' al ' in fecha_texto:
            # Tomar solo la fecha de inicio
            fecha_inicio = fecha_texto.split(' al ')[0].strip()
            
            try:
                fecha = self._parsear_fecha(fecha_inicio, mes_default, año)
                if fecha:
                    categoria = self._categorizar_por_titulo(titulo)
                    eventos.append(Evento(
                        fecha=fecha,
                        titulo=titulo,
                        categoria=categoria
                    ))
            except Exception as e:
                self.logger.warning(f"Error parseando rango '{fecha_texto}': {e}")
        
        # Caso 2: Fecha simple "1" o "17/2"
        else:
            try:
                fecha = self._parsear_fecha(fecha_texto, mes_default, año)
                if fecha:
                    categoria = self._categorizar_por_titulo(titulo)
                    eventos.append(Evento(
                        fecha=fecha,
                        titulo=titulo,
                        categoria=categoria
                    ))
            except Exception as e:
                self.logger.warning(f"Error parseando fecha '{fecha_texto}': {e}")
        
        return eventos
    
    def _parsear_fecha(self, fecha_texto: str, mes_default: int, año: int) -> datetime:
        """
        Parsea una fecha que puede estar en formato:
        - "1" (solo día)
        - "17/2" (día/mes)
        
        Args:
            fecha_texto: Texto de la fecha
            mes_default: Mes a usar si no está en el texto
            año: Año
            
        Returns:
            Objeto datetime o None si no se puede parsear
        """
        fecha_texto = fecha_texto.strip()
        
        # Caso 1: "17/2" (día/mes)
        if '/' in fecha_texto:
            partes = fecha_texto.split('/')
            if len(partes) == 2:
                dia = int(partes[0])
                mes = int(partes[1])
                return datetime(año, mes, dia)
        
        # Caso 2: "1" (solo día)
        elif fecha_texto.isdigit():
            dia = int(fecha_texto)
            return datetime(año, mes_default, dia)
        
        return None
    
    def _categorizar_por_titulo(self, titulo: str) -> str:
        """
        Categoriza un evento según palabras clave en el título.
        
        Args:
            titulo: Título del evento
            
        Returns:
            Categoría del evento
        """
        titulo_lower = titulo.lower()
        
        for categoria, palabras in PALABRAS_CLAVE_CATEGORIAS.items():
            if any(palabra in titulo_lower for palabra in palabras):
                return categoria
        
        return CategoriaEvento.OTRO