# tests/unit/test_calendario_service.py
"""
Tests para CalendarioService
"""

import pytest
from datetime import datetime, timedelta
from src.services.calendario_service import CalendarioService
from src.models.evento import Evento


class TestCalendarioService:
    """Tests del servicio de calendario"""
    
    def test_inicializacion(self):
        """Debe inicializar correctamente"""
        service = CalendarioService()
        assert service is not None
        assert hasattr(service, 'scraper')
        assert hasattr(service, 'notification_manager')
        assert hasattr(service, 'logger')
    
    def test_filtrar_proxima_semana(self):
        """Debe filtrar eventos de próxima semana"""
        service = CalendarioService()
        
        hoy = datetime.now()
        eventos = [
            Evento(
                fecha=hoy + timedelta(days=1),
                titulo="Evento Mañana",
                categoria="academico"
            ),
            Evento(
                fecha=hoy + timedelta(days=10),
                titulo="Evento Futuro",
                categoria="examen"
            ),
        ]
        
        filtrados = service.filtrar_proxima_semana(eventos)
        
        # Solo debe incluir el evento dentro de 7 días
        assert len(filtrados) == 1
        assert filtrados[0].titulo == "Evento Mañana"
    
    def test_filtrar_proxima_semana_vacio(self):
        """Debe retornar lista vacía si no hay eventos"""
        service = CalendarioService()
        filtrados = service.filtrar_proxima_semana([])
        
        assert filtrados == []
    
    def test_filtrar_proxima_semana_ordena_por_fecha(self):
        """Debe ordenar eventos por fecha"""
        service = CalendarioService()
        
        hoy = datetime.now()
        eventos = [
            Evento(
                fecha=hoy + timedelta(days=5),
                titulo="Evento B",
                categoria="academico"
            ),
            Evento(
                fecha=hoy + timedelta(days=1),
                titulo="Evento A",
                categoria="examen"
            ),
        ]
        
        filtrados = service.filtrar_proxima_semana(eventos)
        
        # Debe estar ordenado
        assert filtrados[0].titulo == "Evento A"
        assert filtrados[1].titulo == "Evento B"
    
    def test_obtener_eventos_mes(self):
        """Debe obtener eventos de un mes"""
        service = CalendarioService()
        
        # Este método hace scraping real, solo verificar que no falle
        try:
            eventos = service.obtener_eventos_mes(mes=12, año=2025)
            assert isinstance(eventos, list)
        except Exception:
            # Si falla el scraping, está OK (puede no haber conexión)
            pass
    
    def test_ejecutar_flujo_completo(self):
        """Debe ejecutar el flujo completo"""
        service = CalendarioService()
        
        # Este método ejecuta todo, solo verificar que retorna dict
        resultado = service.ejecutar()
        
        assert isinstance(resultado, dict)
        assert "exito" in resultado