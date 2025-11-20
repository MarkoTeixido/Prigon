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
    
    def obtener_eventos_semana(self) -> List[Evento]:
        """
        Obtiene eventos de la próxima semana.
        
        Returns:
            Lista de eventos de la próxima semana
        """
        try:
            self.logger.debug("Obteniendo eventos de la próxima semana...")
            
            # Obtener todos los eventos del scraper
            todos_eventos = self.calendario_service.scraper.obtener_eventos()
            
            # Filtrar solo la próxima semana
            eventos_proximos = self.calendario_service.filtrar_proxima_semana(todos_eventos)
            
            self.logger.debug(f"Eventos obtenidos: {len(eventos_proximos)}")
            return eventos_proximos
            
        except Exception as e:
            self.logger.error(f"Error obteniendo eventos de la semana: {e}", exc_info=True)
            return []
    
    def _obtener_todos_eventos(self) -> List[Evento]:
        """
        Obtiene todos los eventos del calendario.
        """
        try:
            # Obtener eventos del scraper directamente
            self.logger.debug("Obteniendo todos los eventos del calendario...")
            eventos = self.calendario_service.scraper.obtener_eventos()
            
            self.logger.debug(f"Total eventos obtenidos: {len(eventos)}")
            return eventos
            
        except Exception as e:
            self.logger.error(f"Error obteniendo eventos: {e}", exc_info=True)
            return []
    
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
            # Si no se proporcionaron eventos, obtener y filtrar inteligentemente
            if contexto_eventos is None:
                self.logger.debug("Obteniendo y filtrando eventos para el contexto...")
                
                # Obtener todos los eventos
                todos_eventos = self._obtener_todos_eventos()
                
                # ✅ USAR FILTRO INTELIGENTE
                from src.services.evento_filter import EventoFilter
                filtro = EventoFilter()
                contexto_eventos = filtro.filtrar(pregunta, todos_eventos)
                
                self.logger.info(f"Eventos en contexto (filtrados inteligentemente): {len(contexto_eventos)}")
            
            if not contexto_eventos:
                return (
                    "❌ Lo siento, no pude obtener información del calendario en este momento. "
                    "Por favor, consulta https://www.unvime.edu.ar/calendario/"
                )
            
            # Construir contexto con eventos reales
            eventos_texto = self._formatear_eventos_para_llm(contexto_eventos)
            
            # Obtener fecha actual
            fecha_actual = datetime.now().strftime("%d de %B de %Y")
            dia_semana = datetime.now().strftime("%A")
            
            # Construir prompt completo
            prompt_completo = f"""
{self.system_context}

FECHA Y HORA ACTUAL: {dia_semana}, {fecha_actual}

EVENTOS DEL CALENDARIO ACADÉMICO:
{eventos_texto}

---

PREGUNTA DEL ESTUDIANTE:
{pregunta}

INSTRUCCIONES:
- Usa SOLO la información de los eventos proporcionados
- La fecha actual es {fecha_actual}, úsala para interpretar "esta semana", "hoy", "mañana", etc.
- Si la pregunta no se puede responder con los eventos disponibles, dilo amablemente
- Sé conciso (máximo 200 palabras)
- Usa emojis apropiados
- Siempre menciona las fechas de forma clara
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
        
        # Arreglar problema del event loop cerrado
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self.responder(pregunta, contexto_eventos))
    
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
    
    async def buscar_eventos(self, query: str, dias_adelante: int = 90) -> List[Evento]:
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
            todos_eventos = self._obtener_todos_eventos()
            
            if not todos_eventos:
                return []
            
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
            todos_eventos = self._obtener_todos_eventos()
            
            eventos_dia = [
                e for e in todos_eventos
                if e.fecha.date() == fecha.date()
            ]
            
            return eventos_dia
            
        except Exception as e:
            self.logger.error(f"Error obteniendo eventos del día: {e}", exc_info=True)
            return []