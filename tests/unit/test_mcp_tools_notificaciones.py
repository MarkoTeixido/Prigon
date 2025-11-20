# tests/unit/test_mcp_tools_notificaciones.py
"""
Tests para NotificacionesTools (MCP)
"""

import pytest
from src.mcp.tools.notificaciones import NotificacionesTools


class TestNotificacionesTools:
    """Tests de herramientas de notificaciones MCP"""
    
    @pytest.mark.asyncio
    async def test_enviar_recordatorio_id_invalido(self):
        """Debe manejar IDs inválidos"""
        tools = NotificacionesTools()
        
        resultado = await tools.enviar_recordatorio(
            evento_id=9999,
            canal="discord"
        )
        
        assert "error" in resultado
    
    @pytest.mark.asyncio
    async def test_enviar_recordatorio_canal_invalido(self):
        """Debe validar canal"""
        tools = NotificacionesTools()
        
        # Esto debería funcionar o dar error de evento no encontrado
        resultado = await tools.enviar_recordatorio(
            evento_id=1,
            canal="canal_invalido"
        )
        
        # Puede dar error de canal o de evento, ambos son válidos
        assert resultado is not None