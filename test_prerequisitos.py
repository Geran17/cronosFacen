#!/usr/bin/env python
"""Test para verificar que los prerequisitos se cargan y muestran correctamente."""

import sys

sys.path.insert(0, '/home/geran/MEGA/Workspaces/proyectos/cronosFacen/src')

from modelos.daos.asignatura_dao import AsignaturaDAO
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


def test_prerequisitos():
    """Prueba la carga de prerequisitos desde el controlador."""

    dao = AsignaturaDAO(ruta_db=None)

    # Simular lo que hace el controlador
    id_estudiante = 1
    id_carrera = 3

    # 1. Obtener TODAS las asignaturas con prerequisitos
    sql_todas = """SELECT 
        a.id_asignatura,
        a.nombre,
        a.codigo,
        a.semestre,
        a.tipo,
        a.creditos,
        COALESCE(aprereq.prerequisitos, '-') AS prerequisitos
    FROM asignatura a
    LEFT JOIN vw_asignatura_prerequisitos aprereq ON a.id_asignatura = aprereq.id_asignatura
    WHERE a.id_carrera = ?
    ORDER BY a.semestre, a.nombre"""

    todas_asignaturas = dao.ejecutar_consulta(sql=sql_todas, params=(id_carrera,))
    logger.info(f"✓ Cargadas {len(todas_asignaturas)} asignaturas del plan")

    # 2. Obtener cursadas
    sql_cursadas = """SELECT * FROM vw_asignaturas_estudiante_completo
        WHERE id_estudiante = ? AND id_carrera = ?
        ORDER BY semestre, nombre_asignatura"""

    cursadas = dao.ejecutar_consulta(sql=sql_cursadas, params=(id_estudiante, id_carrera))
    logger.info(f"✓ Cargadas {len(cursadas)} asignaturas cursadas")

    # 3. Crear dict cursadas
    dict_cursadas = {a['id_asignatura']: a for a in cursadas}

    # 4. Combinar datos
    estructura_completa = {}
    for asig in todas_asignaturas:
        sem = asig['semestre']
        id_asig = asig['id_asignatura']

        if sem not in estructura_completa:
            estructura_completa[sem] = []

        if id_asig in dict_cursadas:
            asig_final = dict_cursadas[id_asig]
            estado = "CURSADA"
        else:
            asig_final = {
                'nombre_asignatura': asig['nombre'],
                'codigo': asig['codigo'],
                'semestre': asig['semestre'],
                'tipo': asig['tipo'],
                'creditos': asig['creditos'],
                'id_asignatura': id_asig,
                'estado': 'disponible',
                'nota_final': None,
                'cantidad_ejes_tematicos': 0,
                'cantidad_actividades': 0,
                'prerequisitos': asig.get('prerequisitos', '-'),
                'progreso_actividades': 0.0,
            }
            estado = "DISPONIBLE"

        estructura_completa[sem].append(asig_final)

    # 5. Mostrar resultado
    logger.info("\n" + "=" * 100)
    logger.info("PREREQUISITOS CARGADOS:")
    logger.info("=" * 100)

    for sem in sorted(estructura_completa.keys()):
        asigs = estructura_completa[sem]
        logger.info(f"\n📚 SEMESTRE {sem}:")

        for asig in asigs[:5]:  # Mostrar solo los primeros 5
            prereq = asig.get('prerequisitos', '-')
            nombre = asig.get('nombre_asignatura', '')

            if prereq and prereq != '-':
                logger.info(f"   ✓ {nombre:<40} → PREREQUISITOS: {prereq}")
            else:
                logger.info(f"   ○ {nombre:<40} → SIN PREREQUISITOS")

    logger.info("\n" + "=" * 100)
    logger.info(
        f"✅ Test completado: {len(todas_asignaturas)} asignaturas, "
        f"{len(cursadas)} cursadas, {len(estructura_completa)} semestres"
    )


if __name__ == '__main__':
    test_prerequisitos()
