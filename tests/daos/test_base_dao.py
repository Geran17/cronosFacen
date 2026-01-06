import pytest
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from src.modelos.daos.base_dao import DAO
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


class ConcreteDAO(DAO):
    """Implementación concreta de DAO para pruebas."""

    def crear_tabla(self):
        sql = """
        CREATE TABLE IF NOT EXISTS test_table (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            valor INTEGER
        )
        """
        with self.get_conexion() as con:
            cursor = con.cursor()
            cursor.execute(sql)
            con.commit()

    def insertar(self, sql: str, params: tuple = ()):
        return self.ejecutar_insertar(sql, params)

    def eliminar(self, sql: str, params: tuple = ()):
        return self.ejecutar_actualizacion(sql, params)

    def instanciar(self, sql: str, params: tuple = ()):
        return self.ejecutar_consulta(sql, params)

    def existe(self, sql: str, params: tuple = ()):
        resultado = self.ejecutar_consulta(sql, params)
        return len(resultado) > 0


class TestDAOInit:
    """Tests para la inicialización del DAO."""

    def test_init_con_ruta_db(self):
        """Verifica que el DAO se inicializa con ruta de BD."""
        dao = ConcreteDAO(ruta_db="/ruta/test.db")
        assert dao.ruta_db == "/ruta/test.db"

    def test_init_sin_ruta_db(self):
        """Verifica que el DAO se inicializa sin ruta (None)."""
        dao = ConcreteDAO()
        assert dao.ruta_db is None


class TestDAOEjecutarInsertar:
    """Tests para ejecutar_insertar."""

    def test_insertar_exitoso(self, db_temporal):
        """Verifica que la inserción es exitosa."""
        dao = ConcreteDAO(ruta_db=db_temporal)
        dao.crear_tabla()

        sql = "INSERT INTO test_table (nombre, valor) VALUES (?, ?)"
        resultado = dao.ejecutar_insertar(sql, ("test", 42))

        assert resultado is not None
        assert resultado == 1

    def test_insertar_multiple(self, db_temporal):
        """Verifica que se pueden insertar múltiples registros."""
        dao = ConcreteDAO(ruta_db=db_temporal)
        dao.crear_tabla()

        sql = "INSERT INTO test_table (nombre, valor) VALUES (?, ?)"

        id1 = dao.ejecutar_insertar(sql, ("registro1", 10))
        id2 = dao.ejecutar_insertar(sql, ("registro2", 20))

        assert id1 is not None
        assert id2 is not None
        assert id1 < id2

    def test_insertar_con_parametros_vacios(self, db_temporal):
        """Verifica inserción sin parámetros."""
        dao = ConcreteDAO(ruta_db=db_temporal)
        dao.crear_tabla()

        sql = "INSERT INTO test_table (nombre, valor) VALUES ('default', 0)"
        resultado = dao.ejecutar_insertar(sql)

        assert resultado is not None


class TestDAOEjecutarConsulta:
    """Tests para ejecutar_consulta."""

    def test_consulta_exitosa(self, db_temporal):
        """Verifica que las consultas retornan resultados correctos."""
        dao = ConcreteDAO(ruta_db=db_temporal)
        dao.crear_tabla()

        # Insertar datos
        dao.ejecutar_insertar(
            "INSERT INTO test_table (nombre, valor) VALUES (?, ?)", ("test1", 100)
        )

        # Consultar
        sql = "SELECT * FROM test_table WHERE nombre = ?"
        resultado = dao.ejecutar_consulta(sql, ("test1",))

        assert len(resultado) == 1
        assert resultado[0]["nombre"] == "test1"
        assert resultado[0]["valor"] == 100

    def test_consulta_vacia(self, db_temporal):
        """Verifica que consultas sin resultados retornan lista vacía."""
        dao = ConcreteDAO(ruta_db=db_temporal)
        dao.crear_tabla()

        sql = "SELECT * FROM test_table WHERE nombre = ?"
        resultado = dao.ejecutar_consulta(sql, ("inexistente",))

        assert resultado == []

    def test_consulta_multiples_resultados(self, db_temporal):
        """Verifica consultas con múltiples resultados."""
        dao = ConcreteDAO(ruta_db=db_temporal)
        dao.crear_tabla()

        # Insertar múltiples registros
        dao.ejecutar_insertar("INSERT INTO test_table (nombre, valor) VALUES (?, ?)", ("tipo1", 10))
        dao.ejecutar_insertar("INSERT INTO test_table (nombre, valor) VALUES (?, ?)", ("tipo1", 20))
        dao.ejecutar_insertar("INSERT INTO test_table (nombre, valor) VALUES (?, ?)", ("tipo2", 30))

        sql = "SELECT * FROM test_table WHERE nombre = ?"
        resultado = dao.ejecutar_consulta(sql, ("tipo1",))

        assert len(resultado) == 2
        assert all(r["nombre"] == "tipo1" for r in resultado)

    def test_consulta_retorna_diccionarios(self, db_temporal):
        """Verifica que los resultados son diccionarios."""
        dao = ConcreteDAO(ruta_db=db_temporal)
        dao.crear_tabla()

        dao.ejecutar_insertar("INSERT INTO test_table (nombre, valor) VALUES (?, ?)", ("test", 50))

        resultado = dao.ejecutar_consulta("SELECT * FROM test_table")

        assert len(resultado) == 1
        assert isinstance(resultado[0], dict)
        assert "nombre" in resultado[0]
        assert "valor" in resultado[0]


class TestDAOEjecutarActualizacion:
    """Tests para ejecutar_actualizacion."""

    def test_actualizacion_exitosa(self, db_temporal):
        """Verifica que la actualización es exitosa."""
        dao = ConcreteDAO(ruta_db=db_temporal)
        dao.crear_tabla()

        # Insertar
        dao.ejecutar_insertar("INSERT INTO test_table (nombre, valor) VALUES (?, ?)", ("test", 10))

        # Actualizar
        sql = "UPDATE test_table SET valor = ? WHERE nombre = ?"
        resultado = dao.ejecutar_actualizacion(sql, (99, "test"))

        assert resultado is True

    def test_actualizacion_sin_registros_afectados(self, db_temporal):
        """Verifica actualización sin registros afectados."""
        dao = ConcreteDAO(ruta_db=db_temporal)
        dao.crear_tabla()

        sql = "UPDATE test_table SET valor = ? WHERE nombre = ?"
        resultado = dao.ejecutar_actualizacion(sql, (99, "inexistente"))

        assert resultado is False

    def test_eliminacion_exitosa(self, db_temporal):
        """Verifica que la eliminación es exitosa."""
        dao = ConcreteDAO(ruta_db=db_temporal)
        dao.crear_tabla()

        dao.ejecutar_insertar("INSERT INTO test_table (nombre, valor) VALUES (?, ?)", ("test", 10))

        sql = "DELETE FROM test_table WHERE nombre = ?"
        resultado = dao.ejecutar_actualizacion(sql, ("test",))

        assert resultado is True


class TestDAOGetConexion:
    """Tests para get_conexion."""

    def test_get_conexion_context_manager(self, db_temporal):
        """Verifica que get_conexion funciona como context manager."""
        dao = ConcreteDAO(ruta_db=db_temporal)

        with dao.get_conexion() as con:
            assert con is not None
            assert isinstance(con, sqlite3.Connection)

    def test_get_conexion_multiple_contextos(self, db_temporal):
        """Verifica múltiples contextos de conexión."""
        dao = ConcreteDAO(ruta_db=db_temporal)

        with dao.get_conexion() as con1:
            con1_id = id(con1)

        with dao.get_conexion() as con2:
            con2_id = id(con2)

        # Las conexiones pueden ser diferentes instancias
        assert con1_id is not None
        assert con2_id is not None


class TestDAOAbstractMethods:
    """Tests para métodos abstractos."""

    def test_no_se_puede_instanciar_dao_directamente(self):
        """Verifica que DAO es abstracta y no puede instanciarse."""
        with pytest.raises(TypeError):
            DAO()

    def test_dao_concreto_debe_implementar_metodos_abstractos(self):
        """Verifica que las subclases deben implementar métodos abstractos."""

        class DAOIncompleto(DAO):
            def crear_tabla(self):
                pass

            def insertar(self, sql, params=()):
                pass

            def eliminar(self, sql, params=()):
                pass

            # Faltan instanciar y existe

        with pytest.raises(TypeError):
            DAOIncompleto()


class TestDAOIntegracion:
    """Tests de integración del DAO."""

    def test_flujo_completo_crud(self, db_temporal):
        """Verifica un flujo completo CRUD."""
        dao = ConcreteDAO(ruta_db=db_temporal)
        dao.crear_tabla()

        # CREATE
        id_insertado = dao.insertar(
            "INSERT INTO test_table (nombre, valor) VALUES (?, ?)", ("producto", 100)
        )
        assert id_insertado is not None

        # READ
        registros = dao.instanciar("SELECT * FROM test_table WHERE id = ?", (id_insertado,))
        assert len(registros) == 1
        assert registros[0]["nombre"] == "producto"

        # UPDATE
        actualizado = dao.ejecutar_actualizacion(
            "UPDATE test_table SET valor = ? WHERE id = ?", (200, id_insertado)
        )
        assert actualizado is True

        # Verificar actualización
        registros_actualizados = dao.instanciar(
            "SELECT * FROM test_table WHERE id = ?", (id_insertado,)
        )
        assert registros_actualizados[0]["valor"] == 200

        # DELETE
        eliminado = dao.eliminar("DELETE FROM test_table WHERE id = ?", (id_insertado,))
        assert eliminado is True

        # Verificar eliminación
        registros_finales = dao.instanciar("SELECT * FROM test_table WHERE id = ?", (id_insertado,))
        assert len(registros_finales) == 0

    def test_existe_metodo(self, db_temporal):
        """Verifica el método existe."""
        dao = ConcreteDAO(ruta_db=db_temporal)
        dao.crear_tabla()

        # Registra no existe
        existe = dao.existe("SELECT * FROM test_table WHERE nombre = ?", ("inexistente",))
        assert existe is False

        # Insertar registro
        dao.ejecutar_insertar(
            "INSERT INTO test_table (nombre, valor) VALUES (?, ?)", ("existente", 50)
        )

        # Registro existe
        existe = dao.existe("SELECT * FROM test_table WHERE nombre = ?", ("existente",))
        assert existe is True
