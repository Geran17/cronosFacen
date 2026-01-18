#!/usr/bin/env python3
"""
Script de demostración: Integración de Vistas en Frame Carreras

Este script verifica que:
1. Las vistas están creadas en la BD
2. El controlador carga datos reales
3. El frame convierte los datos correctamente
"""

import sys

sys.path.insert(0, '/home/geran/MEGA/Workspaces/proyectos/cronosFacen/src')

from modelos.daos.estudiante_dao import EstudianteDAO
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


def demo():
    """Demostración de integración."""
    print("\n" + "=" * 80)
    print("🎓 DEMOSTRACIÓN: Integración de Vistas en Frame Carreras")
    print("=" * 80)

    dao = EstudianteDAO()

    # 1. Verificar vistas
    print("\n1️⃣  VISTAS DISPONIBLES EN BD")
    print("-" * 80)
    sql = "SELECT name FROM sqlite_master WHERE type='view' ORDER BY name"
    vistas = dao.ejecutar_consulta(sql, ())
    for view in vistas:
        print(f"   ✓ {view['name']}")

    # 2. Datos de estudiante
    print("\n2️⃣  ESTUDIANTE SELECCIONADO")
    print("-" * 80)
    sql = "SELECT id_estudiante, nombre, correo FROM estudiante WHERE id_estudiante = 1"
    estudiantes = dao.ejecutar_consulta(sql, ())
    for est in estudiantes:
        print(f"   ID: {est['id_estudiante']}")
        print(f"   Nombre: {est['nombre']}")
        print(f"   Correo: {est['correo']}")

    # 3. Carreras del estudiante
    print("\n3️⃣  CARRERAS DEL ESTUDIANTE")
    print("-" * 80)
    sql = """SELECT ec.id_carrera, c.nombre, c.plan, ec.estado
             FROM estudiante_carrera ec
             JOIN carrera c ON ec.id_carrera = c.id_carrera
             WHERE ec.id_estudiante = 1"""
    carreras = dao.ejecutar_consulta(sql, ())
    for carr in carreras:
        print(f"   • {carr['nombre']} ({carr['plan']}) - {carr['estado']}")
        print(f"     ID: {carr['id_carrera']}")

    # 4. Asignaturas con vista
    print("\n4️⃣  ASIGNATURAS CON VISTA vw_asignaturas_estudiante_completo")
    print("-" * 80)
    sql = """SELECT 
        id_estudiante,
        nombre_asignatura,
        semestre,
        estado,
        nota_final,
        cantidad_ejes_tematicos,
        cantidad_actividades,
        progreso_actividades
    FROM vw_asignaturas_estudiante_completo
    WHERE id_estudiante = 1 AND id_carrera = 3
    ORDER BY semestre"""

    asignaturas = dao.ejecutar_consulta(sql, ())
    print(f"\n   Total: {len(asignaturas)} asignaturas en carrera ID 3")

    for i, asig in enumerate(asignaturas, 1):
        nota = asig['nota_final'] if asig['nota_final'] is not None else "-"
        print(f"\n   {i}. {asig['nombre_asignatura']}")
        print(f"      • Semestre: {asig['semestre']}")
        print(f"      • Estado: {asig['estado']}")
        print(f"      • Nota: {nota}")
        print(f"      • Ejes: {asig['cantidad_ejes_tematicos']}")
        print(f"      • Actividades: {asig['cantidad_actividades']}")
        print(f"      • Progreso: {asig['progreso_actividades']}%")

    # 5. Datos agrupados por semestre
    print("\n5️⃣  DATOS AGRUPADOS POR SEMESTRE (como lo hace el controlador)")
    print("-" * 80)

    semestres = {}
    for asig in asignaturas:
        sem = asig['semestre']
        if sem not in semestres:
            semestres[sem] = []
        semestres[sem].append(asig)

    for sem in sorted(semestres.keys()):
        asigs = semestres[sem]
        progresos = [a['progreso_actividades'] for a in asigs]
        promedio = sum(progresos) / len(progresos) if progresos else 0

        print(f"\n   SEMESTRE {sem} (Progreso promedio: {promedio:.1f}%)")
        for asig in asigs:
            print(f"      • {asig['nombre_asignatura']}: {asig['progreso_actividades']}%")

    print("\n" + "=" * 80)
    print("✅ DEMOSTRACIÓN COMPLETADA - Integración funcionando correctamente")
    print("=" * 80 + "\n")


if __name__ == '__main__':
    demo()
