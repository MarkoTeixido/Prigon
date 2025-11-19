# src/utils/logger.py
"""
📝 Sistema de logging profesional para Pregon
"""

import logging
import sys
from pathlib import Path
from typing import Optional
import colorlog
from src.config.settings import settings, get_logs_dir
from src.config.constants import LOG_FORMAT, LOG_DATE_FORMAT, LOG_MAX_BYTES, LOG_BACKUP_COUNT


def setup_logger(
    name: str,
    level: Optional[str] = None,
    log_to_file: bool = True
) -> logging.Logger:
    """
    Configura y retorna un logger con formato profesional.
    
    Args:
        name: Nombre del logger (generalmente __name__)
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Si True, también guarda logs en archivo
        
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    
    # Evitar duplicar handlers si ya está configurado
    if logger.handlers:
        return logger
    
    # Nivel de logging
    log_level = level or settings.log_level
    logger.setLevel(getattr(logging, log_level))
    
    # Handler para consola con colores
    console_handler = colorlog.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level))
    
    # Formato con colores para consola
    console_formatter = colorlog.ColoredFormatter(
        fmt='%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(name)s%(reset)s - %(message)s',
        datefmt=LOG_DATE_FORMAT,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Handler para archivo (sin colores)
    if log_to_file and settings.log_to_file:
        try:
            logs_dir = get_logs_dir()
            log_file = logs_dir / 'pregon.log'
            
            # RotatingFileHandler para no llenar el disco
            from logging.handlers import RotatingFileHandler
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=LOG_MAX_BYTES,
                backupCount=LOG_BACKUP_COUNT,
                encoding='utf-8'
            )
            file_handler.setLevel(getattr(logging, log_level))
            
            # Formato para archivo (más detallado)
            file_formatter = logging.Formatter(
                fmt=LOG_FORMAT,
                datefmt=LOG_DATE_FORMAT
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
            
        except Exception as e:
            logger.warning(f"No se pudo configurar logging a archivo: {e}")
    
    return logger


# Logger por defecto del módulo
logger = setup_logger(__name__)