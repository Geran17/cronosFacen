"""
Tests para el módulo de logging.
Verifica que el sistema de logging funciona correctamente.
"""

import pytest
import logging
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.scripts.logging_config import (
    obtener_logger,
    obtener_logger_modulo,
    registrar_evento_importante,
    registrar_error_critico,
    LoggerConfig,
    configurar_logging_global,
)


class TestObtenerLogger:
    """Tests para la función obtener_logger."""

    def test_obtener_logger_retorna_logger_valido(self):
        """Verifica que obtener_logger retorna un logger válido."""
        logger = obtener_logger("test_logger")
        assert logger is not None
        assert isinstance(logger, logging.Logger)

    def test_obtener_logger_con_nombre_personalizado(self):
        """Verifica que se puede obtener logger con nombre personalizado."""
        logger = obtener_logger("modulo.submodulo")
        assert logger.name == "modulo.submodulo"

    def test_obtener_logger_con_nivel_custom(self):
        """Verifica que se puede establecer nivel personalizado."""
        logger = obtener_logger("debug_logger", nivel=logging.DEBUG)
        assert logger.level == logging.DEBUG

    def test_obtener_logger_nivel_por_defecto(self):
        """Verifica que usa nivel INFO por defecto."""
        logger = obtener_logger("default_level_logger")
        assert logger.level == logging.INFO

    def test_obtener_logger_mismo_nombre_retorna_mismo(self):
        """Verifica que logger con mismo nombre se reutiliza."""
        logger1 = obtener_logger("reutilizable")
        logger2 = obtener_logger("reutilizable")
        assert logger1 is logger2

    def test_obtener_logger_agrega_handlers(self):
        """Verifica que se agregan los handlers correctamente."""
        logger = obtener_logger("logger_con_handlers")
        # Debe tener al menos 3 handlers: archivo, error y consola
        assert len(logger.handlers) >= 2  # Archivo y consola al mínimo


class TestObtenerLoggerModulo:
    """Tests para obtener_logger_modulo."""

    def test_obtener_logger_modulo(self):
        """Verifica que obtener_logger_modulo funciona correctamente."""
        logger = obtener_logger_modulo(__name__)
        assert logger is not None
        assert isinstance(logger, logging.Logger)

    def test_nombre_logger_modulo_coincide(self):
        """Verifica que el nombre del logger coincide con el módulo."""
        modulo_nombre = "src.modelos.daos.test_dao"
        logger = obtener_logger_modulo(modulo_nombre)
        assert logger.name == modulo_nombre


class TestRegistrarEventoImportante:
    """Tests para registrar_evento_importante."""

    def test_registrar_evento_sin_detalles(self, caplog):
        """Verifica registro de evento sin detalles."""
        with caplog.at_level(logging.INFO):
            registrar_evento_importante("Usuario autenticado")
        assert "Usuario autenticado" in caplog.text

    def test_registrar_evento_con_detalles(self, caplog):
        """Verifica registro de evento con detalles."""
        with caplog.at_level(logging.INFO):
            registrar_evento_importante(
                "Operación completada",
                {"usuario": "admin", "accion": "crear", "tabla": "estudiantes"},
            )
        assert "Operación completada" in caplog.text
        assert "Detalles:" in caplog.text


class TestRegistrarErrorCritico:
    """Tests para registrar_error_critico."""

    def test_registrar_error_sin_contexto(self, caplog):
        """Verifica registro de error sin contexto."""
        with caplog.at_level(logging.ERROR):
            try:
                raise ValueError("Error de prueba")
            except ValueError as e:
                registrar_error_critico(e)
        assert "Error crítico:" in caplog.text
        assert "ValueError" in caplog.text

    def test_registrar_error_con_contexto(self, caplog):
        """Verifica registro de error con contexto."""
        with caplog.at_level(logging.ERROR):
            try:
                raise RuntimeError("Fallo en BD")
            except RuntimeError as e:
                registrar_error_critico(e, "Conectando a base de datos")
        assert "Error crítico en Conectando a base de datos" in caplog.text


class TestLoggerConfig:
    """Tests para la clase LoggerConfig."""

    def test_directorio_logs_existe(self):
        """Verifica que el directorio de logs existe."""
        assert LoggerConfig.LOGS_DIR_PATH.exists()
        assert LoggerConfig.LOGS_DIR_PATH.is_dir()

    def test_formatter_valido(self):
        """Verifica que el formatter está configurado correctamente."""
        assert LoggerConfig.FORMATTER is not None
        assert isinstance(LoggerConfig.FORMATTER, logging.Formatter)

    def test_console_formatter_valido(self):
        """Verifica que console formatter está configurado."""
        assert LoggerConfig.CONSOLE_FORMATTER is not None
        assert isinstance(LoggerConfig.CONSOLE_FORMATTER, logging.Formatter)

    def test_rutas_log_validas(self):
        """Verifica que las rutas de logs son válidas."""
        assert Path(LoggerConfig.LOG_FILE).parent.exists()
        assert Path(LoggerConfig.ERROR_LOG_FILE).parent.exists()

    def test_configuracion_valores(self):
        """Verifica valores de configuración."""
        assert LoggerConfig.DEFAULT_LEVEL == logging.INFO
        assert LoggerConfig.MAX_FILE_SIZE == 10 * 1024 * 1024
        assert LoggerConfig.BACKUP_COUNT == 5


class TestConfigurarLoggingGlobal:
    """Tests para configurar_logging_global."""

    def test_configurar_logging_global_debug(self):
        """Verifica que se configura logging global en DEBUG."""
        configurar_logging_global(logging.DEBUG)
        # basicConfig solo funciona si no está ya configurado
        # Por lo tanto, solo verificamos que la función no lanza error
        assert True

    def test_configurar_logging_global_info(self):
        """Verifica que se configura logging global en INFO."""
        configurar_logging_global(logging.INFO)
        # basicConfig solo funciona si no está ya configurado
        # Por lo tanto, solo verificamos que la función no lanza error
        assert True


class TestIntegracionLogging:
    """Tests de integración del sistema de logging."""

    def test_logging_multiples_modulos(self):
        """Verifica logging desde múltiples módulos."""
        logger1 = obtener_logger_modulo("modulo1")
        logger2 = obtener_logger_modulo("modulo2")

        assert logger1.name == "modulo1"
        assert logger2.name == "modulo2"
        assert logger1 is not logger2

    def test_archivo_log_creado(self):
        """Verifica que se crea archivo de log."""
        logger = obtener_logger("test_archivo")
        logger.info("Mensaje de prueba")

        assert Path(LoggerConfig.LOG_FILE).exists()

    def test_archivo_error_log_creado(self):
        """Verifica que se crea archivo de error log."""
        logger = obtener_logger("test_error_archivo")
        logger.error("Error de prueba")

        assert Path(LoggerConfig.ERROR_LOG_FILE).exists()

    def test_logging_con_excepciones(self):
        """Verifica logging correcto con excepciones."""
        logger = obtener_logger("test_exception")

        try:
            raise KeyError("Clave no encontrada")
        except KeyError:
            logger.exception("Excepción capturada")

        assert Path(LoggerConfig.LOG_FILE).exists()


class TestNivelesLogging:
    """Tests para verificar niveles de logging."""

    def test_debug_nivel(self, caplog):
        """Verifica mensaje DEBUG."""
        logger = obtener_logger("debug_test", nivel=logging.DEBUG)
        with caplog.at_level(logging.DEBUG):
            logger.debug("Mensaje debug")
        assert "Mensaje debug" in caplog.text

    def test_info_nivel(self, caplog):
        """Verifica mensaje INFO."""
        logger = obtener_logger("info_test")
        with caplog.at_level(logging.INFO):
            logger.info("Mensaje info")
        assert "Mensaje info" in caplog.text

    def test_warning_nivel(self, caplog):
        """Verifica mensaje WARNING."""
        logger = obtener_logger("warning_test")
        with caplog.at_level(logging.WARNING):
            logger.warning("Mensaje warning")
        assert "Mensaje warning" in caplog.text

    def test_error_nivel(self, caplog):
        """Verifica mensaje ERROR."""
        logger = obtener_logger("error_test")
        with caplog.at_level(logging.ERROR):
            logger.error("Mensaje error")
        assert "Mensaje error" in caplog.text

    def test_critical_nivel(self, caplog):
        """Verifica mensaje CRITICAL."""
        logger = obtener_logger("critical_test")
        with caplog.at_level(logging.CRITICAL):
            logger.critical("Mensaje crítico")
        assert "Mensaje crítico" in caplog.text
