from os.path import join
import os
import tempfile

NAME_APP = "cronosFacen"

# --- Rutas Base ---
RUTA_USUARIO = os.path.expanduser("~")

# --- Carpeta Temporal ---
DIRECTORIO_TEMPORAL = tempfile.gettempdir()

# --- Rutas de la Aplicación ---

# Directorio para archivos de configuración (ej. settings.ini).
# Sigue la especificación XDG para Linux.
# Ejemplo: /home/geran/.config/bibliotecaTK
RUTA_CONFIG = join(RUTA_USUARIO, ".config", NAME_APP)
LOGS_DIR = join(RUTA_USUARIO, ".config", NAME_APP)

# Directorio para archivos de datos del usuario (ej. la base de datos, portadas).
# Sigue la especificación XDG para Linux.
# Ejemplo: /home/geran/.local/share/bibliotecaTK
RUTA_DATA = join(RUTA_USUARIO, ".local", "share", NAME_APP)

# --- Rutas de los archivos ---#

# Archivo de configuración, para los datos de configuracion de la aplicacion
CONFIG_INI = join(RUTA_CONFIG, "settings.ini")

# Archivo de configuracion para la base de datos
RUTA_DB = join(RUTA_DATA, "cronosFacen.sqlite")
RUTA_DB_TEST = join(RUTA_DATA, "cronosFacen_test.sqlite")

# Obtenemos el nombre del sistema operativo
SISTEMA_OPERATIVO = os.name


def inicializar_directorios():
    """
    Asegura que los directorios de configuración y datos de la aplicación existan.
    Se debe llamar esta función al inicio de la aplicación.
    """
    os.makedirs(RUTA_CONFIG, exist_ok=True)
    os.makedirs(RUTA_DATA, exist_ok=True)
