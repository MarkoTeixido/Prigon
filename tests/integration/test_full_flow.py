# tests/integration/test_full_flow.py
"""
Tests de integración del flujo completo
"""

import pytest
from src.services.calendario_service import CalendarioService
from src.mcp.server import PregonMCPServer


@pytest.mark.integration
@pytest.mark.slow
class TestFullFlow:
    """Tests de integración del flujo completo"""
    
    def test_calendario_service_ejecutar(self):
        """Debe ejecutar el servicio completo"""
        service = CalendarioService()
        resultado = service.ejecutar()
        
        assert resultado is not None
        assert "exito" in resultado
    
    def test_scraper_extrae_eventos_reales(self):
        """Debe extraer eventos del calendario real"""
        service = CalendarioService()
        
        # Forzar scraping
        contenido = service.scraper.descargar_contenido()
        eventos = service.scraper.extraer_eventos(contenido)
        
        assert eventos is not None
        assert isinstance(eventos, list)
        assert len(eventos) > 0
    
    @pytest.mark.asyncio
    async def test_mcp_server_workflow_completo(self):
        """Test de workflow completo del MCP Server"""
        server = PregonMCPServer()
        
        # 1. Listar herramientas
        tools = server.list_tools()
        assert len(tools) == 6
        
        # 2. Obtener eventos
        response1 = await server.call_tool("get_eventos_semana", {})
        assert response1.isError is False
        
        # 3. Buscar exámenes
        response2 = await server.call_tool("buscar_eventos", {"categoria": "examen"})
        assert response2.isError is False
        
        # 4. Generar link
        response3 = await server.call_tool("generar_link_calendar", {"evento_id": 1})
        assert response3.isError is False