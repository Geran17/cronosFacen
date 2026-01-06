import pytest
import os
import sqlite3
import uuid
from pathlib import Path
from src.modelos.daos.eje_tematico_dao import EjeTematicoDAO
from src.modelos.daos.asignatura_dao import AsignaturaDAO
from src.modelos.daos.carrera_dao import CarreraDAO
from src.modelos.dtos.eje_tematico_dto import EjeTematicoDTO
from src.modelos.dtos.asignatura_dto import AsignaturaDTO
from src.modelos.dtos.carrera_dto import CarreraDTO


def get_unique():
    """Genera un sufijo único para evitar conflictos UNIQUE"""
    return str(uuid.uuid4())[:8]


@pytest.fixture
def db_path(tmp_path):
    """Crea una ruta temporal para la base de datos de prueba."""
    db_file = tmp_path / "test_eje_tematico.db"
    yield str(db_file)
    if db_file.exists():
        db_file.unlink()


@pytest.fixture
def carrera_dao(db_path):
    """Crea una instancia del CarreraDAO con tabla creada."""
    dao = CarreraDAO(ruta_db=db_path)
    dao.crear_tabla()
    yield dao


@pytest.fixture
def asignatura_dao(db_path, carrera_dao):
    """Crea una instancia del AsignaturaDAO con tabla creada."""
    dao = AsignaturaDAO(ruta_db=db_path)
    dao.crear_tabla()
    yield dao


@pytest.fixture
def eje_tematico_dao(db_path, carrera_dao, asignatura_dao):
    """Crea una instancia del EjeTematicoDAO con tabla creada."""
    dao = EjeTematicoDAO(ruta_db=db_path)
    dao.crear_tabla()
    yield dao


@pytest.fixture
def asignatura_para_ejes(carrera_dao, asignatura_dao):
    """Crea una carrera y asignatura, retorna id_asignatura."""
    carrera = CarreraDTO(nombre="Ingeniería", plan="Plan2023", modalidad="Presencial")
    id_carrera = carrera_dao.insertar(carrera)

    uid = get_unique()
    asignatura = AsignaturaDTO(
        nombre=f"Sistemas-{uid}",
        codigo=f"SIS{uid[:3]}",
        creditos=3,
        tipo="obligatoria",
        id_carrera=id_carrera,
    )
    id_asignatura = asignatura_dao.insertar(asignatura)

    yield id_asignatura


class TestEjeTematicoDAO:
    """Suite de pruebas para la clase EjeTematicoDAO."""

    def test_crear_tabla(self, eje_tematico_dao):
        """Verifica que la tabla se crea correctamente."""
        with eje_tematico_dao.get_conexion() as con:
            cursor = con.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='eje_tematico'"
            )
            resultado = cursor.fetchone()
            assert resultado is not None, "La tabla 'eje_tematico' no fue creada"

    def test_insertar(self, eje_tematico_dao, asignatura_para_ejes):
        """Verifica que se inserta correctamente un registro."""
        uid = get_unique()
        eje_dto = EjeTematicoDTO(
            nombre=f"Tema-{uid}",
            orden=1,
            id_asignatura=asignatura_para_ejes,
        )

        id_insertado = eje_tematico_dao.insertar(eje_dto)

        assert id_insertado is not None, "No se obtuvo ID después de insertar"
        assert id_insertado > 0, "El ID insertado debe ser mayor a 0"

    def test_insertar_multiples(self, eje_tematico_dao, asignatura_para_ejes):
        """Verifica que se pueden insertar múltiples registros."""
        u1, u2, u3 = get_unique(), get_unique(), get_unique()
        ejes = [
            EjeTematicoDTO(nombre=f"Tema-{u1}", orden=1, id_asignatura=asignatura_para_ejes),
            EjeTematicoDTO(nombre=f"Tema-{u2}", orden=2, id_asignatura=asignatura_para_ejes),
            EjeTematicoDTO(nombre=f"Tema-{u3}", orden=3, id_asignatura=asignatura_para_ejes),
        ]

        ids = [eje_tematico_dao.insertar(eje) for eje in ejes]

        assert all(id is not None for id in ids), "Todos los IDs deben ser válidos"
        assert len(ids) == 3, "Debe insertar 3 registros"

    def test_instanciar_existente(self, eje_tematico_dao, asignatura_para_ejes):
        """Verifica que se instancia correctamente un eje existente."""
        uid = get_unique()
        eje_original = EjeTematicoDTO(
            nombre=f"Tema-{uid}",
            orden=1,
            id_asignatura=asignatura_para_ejes,
        )
        id_creado = eje_tematico_dao.insertar(eje_original)

        eje_recuperado = EjeTematicoDTO(id_eje_tematico=id_creado)
        resultado = eje_tematico_dao.instanciar(eje_recuperado)

        assert resultado is True, "Debería encontrar el eje temático"
        assert eje_recuperado.nombre == eje_original.nombre, "El nombre debe coincidir"
        assert eje_recuperado.orden == eje_original.orden, "El orden debe coincidir"

    def test_instanciar_inexistente(self, eje_tematico_dao):
        """Verifica que no se instancia un ID que no existe."""
        eje_inexistente = EjeTematicoDTO(id_eje_tematico=999)
        resultado = eje_tematico_dao.instanciar(eje_inexistente)

        assert resultado is False, "No debería encontrar un eje inexistente"

    def test_instanciar_id_invalido(self, eje_tematico_dao):
        """Verifica el manejo de ID inválido."""
        eje_invalido = EjeTematicoDTO(id_eje_tematico=None)
        resultado = eje_tematico_dao.instanciar(eje_invalido)

        assert resultado is False, "No debería instanciar con ID None"

    def test_existe_verdadero(self, eje_tematico_dao, asignatura_para_ejes):
        """Verifica que existe() retorna True para un registro insertado."""
        uid = get_unique()
        eje_original = EjeTematicoDTO(
            nombre=f"Tema-{uid}",
            orden=1,
            id_asignatura=asignatura_para_ejes,
        )
        id_creado = eje_tematico_dao.insertar(eje_original)

        eje_verificar = EjeTematicoDTO(id_eje_tematico=id_creado)
        existe = eje_tematico_dao.existe(eje_verificar)

        assert existe is True, "Debería confirmar que el eje existe"

    def test_existe_falso(self, eje_tematico_dao):
        """Verifica que existe() retorna False para un ID inexistente."""
        eje_no_existe = EjeTematicoDTO(id_eje_tematico=999)
        existe = eje_tematico_dao.existe(eje_no_existe)

        assert existe is False, "No debería encontrar un eje inexistente"

    def test_existe_id_invalido(self, eje_tematico_dao):
        """Verifica el manejo de ID inválido en existe()."""
        eje_invalido = EjeTematicoDTO(id_eje_tematico=None)
        existe = eje_tematico_dao.existe(eje_invalido)

        assert existe is False, "No debería confirmar existencia con ID None"

    def test_eliminar(self, eje_tematico_dao, asignatura_para_ejes):
        """Verifica que se elimina correctamente un registro."""
        uid = get_unique()
        eje_original = EjeTematicoDTO(
            nombre=f"Tema-{uid}",
            orden=1,
            id_asignatura=asignatura_para_ejes,
        )
        id_creado = eje_tematico_dao.insertar(eje_original)

        eje_verificar = EjeTematicoDTO(id_eje_tematico=id_creado)
        assert eje_tematico_dao.existe(eje_verificar) is True

        resultado_eliminacion = eje_tematico_dao.eliminar(eje_verificar)
        assert resultado_eliminacion is True, "La eliminación debe retornar True"
        assert eje_tematico_dao.existe(eje_verificar) is False, "El registro debe estar eliminado"

    def test_eliminar_inexistente(self, eje_tematico_dao):
        """Verifica que eliminar un registro inexistente retorna False."""
        eje_no_existe = EjeTematicoDTO(id_eje_tematico=999)
        resultado = eje_tematico_dao.eliminar(eje_no_existe)

        assert resultado is False, "No debe eliminar un registro inexistente"

    def test_ciclo_completo(self, eje_tematico_dao, asignatura_para_ejes):
        """Verifica un ciclo completo: crear, instanciar, eliminar."""
        uid = get_unique()
        # 1. Crear
        eje_original = EjeTematicoDTO(
            nombre=f"Tema-{uid}",
            orden=1,
            id_asignatura=asignatura_para_ejes,
        )
        id_creado = eje_tematico_dao.insertar(eje_original)
        assert id_creado is not None

        # 2. Instanciar
        eje_recuperado = EjeTematicoDTO(id_eje_tematico=id_creado)
        assert eje_tematico_dao.instanciar(eje_recuperado) is True
        assert eje_recuperado.nombre == eje_original.nombre

        # 3. Verificar existencia
        assert eje_tematico_dao.existe(eje_recuperado) is True

        # 4. Eliminar
        assert eje_tematico_dao.eliminar(eje_recuperado) is True
        assert eje_tematico_dao.existe(eje_recuperado) is False
