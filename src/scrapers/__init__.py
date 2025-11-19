# src/scrapers/__init__.py
"""
Scrapers del proyecto Pregon
"""

from .base import BaseScraper
from .unvime_scraper import UNVimeScraper

__all__ = ['BaseScraper', 'UNVimeScraper']