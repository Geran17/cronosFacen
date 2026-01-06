#!/usr/bin/env python3
"""
Script ejecutable para crear indices en la base de datos.

Uso:
    python setup_indices.py
"""

import sys
import os

# Agregar el directorio padre al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.utilidades.config import inicializar_directorios, RUTA_DB
from src.scripts.crear_indices import crear_todos_los_indices, verificar_indices

if __name__ == "__main__":
    inicializar_directorios()

    print("\n" + "=" * 70)
    print("🗄️  CONFIGURADOR DE ÍNDICES - MVP ORGANIZACIÓN ACADÉMICA")
    print("=" * 70)
    print(f"\n📍 Base de datos: {RUTA_DB}\n")

    if crear_todos_los_indices():
        print("\n✅ Índices creados correctamente\n")

        # Mostrar resumen
        indices = verificar_indices()
        total = sum(len(v) for v in indices.values())
        print(f"📊 Total de índices: {total}")
        print(f"📊 Tablas indexadas: {len(indices)}")
        print("\nDetalle:")
        for tabla, lista_indices in sorted(indices.items()):
            print(f"  • {tabla}: {len(lista_indices)} índice(s)")

        print("\n" + "=" * 70 + "\n")
    else:
        print("\n❌ Error: No se pudieron crear los índices\n")
        sys.exit(1)
