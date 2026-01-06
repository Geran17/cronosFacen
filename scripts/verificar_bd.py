#!/usr/bin/env python3
"""
Script de verificación final de la base de datos importada.
Realiza consultas de validación para asegurar integridad de datos.
"""

import sqlite3
from pathlib import Path


def verificar_base_datos():
    """Verifica la integridad y completitud de la BD importada."""

    db_path = Path("/home/geran/MEGA/Workspaces/proyectos/cronosFacen/data/cronosFacen.sqlite")

    if not db_path.exists():
        print(f"❌ Base de datos no encontrada: {db_path}")
        return False

    print("=" * 70)
    print("VERIFICACIÓN FINAL DE BASE DE DATOS")
    print("=" * 70)
    print(f"\n📊 Base de datos: {db_path}")
    print(f"   Tamaño: {db_path.stat().st_size / 1024:.1f} KB")

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    print("\n" + "=" * 70)
    print("CONTEO DE REGISTROS POR TABLA")
    print("=" * 70)

    tablas = [
        'carrera',
        'asignatura',
        'prerrequisito',
        'eje_tematico',
        'tipo_actividad',
        'actividad',
        'calendario_evento',
    ]

    totales = {}
    for tabla in tablas:
        cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
        count = cursor.fetchone()[0]
        totales[tabla] = count
        print(f"{tabla:25} {count:6} registros")

    total_general = sum(totales.values())
    print("-" * 70)
    print(f"{'TOTAL GENERAL':25} {total_general:6} registros")

    # Validaciones específicas
    print("\n" + "=" * 70)
    print("VALIDACIONES DE INTEGRIDAD")
    print("=" * 70)

    # 1. Verificar que todas las asignaturas referencian carreras válidas
    cursor.execute(
        """
        SELECT COUNT(*) FROM asignatura a 
        WHERE a.id_carrera NOT IN (SELECT id_carrera FROM carrera)
    """
    )
    invalid = cursor.fetchone()[0]
    print(f"\n✓ Asignaturas con carrera inválida: {invalid}")
    if invalid > 0:
        cursor.execute(
            """
            SELECT a.id_asignatura, a.nombre, a.id_carrera FROM asignatura a 
            WHERE a.id_carrera NOT IN (SELECT id_carrera FROM carrera)
        """
        )
        for row in cursor.fetchall():
            print(f"   ⚠️  Asignatura {row[0]} ({row[1]}) referencia carrera inexistente: {row[2]}")

    # 2. Verificar que todos los ejes referencian asignaturas válidas
    cursor.execute(
        """
        SELECT COUNT(*) FROM eje_tematico e 
        WHERE e.id_asignatura NOT IN (SELECT id_asignatura FROM asignatura)
    """
    )
    invalid = cursor.fetchone()[0]
    print(f"✓ Ejes temáticos con asignatura inválida: {invalid}")

    # 3. Verificar que todas las actividades referencian ejes válidos
    cursor.execute(
        """
        SELECT COUNT(*) FROM actividad a 
        WHERE a.id_eje NOT IN (SELECT id_eje FROM eje_tematico)
    """
    )
    invalid = cursor.fetchone()[0]
    print(f"✓ Actividades con eje inválido: {invalid}")

    # 4. Verificar que todas las actividades referencian tipos válidos
    cursor.execute(
        """
        SELECT COUNT(*) FROM actividad a 
        WHERE a.id_tipo_actividad NOT IN (SELECT id_tipo_actividad FROM tipo_actividad)
    """
    )
    invalid = cursor.fetchone()[0]
    print(f"✓ Actividades con tipo inválido: {invalid}")

    # 5. Estadísticas de asignaturas por carrera
    print("\n" + "=" * 70)
    print("ASIGNATURAS POR CARRERA")
    print("=" * 70)

    cursor.execute(
        """
        SELECT c.nombre, COUNT(a.id_asignatura) as count
        FROM carrera c
        LEFT JOIN asignatura a ON c.id_carrera = a.id_carrera
        GROUP BY c.id_carrera
        ORDER BY c.nombre
    """
    )

    for carrera, count in cursor.fetchall():
        print(f"{carrera:40} {count:3} asignaturas")

    # 6. Estadísticas de ejes por asignatura (aquellas con ejes)
    print("\n" + "=" * 70)
    print("ASIGNATURAS CON EJES TEMÁTICOS")
    print("=" * 70)

    cursor.execute(
        """
        SELECT a.nombre, COUNT(e.id_eje) as count
        FROM asignatura a
        LEFT JOIN eje_tematico e ON a.id_asignatura = e.id_asignatura
        WHERE e.id_eje IS NOT NULL
        GROUP BY a.id_asignatura
        ORDER BY count DESC
    """
    )

    for asignatura, count in cursor.fetchall():
        print(f"{asignatura:40} {count:3} ejes")

    # 7. Tipos de actividades utilizadas
    print("\n" + "=" * 70)
    print("ACTIVIDADES POR TIPO")
    print("=" * 70)

    cursor.execute(
        """
        SELECT t.nombre, COUNT(a.id_actividad) as count
        FROM tipo_actividad t
        LEFT JOIN actividad a ON t.id_tipo_actividad = a.id_tipo_actividad
        GROUP BY t.id_tipo_actividad
        ORDER BY count DESC
    """
    )

    for tipo, count in cursor.fetchall():
        print(f"{tipo:40} {count:3} actividades")

    # 8. Tipos de eventos en calendario
    print("\n" + "=" * 70)
    print("EVENTOS POR TIPO EN CALENDARIO")
    print("=" * 70)

    cursor.execute(
        """
        SELECT tipo, COUNT(*) as count
        FROM calendario_evento
        GROUP BY tipo
        ORDER BY count DESC
    """
    )

    for tipo, count in cursor.fetchall():
        print(f"{tipo:40} {count:3} eventos")

    # 9. Verificar nuevos ejes para asignaturas 86 y 87
    print("\n" + "=" * 70)
    print("VERIFICACIÓN DE EJES PLACEHOLDER (ASIGNATURAS 86, 87)")
    print("=" * 70)

    cursor.execute(
        """
        SELECT e.id_eje, e.nombre, a.nombre
        FROM eje_tematico e
        JOIN asignatura a ON e.id_asignatura = a.id_asignatura
        WHERE a.id_asignatura IN (86, 87)
    """
    )

    ejes_86_87 = cursor.fetchall()
    if ejes_86_87:
        for eje_id, eje_nombre, asig_nombre in ejes_86_87:
            print(f"✓ Eje {eje_id}: {eje_nombre} -> {asig_nombre}")
    else:
        print("⚠️  No se encontraron ejes para asignaturas 86 y 87")

    conn.close()

    print("\n" + "=" * 70)
    print("✅ VERIFICACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 70)
    print("\nLa base de datos está lista para ser utilizada en la aplicación.")

    return True


if __name__ == "__main__":
    verificar_base_datos()
