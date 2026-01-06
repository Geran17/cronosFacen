#!/usr/bin/env python3
"""
Herramienta interactiva para consultar la base de datos de CronosFacen.
Permite verificar datos importados de forma rápida.
"""

import sqlite3
from pathlib import Path


def conectar():
    """Conecta a la base de datos."""
    db_path = Path("/home/geran/MEGA/Workspaces/proyectos/cronosFacen/data/cronosFacen.sqlite")
    return sqlite3.connect(str(db_path)), db_path


def mostrar_menu():
    """Muestra el menú de opciones."""
    print("\n" + "=" * 70)
    print("🔍 CONSULTAS A BASE DE DATOS - CronosFacen")
    print("=" * 70)
    print("\n1. Ver carreras")
    print("2. Ver asignaturas de una carrera")
    print("3. Ver ejes de una asignatura")
    print("4. Ver actividades de un eje")
    print("5. Ver eventos de calendario")
    print("6. Estadísticas generales")
    print("7. Salir")
    return input("\nOpción (1-7): ").strip()


def listar_carreras(cursor):
    """Lista todas las carreras."""
    cursor.execute("SELECT id_carrera, codigo, nombre, plan FROM carrera ORDER BY nombre")
    print("\n📚 CARRERAS")
    print("-" * 70)
    for row in cursor.fetchall():
        print(f"ID: {row[0]:2}  |  Código: {row[1]:4}  |  {row[2]:35}  |  Plan: {row[3]}")


def listar_asignaturas_carrera(cursor):
    """Lista asignaturas de una carrera específica."""
    carrera_id = input("\nID de carrera: ").strip()

    cursor.execute(
        """
        SELECT a.id_asignatura, a.codigo, a.nombre, a.creditos, a.horas_semanales, a.tipo
        FROM asignatura a
        WHERE a.id_carrera = ?
        ORDER BY a.nombre
    """,
        (carrera_id,),
    )

    asignaturas = cursor.fetchall()

    if not asignaturas:
        print(f"⚠️  No hay asignaturas para carrera ID {carrera_id}")
        return

    print(f"\n📖 ASIGNATURAS (Carrera ID: {carrera_id})")
    print("-" * 90)
    print(f"{'ID':3} {'Código':8} {'Nombre':35} {'Cr':3} {'H/S':3} {'Tipo':10}")
    print("-" * 90)

    for row in asignaturas:
        print(f"{row[0]:3} {row[1]:8} {row[2]:35} {row[3]:3} {row[4]:3} {row[5]:10}")


def listar_ejes_asignatura(cursor):
    """Lista ejes de una asignatura específica."""
    asig_id = input("\nID de asignatura: ").strip()

    cursor.execute(
        """
        SELECT e.id_eje, e.nombre, e.orden, COUNT(a.id_actividad) as actividades
        FROM eje_tematico e
        LEFT JOIN actividad a ON e.id_eje = a.id_eje
        WHERE e.id_asignatura = ?
        GROUP BY e.id_eje
        ORDER BY e.orden
    """,
        (asig_id,),
    )

    ejes = cursor.fetchall()

    if not ejes:
        print(f"⚠️  No hay ejes para asignatura ID {asig_id}")
        return

    print(f"\n🎯 EJES TEMÁTICOS (Asignatura ID: {asig_id})")
    print("-" * 70)
    print(f"{'ID':3} {'Nombre':40} {'Orden':5} {'Actividades':12}")
    print("-" * 70)

    for row in ejes:
        print(f"{row[0]:3} {row[1]:40} {row[2]:5} {row[3]:12}")


def listar_actividades_eje(cursor):
    """Lista actividades de un eje específico."""
    eje_id = input("\nID de eje temático: ").strip()

    cursor.execute(
        """
        SELECT a.id_actividad, a.titulo, a.fecha_inicio, a.fecha_fin, t.nombre
        FROM actividad a
        JOIN tipo_actividad t ON a.id_tipo_actividad = t.id_tipo_actividad
        WHERE a.id_eje = ?
        ORDER BY a.fecha_inicio
    """,
        (eje_id,),
    )

    actividades = cursor.fetchall()

    if not actividades:
        print(f"⚠️  No hay actividades para eje ID {eje_id}")
        return

    print(f"\n✏️  ACTIVIDADES (Eje ID: {eje_id})")
    print("-" * 100)
    print(f"{'ID':4} {'Título':35} {'Inicio':12} {'Fin':12} {'Tipo':25}")
    print("-" * 100)

    for row in actividades:
        print(f"{row[0]:4} {row[1]:35} {row[2]:12} {row[3]:12} {row[4]:25}")


def listar_eventos_calendario(cursor):
    """Lista eventos del calendario."""
    cursor.execute(
        """
        SELECT id_evento, titulo, tipo, fecha_inicio, fecha_fin
        FROM calendario_evento
        ORDER BY fecha_inicio
    """
    )

    eventos = cursor.fetchall()

    print(f"\n📅 EVENTOS DE CALENDARIO ({len(eventos)} total)")
    print("-" * 90)
    print(f"{'ID':4} {'Título':35} {'Tipo':20} {'Inicio':12} {'Fin':12}")
    print("-" * 90)

    for row in eventos[:20]:  # Mostrar primeros 20
        print(f"{row[0]:4} {row[1]:35} {row[2]:20} {row[3]:12} {row[4]:12}")

    if len(eventos) > 20:
        print(f"\n... y {len(eventos) - 20} eventos más")


def estadisticas(cursor):
    """Muestra estadísticas generales."""
    print("\n" + "=" * 70)
    print("📊 ESTADÍSTICAS GENERALES")
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

    total = 0
    for tabla in tablas:
        cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
        count = cursor.fetchone()[0]
        total += count
        print(f"{tabla:25} {count:6} registros")

    print("-" * 40)
    print(f"{'TOTAL':25} {total:6} registros")

    # Mostrar asignaturas sin ejes
    cursor.execute(
        """
        SELECT COUNT(DISTINCT a.id_asignatura)
        FROM asignatura a
        WHERE a.id_asignatura NOT IN (SELECT DISTINCT id_asignatura FROM eje_tematico)
    """
    )
    sin_ejes = cursor.fetchone()[0]
    print(f"\nAsignaturas SIN ejes temáticos: {sin_ejes}")

    # Ejes placeholder creados
    cursor.execute(
        """
        SELECT e.id_eje, e.nombre, a.nombre
        FROM eje_tematico e
        JOIN asignatura a ON e.id_asignatura = a.id_asignatura
        WHERE a.id_asignatura IN (86, 87)
    """
    )

    ejes = cursor.fetchall()
    if ejes:
        print("\n✅ Ejes placeholder creados:")
        for row in ejes:
            print(f"   - Eje {row[0]}: {row[1]} ({row[2]})")


def main():
    """Función principal."""
    try:
        conn, db_path = conectar()
        cursor = conn.cursor()

        print(f"\n✅ Conectado a: {db_path}")

        while True:
            opcion = mostrar_menu()

            if opcion == "1":
                listar_carreras(cursor)
            elif opcion == "2":
                listar_asignaturas_carrera(cursor)
            elif opcion == "3":
                listar_ejes_asignatura(cursor)
            elif opcion == "4":
                listar_actividades_eje(cursor)
            elif opcion == "5":
                listar_eventos_calendario(cursor)
            elif opcion == "6":
                estadisticas(cursor)
            elif opcion == "7":
                print("\n👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción inválida")

    except Exception as e:
        print(f"\n❌ Error: {e}")

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()
