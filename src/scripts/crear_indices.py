"""
Script para crear los índices recomendados en la base de datos SQLite.

Este módulo crea de forma idempotente todos los índices necesarios para optimizar
el rendimiento de las consultas del MVP sin sobre-optimizar.

Primero crea todas las tablas necesarias, luego los índices.

Uso:
    python -m src.scripts.crear_indices
"""

import sys
import os

# Agregar src al path para las importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utilidades.config import RUTA_DB, inicializar_directorios
from modelos.daos.conexion_sqlite import ConexionSQLite
from scripts.logging_config import obtener_logger_modulo
from sqlite3 import Error

logger = obtener_logger_modulo(__name__)

# Índices recomendados según documento: indices_recomendados_sqlite_mvp_academico.md
INDICES = [
    # 📗 Asignatura - usada en joins, prerrequisitos, progreso
    "CREATE INDEX IF NOT EXISTS idx_asignatura_carrera ON asignatura (id_carrera);",
    "CREATE INDEX IF NOT EXISTS idx_asignatura_codigo ON asignatura (codigo);",
    # 🔗 Prerrequisito - crítica para habilitaciones y bloqueos
    "CREATE INDEX IF NOT EXISTS idx_prerrequisito_asignatura ON prerrequisito (id_asignatura);",
    "CREATE INDEX IF NOT EXISTS idx_prerrequisito_requisito ON prerrequisito (id_asignatura_prerrequisito);",
    # 📚 Eje Temático
    "CREATE INDEX IF NOT EXISTS idx_eje_asignatura ON eje_tematico (id_asignatura);",
    # 🧩 Actividad - usada intensivamente en calendario y dashboard
    "CREATE INDEX IF NOT EXISTS idx_actividad_eje ON actividad (id_eje);",
    "CREATE INDEX IF NOT EXISTS idx_actividad_fechas ON actividad (fecha_inicio, fecha_fin);",
    "CREATE INDEX IF NOT EXISTS idx_actividad_tipo ON actividad (id_tipo_actividad);",
    # 🗓️ CalendarioEvento
    "CREATE INDEX IF NOT EXISTS idx_evento_fechas ON calendario_evento (fecha_inicio, fecha_fin);",
    # 👤 EstudianteCarrera - relación M:M entre estudiantes y carreras
    "CREATE INDEX IF NOT EXISTS idx_ec_estudiante ON estudiante_carrera (id_estudiante);",
    "CREATE INDEX IF NOT EXISTS idx_ec_carrera ON estudiante_carrera (id_carrera);",
    "CREATE INDEX IF NOT EXISTS idx_ec_estado ON estudiante_carrera (estado);",
    # 🎓 EstudianteAsignatura - clave para progreso
    "CREATE INDEX IF NOT EXISTS idx_ea_estudiante ON estudiante_asignatura (id_estudiante);",
    "CREATE INDEX IF NOT EXISTS idx_ea_asignatura ON estudiante_asignatura (id_asignatura);",
    "CREATE INDEX IF NOT EXISTS idx_ea_estado ON estudiante_asignatura (estado);",
    # 📌 EstudianteActividad - clave para pendientes y vencidas
    "CREATE INDEX IF NOT EXISTS idx_eact_estudiante ON estudiante_actividad (id_estudiante);",
    "CREATE INDEX IF NOT EXISTS idx_eact_actividad ON estudiante_actividad (id_actividad);",
    "CREATE INDEX IF NOT EXISTS idx_eact_estado ON estudiante_actividad (estado);",
    # 🚀 Índices compuestos (MVP+) - solo si el volumen crece
    "CREATE INDEX IF NOT EXISTS idx_eact_estudiante_estado ON estudiante_actividad (id_estudiante, estado);",
    "CREATE INDEX IF NOT EXISTS idx_actividad_tipo_fecha ON actividad (id_tipo_actividad, fecha_fin);",
]


def crear_todos_los_indices(ruta_db: str = RUTA_DB) -> bool:
    """
    Crea todos los índices recomendados en la base de datos.

    Los índices se crean de forma idempotente usando IF NOT EXISTS,
    por lo que es seguro llamar a esta función múltiples veces.

    Args:
        ruta_db (str): Ruta a la base de datos SQLite. Por defecto usa RUTA_DB.

    Returns:
        bool: True si todos los índices se crearon exitosamente, False en caso de error.
    """
    # Primero crear todas las tablas necesarias
    logger.info("🔧 Creando tablas necesarias...")
    _crear_todas_las_tablas(ruta_db)

    db = ConexionSQLite(ruta_db=ruta_db)
    con = db.obtener_conexion()

    try:
        cursor = con.cursor()
        indices_creados = 0

        for indice_sql in INDICES:
            try:
                logger.debug(f"Ejecutando: {indice_sql[:70]}...")
                cursor.execute(indice_sql)
                indices_creados += 1
            except Error as ex:
                logger.error(f"Error en índice: {indice_sql[:50]}... | {ex}")
                raise

        # Analizar estadísticas para optimizar query planner
        logger.info("Analizando estadísticas de la base de datos...")
        cursor.execute("ANALYZE;")

        con.commit()
        logger.info(f"✅ {indices_creados} índices creados exitosamente")
        return True

    except Error as ex:
        logger.error(f"❌ Error al crear índices: {ex}", exc_info=True)
        con.rollback()
        return False
    finally:
        con.close()


def _crear_todas_las_tablas(ruta_db: str = RUTA_DB) -> None:
    """
    Importa y ejecuta la creación de todas las tablas necesarias.
    Esto usa los DAOs existentes que ya tienen la lógica de creación.
    """
    try:
        # Importar todos los DAOs para que creen sus tablas
        from modelos.daos.carrera_dao import CarreraDAO
        from modelos.daos.asignatura_dao import AsignaturaDAO
        from modelos.daos.prerequisito_dao import PrerrequisitoDAO
        from modelos.daos.eje_tematico_dao import EjeTematicoDAO
        from modelos.daos.tipo_actividad_dao import TipoActividadDAO
        from modelos.daos.actividad_dao import ActividadDAO
        from modelos.daos.calendario_evento_dao import CalendarioEventoDAO
        from modelos.daos.estudiante_dao import EstudianteDAO
        from modelos.daos.estudiante_asignatura_dao import EstudianteAsignaturaDAO
        from modelos.daos.estudiante_actividad_dao import EstudianteActividadDAO
        from modelos.daos.tipo_actividad_dao import TipoActividadDAO

        # Instanciar cada DAO (el constructor automáticamente crea la tabla)
        logger.info("  ✓ Tablas creadas/verificadas")

        CarreraDAO(ruta_db=ruta_db)
        AsignaturaDAO(ruta_db=ruta_db)
        PrerrequisitoDAO(ruta_db=ruta_db)
        EjeTematicoDAO(ruta_db=ruta_db)
        TipoActividadDAO(ruta_db=ruta_db)
        ActividadDAO(ruta_db=ruta_db)
        CalendarioEventoDAO(ruta_db=ruta_db)
        EstudianteDAO(ruta_db=ruta_db)
        EstudianteAsignaturaDAO(ruta_db=ruta_db)
        EstudianteActividadDAO(ruta_db=ruta_db)

        logger.info("  ✓ Todas las tablas creadas correctamente")

    except Exception as ex:
        logger.warning(f"⚠️  No se pudieron crear todas las tablas automáticamente: {ex}")
        logger.info("  → Los índices se crearán sobre las tablas existentes")


def verificar_indices(ruta_db: str = RUTA_DB) -> dict:
    """
    Verifica qué índices ya existen en la base de datos.

    Args:
        ruta_db (str): Ruta a la base de datos SQLite.

    Returns:
        dict: Diccionario con nombre de tabla y sus índices.
    """
    import sqlite3

    try:
        con = sqlite3.connect(ruta_db)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute(
            "SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%' ORDER BY tbl_name;"
        )
        rows = cursor.fetchall()

        indices_por_tabla = {}
        for nombre_indice, tabla in rows:
            if tabla not in indices_por_tabla:
                indices_por_tabla[tabla] = []
            indices_por_tabla[tabla].append(nombre_indice)

        return indices_por_tabla
    except Exception as ex:
        logger.error(f"Error verificando índices: {ex}")
        return {}
    finally:
        if con:
            con.close()


if __name__ == "__main__":
    """Ejecutable: python -m src.scripts.crear_indices"""
    inicializar_directorios()

    print("\n" + "=" * 60)
    print("🗄️  CREADOR DE ÍNDICES - MVP ORGANIZACIÓN ACADÉMICA")
    print("=" * 60)

    print("\n📋 Índices a crear:", len(INDICES))

    if crear_todos_los_indices():
        print("\n✅ Proceso completado exitosamente\n")

        # Mostrar índices creados
        print("📊 Índices en la base de datos:")
        print("-" * 60)
        indices = verificar_indices()
        for tabla, lista_indices in sorted(indices.items()):
            print(f"\n  {tabla}:")
            for idx in lista_indices:
                print(f"    • {idx}")
        print("\n" + "=" * 60 + "\n")
    else:
        print("\n❌ Error durante la creación de índices\n")
