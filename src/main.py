import sys
import os

# Agregar el directorio src al path para importaciones relativas
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utilidades.config import inicializar_directorios
from scripts.crear_indices import crear_todos_los_indices
from scripts.crear_views import crear_todas_las_views
from ui.ttk.appTTK import AppTTK


def main():
    """Función principal del programa."""
    # inicializamos los directorios de configuraciones
    inicializar_directorios()

    # creamos los índices recomendados en la base de datos
    crear_todos_los_indices()

    # creamos las VIEWS recomendadas en la base de datos
    crear_todas_las_views()

    # lazamos la ventana de la aplicacion
    app_ttk = AppTTK()
    app_ttk.mainloop()


if __name__ == "__main__":
    main()
