import sqlite3
import threading
from sqlite3 import Connection, Cursor
from utilidades.config import RUTA_DB
from os.path import join


class ConexionSQLite:
    """
    Clase Singleton thread-safe para gestionar conexiones SQLite.
    Cada thread obtiene su propia conexión.
    """

    _instancia = None
    _lock = threading.Lock()
    _local = threading.local()  # Almacenamiento local por thread

    def __new__(cls, ruta_db: str = None):
        if cls._instancia is None:
            with cls._lock:
                if cls._instancia is None:
                    cls._instancia = super().__new__(cls)
                    cls._instancia._ruta_db = None
        return cls._instancia

    def __init__(self, ruta_db: str = None):
        """
        Inicializa la ruta de la base de datos.
        La conexión se crea por thread según sea necesario.
        """
        if ruta_db is None:
            ruta_db = RUTA_DB

        # Guardamos la ruta para crear conexiones en cada thread
        if self._ruta_db is None:
            self._ruta_db = ruta_db

    def _obtener_conexion_thread(self) -> Connection:
        if not hasattr(self._local, 'conexion') or self._local.conexion is None:
            try:
                self._local.conexion = sqlite3.connect(
                    self._ruta_db,
                    check_same_thread=False,
                    timeout=10.0,  # Espera 10 segundos si hay lock
                )
                self._local.conexion.row_factory = sqlite3.Row

                # Optimizaciones de rendimiento
                self._local.conexion.execute("PRAGMA foreign_keys = ON")
                self._local.conexion.execute("PRAGMA journal_mode = WAL")  # Write-Ahead Logging
                self._local.conexion.execute("PRAGMA synchronous = NORMAL")
                self._local.conexion.execute("PRAGMA cache_size = -64000")  # 64MB cache
                self._local.conexion.execute("PRAGMA temp_store = MEMORY")

            except sqlite3.Error as err:
                print(f"Error al conectar: {err}")
                self._local.conexion = None
                raise
        else:
            # Verificar que la conexión sigue siendo válida
            try:
                self._local.conexion.execute("SELECT 1")
            except sqlite3.Error:
                # Si la conexión está cerrada, crear una nueva
                self._local.conexion = None
                return self._obtener_conexion_thread()

        return self._local.conexion

    def obtener_conexion(self) -> Connection:
        """
        Retorna la conexión de la base de datos para el thread actual.
        """
        conexion = self._obtener_conexion_thread()
        if conexion is None:
            raise RuntimeError("No hay conexión a la base de datos establecida")
        return conexion

    def obtener_cursor(self) -> Cursor:
        """
        Retorna un cursor para ejecutar consultas en el thread actual.
        """
        return self.obtener_conexion().cursor()

    def cerrar(self):
        """
        Cierra la conexión del thread actual.
        """
        if hasattr(self._local, 'conexion') and self._local.conexion is not None:
            self._local.conexion.close()
            self._local.conexion = None

    @classmethod
    def cerrar_todas(cls):
        """
        Cierra todas las conexiones (útil al finalizar la aplicación).
        Nota: Solo cierra la conexión del thread actual ya que no podemos
        acceder a las conexiones de otros threads.
        """
        if cls._instancia is not None:
            cls._instancia.cerrar()

    @classmethod
    def resetear(cls):
        """
        Resetea el Singleton (útil principalmente para tests).
        Cierra la conexión del thread actual y reinicia las variables de clase.
        """
        if cls._instancia is not None:
            cls._instancia.cerrar()

        with cls._lock:
            cls._instancia = None
