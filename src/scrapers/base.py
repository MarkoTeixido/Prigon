# src/scrapers/base.py
"""
🕷️ Clase base abstracta para scrapers
Implementa el patrón Template Method
"""

from abc import ABC, abstractmethod
from typing import List
from src.models.evento import Evento
from src.utils.logger import setup_logger


class BaseScraper(ABC):
    """
    Clase abstracta que define la interfaz para todos los scrapers.
    
    Los scrapers concretos deben implementar:
    - descargar_contenido()
    - extraer_eventos()
    """
    
    def __init__(self):
        """Inicializa el scraper"""
        self.logger = setup_logger(self.__class__.__name__)
    
    @abstractmethod
    def descargar_contenido(self) -> str:
        """
        Descarga el contenido a scrapear.
        
        Returns:
            Contenido descargado (HTML, JSON, etc.)
        """
        pass
    
    @abstractmethod
    def extraer_eventos(self, contenido: str) -> List[Evento]:
        """
        Extrae eventos del contenido descargado.
        
        Args:
            contenido: Contenido a parsear
            
        Returns:
            Lista de eventos extraídos
        """
        pass
    
    def obtener_eventos(self) -> List[Evento]:
        """
        Método principal (Template Method).
        Orquesta el proceso completo de scraping.
        
        Returns:
            Lista de eventos
        """
        self.logger.info("Iniciando scraping...")
        
        try:
            # Paso 1: Descargar
            contenido = self.descargar_contenido()
            
            # Paso 2: Extraer
            eventos = self.extraer_eventos(contenido)
            
            self.logger.info(f"Scraping completado: {len(eventos)} eventos extraídos")
            return eventos
            
        except Exception as e:
            self.logger.error(f"Error durante el scraping: {e}", exc_info=True)
            raise