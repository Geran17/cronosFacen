import pytest
import os
import sqlite3
import uuid
from pathlib import Path
from src.modelos.daos.asignatura_dao import AsignaturaDAO
from src.modelos.daos.carrera_dao import CarreraDAO
from src.modelos.dtos.asignatura_dto import AsignaturaDTO
from src.modelos.dtos.carrera_dto import CarreraDTO


def get_unique():
    """Genera un sufijo único para evitar conflictos UNIQUE"""
    return str(uuid.uuid4())[:8]


@pytest.fixture
def db_path(tmp_path):
    """Crea una ruta temporal para la base de datos de prueba."""
    db_file = tmp_path / "test_asignatura.db"
    yield str(db_file)
    # Cleanup
    if db_file.exists():
        db_file.unlink()


@pytest.fixture
def carrera_dao(db_path):
    """Crea una instancia del CarreraDAO con base de datos temporal."""
    dao = CarreraDAO(ruta_db=db_path)
    dao.crear_tabla()
    yield dao


@pytest.fixture
def asignatura_dao(db_path):
    """Crea una instancia del AsignaturaDAO con base de datos temporal."""
    # Asegurar que la tabla de carrera existe primero
    carrera_dao_temp = CarreraDAO(ruta_db=db_path)
    carrera_dao_temp.crear_tabla()

    dao = AsignaturaDAO(ruta_db=db_path)
    dao.crear_tabla()
    yield dao


@pytest.fixture
def carrera_fixture(carrera_dao):
    """Crea una carrera de prueba."""
    carrera = CarreraDTO(nombre="Ingeniería", plan="Plan2023", modalidad="Presencial")
    id_carrera = carrera_dao.insertar(carrera)
    return id_carrera


class TestAsignaturaDAO:
    """Suite de pruebas para la clase AsignaturaDAO."""

    def test_crear_tabla(self, asignatura_dao):
        """Verifica que la tabla se crea correctamente."""
        with asignatura_dao.get_conexion() as con:
            cursor = con.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='asignatura'"
            )
            resultado = cursor.fetchone()
            assert resultado is not None, "La tabla 'asignatura' no fue creada"

    def test_insertar(self, asignatura_dao, carrera_fixture):
        """Verifica que se inserta correctamente un registro de asignatura."""
        uid = get_unique()
        asignatura_dto = AsignaturaDTO(
            nombre=f"Sistemas-{uid}",
            codigo=f"SIS{uid[:3]}",
            creditos=3,
            tipo="obligatoria",
            id_carrera=carrera_fixture,
        )

        id_insertado = asignatura_dao.insertar(asignatura_dto)

        assert id_insertado is not None, "No se obtuvo ID después de insertar"
        assert id_insertado > 0, "El ID insertado debe ser mayor a 0"

    def test_insertar_multiples(self, asignatura_dao, carrera_fixture):
        """Verifica que se pueden insertar múltiples registros."""
        u1, u2, u3 = get_unique(), get_unique(), get_unique()
        asignaturas = [
            AsignaturaDTO(
                nombre=f"Sistemas-{u1}",
                codigo=f"SIS{u1[:3]}",
                creditos=3,
                tipo="obligatoria",
                id_carrera=carrera_fixture,
            ),
            AsignaturaDTO(
                nombre=f"Bases-{u2}",
                codigo=f"BAS{u2[:3]}",
                creditos=4,
                tipo="obligatoria",
                id_carrera=carrera_fixture,
            ),
            AsignaturaDTO(
                nombre=f"Redes-{u3}",
                codigo=f"RED{u3[:3]}",
                creditos=3,
                tipo="electiva",
                id_carrera=carrera_fixture,
            ),
        ]

        ids = [asignatura_dao.insertar(asig) for asig in asignaturas]

        assert all(id is not None for id in ids), "Todos los IDs deben ser válidos"
        assert len(ids) == 3, "Debe insertar 3 registros"

    def test_instanciar_existente(self, asignatura_dao, carrera_fixture):
        """Verifica que se instancia correctamente una asignatura existente."""
        uid = get_unique()
        asignatura_original = AsignaturaDTO(
            nombre=f"Sistemas-{uid}",
            codigo=f"SIS{uid[:3]}",
            creditos=3,
            tipo="obligatoria",
            id_carrera=carrera_fixture,
        )
        id_creado = asignatura_dao.insertar(asignatura_original)

        asignatura_recuperada = AsignaturaDTO(id_asignatura=id_creado)
        resultado = asignatura_dao.instanciar(asignatura_recuperada)

        assert resultado is True, "Debería encontrar la asignatura"
        assert (
            asignatura_recuperada.nombre == asignatura_original.nombre
        ), "El nombre debe coincidir"

    def test_instanciar_inexistente(self, asignatura_dao):
        """Verifica que no se instancia un ID que no existe."""
        asignatura_inexistente = AsignaturaDTO(id_asignatura=999)
        resultado = asignatura_dao.instanciar(asignatura_inexistente)

        assert resultado is False, "No debería encontrar una asignatura inexistente"

    def test_instanciar_id_invalido(self, asignatura_dao):
        """Verifica el manejo de ID inválido."""
        asignatura_invalida = AsignaturaDTO(id_asignatura=None)
        resultado = asignatura_dao.instanciar(asignatura_invalida)

        assert resultado is False, "No debería instanciar con ID None"

    def test_existe_verdadero(self, asignatura_dao, carrera_fixture):
        """Verifica que existe() retorna True para un registro insertado."""
        uid = get_unique()
        asignatura_original = AsignaturaDTO(
            nombre=f"Sistemas-{uid}",
            codigo=f"SIS{uid[:3]}",
            creditos=3,
            tipo="obligatoria",
            id_carrera=carrera_fixture,
        )
        id_creado = asignatura_dao.insertar(asignatura_original)

        asignatura_verificar = AsignaturaDTO(id_asignatura=id_creado)
        existe = asignatura_dao.existe(asignatura_verificar)

        assert existe is True, "Debería confirmar que la asignatura existe"

    def test_existe_falso(self, asignatura_dao):
        """Verifica que existe() retorna False para un ID inexistente."""
        asignatura_no_existe = AsignaturaDTO(id_asignatura=999)
        existe = asignatura_dao.existe(asignatura_no_existe)

        assert existe is False, "No debería encontrar una asignatura inexistente"

    def test_existe_id_invalido(self, asignatura_dao):
        """Verifica el manejo de ID inválido en existe()."""
        asignatura_invalida = AsignaturaDTO(id_asignatura=None)
        existe = asignatura_dao.existe(asignatura_invalida)

        assert existe is False, "No debería confirmar existencia con ID None"

    def test_eliminar(self, asignatura_dao, carrera_fixture):
        """Verifica que se elimina correctamente un registro."""
        uid = get_unique()
        asignatura_original = AsignaturaDTO(
            nombre=f"Sistemas-{uid}",
            codigo=f"SIS{uid[:3]}",
            creditos=3,
            tipo="obligatoria",
            id_carrera=carrera_fixture,
        )
        id_creado = asignatura_dao.insertar(asignatura_original)

        asignatura_verificar = AsignaturaDTO(id_asignatura=id_creado)
        assert asignatura_dao.existe(asignatura_verificar) is True

        resultado_eliminacion = asignatura_dao.eliminar(asignatura_verificar)
        assert resultado_eliminacion is True, "La eliminación debe retornar True"
        assert (
            asignatura_dao.existe(asignatura_verificar) is False
        ), "El registro debe estar eliminado"

    def test_eliminar_inexistente(self, asignatura_dao):
        """Verifica que eliminar un registro inexistente retorna False."""
        asignatura_no_existe = AsignaturaDTO(id_asignatura=999)
        resultado = asignatura_dao.eliminar(asignatura_no_existe)

        assert resultado is False, "No debe eliminar un registro inexistente"

    def test_ciclo_completo(self, asignatura_dao, carrera_fixture):
        """Verifica un ciclo completo: crear, instanciar, modificar, eliminar."""
        uid = get_unique()
        # 1. Crear
        asignatura_original = AsignaturaDTO(
            nombre=f"Sistemas-{uid}",
            codigo=f"SIS{uid[:3]}",
            creditos=3,
            tipo="obligatoria",
            id_carrera=carrera_fixture,
        )
        id_creado = asignatura_dao.insertar(asignatura_original)
        assert id_creado is not None

        # 2. Instanciar
        asignatura_recuperada = AsignaturaDTO(id_asignatura=id_creado)
        assert asignatura_dao.instanciar(asignatura_recuperada) is True
        assert asignatura_recuperada.nombre == asignatura_original.nombre

        # 3. Verificar existencia
        assert asignatura_dao.existe(asignatura_recuperada) is True

        # 4. Eliminar
        assert asignatura_dao.eliminar(asignatura_recuperada) is True
        assert asignatura_dao.existe(asignatura_recuperada) is False
