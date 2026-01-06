#!/usr/bin/env python3
"""
Script de prueba para el diálogo DialogoAdministrarEstudianteCarrera

Este script permite probar el diálogo de forma independiente sin necesidad
de ejecutar toda la aplicación.

Uso:
    python scripts/test_dialogo_estudiante_carrera.py
"""

import sys
import os

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def main():
    """Función principal del script de prueba"""

    # Crear ventana principal
    root = ttk.Window(
        title="Prueba - Diálogo Estudiante-Carrera",
        themename="darkly",
        size=(400, 300),
        position=(100, 100),
    )

    # Frame central
    frame = ttk.Frame(root, padding=20)
    frame.pack(fill=BOTH, expand=True)

    # Título
    ttk.Label(
        frame, text="Prueba del Diálogo", font=("Helvetica", 18, "bold"), bootstyle="info"
    ).pack(pady=20)

    # Label informativo
    ttk.Label(
        frame,
        text="Click en el botón para abrir el administrador\nde inscripciones estudiante-carrera",
        font=("Helvetica", 10),
        bootstyle="secondary",
        justify=CENTER,
    ).pack(pady=10)

    # Función para abrir el diálogo
    def abrir_dialogo():
        try:
            # Importar aquí para detectar errores
            from ui.ttk.dialogos import DialogoAdministrarEstudianteCarrera

            # Crear y mostrar el diálogo
            dialogo = DialogoAdministrarEstudianteCarrera(parent=root)
            dialogo.grab_set()  # Hacer modal
            root.wait_window(dialogo)  # Esperar cierre

            print("✅ Diálogo cerrado correctamente")

        except ImportError as e:
            print(f"❌ Error de importación: {e}")
            ttk.dialogs.Messagebox.show_error(
                "Error de Importación",
                f"No se pudo importar el diálogo:\n{str(e)}\n\n"
                "Asegúrate de que el controlador esté creado.",
            )
        except Exception as e:
            print(f"❌ Error al abrir diálogo: {e}")
            import traceback

            traceback.print_exc()
            ttk.dialogs.Messagebox.show_error("Error", f"Error al abrir el diálogo:\n{str(e)}")

    # Botón para abrir el diálogo
    btn_abrir = ttk.Button(
        frame,
        text="🎓 Abrir Administrador Estudiante-Carrera",
        command=abrir_dialogo,
        bootstyle="info",
        width=40,
    )
    btn_abrir.pack(pady=20)

    # Separador
    ttk.Separator(frame).pack(fill=X, pady=10)

    # Botón de salir
    ttk.Button(frame, text="Salir", command=root.quit, bootstyle="danger", width=40).pack(pady=5)

    # Información de versión
    ttk.Label(
        frame, text="Script de Prueba v1.0", font=("Helvetica", 8), bootstyle="secondary"
    ).pack(side=BOTTOM, pady=5)

    print("=" * 60)
    print("  Script de Prueba - Diálogo Estudiante-Carrera")
    print("=" * 60)
    print()
    print("📋 Instrucciones:")
    print("  1. Click en el botón para abrir el diálogo")
    print("  2. Prueba todas las funcionalidades")
    print("  3. Cierra el diálogo para volver aquí")
    print()
    print("⚠️  Nota: Si hay errores, verifica que el controlador")
    print("   ControlarAdministrarEstudianteCarrera esté creado.")
    print()
    print("=" * 60)

    # Iniciar aplicación
    root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error fatal: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
