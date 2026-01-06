#!/usr/bin/env python3
"""
Script para eliminar el campo id_carrera de la tabla estudiante.

Este script realiza la migración de la estructura de la tabla estudiante,
eliminando el campo id_carrera. Los datos de carreras deben estar previamente
migrados a la tabla estudiante_carrera.

⚠️ IMPORTANTE:
   - Ejecutar primero scripts/migrar_estudiante_carrera.py
   - Este script es destructivo y no se puede revertir fácilmente
   - Se recomienda hacer backup de la base de datos antes de ejecutar

Uso:
    python scripts/eliminar_id_carrera_estudiante.py

Opciones:
    --force : Omite confirmación de seguridad
"""

import sys
import os
import sqlite3
from datetime import datetime

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

from modelos.daos.conexion_sqlite import ConexionSQLite
from utilidades.config import RUTA_DB


def print_header(titulo):
    """Imprime encabezado formateado"""
    print(f"\n{'='*75}")
    print(f"  {titulo}")
    print(f"{'='*75}\n")


def crear_backup():
    """
    Crea un backup de la base de datos antes de la migración.

    Returns:
        str: Ruta del archivo de backup creado
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"{RUTA_DB}.backup_{timestamp}"

    try:
        import shutil

        shutil.copy2(RUTA_DB, backup_path)
        print(f"✅ Backup creado: {backup_path}\n")
        return backup_path
    except Exception as ex:
        print(f"❌ Error al crear backup: {ex}")
        return None


def verificar_migracion_previa():
    """
    Verifica que los datos hayan sido migrados a estudiante_carrera.

    Returns:
        tuple: (estudiantes_sin_carrera, total_estudiantes)
    """
    print_header("🔍 VERIFICANDO MIGRACIÓN PREVIA")

    conexion = ConexionSQLite()

    # Verificar que existe la tabla estudiante_carrera
    sql_check_table = """
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='estudiante_carrera'
    """
    result = conexion.ejecutar_consulta(sql_check_table, ())

    if not result:
        print("❌ ERROR: La tabla estudiante_carrera no existe.")
        print("   Ejecutar primero: python scripts/migrar_estudiante_carrera.py\n")
        return None, None

    # Contar estudiantes
    sql_estudiantes = "SELECT COUNT(*) as count FROM estudiante"
    result_est = conexion.ejecutar_consulta(sql_estudiantes, ())
    total_estudiantes = result_est[0]['count'] if result_est else 0

    # Contar estudiantes sin carrera en estudiante_carrera
    sql_sin_carrera = """
        SELECT COUNT(*) as count
        FROM estudiante e
        WHERE NOT EXISTS (
            SELECT 1 FROM estudiante_carrera ec
            WHERE ec.id_estudiante = e.id_estudiante
        )
    """
    result_sin = conexion.ejecutar_consulta(sql_sin_carrera, ())
    sin_carrera = result_sin[0]['count'] if result_sin else 0

    print(f"Total de estudiantes: {total_estudiantes}")
    print(f"Estudiantes sin carrera en estudiante_carrera: {sin_carrera}\n")

    if sin_carrera > 0:
        print(f"⚠️  ADVERTENCIA: {sin_carrera} estudiantes no tienen carrera asignada")
        print("   en la tabla estudiante_carrera.\n")
        print("   Ejecutar primero: python scripts/migrar_estudiante_carrera.py\n")
    else:
        print("✅ Todos los estudiantes tienen al menos una carrera asignada\n")

    return sin_carrera, total_estudiantes


def eliminar_campo_id_carrera():
    """
    Elimina el campo id_carrera de la tabla estudiante.

    En SQLite no se puede eliminar columnas directamente,
    por lo que se debe recrear la tabla.

    Returns:
        bool: True si la migración fue exitosa, False en caso contrario
    """
    print_header("🔨 ELIMINANDO CAMPO id_carrera")

    conexion = ConexionSQLite()
    conn = sqlite3.connect(RUTA_DB)
    cursor = conn.cursor()

    try:
        # Desactivar foreign keys temporalmente
        cursor.execute("PRAGMA foreign_keys = OFF")

        # Iniciar transacción
        cursor.execute("BEGIN TRANSACTION")

        print("1. Creando tabla temporal...")
        # Crear tabla temporal sin id_carrera
        cursor.execute(
            """
            CREATE TABLE estudiante_new (
                id_estudiante INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                correo TEXT NOT NULL UNIQUE
            )
        """
        )
        print("   ✅ Tabla temporal creada\n")

        print("2. Copiando datos...")
        # Copiar datos (sin id_carrera)
        cursor.execute(
            """
            INSERT INTO estudiante_new (id_estudiante, nombre, correo)
            SELECT id_estudiante, nombre, correo
            FROM estudiante
        """
        )
        rows_copied = cursor.rowcount
        print(f"   ✅ {rows_copied} registros copiados\n")

        print("3. Eliminando tabla antigua...")
        # Eliminar tabla antigua
        cursor.execute("DROP TABLE estudiante")
        print("   ✅ Tabla antigua eliminada\n")

        print("4. Renombrando tabla nueva...")
        # Renombrar tabla nueva
        cursor.execute("ALTER TABLE estudiante_new RENAME TO estudiante")
        print("   ✅ Tabla renombrada\n")

        # Commit de la transacción
        cursor.execute("COMMIT")

        # Reactivar foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")

        conn.close()

        print("✅ Migración completada exitosamente\n")
        return True

    except Exception as ex:
        print(f"\n❌ Error durante la migración: {ex}")
        cursor.execute("ROLLBACK")
        cursor.execute("PRAGMA foreign_keys = ON")
        conn.close()
        return False


def verificar_estructura_final():
    """
    Verifica que la estructura final de la tabla sea correcta.

    Returns:
        bool: True si la verificación es exitosa
    """
    print_header("✔️  VERIFICANDO ESTRUCTURA FINAL")

    conn = sqlite3.connect(RUTA_DB)
    cursor = conn.cursor()

    # Obtener información de la tabla
    cursor.execute("PRAGMA table_info(estudiante)")
    columns = cursor.fetchall()

    print("Columnas de la tabla estudiante:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")

    conn.close()

    # Verificar que NO existe id_carrera
    column_names = [col[1] for col in columns]

    if 'id_carrera' in column_names:
        print("\n❌ ERROR: El campo id_carrera todavía existe\n")
        return False

    if 'id_estudiante' in column_names and 'nombre' in column_names and 'correo' in column_names:
        print("\n✅ Estructura correcta: id_carrera eliminado exitosamente\n")
        return True
    else:
        print("\n❌ ERROR: Faltan campos esperados\n")
        return False


def main():
    """Función principal del script"""
    print_header("⚠️  ELIMINAR id_carrera DE TABLA estudiante")

    print("Este script eliminará el campo id_carrera de la tabla estudiante.")
    print("Las carreras de los estudiantes deben estar en la tabla estudiante_carrera.\n")

    # Verificar argumento --force
    force = '--force' in sys.argv

    # Verificar migración previa
    sin_carrera, total = verificar_migracion_previa()

    if sin_carrera is None:
        return 1

    if sin_carrera > 0 and not force:
        print("❌ No se puede continuar: hay estudiantes sin carrera asignada.")
        print("   Opciones:")
        print("   1. Ejecutar: python scripts/migrar_estudiante_carrera.py")
        print("   2. Usar --force para continuar de todas formas (no recomendado)\n")
        return 1

    # Solicitar confirmación
    if not force:
        print("⚠️  ADVERTENCIA: Esta operación es DESTRUCTIVA y NO REVERSIBLE")
        print("   Se recomienda tener un backup de la base de datos.\n")
        respuesta = input("¿Desea continuar? (escriba 'SI' para confirmar): ")

        if respuesta != 'SI':
            print("\n❌ Operación cancelada por el usuario\n")
            return 0

    # Crear backup
    print_header("💾 CREANDO BACKUP")
    backup_path = crear_backup()

    if not backup_path and not force:
        print("❌ No se pudo crear backup. Operación cancelada.")
        print("   Use --force para continuar sin backup (no recomendado)\n")
        return 1

    # Ejecutar migración
    if eliminar_campo_id_carrera():
        # Verificar resultado
        if verificar_estructura_final():
            print_header("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
            if backup_path:
                print(f"Backup disponible en: {backup_path}")
            print("\nLa tabla estudiante ya no tiene el campo id_carrera.")
            print("Use EstudianteCarreraService para gestionar las carreras.\n")
            return 0
        else:
            print_header("❌ ERROR EN VERIFICACIÓN")
            if backup_path:
                print(f"⚠️  Restaurar desde backup: {backup_path}\n")
            return 1
    else:
        print_header("❌ ERROR EN MIGRACIÓN")
        if backup_path:
            print(f"⚠️  Restaurar desde backup: {backup_path}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
