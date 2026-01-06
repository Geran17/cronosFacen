#!/usr/bin/env python3
"""
Script completo de importación de datos desde CSV a SQLite.
Crea las tablas y luego importa todos los CSVs.
"""

import csv
import sqlite3
from pathlib import Path
import sys


def crear_tablas(cursor):
    """Crea todas las tablas necesarias."""

    print("📋 Creando tablas...")

    sql_create = [
        """
        CREATE TABLE IF NOT EXISTS carrera (
            id_carrera INTEGER PRIMARY KEY,
            codigo TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            plan TEXT,
            modalidad TEXT,
            creditos_totales INTEGER DEFAULT 0
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS asignatura (
            id_asignatura INTEGER PRIMARY KEY,
            codigo TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            creditos INTEGER DEFAULT 3,
            horas_semanales INTEGER DEFAULT 4,
            tipo TEXT DEFAULT 'obligatoria',
            id_carrera INTEGER NOT NULL,
            FOREIGN KEY (id_carrera) REFERENCES carrera(id_carrera)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS prerrequisito (
            id_asignatura INTEGER NOT NULL,
            id_asignatura_prerrequisito INTEGER NOT NULL,
            PRIMARY KEY (id_asignatura, id_asignatura_prerrequisito),
            FOREIGN KEY (id_asignatura) REFERENCES asignatura(id_asignatura),
            FOREIGN KEY (id_asignatura_prerrequisito) REFERENCES asignatura(id_asignatura)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS eje_tematico (
            id_eje INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            orden INTEGER,
            id_asignatura INTEGER NOT NULL,
            FOREIGN KEY (id_asignatura) REFERENCES asignatura(id_asignatura)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS tipo_actividad (
            id_tipo_actividad INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            siglas TEXT,
            descripcion TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS actividad (
            id_actividad INTEGER PRIMARY KEY,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            fecha_inicio TEXT,
            fecha_fin TEXT,
            id_eje INTEGER NOT NULL,
            id_tipo_actividad INTEGER NOT NULL,
            FOREIGN KEY (id_eje) REFERENCES eje_tematico(id_eje),
            FOREIGN KEY (id_tipo_actividad) REFERENCES tipo_actividad(id_tipo_actividad)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS calendario_evento (
            id_evento INTEGER PRIMARY KEY,
            titulo TEXT NOT NULL,
            tipo TEXT,
            fecha_inicio TEXT,
            fecha_fin TEXT,
            afecta_actividades INTEGER DEFAULT 0
        )
        """,
    ]

    for sql in sql_create:
        try:
            cursor.execute(sql)
        except sqlite3.OperationalError as e:
            print(f"⚠️  {e}")

    print("   ✓ Tablas creadas")


def cargar_csv(archivo):
    """Carga un CSV y retorna lista de diccionarios."""
    if not archivo.exists():
        return []

    with open(archivo, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def importar_datos(db_path, csv_dir):
    """Importa todos los CSV al database SQLite."""

    db_path = Path(db_path)
    csv_dir = Path(csv_dir)

    # Crear conexión
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    try:
        # Crear tablas
        crear_tablas(cursor)

        # Orden de importación (respeta restricciones FK)
        tablas = [
            (
                'carrera.csv',
                'carrera',
                ['id_carrera', 'codigo', 'nombre', 'plan', 'modalidad', 'creditos_totales'],
            ),
            (
                'asignatura.csv',
                'asignatura',
                [
                    'id_asignatura',
                    'codigo',
                    'nombre',
                    'creditos',
                    'horas_semanales',
                    'tipo',
                    'id_carrera',
                ],
            ),
            ('preRequisito.csv', 'prerrequisito', ['id_asignatura', 'id_asignatura_prerrequisito']),
            ('eje_tematico.csv', 'eje_tematico', ['id_eje', 'nombre', 'orden', 'id_asignatura']),
            (
                'tipo.csv',
                'tipo_actividad',
                ['id_tipo_actividad', 'nombre', 'siglas', 'descripcion'],
            ),
            (
                'actividad.csv',
                'actividad',
                [
                    'id_actividad',
                    'titulo',
                    'descripcion',
                    'fecha_inicio',
                    'fecha_fin',
                    'id_eje',
                    'id_tipo_actividad',
                ],
            ),
            (
                'calendario_evento.csv',
                'calendario_evento',
                ['id_evento', 'titulo', 'tipo', 'fecha_inicio', 'fecha_fin', 'afecta_actividades'],
            ),
        ]

        print("\n" + "=" * 70)
        print("IMPORTACIÓN DE DATOS")
        print("=" * 70)

        stats = {}
        errores = []

        for csv_file, tabla, columnas in tablas:
            archivo = csv_dir / csv_file

            if not archivo.exists():
                print(f"⚠️  {csv_file} no encontrado, omitiendo...")
                continue

            print(f"\n📥 Importando {tabla}...")

            # Cargar datos
            rows = cargar_csv(archivo)

            if not rows:
                print(f"   ⚠️  Sin datos")
                continue

            # Insertar datos
            placeholders = ','.join(['?' for _ in columnas])
            insert_sql = f"INSERT INTO {tabla} ({','.join(columnas)}) VALUES ({placeholders})"

            inserted = 0
            for i, row in enumerate(rows):
                try:
                    valores = [row.get(col, None) for col in columnas]
                    # Convertir strings vacíos a None
                    valores = [v if v != '' else None for v in valores]
                    cursor.execute(insert_sql, valores)
                    inserted += 1
                except sqlite3.IntegrityError as e:
                    errores.append(f"Tabla {tabla}, fila {i+1}: {e}")
                except Exception as e:
                    errores.append(f"Tabla {tabla}, fila {i+1}: {e}")

            stats[tabla] = inserted
            print(f"   ✓ {inserted}/{len(rows)} registros importados")

        conn.commit()

        # Estadísticas finales
        print("\n" + "=" * 70)
        print("RESUMEN DE IMPORTACIÓN")
        print("=" * 70)

        for tabla, count in stats.items():
            print(f"{tabla:25} {count:5} registros")

        total = sum(stats.values())
        print("-" * 70)
        print(f"{'TOTAL':25} {total:5} registros")

        if errores:
            print(f"\n⚠️  {len(errores)} errores encontrados:")
            for err in errores[:10]:
                print(f"   - {err}")
            if len(errores) > 10:
                print(f"   ... y {len(errores) - 10} más")

        print("\n✅ Importación completada")

        # Mostrar conteos en BD
        print("\n" + "=" * 70)
        print("VERIFICACIÓN EN BASE DE DATOS")
        print("=" * 70)

        for tabla in [
            'carrera',
            'asignatura',
            'prerrequisito',
            'eje_tematico',
            'tipo_actividad',
            'actividad',
            'calendario_evento',
        ]:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = cursor.fetchone()[0]
                print(f"{tabla:25} {count:5} registros")
            except:
                pass

        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

    finally:
        conn.close()


if __name__ == "__main__":
    # Determinar ruta de la BD
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    else:
        # Ruta por defecto según config.py
        db_path = Path("/home/geran/MEGA/Workspaces/proyectos/cronosFacen/data/cronosFacen.sqlite")

    csv_dir = Path("/home/geran/MEGA/Workspaces/proyectos/cronosFacen/data/exported_csv")

    print(f"Base de datos: {db_path}")
    print(f"Directorio CSV: {csv_dir}")

    # Crear directorio si no existe
    db_path.parent.mkdir(parents=True, exist_ok=True)

    success = importar_datos(db_path, csv_dir)
    sys.exit(0 if success else 1)
