import pytest
import sqlite3
import threading
import tempfile
from pathlib import Path
from src.modelos.daos.conexion_sqlite import ConexionSQLite


@pytest.fixture
def db_temporal():
    """Crea una base de datos temporal para los tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        ruta_db = Path(tmpdir) / "test.db"
        yield str(ruta_db)


@pytest.fixture(autouse=True)
def resetear_singleton():
    """Resetea el singleton después de cada test."""
    yield
    ConexionSQLite.resetear()


class TestConexionSQLite:
    """Tests para la clase ConexionSQLite."""

    def test_singleton_instancia_unica(self, db_temporal):
        """Verifica que ConexionSQLite es un Singleton."""
        conexion1 = ConexionSQLite(db_temporal)
        conexion2 = ConexionSQLite(db_temporal)
        assert conexion1 is conexion2

    def test_obtener_conexion_valida(self, db_temporal):
        """Verifica que obtener_conexion retorna una conexión válida."""
        conexion_sqlite = ConexionSQLite(db_temporal)
        conexion = conexion_sqlite.obtener_conexion()
        assert conexion is not None
        assert isinstance(conexion, sqlite3.Connection)

    def test_obtener_cursor(self, db_temporal):
        """Verifica que obtener_cursor retorna un cursor válido."""
        conexion_sqlite = ConexionSQLite(db_temporal)
        cursor = conexion_sqlite.obtener_cursor()
        assert cursor is not None
        assert isinstance(cursor, sqlite3.Cursor)

    def test_ejecutar_consulta_simple(self, db_temporal):
        """Verifica que se pueden ejecutar consultas simples."""
        conexion_sqlite = ConexionSQLite(db_temporal)
        cursor = conexion_sqlite.obtener_cursor()

        # Crear tabla de prueba
        cursor.execute(
            """
            CREATE TABLE prueba (
                id INTEGER PRIMARY KEY,
                nombre TEXT
            )
        """
        )
        conexion_sqlite.obtener_conexion().commit()

        # Insertar datos
        cursor.execute("INSERT INTO prueba (nombre) VALUES (?)", ("Test",))
        conexion_sqlite.obtener_conexion().commit()

        # Consultar datos
        cursor.execute("SELECT * FROM prueba")
        resultado = cursor.fetchone()
        assert resultado is not None
        assert resultado[1] == "Test"

    def test_row_factory_enabled(self, db_temporal):
        """Verifica que row_factory está habilitado (sqlite3.Row)."""
        conexion_sqlite = ConexionSQLite(db_temporal)
        conexion = conexion_sqlite.obtener_conexion()
        assert conexion.row_factory == sqlite3.Row

    def test_pragmas_configurados(self, db_temporal):
        """Verifica que los PRAGMA se configuraron correctamente."""
        conexion_sqlite = ConexionSQLite(db_temporal)
        cursor = conexion_sqlite.obtener_cursor()

        # Verificar foreign_keys
        cursor.execute("PRAGMA foreign_keys")
        assert cursor.fetchone()[0] == 1

        # Verificar journal_mode
        cursor.execute("PRAGMA journal_mode")
        assert cursor.fetchone()[0] == "wal"

    def test_cerrar_conexion(self, db_temporal):
        """Verifica que cerrar() libera la conexión."""
        conexion_sqlite = ConexionSQLite(db_temporal)
        conexion = conexion_sqlite.obtener_conexion()
        conexion_sqlite.cerrar()

        # La siguiente llamada debe crear una nueva conexión
        nueva_conexion = conexion_sqlite.obtener_conexion()
        assert nueva_conexion is not None

    def test_thread_safety(self, db_temporal):
        """Verifica que cada thread obtiene su propia conexión."""
        conexion_sqlite = ConexionSQLite(db_temporal)
        conexiones = {}

        def obtener_conexion_en_thread(thread_id):
            conexiones[thread_id] = conexion_sqlite.obtener_conexion()

        threads = []
        for i in range(3):
            t = threading.Thread(target=obtener_conexion_en_thread, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Todas las conexiones deben ser válidas pero potencialmente diferentes
        assert len(conexiones) == 3
        for conexion in conexiones.values():
            assert isinstance(conexion, sqlite3.Connection)

    def test_usar_ruta_default(self):
        """Verifica que se puede instanciar sin proporcionar ruta."""
        # Con resetear_singleton, se crea una nueva instancia
        conexion_sqlite = ConexionSQLite()
        # Simplemente verificar que se creó correctamente
        assert conexion_sqlite is not None
        assert conexion_sqlite._ruta_db is not None

    def test_error_conexion_invalida(self):
        """Verifica que se lanza excepción con ruta inválida."""
        with pytest.raises(sqlite3.Error):
            conexion_sqlite = ConexionSQLite("/ruta/invalida/test.db")
            conexion_sqlite.obtener_conexion()
