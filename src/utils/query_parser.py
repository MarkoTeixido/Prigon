# src/utils/query_parser.py
"""
🧠 Parser inteligente de consultas de usuario
Extrae intención, fechas y tipos de eventos de preguntas en lenguaje natural
"""

import re
from typing import Optional, List, Dict
from datetime import datetime
from src.utils.logger import setup_logger


class QueryParser:
    """
    Parser de consultas que extrae:
    - Mes mencionado
    - Año mencionado
    - Tipo de evento (examen, feriado, etc.)
    - Intención temporal (hoy, esta semana, próximo mes)
    """
    
    def __init__(self):
        self.logger = setup_logger("QueryParser")
        
        # Mapeo de meses en español
        self.meses = {
            "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
            "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
            "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
        }
        
        # Mapeo de tipos de eventos
        self.tipos_evento = {
            "examen": ["examen", "exámenes", "final", "finales", "evaluacion", "evaluación"],
            "feriado": ["feriado", "feriados", "día libre", "no laborable"],
            "academico": ["clase", "clases", "cuatrimestre", "inicio", "fin"],
            "receso": ["vacaciones", "receso", "descanso"],
            "institucional": ["fundación", "aniversario", "institucional"],
        }
        
        # Palabras temporales
        self.palabras_temporales = {
            "hoy": "today",
            "mañana": "tomorrow",
            "esta semana": "this_week",
            "próxima semana": "next_week",
            "este mes": "this_month",
            "próximo mes": "next_month",
            "este año": "this_year"
        }
    
    def parse(self, consulta: str) -> Dict:
        """
        Parsea una consulta y extrae información relevante.
        
        Args:
            consulta: Pregunta del usuario
            
        Returns:
            Diccionario con información extraída:
            {
                'mes': int | None,
                'año': int | None,
                'tipo_evento': str | None,
                'temporal': str | None,
                'keywords': List[str]
            }
        """
        consulta_lower = consulta.lower()
        
        resultado = {
            'mes': self._detectar_mes(consulta_lower),
            'año': self._detectar_año(consulta_lower),
            'tipo_evento': self._detectar_tipo_evento(consulta_lower),
            'temporal': self._detectar_temporal(consulta_lower),
            'keywords': self._extraer_keywords(consulta_lower),
            'query_original': consulta
        }
        
        self.logger.debug(f"Query parseada: {resultado}")
        
        return resultado
    
    def _detectar_mes(self, texto: str) -> Optional[int]:
        """Detecta si se menciona un mes en el texto"""
        for nombre, numero in self.meses.items():
            if nombre in texto:
                self.logger.debug(f"Mes detectado: {nombre} ({numero})")
                return numero
        return None
    
    def _detectar_año(self, texto: str) -> Optional[int]:
        """Detecta si se menciona un año (2024, 2025, etc.)"""
        match = re.search(r'\b(202[0-9])\b', texto)
        if match:
            año = int(match.group(1))
            self.logger.debug(f"Año detectado: {año}")
            return año
        return None
    
    def _detectar_tipo_evento(self, texto: str) -> Optional[str]:
        """Detecta el tipo de evento mencionado"""
        for tipo, keywords in self.tipos_evento.items():
            for keyword in keywords:
                if keyword in texto:
                    self.logger.debug(f"Tipo de evento detectado: {tipo}")
                    return tipo
        return None
    
    def _detectar_temporal(self, texto: str) -> Optional[str]:
        """Detecta referencias temporales (hoy, esta semana, etc.)"""
        for frase, codigo in self.palabras_temporales.items():
            if frase in texto:
                self.logger.debug(f"Temporal detectado: {frase} ({codigo})")
                return codigo
        return None
    
    def _extraer_keywords(self, texto: str) -> List[str]:
        """Extrae palabras clave importantes"""
        # Palabras a ignorar (stop words)
        stop_words = {
            'el', 'la', 'los', 'las', 'un', 'una', 'de', 'del', 'en', 
            'a', 'para', 'por', 'con', 'sin', 'sobre', 'es', 'son',
            'que', 'qué', 'cuándo', 'cuando', 'dónde', 'donde', 'cómo',
            'hay', 'me', 'te', 'se', 'lo', 'cual', 'cuales'
        }
        
        # Tokenizar y limpiar
        palabras = re.findall(r'\b\w+\b', texto)
        keywords = [
            p for p in palabras 
            if len(p) > 3 and p not in stop_words
        ]
        
        return keywords[:10]  # Máximo 10 keywords