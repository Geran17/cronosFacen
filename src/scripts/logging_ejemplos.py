"""
Ejemplo de uso del módulo de logging en la aplicación.
"""

import sys
import os

# Agregar src al path para las importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.logging_config import (
    obtener_logger,
    obtener_logger_modulo,
    registrar_evento_importante,
    registrar_error_critico,
    configurar_logging_global,
)
import logging


# ============================================================================
# EJEMPLO 1: Logging básico en un módulo
# ============================================================================
def ejemplo_uso_basico():
    """Ejemplo de uso básico del logger."""
    logger = obtener_logger_modulo(__name__)

    logger.debug("Mensaje de debug (solo en archivo)")
    logger.info("Información general de la aplicación")
    logger.warning("Advertencia importante")
    logger.error("Se produjo un error")


# ============================================================================
# EJEMPLO 2: Registrar eventos importantes
# ============================================================================
def ejemplo_evento_importante():
    """Ejemplo de registro de eventos importantes."""
    registrar_evento_importante(
        "Usuario iniciado sesión",
        {
            "usuario_id": 42,
            "nombre_usuario": "juan.perez",
            "ip": "192.168.1.100",
            "hora": "2025-12-29 14:30:00",
        },
    )

    registrar_evento_importante(
        "Operación de base de datos completada",
        {
            "tabla": "estudiantes",
            "operacion": "INSERT",
            "registros_afectados": 5,
            "duracion_ms": 123,
        },
    )


# ============================================================================
# EJEMPLO 3: Registrar errores críticos
# ============================================================================
def ejemplo_error_critico():
    """Ejemplo de registro de errores críticos."""
    try:
        # Simular un error
        resultado = 10 / 0
    except Exception as e:
        registrar_error_critico(e, "Calculando promedio de calificaciones")


# ============================================================================
# EJEMPLO 4: Logger personalizado para un módulo específico
# ============================================================================
def ejemplo_logger_personalizado():
    """Ejemplo de logger personalizado con nivel DEBUG."""
    logger = obtener_logger(__name__, nivel=logging.DEBUG)

    logger.debug("Mensaje de debug detallado")
    logger.info("Información del módulo")
    logger.warning("Advertencia del módulo")
    logger.error("Error del módulo")


# ============================================================================
# EJEMPLO 5: Manejo de excepciones con logging
# ============================================================================
def procesar_datos_estudiante(estudiante_id: int):
    """Ejemplo de función con logging de errores."""
    logger = obtener_logger_modulo(__name__)

    try:
        logger.info(f"Iniciando procesamiento del estudiante {estudiante_id}")

        # Simular procesamiento
        if estudiante_id <= 0:
            raise ValueError("ID de estudiante inválido")

        logger.info(f"Estudiante {estudiante_id} procesado exitosamente")
        return {"status": "success", "estudiante_id": estudiante_id}

    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}", exc_info=True)
        return {"status": "error", "mensaje": str(e)}
    except Exception as e:
        registrar_error_critico(e, f"Procesamiento del estudiante {estudiante_id}")
        return {"status": "error", "mensaje": "Error crítico"}


# ============================================================================
# EJEMPLO 6: Configuración global del logging
# ============================================================================
def ejemplo_configuracion_global():
    """Ejemplo de configuración global del logging."""
    # Configurar logging global en DEBUG
    configurar_logging_global(logging.DEBUG)

    logger = obtener_logger_modulo(__name__)
    logger.debug("Ahora se muestran mensajes de DEBUG")


if __name__ == "__main__":
    print("=== Ejecutando ejemplos de logging ===\n")

    print("1. Uso básico:")
    ejemplo_uso_basico()

    print("\n2. Evento importante:")
    ejemplo_evento_importante()

    print("\n3. Error crítico:")
    ejemplo_error_critico()

    print("\n4. Logger personalizado:")
    ejemplo_logger_personalizado()

    print("\n5. Procesamiento con logging:")
    resultado = procesar_datos_estudiante(42)
    print(f"Resultado: {resultado}")

    print("\n6. Configuración global:")
    ejemplo_configuracion_global()

    print("\n✅ Revisa los archivos en la carpeta 'logs/' para ver los registros")
