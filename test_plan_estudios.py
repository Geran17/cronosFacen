#!/usr/bin/env python3
"""Script para verificar todas las asignaturas de la carrera"""

import sys

sys.path.insert(0, '/home/geran/MEGA/Workspaces/proyectos/cronosFacen/src')

from modelos.daos.asignatura_dao import AsignaturaDAO

dao = AsignaturaDAO(ruta_db=None)

# Obtener todas las asignaturas de la carrera 3
sql = '''SELECT id_asignatura, nombre, semestre FROM asignatura 
         WHERE id_carrera = 3 ORDER BY semestre, nombre'''
asignaturas = dao.ejecutar_consulta(sql, ())

print("\n" + "=" * 80)
print("TODAS LAS ASIGNATURAS DEL PLAN DE ESTUDIOS - CARRERA 3")
print("=" * 80)

# Agrupar por semestre
por_sem = {}
for a in asignaturas:
    sem = a['semestre']
    if sem not in por_sem:
        por_sem[sem] = []
    por_sem[sem].append(a['nombre'])

print(f"\nTotal de asignaturas: {len(asignaturas)}")
print(f"Semestres: {sorted(por_sem.keys())}\n")

for sem in sorted(por_sem.keys()):
    asigs = por_sem[sem]
    print(f"SEMESTRE {sem} ({len(asigs)} asignaturas):")
    for asig in asigs:
        print(f"  • {asig}")
    print()

print("=" * 80 + "\n")
