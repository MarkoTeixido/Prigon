# tests/unit/test_mcp_server.py
"""
Tests para el MCP Server
"""

import pytest
from src.mcp.server import PregonMCPServer


class TestMCPServer:
    """Tests del servidor MCP"""
    
    def test_server_initialization(self):
        """Debe inicializar correctamente"""
        server = PregonMCPServer()
        assert server is not None
        assert len(server.tools) == 6
    
    def test_list_tools(self):
        """Debe listar todas las herramientas"""
        server = PregonMCPServer()
        tools = server.list_tools()
        
        assert len(tools) == 6
        tool_names = [t['name'] for t in tools]
        
        assert "get_eventos_semana" in tool_names
        assert "buscar_eventos" in tool_names
        assert "get_proximos_examenes" in tool_names
    
    def test_get_capabilities(self):
        """Debe retornar capacidades correctas"""
        server = PregonMCPServer()
        caps = server.get_capabilities()
        
        assert caps["tools"] is True
        assert "resources" in caps
        assert "prompts" in caps
    
    @pytest.mark.asyncio
    async def test_call_tool_get_eventos_semana(self):
        """Debe ejecutar get_eventos_semana"""
        server = PregonMCPServer()
        response = await server.call_tool("get_eventos_semana", {})
        
        assert response is not None
        assert response.isError is False
        assert len(response.content) > 0
    
    @pytest.mark.asyncio
    async def test_call_tool_buscar_eventos(self):
        """Debe buscar eventos por categoría"""
        server = PregonMCPServer()
        response = await server.call_tool(
            "buscar_eventos",
            {"categoria": "examen"}
        )
        
        assert response is not None
        assert response.isError is False
    
    @pytest.mark.asyncio
    async def test_call_tool_invalid(self):
        """Debe manejar herramientas inválidas"""
        server = PregonMCPServer()
        response = await server.call_tool("invalid_tool", {})
        
        assert response.isError is True