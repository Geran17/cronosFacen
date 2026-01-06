#!/usr/bin/env python3
"""
Script para mapear actividades de asignaturas 86 y 87 a sus ejes temáticos recién creados.
Luego genera un script de importación para SQLite.
"""

import csv
import sqlite3
from pathlib import Path

# Rutas
DATA_DIR = Path("/home/geran/MEGA/Workspaces/proyectos/cronosFacen/data/exported_csv")
SQL_FILE = Path("/home/geran/MEGA/Workspaces/proyectos/cronosFacen/data/calendarioFacen.db.sql")

# Mapeo de asignaturas a ejes temáticos recién creados
ASIGNATURA_EJE_MAP = {
    86: 326,  # Calendario Académico 2025 -> eje 326
    87: 327,  # Congresos -> eje 327
}


def analizar_actividades():
    """Lee actividad.csv y determina qué actividades pertenecen a asignaturas 86 y 87."""

    actividades_archivo = DATA_DIR / "actividad.csv"

    # Leer el archivo original SQL para verificar asignaciones
    print("=== Analizando actividades ===\n")

    # Para la versión actual, leer directamente del CSV
    if not actividades_archivo.exists():
        print(f"⚠️  {actividades_archivo} no existe")
        return

    with open(actividades_archivo, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Agrupar por id_eje actual para análisis
    eje_counts = {}
    for row in rows:
        eje = row.get('id_eje', '')
        eje_counts[eje] = eje_counts.get(eje, 0) + 1

    print(f"Total actividades en CSV: {len(rows)}")
    print(f"Ejes temáticos únicos: {len(eje_counts)}")
    print(f"Eje con más actividades: {max(eje_counts.items(), key=lambda x: x[1])}")

    # Cargar eje_tematico para mapear eje -> asignatura
    eje_tematico_file = DATA_DIR / "eje_tematico.csv"
    eje_to_asignatura = {}

    with open(eje_tematico_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            eje_to_asignatura[row['id_eje']] = row['id_asignatura']

    print("\n=== Asignación de ejes a asignaturas ===")
    print(f"Ejes para asignatura 86: ", end="")
    ejes_86 = [e for e, a in eje_to_asignatura.items() if a == '86']
    print(ejes_86 if ejes_86 else "NINGUNO (será creado)")

    print(f"Ejes para asignatura 87: ", end="")
    ejes_87 = [e for e, a in eje_to_asignatura.items() if a == '87']
    print(ejes_87 if ejes_87 else "NINGUNO (será creado)")

    # Ahora necesitamos obtener datos originales del SQL para asignaturas 86, 87
    print("\n=== Buscando actividades de asignaturas 86 y 87 en SQL ===")

    actividades_86_87 = {"86": [], "87": []}

    if SQL_FILE.exists():
        with open(SQL_FILE, 'r', encoding='utf-8') as f:
            contenido = f.read()

        # Buscar INSERT INTO actividad... VALUES para id_asignatura 86 o 87
        import re

        # Pattern para extraer valores
        pattern = r"INSERT INTO actividad VALUES \((\d+),(\d+),(\d+),'([^']*)',(?:'([^']*)'|NULL),([^,]+),([^,]+),([^,]+),([^)]+)\)"

        matches = re.findall(pattern, contenido)

        for match in matches:
            id_act, id_asig, id_tipo = int(match[0]), int(match[1]), int(match[2])
            nombre = match[3]

            if id_asig in [86, 87]:
                actividades_86_87[str(id_asig)].append(
                    {'id': id_act, 'nombre': nombre, 'id_asignatura': id_asig, 'id_tipo': id_tipo}
                )

        print(f"Actividades de asignatura 86 encontradas: {len(actividades_86_87['86'])}")
        print(f"Actividades de asignatura 87 encontradas: {len(actividades_86_87['87'])}")

        if actividades_86_87['86']:
            print("\nPrimeras actividades de 86:")
            for act in actividades_86_87['86'][:3]:
                print(f"  - ID {act['id']}: {act['nombre']}")

        if actividades_86_87['87']:
            print("\nPrimeras actividades de 87:")
            for act in actividades_86_87['87'][:3]:
                print(f"  - ID {act['id']}: {act['nombre']}")

    return rows, eje_to_asignatura


def generar_script_importacion():
    """Genera un script Python para importar todos los CSVs a SQLite."""

    script_path = Path(
        "/home/geran/MEGA/Workspaces/proyectos/cronosFacen/scripts/importar_datos.py"
    )

    script_content = '''#!/usr/bin/env python3
"""
Script de importación de CSVs a base de datos SQLite.
Importa todos los archivos CSV normalizados a la base de datos.
"""

import csv
import sqlite3
from pathlib import Path
import sys

def importar_datos(db_path, csv_dir):
    """Importa todos los CSV al database SQLite."""
    
    csv_dir = Path(csv_dir)
    db_path = Path(db_path)
    
    # Conexión a la BD
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Orden de importación (respeta restricciones FK)
    tablas = [
        ('carrera.csv', 'carrera', ['id_carrera', 'codigo', 'nombre', 'plan', 'modalidad', 'creditos_totales']),
        ('asignatura.csv', 'asignatura', ['id_asignatura', 'codigo', 'nombre', 'creditos', 'horas_semanales', 'tipo', 'id_carrera']),
        ('preRequisito.csv', 'prerrequisito', ['id_asignatura', 'id_asignatura_prerrequisito']),
        ('eje_tematico.csv', 'eje_tematico', ['id_eje', 'nombre', 'orden', 'id_asignatura']),
        ('tipo.csv', 'tipo_actividad', ['id_tipo_actividad', 'nombre', 'siglas', 'descripcion']),
        ('actividad.csv', 'actividad', ['id_actividad', 'titulo', 'descripcion', 'fecha_inicio', 'fecha_fin', 'id_eje', 'id_tipo_actividad']),
        ('calendario_evento.csv', 'calendario_evento', ['id_evento', 'titulo', 'tipo', 'fecha_inicio', 'fecha_fin', 'afecta_actividades']),
    ]
    
    stats = {}
    
    for csv_file, tabla, columnas in tablas:
        archivo = csv_dir / csv_file
        
        if not archivo.exists():
            print(f"⚠️  {csv_file} no encontrado, omitiendo...")
            continue
        
        print(f"\\n📥 Importando {tabla}...")
        
        # Limpiar tabla (si existe)
        cursor.execute(f"DELETE FROM {tabla}")
        
        # Insertar datos
        with open(archivo, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        placeholders = ','.join(['?' for _ in columnas])
        insert_sql = f"INSERT INTO {tabla} ({','.join(columnas)}) VALUES ({placeholders})"
        
        for row in rows:
            valores = [row.get(col, None) for col in columnas]
            # Convertir strings vacíos a None
            valores = [v if v != '' else None for v in valores]
            cursor.execute(insert_sql, valores)
        
        stats[tabla] = len(rows)
        print(f"   ✓ {len(rows)} registros importados")
    
    conn.commit()
    
    print("\\n" + "="*50)
    print("RESUMEN DE IMPORTACIÓN")
    print("="*50)
    for tabla, count in stats.items():
        print(f"{tabla:30} {count:5} registros")
    
    print("\\n✅ Importación completada exitosamente")
    conn.close()

if __name__ == "__main__":
    # Determinar ruta de la BD
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    else:
        # Buscar setup_database.py para ubicación de BD
        db_path = Path("/home/geran/MEGA/Workspaces/proyectos/cronosFacen/data/") / "cronos_facen.db"
    
    csv_dir = Path("/home/geran/MEGA/Workspaces/proyectos/cronosFacen/data/exported_csv")
    
    print(f"Base de datos: {db_path}")
    print(f"Directorio CSV: {csv_dir}")
    print()
    
    importar_datos(db_path, csv_dir)
'''

    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)

    print(f"\n✅ Script de importación creado: {script_path}")
    return script_path


if __name__ == "__main__":
    print("=" * 60)
    print("ANALIZADOR DE ACTIVIDADES Y MAPEO DE EJES")
    print("=" * 60)

    rows, eje_map = analizar_actividades()
    generar_script_importacion()
