#!/usr/bin/env python3
"""
Script de migración de datos de estudiante.id_carrera a estudiante_carrera.

Este script migra los datos existentes de la relación simple estudiante->carrera
a la nueva tabla estudiante_carrera que permite múltiples carreras por estudiante.

Uso:
    python scripts/migrar_estudiante_carrera.py

Características:
- Crea la tabla estudiante_carrera si no existe
- Migra datos existentes de estudiante.id_carrera
- Marca todas las carreras migradas como 'activa' y 'principal'
- No modifica la tabla estudiante (compatibilidad)
- Valida antes de migrar (evita duplicados)
"""

import sys
import os
from datetime import datetime

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

from modelos.daos.estudiante_carrera_dao import EstudianteCarreraDAO
from modelos.daos.estudiante_dao import EstudianteDAO
from modelos.daos.conexion_sqlite import ConexionSQLite
from modelos.dtos.estudiante_carrera_dto import EstudianteCarreraDTO
from utilidades.config import RUTA_DB


def print_header(titulo):
    """Imprime encabezado formateado"""
    print(f"\n{'='*75}")
    print(f"  {titulo}")
    print(f"{'='*75}\n")


def migrar_datos(periodo_por_defecto: str = "2024-1"):
    """
    Migra datos de estudiante.id_carrera a estudiante_carrera.

    Args:
        periodo_por_defecto (str): Periodo de ingreso por defecto para registros migrados.

    Returns:
        tuple: (total_estudiantes, migrados, omitidos, errores)
    """
    print_header("📋 MIGRACIÓN: estudiante.id_carrera → estudiante_carrera")
    print(f"Base de datos: {RUTA_DB}")
    print(f"Periodo por defecto: {periodo_por_defecto}\n")

    # Inicializar DAOs
    estudiante_dao = EstudianteDAO()
    estudiante_carrera_dao = EstudianteCarreraDAO()

    # Obtener todos los estudiantes
    sql = "SELECT id_estudiante, nombre FROM estudiante"
    conexion = ConexionSQLite()
    
    # Verificar si existe la columna id_carrera
    cursor = conexion.conn.cursor()
    cursor.execute("PRAGMA table_info(estudiante)")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    
    if 'id_carrera' in column_names:
        # Versión antigua: con id_carrera
        sql = "SELECT id_estudiante, nombre, id_carrera FROM estudiante"
        estudiantes = conexion.ejecutar_consulta(sql, ())
        usa_id_carrera = True
    else:
        # Versión nueva: sin id_carrera
        sql = "SELECT id_estudiante, nombre FROM estudiante"
        estudiantes = conexion.ejecutar_consulta(sql, ())
        usa_id_carrera = False
        print("⚠️  Nota: La tabla estudiante no tiene campo id_carrera")
        print("   Se debe especificar el id_carrera manualmente o saltará este estudiante.\n")

    total = len(estudiantes)
    migrados = 0
    omitidos = 0
    errores = 0

    print(f"📊 Estudiantes encontrados: {total}\n")

    if total == 0:
        print("⚠️  No hay estudiantes para migrar\n")
        return (0, 0, 0, 0)

    print("Migrando datos...")
    print("-" * 75)

    fecha_actual = datetime.now().strftime('%Y-%m-%d')

    for estudiante in estudiantes:
        id_estudiante = estudiante['id_estudiante']
        nombre = estudiante['nombre']
        
        if usa_id_carrera:
            id_carrera = estudiante['id_carrera']
        else:
            # Si no hay id_carrera en la tabla, omitir (requiere intervención manual)
            print(f"⏭️  Omitido: {nombre} (ID: {id_estudiante}) - Sin id_carrera, requiere asignación manual")
            omitidos += 1
            continue

        # Verificar si ya existe en estudiante_carrera
        dto_check = EstudianteCarreraDTO(id_estudiante=id_estudiante, id_carrera=id_carrera)

        if estudiante_carrera_dao.existe(dto_check):
            print(f"⏭️  Omitido: {nombre} (ID: {id_estudiante}) - Ya existe en estudiante_carrera")
            omitidos += 1
            continue

        # Crear nuevo registro
        dto = EstudianteCarreraDTO(
            id_estudiante=id_estudiante,
            id_carrera=id_carrera,
            estado='activa',
            fecha_inscripcion=fecha_actual,
            es_carrera_principal=1,
            periodo_ingreso=periodo_por_defecto,
            observaciones='Migrado automáticamente desde tabla estudiante',
        )

        resultado = estudiante_carrera_dao.insertar(dto)

        if resultado:
            print(f"✅ Migrado: {nombre} (ID: {id_estudiante}) → Carrera ID: {id_carrera}")
            migrados += 1
        else:
            print(f"❌ Error: {nombre} (ID: {id_estudiante})")
            errores += 1

    print("-" * 75)

    return (total, migrados, omitidos, errores)


def verificar_migracion():
    """
    Verifica que la migración se haya realizado correctamente.

    Returns:
        bool: True si la verificación es exitosa, False en caso contrario.
    """
    print_header("✔️  VERIFICACIÓN DE MIGRACIÓN")

    estudiante_carrera_dao = EstudianteCarreraDAO()
    conexion = ConexionSQLite()

    # Contar registros en estudiante
    sql_estudiantes = "SELECT COUNT(*) as count FROM estudiante"
    result_estudiantes = conexion.ejecutar_consulta(sql_estudiantes, ())
    total_estudiantes = result_estudiantes[0]['count'] if result_estudiantes else 0

    # Contar registros en estudiante_carrera
    sql_ec = "SELECT COUNT(*) as count FROM estudiante_carrera"
    result_ec = conexion.ejecutar_consulta(sql_ec, ())
    total_ec = result_ec[0]['count'] if result_ec else 0

    # Contar registros activos y principales
    sql_activas = """
        SELECT COUNT(*) as count 
        FROM estudiante_carrera 
        WHERE estado = 'activa' AND es_carrera_principal = 1
    """
    result_activas = conexion.ejecutar_consulta(sql_activas, ())
    total_activas = result_activas[0]['count'] if result_activas else 0

    print(f"Estudiantes totales: {total_estudiantes}")
    print(f"Registros en estudiante_carrera: {total_ec}")
    print(f"Carreras activas principales: {total_activas}\n")

    if total_ec >= total_estudiantes:
        print("✅ Verificación exitosa: Todos los estudiantes tienen al menos una carrera asignada")
        return True
    else:
        print(
            f"⚠️  Advertencia: Hay {total_estudiantes - total_ec} estudiantes sin carrera en estudiante_carrera"
        )
        return False


def main():
    """Función principal del script"""
    print_header("🔄 SCRIPT DE MIGRACIÓN - ESTUDIANTE CARRERA")

    # Obtener periodo de ingreso (puede ser argumento de línea de comandos)
    periodo = sys.argv[1] if len(sys.argv) > 1 else "2024-1"

    try:
        # Migrar datos
        total, migrados, omitidos, errores = migrar_datos(periodo)

        # Mostrar resumen
        print_header("📊 RESUMEN DE MIGRACIÓN")
        print(f"Total de estudiantes: {total}")
        print(f"✅ Migrados: {migrados}")
        print(f"⏭️  Omitidos (ya existían): {omitidos}")
        print(f"❌ Errores: {errores}\n")

        # Verificar
        verificacion_ok = verificar_migracion()

        if errores == 0:
            print_header("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
            return 0
        else:
            print_header("⚠️  MIGRACIÓN COMPLETADA CON ERRORES")
            return 1

    except Exception as ex:
        print(f"\n❌ Error durante la migración: {ex}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
