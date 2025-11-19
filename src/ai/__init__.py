# src/ai/__init__.py
"""
Módulo de IA para Pregon
Proporciona capacidades de LLM (Gemini)
"""

from .llm_client import LLMClient, get_llm_client
from .chatbot import CalendarioChatbot

__all__ = ['LLMClient', 'get_llm_client', 'CalendarioChatbot']