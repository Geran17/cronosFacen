"""
Módulo de configuración de logging para la aplicación.
Proporciona funciones para registrar eventos con diferentes niveles de severidad.
Soporta logging en archivos con rotación automática y en consola.
"""

import logging
import logging.handlers
import os
import sys
from os.path import join
from pathlib import Path
from datetime import datetime

# Agregar src al path para las importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utilidades.config import LOGS_DIR


class LoggerConfig:
    """Configuración centralizada de logging para la aplicación."""

    # Ruta base para los logs
    LOGS_DIR_PATH = Path(join(LOGS_DIR, "logs"))

    # Asegurar que el directorio de logs existe
    LOGS_DIR_PATH.mkdir(parents=True, exist_ok=True)

    # Nombre del archivo de log principal
    LOG_FILE = str(LOGS_DIR_PATH / "app.log")

    # Nombre del archivo de log de errores
    ERROR_LOG_FILE = str(LOGS_DIR_PATH / "errors.log")

    # Formato de logs
    FORMATTER = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    # Formato simple para consola
    CONSOLE_FORMATTER = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S'
    )

    # Nivel de log por defecto
    DEFAULT_LEVEL = logging.INFO

    # Tamaño máximo del archivo de log (10 MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024

    # Número de backups a mantener
    BACKUP_COUNT = 5


def obtener_logger(nombre: str, nivel: int = None) -> logging.Logger:
    """
    Obtiene un logger configurado para la aplicación.

    Args:
        nombre: Nombre del logger (generalmente __name__)
        nivel: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
               Si es None, usa el nivel por defecto (INFO)

    Returns:
        logging.Logger: Logger configurado

    Ejemplo:
        >>> logger = obtener_logger(__name__)
        >>> logger.info("Mensaje informativo")
        >>> logger.error("Error en la aplicación")
    """
    logger = logging.getLogger(nombre)

    # No agregar handlers si ya fueron agregados (evitar duplicados)
    if logger.handlers:
        return logger

    # Establecer nivel
    if nivel is None:
        nivel = LoggerConfig.DEFAULT_LEVEL
    logger.setLevel(nivel)

    # Handler para archivo general (con rotación)
    archivo_handler = logging.handlers.RotatingFileHandler(
        LoggerConfig.LOG_FILE,
        maxBytes=LoggerConfig.MAX_FILE_SIZE,
        backupCount=LoggerConfig.BACKUP_COUNT,
        encoding='utf-8',
    )
    archivo_handler.setLevel(logging.DEBUG)
    archivo_handler.setFormatter(LoggerConfig.FORMATTER)
    logger.addHandler(archivo_handler)

    # Handler para archivo de errores (solo ERROR y CRITICAL)
    error_handler = logging.handlers.RotatingFileHandler(
        LoggerConfig.ERROR_LOG_FILE,
        maxBytes=LoggerConfig.MAX_FILE_SIZE,
        backupCount=LoggerConfig.BACKUP_COUNT,
        encoding='utf-8',
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(LoggerConfig.FORMATTER)
    logger.addHandler(error_handler)

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(LoggerConfig.CONSOLE_FORMATTER)
    logger.addHandler(console_handler)

    return logger


def configurar_logging_global(nivel: int = logging.INFO):
    """
    Configura el logging a nivel global para toda la aplicación.

    Args:
        nivel: Nivel de logging global (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Ejemplo:
        >>> configurar_logging_global(logging.DEBUG)
    """
    logging.basicConfig(
        level=nivel,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )


def obtener_logger_modulo(modulo_nombre: str) -> logging.Logger:
    """
    Obtiene un logger específico para un módulo.

    Args:
        modulo_nombre: Nombre del módulo (típicamente __name__)

    Returns:
        logging.Logger: Logger configurado para el módulo

    Ejemplo:
        >>> logger = obtener_logger_modulo(__name__)
    """
    return obtener_logger(modulo_nombre)


def registrar_evento_importante(evento: str, detalles: dict = None):
    """
    Registra un evento importante en la aplicación.

    Args:
        evento: Descripción del evento
        detalles: Diccionario con detalles adicionales del evento

    Ejemplo:
        >>> registrar_evento_importante(
        ...     "Usuario autenticado",
        ...     {"usuario_id": 123, "ip": "192.168.1.1"}
        ... )
    """
    logger = obtener_logger("eventos")
    mensaje = evento
    if detalles:
        mensaje = f"{evento} - Detalles: {detalles}"
    logger.info(mensaje)


def registrar_error_critico(error: Exception, contexto: str = ""):
    """
    Registra un error crítico con el contexto completo.

    Args:
        error: La excepción a registrar
        contexto: Contexto adicional del error

    Ejemplo:
        >>> try:
        ...     # código que falla
        ... except Exception as e:
        ...     registrar_error_critico(e, "Procesando datos de usuario")
    """
    logger = obtener_logger("errores_criticos")
    if contexto:
        logger.exception(f"Error crítico en {contexto}: {str(error)}")
    else:
        logger.exception(f"Error crítico: {str(error)}")


# Alias para facilitar el uso
logger = obtener_logger("app")
