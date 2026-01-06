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

# VIEWS recomendadas según documento: views_sql_mvp_organizacion_academica_sqlite.md
VIEWS = [
    # 1. Vista: Progreso general del estudiante
    (
        "vw_progreso_estudiante",
        """
        CREATE VIEW IF NOT EXISTS vw_progreso_estudiante AS
        SELECT
            e.id_estudiante,
            e.id_carrera,
            COUNT(DISTINCT a.id_asignatura) AS total_asignaturas,
            SUM(CASE WHEN ea.estado = 'aprobada' THEN 1 ELSE 0 END) AS asignaturas_aprobadas,
            ROUND(
                100.0 * SUM(CASE WHEN ea.estado = 'aprobada' THEN 1 ELSE 0 END)
                / COUNT(DISTINCT a.id_asignatura),
                2
            ) AS porcentaje_avance
        FROM estudiante e
        JOIN carrera c ON e.id_carrera = c.id_carrera
        JOIN asignatura a ON c.id_carrera = a.id_carrera
        LEFT JOIN estudiante_asignatura ea
            ON a.id_asignatura = ea.id_asignatura
           AND ea.id_estudiante = e.id_estudiante
        GROUP BY e.id_estudiante, e.id_carrera;
        """,
    ),
    # 2. Vista: Estudiante con carrera (base para otras vistas)
    (
        "vw_estudiante_carrera",
        """
        CREATE VIEW IF NOT EXISTS vw_estudiante_carrera AS
        SELECT
            e.id_estudiante,
            e.nombre,
            e.id_carrera,
            c.nombre AS carrera,
            c.plan,
            c.modalidad,
            c.creditos_totales
        FROM estudiante e
        JOIN carrera c ON e.id_carrera = c.id_carrera;
        """,
    ),
    # 3. Vista: Asignaturas habilitadas para cursar (corregida)
    (
        "vw_asignaturas_habilitadas",
        """
        CREATE VIEW IF NOT EXISTS vw_asignaturas_habilitadas AS
        SELECT DISTINCT
            a.id_asignatura,
            a.nombre,
            a.codigo,
            a.id_carrera
        FROM asignatura a
        WHERE NOT EXISTS (
            SELECT 1 FROM prerrequisito p
            WHERE p.id_asignatura = a.id_asignatura
        )
        UNION
        SELECT DISTINCT
            a.id_asignatura,
            a.nombre,
            a.codigo,
            a.id_carrera
        FROM asignatura a
        JOIN prerrequisito p ON a.id_asignatura = p.id_asignatura
        WHERE EXISTS (
            SELECT 1 FROM estudiante_asignatura ea
            WHERE ea.id_asignatura = p.id_asignatura_prerrequisito
            AND ea.estado = 'aprobada'
        );
        """,
    ),
    # 4. Vista: Asignaturas bloqueadas (corregida)
    (
        "vw_asignaturas_bloqueadas",
        """
        CREATE VIEW IF NOT EXISTS vw_asignaturas_bloqueadas AS
        SELECT DISTINCT
            a.id_asignatura,
            a.nombre,
            a.codigo,
            p.id_asignatura_prerrequisito AS prerrequisito_id
        FROM asignatura a
        JOIN prerrequisito p ON a.id_asignatura = p.id_asignatura
        WHERE NOT EXISTS (
            SELECT 1 FROM estudiante_asignatura ea
            WHERE ea.id_asignatura = p.id_asignatura_prerrequisito
            AND ea.estado = 'aprobada'
        );
        """,
    ),
    # 5. Vista: Actividades pendientes del estudiante
    (
        "vw_actividades_pendientes",
        """
        CREATE VIEW IF NOT EXISTS vw_actividades_pendientes AS
        SELECT
            act.id_actividad,
            act.titulo,
            act.descripcion,
            act.fecha_inicio,
            act.fecha_fin,
            ta.nombre AS tipo_actividad,
            ta.siglas,
            e.id_eje,
            a.id_asignatura,
            a.nombre AS asignatura
        FROM actividad act
        LEFT JOIN tipo_actividad ta ON act.id_tipo_actividad = ta.id_tipo_actividad
        LEFT JOIN eje_tematico e ON act.id_eje = e.id_eje
        LEFT JOIN asignatura a ON e.id_asignatura = a.id_asignatura
        WHERE act.fecha_inicio <= DATE('now');
        """,
    ),
    # 6. Vista: Actividades vencidas
    (
        "vw_actividades_vencidas",
        """
        CREATE VIEW IF NOT EXISTS vw_actividades_vencidas AS
        SELECT
            act.id_actividad,
            act.titulo,
            act.fecha_fin,
            ta.nombre AS tipo_actividad,
            ta.siglas,
            a.nombre AS asignatura
        FROM actividad act
        LEFT JOIN tipo_actividad ta ON act.id_tipo_actividad = ta.id_tipo_actividad
        LEFT JOIN eje_tematico e ON act.id_eje = e.id_eje
        LEFT JOIN asignatura a ON e.id_asignatura = a.id_asignatura
        WHERE act.fecha_fin < DATE('now');
        """,
    ),
    # 7. Vista: Actividades de la semana
    (
        "vw_actividades_semana",
        """
        CREATE VIEW IF NOT EXISTS vw_actividades_semana AS
        SELECT
            act.id_actividad,
            act.titulo,
            act.fecha_inicio,
            act.fecha_fin,
            ta.nombre AS tipo_actividad,
            ta.siglas,
            a.nombre AS asignatura
        FROM actividad act
        LEFT JOIN tipo_actividad ta ON act.id_tipo_actividad = ta.id_tipo_actividad
        LEFT JOIN eje_tematico e ON act.id_eje = e.id_eje
        LEFT JOIN asignatura a ON e.id_asignatura = a.id_asignatura
        WHERE act.fecha_inicio BETWEEN DATE('now') AND DATE('now', '+7 days');
        """,
    ),
    # 8. Vista: Actividades por asignatura
    (
        "vw_actividades_por_asignatura",
        """
        CREATE VIEW IF NOT EXISTS vw_actividades_por_asignatura AS
        SELECT
            a.id_asignatura,
            a.nombre AS asignatura,
            a.codigo,
            act.id_actividad,
            act.titulo,
            act.fecha_inicio,
            act.fecha_fin,
            ta.nombre AS tipo_actividad,
            ta.siglas
        FROM actividad act
        LEFT JOIN eje_tematico e ON act.id_eje = e.id_eje
        LEFT JOIN asignatura a ON e.id_asignatura = a.id_asignatura
        LEFT JOIN tipo_actividad ta ON act.id_tipo_actividad = ta.id_tipo_actividad;
        """,
    ),
    # 9. Vista: Calendario unificado
    (
        "vw_calendario_unificado",
        """
        CREATE VIEW IF NOT EXISTS vw_calendario_unificado AS
        SELECT
            id_actividad AS id,
            titulo,
            fecha_inicio,
            fecha_fin,
            'actividad' AS origen,
            NULL AS tipo
        FROM actividad
        UNION ALL
        SELECT
            id_evento AS id,
            titulo,
            fecha_inicio,
            fecha_fin,
            'evento' AS origen,
            tipo
        FROM calendario_evento;
        """,
    ),
    # 10. Vista: Dashboard rápido del estudiante
    (
        "vw_dashboard_estudiante",
        """
        CREATE VIEW IF NOT EXISTS vw_dashboard_estudiante AS
        SELECT
            e.id_estudiante,
            COUNT(DISTINCT act.id_actividad) AS total_actividades,
            SUM(CASE WHEN ea.estado = 'entregada' THEN 1 ELSE 0 END) AS entregadas,
            SUM(CASE WHEN act.fecha_fin < DATE('now') AND ea.estado IS NULL THEN 1 ELSE 0 END) AS vencidas,
            SUM(CASE WHEN act.fecha_fin < DATE('now') AND ea.estado = 'entregada' THEN 1 ELSE 0 END) AS vencidas_entregadas
        FROM estudiante e
        LEFT JOIN estudiante_actividad ea ON e.id_estudiante = ea.id_estudiante
        LEFT JOIN actividad act ON ea.id_actividad = act.id_actividad
        GROUP BY e.id_estudiante;
        """,
    ),
    # 11. Vista: Resumen académico por estudiante
    (
        "vw_resumen_academico",
        """
        CREATE VIEW IF NOT EXISTS vw_resumen_academico AS
        SELECT
            e.id_estudiante,
            e.nombre,
            c.nombre AS carrera,
            COUNT(DISTINCT a.id_asignatura) AS total_asignaturas,
            SUM(CASE WHEN ea.estado = 'aprobada' THEN 1 ELSE 0 END) AS aprobadas,
            SUM(CASE WHEN ea.estado = 'cursando' THEN 1 ELSE 0 END) AS cursando,
            SUM(CASE WHEN ea.estado = 'reprobada' THEN 1 ELSE 0 END) AS reprobadas,
            ROUND(
                100.0 * SUM(CASE WHEN ea.estado = 'aprobada' THEN 1 ELSE 0 END)
                / COUNT(DISTINCT a.id_asignatura),
                2
            ) AS porcentaje_avance
        FROM estudiante e
        JOIN carrera c ON e.id_carrera = c.id_carrera
        JOIN asignatura a ON c.id_carrera = a.id_carrera
        LEFT JOIN estudiante_asignatura ea ON a.id_asignatura = ea.id_asignatura AND ea.id_estudiante = e.id_estudiante
        GROUP BY e.id_estudiante, e.nombre, c.nombre;
        """,
    ),
    # 12. Vista: Progreso por carrera
    (
        "vw_progreso_carreras",
        """
        CREATE VIEW IF NOT EXISTS vw_progreso_carreras AS
        SELECT
            c.id_carrera,
            c.nombre AS carrera,
            c.codigo,
            COUNT(DISTINCT pe.id_estudiante) AS total_estudiantes,
            COALESCE(ROUND(AVG(pe.porcentaje_avance), 2), 0) AS progreso_promedio,
            CASE
                WHEN COALESCE(AVG(pe.porcentaje_avance), 0) >= 70 THEN 'Activo'
                WHEN COALESCE(AVG(pe.porcentaje_avance), 0) >= 40 THEN 'Regular'
                ELSE 'En Riesgo'
            END AS estado
        FROM carrera c
        LEFT JOIN vw_progreso_estudiante pe ON c.id_carrera = pe.id_carrera
        GROUP BY c.id_carrera, c.nombre, c.codigo;
        """,
    ),
]


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
