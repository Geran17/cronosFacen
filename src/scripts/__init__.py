"""
Módulo de scripts de la aplicación.
Incluye utilidades para logging, configuración, etc.
"""

from .logging_config import (
    obtener_logger,
    obtener_logger_modulo,
    registrar_evento_importante,
    registrar_error_critico,
    configurar_logging_global,
    LoggerConfig,
    logger,
)

__all__ = [
    "obtener_logger",
    "obtener_logger_modulo",
    "registrar_evento_importante",
    "registrar_error_critico",
    "configurar_logging_global",
    "LoggerConfig",
    "logger",
]
