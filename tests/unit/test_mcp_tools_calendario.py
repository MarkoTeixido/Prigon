# tests/unit/test_mcp_tools_calendario.py
"""
Tests para CalendarioTools (MCP)
"""

import pytest
from src.mcp.tools.calendario import CalendarioTools


class TestCalendarioTools:
    """Tests de herramientas de calendario MCP"""
    
    @pytest.mark.asyncio
    async def test_generar_link_evento_valido(self):
        """Debe generar link para evento válido"""
        tools = CalendarioTools()
        
        resultado = await tools.generar_link(evento_id=1)
        
        assert resultado is not None
        assert isinstance(resultado, dict)
    
    @pytest.mark.asyncio
    async def test_generar_link_id_invalido(self):
        """Debe manejar IDs inválidos"""
        tools = CalendarioTools()
        
        resultado = await tools.generar_link(evento_id=9999)
        
        assert "error" in resultado
    
    @pytest.mark.asyncio
    async def test_generar_link_id_negativo(self):
        """Debe rechazar IDs negativos"""
        tools = CalendarioTools()
        
        resultado = await tools.generar_link(evento_id=-1)
        
        assert "error" in resultado
    
    @pytest.mark.asyncio
    async def test_agregar_evento_id_cero(self):
        """Debe rechazar ID cero"""
        tools = CalendarioTools()
        
        resultado = await tools.agregar_evento(evento_id=0)
        
        assert "error" in resultado
    
    @pytest.mark.asyncio
    async def test_obtener_todos_eventos(self):
        """Debe obtener eventos del scraper"""
        tools = CalendarioTools()
        
        eventos = tools._obtener_todos_eventos()
        
        assert eventos is not None
        assert isinstance(eventos, list)