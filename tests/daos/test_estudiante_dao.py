import pytest
import os
import sqlite3
import uuid
from pathlib import Path
from src.modelos.daos.estudiante_dao import EstudianteDAO
from src.modelos.daos.carrera_dao import CarreraDAO
from src.modelos.dtos.estudiante_dto import EstudianteDTO
from src.modelos.dtos.carrera_dto import CarreraDTO


def get_unique():
    """Genera un sufijo único para evitar conflictos UNIQUE"""
    return str(uuid.uuid4())[:8]


@pytest.fixture
def db_path(tmp_path):
    """Crea una ruta temporal para la base de datos de prueba."""
    db_file = tmp_path / "test_estudiante.db"
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
def estudiante_dao(db_path):
    """Crea una instancia del EstudianteDAO con base de datos temporal."""
    # Asegurar que la tabla de carrera existe primero
    carrera_dao_temp = CarreraDAO(ruta_db=db_path)
    carrera_dao_temp.crear_tabla()

    dao = EstudianteDAO(ruta_db=db_path)
    dao.crear_tabla()
    yield dao


@pytest.fixture
def carrera_fixture(carrera_dao):
    """Crea una carrera de prueba."""
    carrera = CarreraDTO(nombre="Ingeniería", plan="Plan2023", modalidad="Presencial")
    id_carrera = carrera_dao.insertar(carrera)
    return id_carrera


class TestEstudianteDAO:
    """Suite de pruebas para la clase EstudianteDAO."""

    def test_crear_tabla(self, estudiante_dao):
        """Verifica que la tabla se crea correctamente."""
        with estudiante_dao.get_conexion() as con:
            cursor = con.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='estudiante'"
            )
            resultado = cursor.fetchone()
            assert resultado is not None, "La tabla 'estudiante' no fue creada"

    def test_insertar(self, estudiante_dao, carrera_fixture):
        """Verifica que se inserta correctamente un registro de estudiante."""
        uid = get_unique()
        estudiante_dto = EstudianteDTO(
            nombre=f"Juan-{uid}",
            correo=f"juan{uid}@universidad.edu",
            id_carrera=carrera_fixture,
        )

        id_insertado = estudiante_dao.insertar(estudiante_dto)

        assert id_insertado is not None, "No se obtuvo ID después de insertar"
        assert id_insertado > 0, "El ID insertado debe ser mayor a 0"

    def test_insertar_multiples(self, estudiante_dao, carrera_fixture):
        """Verifica que se pueden insertar múltiples registros."""
        u1, u2, u3 = get_unique(), get_unique(), get_unique()
        estudiantes = [
            EstudianteDTO(
                nombre=f"Juan-{u1}", correo=f"juan{u1}@universidad.edu", id_carrera=carrera_fixture
            ),
            EstudianteDTO(
                nombre=f"Maria-{u2}",
                correo=f"maria{u2}@universidad.edu",
                id_carrera=carrera_fixture,
            ),
            EstudianteDTO(
                nombre=f"Carlos-{u3}",
                correo=f"carlos{u3}@universidad.edu",
                id_carrera=carrera_fixture,
            ),
        ]

        ids = [estudiante_dao.insertar(est) for est in estudiantes]

        assert all(id is not None for id in ids), "Todos los IDs deben ser válidos"
        assert len(ids) == 3, "Debe insertar 3 registros"

    def test_instanciar_existente(self, estudiante_dao, carrera_fixture):
        """Verifica que se instancia correctamente un estudiante existente."""
        uid = get_unique()
        estudiante_original = EstudianteDTO(
            nombre=f"Juan-{uid}",
            correo=f"juan{uid}@universidad.edu",
            id_carrera=carrera_fixture,
        )
        id_creado = estudiante_dao.insertar(estudiante_original)

        estudiante_recuperado = EstudianteDTO(id_estudiante=id_creado)
        resultado = estudiante_dao.instanciar(estudiante_recuperado)

        assert resultado is True, "Debería encontrar el estudiante"
        assert (
            estudiante_recuperado.nombre == estudiante_original.nombre
        ), "El nombre debe coincidir"

    def test_instanciar_inexistente(self, estudiante_dao):
        """Verifica que no se instancia un ID que no existe."""
        estudiante_inexistente = EstudianteDTO(id_estudiante=999)
        resultado = estudiante_dao.instanciar(estudiante_inexistente)

        assert resultado is False, "No debería encontrar un estudiante inexistente"

    def test_instanciar_id_invalido(self, estudiante_dao):
        """Verifica el manejo de ID inválido."""
        estudiante_invalido = EstudianteDTO(id_estudiante=None)
        resultado = estudiante_dao.instanciar(estudiante_invalido)

        assert resultado is False, "No debería instanciar con ID None"

    def test_existe_verdadero(self, estudiante_dao, carrera_fixture):
        """Verifica que existe() retorna True para un registro insertado."""
        uid = get_unique()
        estudiante_original = EstudianteDTO(
            nombre=f"Juan-{uid}",
            correo=f"juan{uid}@universidad.edu",
            id_carrera=carrera_fixture,
        )
        id_creado = estudiante_dao.insertar(estudiante_original)

        estudiante_verificar = EstudianteDTO(id_estudiante=id_creado)
        existe = estudiante_dao.existe(estudiante_verificar)

        assert existe is True, "Debería confirmar que el estudiante existe"

    def test_existe_falso(self, estudiante_dao):
        """Verifica que existe() retorna False para un ID inexistente."""
        estudiante_no_existe = EstudianteDTO(id_estudiante=999)
        existe = estudiante_dao.existe(estudiante_no_existe)

        assert existe is False, "No debería encontrar un estudiante inexistente"

    def test_existe_id_invalido(self, estudiante_dao):
        """Verifica el manejo de ID inválido en existe()."""
        estudiante_invalido = EstudianteDTO(id_estudiante=None)
        existe = estudiante_dao.existe(estudiante_invalido)

        assert existe is False, "No debería confirmar existencia con ID None"

    def test_eliminar(self, estudiante_dao, carrera_fixture):
        """Verifica que se elimina correctamente un registro."""
        uid = get_unique()
        estudiante_original = EstudianteDTO(
            nombre=f"Juan-{uid}",
            correo=f"juan{uid}@universidad.edu",
            id_carrera=carrera_fixture,
        )
        id_creado = estudiante_dao.insertar(estudiante_original)

        estudiante_verificar = EstudianteDTO(id_estudiante=id_creado)
        assert estudiante_dao.existe(estudiante_verificar) is True

        resultado_eliminacion = estudiante_dao.eliminar(estudiante_verificar)
        assert resultado_eliminacion is True, "La eliminación debe retornar True"
        assert (
            estudiante_dao.existe(estudiante_verificar) is False
        ), "El registro debe estar eliminado"

    def test_eliminar_inexistente(self, estudiante_dao):
        """Verifica que eliminar un registro inexistente retorna False."""
        estudiante_no_existe = EstudianteDTO(id_estudiante=999)
        resultado = estudiante_dao.eliminar(estudiante_no_existe)

        assert resultado is False, "No debe eliminar un registro inexistente"

    def test_ciclo_completo(self, estudiante_dao, carrera_fixture):
        """Verifica un ciclo completo: crear, instanciar, modificar, eliminar."""
        uid = get_unique()
        # 1. Crear
        estudiante_original = EstudianteDTO(
            nombre=f"Juan-{uid}",
            correo=f"juan{uid}@universidad.edu",
            id_carrera=carrera_fixture,
        )
        id_creado = estudiante_dao.insertar(estudiante_original)
        assert id_creado is not None

        # 2. Instanciar
        estudiante_recuperado = EstudianteDTO(id_estudiante=id_creado)
        assert estudiante_dao.instanciar(estudiante_recuperado) is True
        assert estudiante_recuperado.nombre == estudiante_original.nombre

        # 3. Verificar existencia
        assert estudiante_dao.existe(estudiante_recuperado) is True

        # 4. Eliminar
        assert estudiante_dao.eliminar(estudiante_recuperado) is True
        assert estudiante_dao.existe(estudiante_recuperado) is False
