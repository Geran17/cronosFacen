#!/usr/bin/env python3
"""
Script ejecutable para crear VIEWS en la base de datos.

Uso:
    python setup_views.py
"""

import sys
import os

# Agregar el directorio padre al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.utilidades.config import inicializar_directorios, RUTA_DB
from src.scripts.crear_views import crear_todas_las_views, verificar_views, listar_columnas_view

if __name__ == "__main__":
    inicializar_directorios()

    print("\n" + "=" * 75)
    print("📊 CONFIGURADOR DE VIEWS - MVP ORGANIZACIÓN ACADÉMICA")
    print("=" * 75)
    print(f"\n📍 Base de datos: {RUTA_DB}\n")

    if crear_todas_las_views():
        print("\n✅ VIEWS creadas correctamente\n")

        # Mostrar resumen
        views = verificar_views()
        total = len(views)
        print(f"📊 Total de VIEWS: {total}")
        print(f"📊 Categorías:\n")

        # Categorizar views
        categorias = {
            "Progreso": [
                v for v in views.keys() if "progreso" in v or "resumen" in v or "academico" in v
            ],
            "Asignaturas": [v for v in views.keys() if "asignatura" in v],
            "Actividades": [v for v in views.keys() if "actividad" in v or "semana" in v],
            "Calendario": [v for v in views.keys() if "calendario" in v],
            "Dashboard": [v for v in views.keys() if "dashboard" in v],
            "Estudiante": [v for v in views.keys() if "estudiante" in v],
        }

        for categoria, lista_views in categorias.items():
            if lista_views:
                print(f"  {categoria}:")
                for vista in lista_views:
                    cols = len(listar_columnas_view(vista))
                    print(f"    • {vista} ({cols} columnas)")

        print("\n" + "=" * 75 + "\n")
    else:
        print("\n❌ Error: No se pudieron crear las VIEWS\n")
        sys.exit(1)
