#!/usr/bin/env python3
"""
Script de validación de integridad referencial antes de importar.
"""

import csv
from pathlib import Path
from collections import defaultdict

DATA_DIR = Path("/home/geran/MEGA/Workspaces/proyectos/cronosFacen/data/exported_csv")


def cargar_csv(nombre):
    """Carga un CSV y retorna lista de diccionarios."""
    archivo = DATA_DIR / nombre
    if not archivo.exists():
        print(f"⚠️  {nombre} no encontrado")
        return []

    with open(archivo, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def validar_integridad():
    """Valida todas las restricciones de clave foránea."""

    print("=" * 70)
    print("VALIDACIÓN DE INTEGRIDAD REFERENCIAL")
    print("=" * 70)

    # Cargar todos los datos
    print("\n📂 Cargando archivos CSV...")
    carrera = cargar_csv('carrera.csv')
    asignatura = cargar_csv('asignatura.csv')
    prerrequisito = cargar_csv('preRequisito.csv')
    eje_tematico = cargar_csv('eje_tematico.csv')
    tipo_actividad = cargar_csv('tipo.csv')
    actividad = cargar_csv('actividad.csv')
    calendario_evento = cargar_csv('calendario_evento.csv')

    # Crear índices de IDs
    carrera_ids = {row['id_carrera']: row for row in carrera}
    asignatura_ids = {row['id_asignatura']: row for row in asignatura}
    eje_ids = {row['id_eje']: row for row in eje_tematico}
    tipo_ids = {row['id_tipo_actividad']: row for row in tipo_actividad}

    # Diccionarios de conteo de errores
    errores = defaultdict(list)

    # Validar asignatura.id_carrera -> carrera.id_carrera
    print("\n✓ Validando asignatura.id_carrera -> carrera.id_carrera")
    for row in asignatura:
        if row['id_carrera'] not in carrera_ids:
            errores['asignatura_carrera'].append(
                f"Asignatura {row['id_asignatura']} referencia carrera inexistente: {row['id_carrera']}"
            )
    if errores['asignatura_carrera']:
        print(f"  ✗ {len(errores['asignatura_carrera'])} errores encontrados")
        for err in errores['asignatura_carrera'][:5]:
            print(f"    - {err}")
    else:
        print(f"  ✓ OK - {len(asignatura)} asignaturas válidas")

    # Validar prerrequisito.id_asignatura -> asignatura.id_asignatura (ambos lados)
    print("\n✓ Validando prerrequisito -> asignatura")
    for row in prerrequisito:
        if row['id_asignatura'] not in asignatura_ids:
            errores['prereq_asig1'].append(
                f"Prerrequisito referencia asignatura inexistente: {row['id_asignatura']}"
            )
        if row['id_asignatura_prerrequisito'] not in asignatura_ids:
            errores['prereq_asig2'].append(
                f"Prerrequisito referencia asignatura prerrequisito inexistente: {row['id_asignatura_prerrequisito']}"
            )

    error_count = len(errores['prereq_asig1']) + len(errores['prereq_asig2'])
    if error_count:
        print(f"  ✗ {error_count} errores encontrados")
    else:
        print(f"  ✓ OK - {len(prerrequisito)} prerrequisitos válidos")

    # Validar eje_tematico.id_asignatura -> asignatura.id_asignatura
    print("\n✓ Validando eje_tematico.id_asignatura -> asignatura.id_asignatura")
    for row in eje_tematico:
        if row['id_asignatura'] not in asignatura_ids:
            errores['eje_asig'].append(
                f"Eje {row['id_eje']} referencia asignatura inexistente: {row['id_asignatura']}"
            )
    if errores['eje_asig']:
        print(f"  ✗ {len(errores['eje_asig'])} errores encontrados")
    else:
        print(f"  ✓ OK - {len(eje_tematico)} ejes temáticos válidos")

    # Validar actividad.id_eje -> eje_tematico.id_eje
    print("\n✓ Validando actividad.id_eje -> eje_tematico.id_eje")
    for row in actividad:
        if row['id_eje'] not in eje_ids:
            errores['act_eje'].append(
                f"Actividad {row['id_actividad']} referencia eje inexistente: {row['id_eje']}"
            )
    if errores['act_eje']:
        print(f"  ✗ {len(errores['act_eje'])} errores encontrados")
        for err in errores['act_eje'][:5]:
            print(f"    - {err}")
    else:
        print(f"  ✓ OK - {len(actividad)} actividades con ejes válidos")

    # Validar actividad.id_tipo_actividad -> tipo_actividad.id_tipo_actividad
    print("\n✓ Validando actividad.id_tipo_actividad -> tipo_actividad.id_tipo_actividad")
    for row in actividad:
        if row['id_tipo_actividad'] not in tipo_ids:
            errores['act_tipo'].append(
                f"Actividad {row['id_actividad']} referencia tipo inexistente: {row['id_tipo_actividad']}"
            )
    if errores['act_tipo']:
        print(f"  ✗ {len(errores['act_tipo'])} errores encontrados")
        for err in errores['act_tipo'][:5]:
            print(f"    - {err}")
    else:
        print(f"  ✓ OK - {len(actividad)} actividades con tipos válidos")

    # Estadísticas finales
    print("\n" + "=" * 70)
    print("RESUMEN DE VALIDACIÓN")
    print("=" * 70)

    tablas = [
        ('carrera', len(carrera)),
        ('asignatura', len(asignatura)),
        ('prerrequisito', len(prerrequisito)),
        ('eje_tematico', len(eje_tematico)),
        ('tipo_actividad', len(tipo_actividad)),
        ('actividad', len(actividad)),
        ('calendario_evento', len(calendario_evento)),
    ]

    for tabla, count in tablas:
        print(f"{tabla:25} {count:5} registros")

    total_errors = sum(len(v) for v in errores.values())

    print("\n" + "-" * 70)
    if total_errors == 0:
        print("✅ VALIDACIÓN EXITOSA - Todos los datos están integrales")
        print("   Listo para importar a la base de datos")
        return True
    else:
        print(f"❌ VALIDACIÓN FALLIDA - {total_errors} errores encontrados")
        print("   Por favor revisar los errores antes de importar")
        return False


if __name__ == "__main__":
    success = validar_integridad()
    exit(0 if success else 1)
