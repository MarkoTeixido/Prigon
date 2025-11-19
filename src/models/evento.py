# src/models/event.py
"""
📋 Modelo de datos para eventos del calendario académico
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from src.config.constants import CategoriaEvento, DIAS_SEMANA_ESPANOL


class Evento(BaseModel):
    """
    Representa un evento del calendario académico.
    
    Attributes:
        fecha: Fecha del evento
        titulo: Descripción del evento
        categoria: Categoría del evento (académico, feriado, etc.)
        mes: Mes del evento (1-12)
        dia: Día del evento (1-31)
    """
    
    fecha: datetime = Field(..., description="Fecha del evento")
    titulo: str = Field(..., min_length=1, description="Título o descripción del evento")
    categoria: str = Field(
        default=CategoriaEvento.OTRO,
        description="Categoría del evento"
    )
    
    @validator('titulo')
    def titulo_no_vacio(cls, v):
        """Valida que el título no esté vacío después de strip"""
        if not v.strip():
            raise ValueError('El título no puede estar vacío')
        return v.strip()
    
    @validator('categoria')
    def categoria_valida(cls, v):
        """Valida que la categoría sea válida"""
        categorias_validas = [
            CategoriaEvento.ACADEMICO,
            CategoriaEvento.EXAMEN,
            CategoriaEvento.FERIADO,
            CategoriaEvento.ADMINISTRATIVO,
            CategoriaEvento.RECESO,
            CategoriaEvento.INSTITUCIONAL,
            CategoriaEvento.OTRO
        ]
        if v not in categorias_validas:
            raise ValueError(f'Categoría inválida: {v}')
        return v
    
    @property
    def dia(self) -> int:
        """Retorna el día del mes"""
        return self.fecha.day
    
    @property
    def mes(self) -> int:
        """Retorna el mes"""
        return self.fecha.month
    
    @property
    def año(self) -> int:
        """Retorna el año"""
        return self.fecha.year
    
    @property
    def dia_semana(self) -> str:
        """Retorna el día de la semana en español"""
        dia_ingles = self.fecha.strftime("%A")
        return DIAS_SEMANA_ESPANOL.get(dia_ingles, dia_ingles)
    
    def fecha_formateada(self, formato: str = "%d/%m/%Y") -> str:
        """
        Retorna la fecha formateada.
        
        Args:
            formato: Formato de fecha (default: dd/mm/yyyy)
            
        Returns:
            Fecha formateada como string
        """
        return self.fecha.strftime(formato)
    
    def fecha_legible(self) -> str:
        """
        Retorna la fecha en formato legible para humanos.
        
        Returns:
            String como "20/11 (Miércoles)"
        """
        return f"{self.fecha_formateada('%d/%m')} ({self.dia_semana})"
    
    def __str__(self) -> str:
        """Representación en string del evento"""
        return f"{self.fecha_legible()} - {self.titulo} [{self.categoria}]"
    
    def __repr__(self) -> str:
        """Representación técnica del evento"""
        return f"Evento(fecha={self.fecha}, titulo='{self.titulo}', categoria='{self.categoria}')"
    
    class Config:
        """Configuración de Pydantic"""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        json_schema_extra = {
            "example": {
                "fecha": "2025-11-20T00:00:00",
                "titulo": "Fin del Segundo Cuatrimestre",
                "categoria": "academico"
            }
        }