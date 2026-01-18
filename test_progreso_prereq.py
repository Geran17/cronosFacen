#!/usr/bin/env python
"""Test para verificar que el progreso de prerequisitos se calcula correctamente."""

import sys

sys.path.insert(0, '/home/geran/MEGA/Workspaces/proyectos/cronosFacen/src')

from modelos.daos.asignatura_dao import AsignaturaDAO
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


def test_progreso_prerequisitos():
    """Prueba la funcionalidad de progreso de prerequisitos."""

    dao = AsignaturaDAO(ruta_db=None)

    id_estudiante = 1
    id_carrera = 3

    # Obtener cursadas
    sql_cursadas = """SELECT * FROM vw_asignaturas_estudiante_completo
        WHERE id_estudiante = ? AND id_carrera = ?
        ORDER BY semestre, nombre_asignatura"""

    cursadas = dao.ejecutar_consulta(sql=sql_cursadas, params=(id_estudiante, id_carrera))

    logger.info("\n" + "=" * 120)
    logger.info("ASIGNATURAS CURSADAS (PARA VERIFICAR PREREQUISITOS)")
    logger.info("=" * 120)

    dict_asignaturas_por_nombre = {}
    for asig in cursadas:
        nombre = asig['nombre_asignatura']
        estado = asig['estado']
        dict_asignaturas_por_nombre[nombre] = asig
        logger.info(f"✓ {nombre:<50} → Estado: {estado}")

    # Obtener todas
    sql_todas = """SELECT 
        a.id_asignatura,
        a.nombre,
        a.semestre,
        COALESCE(aprereq.prerequisitos, '-') AS prerequisitos
    FROM asignatura a
    LEFT JOIN vw_asignatura_prerequisitos aprereq ON a.id_asignatura = aprereq.id_asignatura
    WHERE a.id_carrera = ?
    ORDER BY a.semestre, a.nombre"""

    todas = dao.ejecutar_consulta(sql=sql_todas, params=(id_carrera,))

    logger.info("\n" + "=" * 120)
    logger.info("PROGRESO DE PREREQUISITOS")
    logger.info("=" * 120)

    for asig in todas:
        nombre = asig['nombre']
        semestre = asig['semestre']
        prereq_str = asig['prerequisitos']

        if prereq_str and prereq_str != '-':
            prereqs_list = [p.strip() for p in prereq_str.split(',')]
            prereqs_completados = 0

            for prereq_nombre in prereqs_list:
                if prereq_nombre in dict_asignaturas_por_nombre:
                    prereq_data = dict_asignaturas_por_nombre[prereq_nombre]
                    if prereq_data.get('estado') in ['completada', 'aprobada']:
                        prereqs_completados += 1

            total_prereqs = len(prereqs_list)
            progreso = (prereqs_completados / total_prereqs * 100) if total_prereqs > 0 else 0.0

            logger.info(f"\nSemestre {semestre}: {nombre:<45}")
            logger.info(f"  Prerequisitos: {prereq_str}")
            logger.info(f"  Completados: {prereqs_completados}/{total_prereqs} ({progreso:.0f}%)")


if __name__ == '__main__':
    test_progreso_prerequisitos()
