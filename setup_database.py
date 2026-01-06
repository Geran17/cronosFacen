#!/usr/bin/env python3
"""
Script de configuración completa de la base de datos.

Crea en orden:
1. Tablas (via DAOs)
2. Índices
3. VIEWS

Uso:
    python setup_database.py
"""

import sys
import os

# Agregar src al path para las importaciones
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from utilidades.config import inicializar_directorios, RUTA_DB
from scripts.crear_indices import crear_todos_los_indices, verificar_indices
from scripts.crear_views import crear_todas_las_views, verificar_views


def print_header(titulo):
    """Imprime encabezado formateado"""
    print(f"\n{'='*75}")
    print(f"  {titulo}")
    print(f"{'='*75}\n")


def main():
    inicializar_directorios()

    print_header("🗄️  CONFIGURACIÓN COMPLETA DE BASE DE DATOS - MVP")
    print(f"📍 Base de datos: {RUTA_DB}\n")

    # Paso 1: Índices
    print("1️⃣  Creando índices...")
    if crear_todos_los_indices():
        indices = verificar_indices()
        print(f"   ✅ {len(indices)} tablas indexadas\n")
    else:
        print("   ❌ Error en índices\n")
        return False

    # Paso 2: VIEWS
    print("2️⃣  Creando VIEWS...")
    if crear_todas_las_views():
        views = verificar_views()
        print(f"   ✅ {len(views)} VIEWS creadas\n")
    else:
        print("   ❌ Error en VIEWS\n")
        return False

    # Resumen final
    print_header("✅ CONFIGURACIÓN COMPLETADA")
    print(f"📊 Índices: {len(indices)} en {len(indices)} tablas")
    print(f"📊 VIEWS: {len(views)} creadas")
    print(f"📍 Base de datos lista: {RUTA_DB}\n")

    return True


if __name__ == "__main__":
    if main():
        print("=" * 75 + "\n")
        sys.exit(0)
    else:
        print("\n❌ Error en configuración\n")
        sys.exit(1)
