# tests/integration/test_mcp_scraper.py
"""
Tests de integración: MCP Server + Scraper
"""

import pytest
from src.mcp.server import PregonMCPServer


@pytest.mark.integration
@pytest.mark.slow
class TestMCPScraperIntegration:
    """Tests de integración MCP → Scraper"""
    
    @pytest.mark.asyncio
    async def test_mcp_obtiene_eventos_reales(self):
        """
        Test de integración completo:
        MCP → EventosTools → Scraper → Web UNViMe
        """
        server = PregonMCPServer()
        
        # Llamar a herramienta que hace scraping real
        response = await server.call_tool("get_eventos_semana", {})
        
        assert response.isError is False
        assert len(response.content) > 0
        
        # Parsear respuesta
        import json
        resultado = json.loads(response.content[0]["text"])
        
        # Verificar estructura
        assert "total" in resultado
        assert "eventos" in resultado
        assert isinstance(resultado["eventos"], list)
    
    @pytest.mark.asyncio
    async def test_mcp_buscar_examenes_reales(self):
        """
        Test de integración: Buscar exámenes reales
        """
        server = PregonMCPServer()
        
        response = await server.call_tool(
            "buscar_eventos",
            {"categoria": "examen"}
        )
        
        assert response.isError is False
        
        import json
        resultado = json.loads(response.content[0]["text"])
        
        assert "total" in resultado
        assert resultado["filtros_aplicados"]["categoria"] == "examen"
    
    @pytest.mark.asyncio
    async def test_mcp_valida_fechas_invalidas(self):
        """
        Test de integración: Validación de fechas
        """
        server = PregonMCPServer()
        
        response = await server.call_tool(
            "buscar_eventos",
            {"desde": "2025-13-40"}  # Fecha inválida
        )
        
        # Debe retornar error de validación
        import json
        resultado = json.loads(response.content[0]["text"])
        
        assert "error" in resultado