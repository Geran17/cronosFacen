"""
Script para crear las VIEWS recomendadas en la base de datos SQLite.

Este módulo crea de forma idempotente todas las vistas necesarias para optimizar
las consultas del MVP sin duplicar lógica SQL en la aplicación.

Uso:
    python -m src.scripts.crear_views
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

# Lista para almacenar VIEWS a medida que se necesitan
VIEWS = []


def agregar_view(nombre: str, sql: str) -> None:
    """
    Agrega una nueva VIEW a la lista de VIEWS a crear.

    Args:
        nombre (str): Nombre de la VIEW
        sql (str): Sentencia SQL para crear la VIEW
    """
    VIEWS.append((nombre, sql))
    logger.debug(f"VIEW agregada: {nombre}")


# ┌────────────────────────────────────────────────────────────┐
# │ Agregar VIEWS aquí
# └────────────────────────────────────────────────────────────┘

# VISTA 1: Eventos Unificados (Actividades + Calendario) CON CARRERA Y ASIGNATURA
agregar_view(
    "vw_eventos_unificados",
    """
    CREATE VIEW IF NOT EXISTS vw_eventos_unificados AS
    SELECT 
        'Actividad' AS tipo_evento,
        a.id_actividad AS id_evento,
        a.titulo,
        a.descripcion,
        a.fecha_inicio,
        a.fecha_fin,
        ta.nombre AS tipo_actividad,
        NULL AS observaciones,
        car.nombre AS carrera,
        car.id_carrera,
        asig.nombre AS asignatura,
        asig.id_asignatura
    FROM actividad a
    LEFT JOIN tipo_actividad ta ON a.id_tipo_actividad = ta.id_tipo_actividad
    LEFT JOIN eje_tematico et ON a.id_eje = et.id_eje
    LEFT JOIN asignatura asig ON et.id_asignatura = asig.id_asignatura
    LEFT JOIN carrera car ON asig.id_carrera = car.id_carrera

    UNION ALL

    SELECT 
        'Evento Calendario' AS tipo_evento,
        c.id_evento AS id_evento,
        c.titulo,
        NULL AS descripcion,
        c.fecha_inicio,
        c.fecha_fin,
        c.tipo AS tipo_actividad,
        CASE WHEN c.afecta_actividades = 1 THEN 'Afecta actividades' ELSE NULL END AS observaciones,
        NULL AS carrera,
        NULL AS id_carrera,
        NULL AS asignatura,
        NULL AS id_asignatura
    FROM calendario_evento c;
    """,
)

# VISTA 2: Estudiante - Asignatura - Carrera (Relación completa)
agregar_view(
    "vw_estudiante_asignatura_carrera",
    """
    CREATE VIEW IF NOT EXISTS vw_estudiante_asignatura_carrera AS
    SELECT 
        carrera.id_carrera,
        carrera.nombre as nombre_carrera,
        asignatura.id_asignatura,
        asignatura.nombre as nombre_asignatura,
        estudiante_asignatura.id_estudiante, 
        estudiante_asignatura.estado, 
        estudiante_asignatura.nota_final
    FROM 
        carrera
        INNER JOIN asignatura ON asignatura.id_carrera = carrera.id_carrera
        INNER JOIN estudiante_asignatura ON estudiante_asignatura.id_asignatura = asignatura.id_asignatura
    ORDER BY carrera.nombre, asignatura.nombre;
    """,
)

# VISTA 4: Estudiante - Actividades con Detalles Completos
agregar_view(
    "vw_estudiante_actividades_detalladas",
    """
    CREATE VIEW IF NOT EXISTS vw_estudiante_actividades_detalladas AS
    SELECT 
        estudiante.id_estudiante AS id_estudiante,
        carrera.id_carrera AS carrera_id,
        asignatura.id_asignatura AS id_asignatura,
        actividad.id_actividad AS actividad_id,
        actividad.id_eje AS eje_id,
        tipo_actividad.id_tipo_actividad AS tipo_actividad_id,
        eje_tematico.nombre AS eje_nombre,
        eje_tematico.orden AS eje_orden,
        asignatura.nombre AS nombre_asignatura,
        actividad.titulo AS titulo,
        actividad.descripcion AS descripcion,
        actividad.fecha_inicio AS fecha_inicio,
        actividad.fecha_fin AS fecha_fin,
        tipo_actividad.nombre AS actividad_nombre,
        tipo_actividad.siglas AS siglas,
        tipo_actividad.prioridad AS prioridad,
        estudiante_actividad.estado AS actividad_estado,
        estudiante_actividad.fecha_entrega AS fecha_entrega,
        CAST((julianday(actividad.fecha_fin) - julianday(actividad.fecha_inicio)) AS INTEGER) AS dias_duracion,
        CAST((julianday(date('now')) - julianday(actividad.fecha_fin)) AS INTEGER) AS dias_desde_fin
    FROM
        actividad
        INNER JOIN eje_tematico ON actividad.id_eje = eje_tematico.id_eje
        INNER JOIN asignatura ON asignatura.id_asignatura = eje_tematico.id_asignatura
        INNER JOIN carrera ON asignatura.id_carrera = carrera.id_carrera
        INNER JOIN tipo_actividad ON actividad.id_tipo_actividad = tipo_actividad.id_tipo_actividad
        INNER JOIN estudiante_actividad ON actividad.id_actividad = estudiante_actividad.id_actividad
        INNER JOIN estudiante ON estudiante_actividad.id_estudiante = estudiante.id_estudiante
    ORDER BY actividad.fecha_fin;
    """,
)


def crear_todas_las_views(ruta_db: str = RUTA_DB) -> bool:
    """
    Crea todas las VIEWS recomendadas en la base de datos.

    Las VIEWS se crean de forma idempotente usando IF NOT EXISTS,
    por lo que es seguro llamar a esta función múltiples veces.

    Args:
        ruta_db (str): Ruta a la base de datos SQLite. Por defecto usa RUTA_DB.

    Returns:
        bool: True si todas las VIEWS se crearon exitosamente, False en caso de error.
    """
    import sqlite3

    con = None
    try:
        con = sqlite3.connect(ruta_db)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        views_creadas = 0

        for nombre_view, sql_view in VIEWS:
            try:
                logger.debug(f"Creando VIEW: {nombre_view}")
                # Primero intentar borrar la vista si existe
                try:
                    cursor.execute(f"DROP VIEW IF EXISTS {nombre_view};")
                except Error:
                    pass  # Ignorar errores de DROP VIEW

                # Luego crear la vista
                cursor.execute(sql_view)
                views_creadas += 1
            except Error as ex:
                logger.error(f"Error en VIEW {nombre_view}: {ex}")
                raise

        con.commit()
        logger.info(f"✅ {views_creadas} VIEWS creadas exitosamente")
        return True

    except Error as ex:
        logger.error(f"❌ Error al crear VIEWS: {ex}", exc_info=True)
        if con:
            con.rollback()
        return False
    finally:
        if con:
            con.close()


def verificar_views(ruta_db: str = RUTA_DB) -> dict:
    """
    Verifica qué VIEWS ya existen en la base de datos.

    Args:
        ruta_db (str): Ruta a la base de datos SQLite.

    Returns:
        dict: Diccionario con nombre y tipo de cada VIEW.
    """
    import sqlite3

    try:
        con = sqlite3.connect(ruta_db)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute(
            "SELECT name, type FROM sqlite_master WHERE type='view' AND name LIKE 'vw_%' ORDER BY name;"
        )
        rows = cursor.fetchall()

        views_encontradas = {}
        for nombre_view, tipo in rows:
            views_encontradas[nombre_view] = tipo

        return views_encontradas
    except Exception as ex:
        logger.error(f"Error verificando VIEWS: {ex}")
        return {}
    finally:
        if con:
            con.close()


def listar_columnas_view(nombre_view: str, ruta_db: str = RUTA_DB) -> list:
    """
    Obtiene las columnas de una VIEW específica.

    Args:
        nombre_view (str): Nombre de la VIEW
        ruta_db (str): Ruta a la base de datos SQLite

    Returns:
        list: Lista de nombres de columnas
    """
    import sqlite3

    try:
        con = sqlite3.connect(ruta_db)
        cursor = con.cursor()
        cursor.execute(f"PRAGMA table_info({nombre_view});")
        columnas = cursor.fetchall()
        return [(col[1], col[2]) for col in columnas]  # (nombre, tipo)
    except Exception as ex:
        logger.error(f"Error obteniendo columnas de {nombre_view}: {ex}")
        return []
    finally:
        if con:
            con.close()


if __name__ == "__main__":
    """Ejecutable: python -m src.scripts.crear_views"""
    inicializar_directorios()

    print("\n" + "=" * 70)
    print("📊 CREADOR DE VIEWS - MVP ORGANIZACIÓN ACADÉMICA")
    print("=" * 70)

    print(f"\n📋 VIEWS a crear: {len(VIEWS)}")

    if crear_todas_las_views():
        print("\n✅ Proceso completado exitosamente\n")

        # Mostrar VIEWS creadas
        print("📊 VIEWS en la base de datos:")
        print("-" * 70)
        views = verificar_views()
        for nombre_view, tipo in sorted(views.items()):
            columnas = listar_columnas_view(nombre_view)
            print(f"\n  📌 {nombre_view} ({len(columnas)} columnas)")
            for col_nombre, col_tipo in columnas[:3]:  # Mostrar primeras 3
                print(f"     • {col_nombre} ({col_tipo})")
            if len(columnas) > 3:
                print(f"     ... + {len(columnas) - 3} más")

        print("\n" + "=" * 70 + "\n")
    else:
        print("\n❌ Error durante la creación de VIEWS\n")
