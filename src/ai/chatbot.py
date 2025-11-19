# src/ai/chatbot.py
"""
🤖 Motor conversacional del Calendario Académico UNViMe
Usa Gemini para responder preguntas sobre eventos
"""

from typing import List, Optional
from datetime import datetime, timedelta
from src.ai.llm_client import get_llm_client
from src.models.evento import Evento
from src.services.calendario_service import CalendarioService
from src.utils.logger import setup_logger


class CalendarioChatbot:
    """
    Chatbot conversacional que responde preguntas sobre el calendario académico.
    Combina datos reales del scraper con inteligencia artificial.
    """
    
    def __init__(self):
        self.logger = setup_logger("CalendarioChatbot")
        self.llm = get_llm_client()
        self.calendario_service = CalendarioService()
        
        # Contexto base del asistente
        self.system_context = """
Eres un asistente académico amigable de la Universidad Nacional de Villa Mercedes (UNViMe).

Tu función es ayudar a estudiantes con información sobre el calendario académico.

Características:
- Eres amigable, conciso y útil
- Usas emojis apropiados (📅 🎓 📝 🎉)
- Das fechas en formato legible (ej: "21 de noviembre")
- Si no tienes información, lo admites honestamente
- Sugieres al usuario consultar la página oficial si es necesario

Categorías de eventos:
- 🎓 ACADEMICO: inicio/fin de clases, cuatrimestres
- 📝 EXAMEN: exámenes, finales, evaluaciones
- 🎉 FERIADO: feriados nacionales/provinciales
- 🏛️ INSTITUCIONAL: aniversarios, eventos especiales
- 🏖️ RECESO: vacaciones, recesos
- 📌 OTRO: fechas importantes varias
"""
    
    async def responder(self, pregunta: str, contexto_eventos: Optional[List[Evento]] = None) -> str:
        """
        Responde una pregunta del usuario sobre el calendario.
        
        Args:
            pregunta: Pregunta del usuario
            contexto_eventos: Lista de eventos relevantes (opcional)
            
        Returns:
            Respuesta del chatbot
        """
        try:
            # Si no se proporcionaron eventos, obtener los próximos
            if contexto_eventos is None:
                contexto_eventos = self.calendario_service.obtener_eventos()[:20]  # Solo los primeros 20
            
            # Construir contexto con eventos reales
            eventos_texto = self._formatear_eventos_para_llm(contexto_eventos)
            
            # Construir prompt completo
            prompt_completo = f"""
{self.system_context}

EVENTOS DEL CALENDARIO ACADÉMICO 2025:
{eventos_texto}

---

PREGUNTA DEL ESTUDIANTE:
{pregunta}

INSTRUCCIONES:
- Usa SOLO la información de los eventos proporcionados
- Si la pregunta no se puede responder con los eventos, dilo amablemente
- Sé conciso (máximo 200 palabras)
- Usa emojis apropiados
"""
            
            self.logger.debug(f"Procesando pregunta: {pregunta[:50]}...")
            
            # Generar respuesta con LLM
            respuesta = await self.llm.chat(
                mensaje=prompt_completo,
                contexto=None  # El contexto ya está en el mensaje
            )
            
            self.logger.debug(f"Respuesta generada: {len(respuesta)} caracteres")
            
            return respuesta
            
        except Exception as e:
            self.logger.error(f"Error generando respuesta: {e}", exc_info=True)
            return (
                "❌ Lo siento, tuve un problema al procesar tu pregunta. "
                "Por favor, intenta de nuevo o consulta el calendario en "
                "https://www.unvime.edu.ar/calendario/"
            )
    
    def responder_sync(self, pregunta: str, contexto_eventos: Optional[List[Evento]] = None) -> str:
        """Versión sincrónica de responder()"""
        import asyncio
        return asyncio.run(self.responder(pregunta, contexto_eventos))
    
    def _formatear_eventos_para_llm(self, eventos: List[Evento]) -> str:
        """
        Formatea eventos para el contexto del LLM.
        
        Args:
            eventos: Lista de eventos
            
        Returns:
            Texto formateado con los eventos
        """
        if not eventos:
            return "No hay eventos disponibles."
        
        # Agrupar por mes
        eventos_por_mes = {}
        for evento in eventos:
            mes_nombre = evento.fecha.strftime("%B %Y")
            if mes_nombre not in eventos_por_mes:
                eventos_por_mes[mes_nombre] = []
            eventos_por_mes[mes_nombre].append(evento)
        
        # Construir texto
        lineas = []
        for mes, eventos_mes in eventos_por_mes.items():
            lineas.append(f"\n{mes.upper()}:")
            for evento in eventos_mes:
                fecha_legible = evento.fecha.strftime("%d/%m/%Y (%A)")
                categoria_emoji = self._get_emoji_categoria(evento.categoria)
                lineas.append(f"  {categoria_emoji} {fecha_legible} - {evento.titulo}")
        
        return "\n".join(lineas)
    
    def _get_emoji_categoria(self, categoria: str) -> str:
        """Retorna emoji según categoría"""
        emojis = {
            "academico": "🎓",
            "examen": "📝",
            "feriado": "🎉",
            "institucional": "🏛️",
            "receso": "🏖️",
            "otro": "📌"
        }
        return emojis.get(categoria.lower(), "📅")
    
    async def buscar_eventos(self, query: str, dias_adelante: int = 30) -> List[Evento]:
        """
        Busca eventos relevantes según una query.
        
        Args:
            query: Término de búsqueda
            dias_adelante: Días a futuro para buscar
            
        Returns:
            Lista de eventos encontrados
        """
        try:
            # Obtener todos los eventos
            todos_eventos = self.calendario_service.obtener_eventos()
            
            # Filtrar por fecha (próximos X días)
            fecha_limite = datetime.now() + timedelta(days=dias_adelante)
            eventos_futuros = [
                e for e in todos_eventos 
                if e.fecha <= fecha_limite
            ]
            
            # Filtrar por query (en título o categoría)
            query_lower = query.lower()
            eventos_encontrados = [
                e for e in eventos_futuros
                if query_lower in e.titulo.lower() or query_lower in e.categoria.lower()
            ]
            
            return eventos_encontrados
            
        except Exception as e:
            self.logger.error(f"Error buscando eventos: {e}", exc_info=True)
            return []
    
    def obtener_eventos_dia(self, fecha: datetime) -> List[Evento]:
        """
        Obtiene eventos de un día específico.
        
        Args:
            fecha: Fecha a consultar
            
        Returns:
            Lista de eventos de ese día
        """
        try:
            todos_eventos = self.calendario_service.obtener_eventos()
            
            eventos_dia = [
                e for e in todos_eventos
                if e.fecha.date() == fecha.date()
            ]
            
            return eventos_dia
            
        except Exception as e:
            self.logger.error(f"Error obteniendo eventos del día: {e}", exc_info=True)
            return []