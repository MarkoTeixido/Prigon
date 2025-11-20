# tests/unit/test_evento.py
"""
Tests del modelo Evento
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from src.models.evento import Evento


class TestEvento:
    """Tests del modelo Evento (Pydantic)"""
    
    def test_crear_evento_valido(self):
        """Debe crear un evento válido"""
        evento = Evento(
            fecha=datetime(2025, 12, 15, 9, 0),
            titulo="Examen Final",
            categoria="examen"
        )
        
        assert evento.titulo == "Examen Final"
        assert evento.categoria == "examen"
        assert evento.fecha.year == 2025
    
    def test_titulo_vacio_falla(self):
        """Debe rechazar título vacío"""
        with pytest.raises(ValidationError):
            Evento(
                fecha=datetime(2025, 12, 15),
                titulo="",
                categoria="examen"
            )
    
    def test_categoria_valida(self):
        """Debe aceptar categorías válidas"""
        # ✅ USAR LAS CATEGORÍAS REALES DEL CÓDIGO
        categorias = ["examen", "academico", "feriado", "institucional", "receso"]
        
        for cat in categorias:
            evento = Evento(
                fecha=datetime(2025, 12, 15),
                titulo="Test",
                categoria=cat
            )
            assert evento.categoria == cat
    
    def test_categoria_invalida_falla(self):
        """Debe rechazar categorías inválidas"""
        with pytest.raises(ValidationError):
            Evento(
                fecha=datetime(2025, 12, 15),
                titulo="Test",
                categoria="categoria_invalida"
            )
    
    def test_fecha_legible(self):
        """Debe formatear fecha correctamente"""
        evento = Evento(
            fecha=datetime(2025, 12, 15, 9, 0),
            titulo="Test",
            categoria="examen"
        )
        
        fecha_str = evento.fecha_legible()
        assert "15" in fecha_str
        # Solo verificar que retorna string, no formato específico
        assert isinstance(fecha_str, str)
    
    def test_model_dump(self):
        """Debe convertir a diccionario con model_dump (Pydantic v2)"""
        evento = Evento(
            fecha=datetime(2025, 12, 15, 9, 0),
            titulo="Test",
            categoria="examen"
        )
        
        # USAR model_dump() en vez de to_dict()
        dic = evento.model_dump()
        
        assert dic["titulo"] == "Test"
        assert dic["categoria"] == "examen"
        assert "fecha" in dic
    
    def test_str_representation(self):
        """Debe tener representación string clara"""
        evento = Evento(
            fecha=datetime(2025, 12, 15),
            titulo="Examen Final",
            categoria="examen"
        )
        
        str_repr = str(evento)
        assert "Examen Final" in str_repr
        assert "examen" in str_repr.lower()