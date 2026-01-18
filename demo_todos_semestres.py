#!/usr/bin/env python3
"""
Script de demostración mejorado: Todos los semestres se muestran en el frame
"""

import sys

sys.path.insert(0, '/home/geran/MEGA/Workspaces/proyectos/cronosFacen/src')

from modelos.daos.estudiante_dao import EstudianteDAO
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


def demo():
    """Demostración de integración completa."""
    print("\n" + "=" * 80)
    print("🎓 DEMOSTRACIÓN: Todos los Semestres en Frame Carreras")
    print("=" * 80)

    dao = EstudianteDAO()

    # Parámetros
    id_estudiante = 1
    id_carrera = 3

    # 1. Obtener todos los semestres
    print("\n1️⃣  SEMESTRES DISPONIBLES EN LA CARRERA")
    print("-" * 80)
    sql = """SELECT DISTINCT semestre FROM asignatura 
             WHERE id_carrera = ? 
             ORDER BY semestre"""
    semestres = dao.ejecutar_consulta(sql, (id_carrera,))
    semestres_nums = [row['semestre'] for row in semestres]
    print(f"   Total de semestres: {len(semestres_nums)}")
    print(f"   Semestres: {semestres_nums}")

    # 2. Obtener asignaturas del estudiante
    print("\n2️⃣  ASIGNATURAS DEL ESTUDIANTE EN ESTA CARRERA")
    print("-" * 80)
    sql = """SELECT 
        semestre,
        nombre_asignatura,
        estado
    FROM vw_asignaturas_estudiante_completo
    WHERE id_estudiante = ? AND id_carrera = ?
    ORDER BY semestre"""
    asignaturas = dao.ejecutar_consulta(sql, (id_estudiante, id_carrera))

    print(f"   Total de asignaturas del estudiante: {len(asignaturas)}")

    # Agrupar por semestre
    asigs_por_sem = {}
    for asig in asignaturas:
        sem = asig['semestre']
        if sem not in asigs_por_sem:
            asigs_por_sem[sem] = []
        asigs_por_sem[sem].append(asig['nombre_asignatura'])

    # 3. Mostrar estructura completa
    print("\n3️⃣  ESTRUCTURA COMPLETA A MOSTRAR EN FRAME")
    print("-" * 80)
    print("\n   Semestres que se mostrarán en el ScrolledFrame:")
    for sem in semestres_nums:
        asigs = asigs_por_sem.get(sem, [])
        if asigs:
            asigs_str = ", ".join(asigs)
            print(f"   • SEMESTRE {sem}: {len(asigs)} asignatura(s)")
            print(f"       └─ {asigs_str}")
        else:
            print(f"   • SEMESTRE {sem}: (vacío - no hay asignaturas)")

    # 4. Resumen
    print("\n4️⃣  RESUMEN")
    print("-" * 80)
    print(f"   Total de semestres mostrados: {len(semestres_nums)}")
    print(f"   Semestres con asignaturas: {len(asigs_por_sem)}")
    print(f"   Semestres vacíos: {len(semestres_nums) - len(asigs_por_sem)}")
    print(f"   Total de asignaturas: {len(asignaturas)}")

    print("\n" + "=" * 80)
    print("✅ Frame Carreras ahora muestra:")
    print(f"   ✓ TODOS los {len(semestres_nums)} semestres de la carrera")
    print(f"   ✓ Las asignaturas del estudiante en cada semestre")
    print(f"   ✓ Semestres vacíos se muestran sin asignaturas")
    print("=" * 80 + "\n")


if __name__ == '__main__':
    demo()
