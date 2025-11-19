# src/ai/llm_client.py
"""
🤖 Cliente LLM usando Google Gemini
"""

from typing import Optional
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from src.config.settings import settings
from src.utils.logger import setup_logger


class LLMClient:
    """Cliente para Google Gemini con manejo robusto de errores"""
    
    def __init__(self):
        self.logger = setup_logger("GeminiClient")
        
        if not settings.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY no está configurada en .env\n"
                "Obtén tu API key gratis en: https://makersuite.google.com/app/apikey"
            )
        
        # Configurar Gemini
        genai.configure(api_key=settings.gemini_api_key)
        
        # Configuración de seguridad (más permisiva para evitar bloqueos innecesarios)
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
        
        # Crear modelo
        self.model = genai.GenerativeModel(
            model_name=settings.llm_model_gemini,
            generation_config={
                "temperature": settings.llm_temperature,
                "max_output_tokens": settings.llm_max_tokens,
            },
            safety_settings=self.safety_settings
        )
        
        self.logger.info(f"✅ Gemini inicializado: {settings.llm_model_gemini}")
    
    def _extraer_respuesta(self, response) -> str:
        """
        Extrae la respuesta del objeto de Gemini de forma robusta.
        
        Args:
            response: Objeto de respuesta de Gemini
            
        Returns:
            Texto de la respuesta
            
        Raises:
            ValueError: Si no se puede extraer respuesta
        """
        try:
            # Intentar acceso directo al texto
            if hasattr(response, 'text'):
                return response.text
        except ValueError as e:
            # Si falla, verificar por qué
            self.logger.warning(f"No se pudo acceder a response.text: {e}")
        
        # Verificar finish_reason
        if hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            
            finish_reason = candidate.finish_reason
            
            # Mapeo de finish_reasons
            finish_reasons = {
                0: "FINISH_REASON_UNSPECIFIED",
                1: "STOP (completado normalmente)",
                2: "MAX_TOKENS (límite de tokens alcanzado)",
                3: "SAFETY (bloqueado por seguridad)",
                4: "RECITATION (bloqueado por recitación)",
                5: "OTHER"
            }
            
            reason_text = finish_reasons.get(finish_reason, f"Desconocido ({finish_reason})")
            
            self.logger.error(f"Finish reason: {reason_text}")
            
            # Si fue bloqueado por seguridad
            if finish_reason == 3:
                if hasattr(candidate, 'safety_ratings'):
                    self.logger.error("Ratings de seguridad:")
                    for rating in candidate.safety_ratings:
                        self.logger.error(f"  - {rating.category}: {rating.probability}")
                
                raise ValueError(
                    "Gemini bloqueó la respuesta por filtros de seguridad. "
                    "Intenta reformular la pregunta o usa un modelo diferente."
                )
            
            # Intentar extraer partes manualmente
            if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                partes = candidate.content.parts
                if partes:
                    textos = [parte.text for parte in partes if hasattr(parte, 'text')]
                    if textos:
                        return ' '.join(textos)
        
        # Si llegamos aquí, no pudimos extraer nada
        raise ValueError(
            f"No se pudo extraer respuesta de Gemini. "
            f"Finish reason: {finish_reason if 'finish_reason' in locals() else 'desconocido'}"
        )
    
    async def chat(self, mensaje: str, contexto: Optional[str] = None) -> str:
        """
        Envía mensaje a Gemini (versión async).
        
        Args:
            mensaje: Mensaje del usuario
            contexto: Contexto adicional (system prompt)
            
        Returns:
            Respuesta de Gemini
        """
        try:
            # Construir prompt completo
            if contexto:
                prompt = f"{contexto}\n\n---\n\n{mensaje}"
            else:
                prompt = mensaje
            
            self.logger.debug(f"Enviando a Gemini: {mensaje[:100]}...")
            
            # Generar respuesta (async)
            response = await self.model.generate_content_async(prompt)
            
            # Extraer respuesta de forma robusta
            respuesta_texto = self._extraer_respuesta(response)
            
            self.logger.debug(f"Respuesta recibida: {len(respuesta_texto)} caracteres")
            
            return respuesta_texto
            
        except Exception as e:
            self.logger.error(f"Error en Gemini: {e}", exc_info=True)
            raise
    
    def chat_sync(self, mensaje: str, contexto: Optional[str] = None) -> str:
        """
        Versión sincrónica de chat.
        
        Args:
            mensaje: Mensaje del usuario
            contexto: Contexto adicional
            
        Returns:
            Respuesta de Gemini
        """
        try:
            # Construir prompt completo
            if contexto:
                prompt = f"{contexto}\n\n---\n\n{mensaje}"
            else:
                prompt = mensaje
            
            self.logger.debug(f"Enviando a Gemini: {mensaje[:100]}...")
            
            # Generar respuesta (sync)
            response = self.model.generate_content(prompt)
            
            # Extraer respuesta de forma robusta
            respuesta_texto = self._extraer_respuesta(response)
            
            self.logger.debug(f"Respuesta recibida: {len(respuesta_texto)} caracteres")
            
            return respuesta_texto
            
        except Exception as e:
            self.logger.error(f"Error en Gemini: {e}", exc_info=True)
            raise
    
    def chat_stream(self, mensaje: str, contexto: Optional[str] = None):
        """
        Versión streaming (para respuestas en tiempo real).
        
        Args:
            mensaje: Mensaje del usuario
            contexto: Contexto adicional
            
        Yields:
            Fragmentos de la respuesta
        """
        try:
            if contexto:
                prompt = f"{contexto}\n\n---\n\n{mensaje}"
            else:
                prompt = mensaje
            
            self.logger.debug(f"Streaming desde Gemini: {mensaje[:100]}...")
            
            # Generar respuesta streaming
            response = self.model.generate_content(prompt, stream=True)
            
            for chunk in response:
                if hasattr(chunk, 'text') and chunk.text:
                    yield chunk.text
            
        except Exception as e:
            self.logger.error(f"Error en Gemini streaming: {e}", exc_info=True)
            raise


# Factory function
def get_llm_client() -> LLMClient:
    """
    Retorna una instancia del cliente Gemini.
    
    Returns:
        Instancia de LLMClient (Gemini)
    """
    return LLMClient()