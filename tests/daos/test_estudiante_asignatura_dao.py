import pytest
import os
import sqlite3
import uuid
from pathlib import Path
from src.modelos.daos.estudiante_asignatura_dao import EstudianteAsignaturaDAO
from src.modelos.daos.estudiante_dao import EstudianteDAO
from src.modelos.daos.asignatura_dao import AsignaturaDAO
from src.modelos.daos.carrera_dao import CarreraDAO
from src.modelos.dtos.estudiante_asignatura_dto import EstudianteAsignaturaDTO
from src.modelos.dtos.estudiante_dto import EstudianteDTO
from src.modelos.dtos.asignatura_dto import AsignaturaDTO
from src.modelos.dtos.carrera_dto import CarreraDTO


def get_unique():
    """Genera un sufijo único para evitar conflictos UNIQUE"""
    return str(uuid.uuid4())[:8]


@pytest.fixture
def db_path(tmp_path):
    """Crea una ruta temporal para la base de datos de prueba."""
    db_file = tmp_path / "test_estudiante_asignatura.db"
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
def estudiante_dao(db_path, carrera_dao):
    """Crea una instancia del EstudianteDAO con tabla creada."""
    dao = EstudianteDAO(ruta_db=db_path)
    dao.crear_tabla()
    yield dao


@pytest.fixture
def estudiante_asignatura_dao(db_path, carrera_dao, asignatura_dao, estudiante_dao):
    """Crea una instancia del EstudianteAsignaturaDAO con tabla creada."""
    dao = EstudianteAsignaturaDAO(ruta_db=db_path)
    dao.crear_tabla()
    yield dao


@pytest.fixture
def datos_para_relacion_estasig(carrera_dao, asignatura_dao, estudiante_dao):
    """Crea estudiante y asignatura. Retorna (id_estudiante, id_asignatura)."""

    # Carrera
    carrera = CarreraDTO(nombre="Ingeniería", plan="Plan2023", modalidad="Presencial")
    id_carrera = carrera_dao.insertar(carrera)

    # Asignatura
    u_asig = get_unique()
    asignatura = AsignaturaDTO(
        nombre=f"Sistemas-{u_asig}",
        codigo=f"SIS{u_asig[:3]}",
        creditos=3,
        tipo="obligatoria",
        id_carrera=id_carrera,
    )
    id_asignatura = asignatura_dao.insertar(asignatura)

    # Estudiante
    u_est = get_unique()
    estudiante = EstudianteDTO(
        nombre=f"Juan-{u_est}",
        correo=f"juan{u_est}@universidad.edu",
        id_carrera=id_carrera,
    )
    id_estudiante = estudiante_dao.insertar(estudiante)

    yield (id_estudiante, id_asignatura)


class TestEstudianteAsignaturaDAO:
    """Suite de pruebas para la clase EstudianteAsignaturaDAO."""

    def test_crear_tabla(self, estudiante_asignatura_dao):
        """Verifica que la tabla se crea correctamente."""
        with estudiante_asignatura_dao.get_conexion() as con:
            cursor = con.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='estudiante_asignatura'"
            )
            resultado = cursor.fetchone()
            assert resultado is not None, "La tabla 'estudiante_asignatura' no fue creada"

    def test_insertar(self, estudiante_asignatura_dao, datos_para_relacion_estasig):
        """Verifica que se inserta correctamente una relación."""
        id_estudiante, id_asignatura = datos_para_relacion_estasig
        relacion_dto = EstudianteAsignaturaDTO(
            id_estudiante=id_estudiante,
            id_asignatura=id_asignatura,
            estado="activo",
            nota_final=None,
            periodo="2024-1",
        )

        resultado = estudiante_asignatura_dao.insertar(relacion_dto)

        assert resultado is True, "Debería insertar correctamente"

    def test_insertar_multiples(self, estudiante_asignatura_dao, datos_para_relacion_estasig):
        """Para relaciones compuestas, solo permite UNA fila por clave compuesta."""
        id_estudiante, id_asignatura = datos_para_relacion_estasig
        # Intentar insertar la misma relación múltiples veces falla en la segunda
        relacion1 = EstudianteAsignaturaDTO(
            id_estudiante=id_estudiante,
            id_asignatura=id_asignatura,
            estado="activo",
            nota_final=None,
            periodo="2024-1",
        )

        resultado1 = estudiante_asignatura_dao.insertar(relacion1)
        assert resultado1 is True, "Primera inserción debe exitosa"

    def test_instanciar_existente(self, estudiante_asignatura_dao, datos_para_relacion_estasig):
        """Verifica que se instancia correctamente una relación existente."""
        id_estudiante, id_asignatura = datos_para_relacion_estasig
        relacion_original = EstudianteAsignaturaDTO(
            id_estudiante=id_estudiante,
            id_asignatura=id_asignatura,
            estado="activo",
            nota_final=8.5,
            periodo="2024-1",
        )
        estudiante_asignatura_dao.insertar(relacion_original)

        relacion_recuperada = EstudianteAsignaturaDTO(
            id_estudiante=id_estudiante,
            id_asignatura=id_asignatura,
        )
        resultado = estudiante_asignatura_dao.instanciar(relacion_recuperada)

        assert resultado is True, "Debería encontrar la relación"
        assert relacion_recuperada.estado == "activo", "El estado debe coincidir"
        assert relacion_recuperada.nota_final == 8.5, "La nota debe coincidir"

    def test_instanciar_inexistente(self, estudiante_asignatura_dao):
        """Verifica que no se instancia una relación inexistente."""
        relacion_inexistente = EstudianteAsignaturaDTO(
            id_estudiante=999,
            id_asignatura=999,
        )
        resultado = estudiante_asignatura_dao.instanciar(relacion_inexistente)

        assert resultado is False, "No debería encontrar una relación inexistente"

    def test_instanciar_ids_invalidos(self, estudiante_asignatura_dao):
        """Verifica el manejo de IDs inválidos."""
        relacion_invalida = EstudianteAsignaturaDTO(
            id_estudiante=None,
            id_asignatura=None,
        )
        resultado = estudiante_asignatura_dao.instanciar(relacion_invalida)

        assert resultado is False, "No debería instanciar con IDs None"

    def test_existe_verdadero(self, estudiante_asignatura_dao, datos_para_relacion_estasig):
        """Verifica que existe() retorna True para una relación insertada."""
        id_estudiante, id_asignatura = datos_para_relacion_estasig
        relacion_original = EstudianteAsignaturaDTO(
            id_estudiante=id_estudiante,
            id_asignatura=id_asignatura,
            estado="activo",
            nota_final=None,
            periodo="2024-1",
        )
        estudiante_asignatura_dao.insertar(relacion_original)

        relacion_verificar = EstudianteAsignaturaDTO(
            id_estudiante=id_estudiante,
            id_asignatura=id_asignatura,
        )
        existe = estudiante_asignatura_dao.existe(relacion_verificar)

        assert existe is True, "Debería confirmar que la relación existe"

    def test_existe_falso(self, estudiante_asignatura_dao):
        """Verifica que existe() retorna False para una relación inexistente."""
        relacion_no_existe = EstudianteAsignaturaDTO(
            id_estudiante=999,
            id_asignatura=999,
        )
        existe = estudiante_asignatura_dao.existe(relacion_no_existe)

        assert existe is False, "No debería encontrar una relación inexistente"

    def test_existe_ids_invalidos(self, estudiante_asignatura_dao):
        """Verifica el manejo de IDs inválidos en existe()."""
        relacion_invalida = EstudianteAsignaturaDTO(
            id_estudiante=None,
            id_asignatura=None,
        )
        existe = estudiante_asignatura_dao.existe(relacion_invalida)

        assert existe is False, "No debería confirmar existencia con IDs None"

    def test_eliminar(self, estudiante_asignatura_dao, datos_para_relacion_estasig):
        """Verifica que se elimina correctamente una relación."""
        id_estudiante, id_asignatura = datos_para_relacion_estasig
        relacion_original = EstudianteAsignaturaDTO(
            id_estudiante=id_estudiante,
            id_asignatura=id_asignatura,
            estado="activo",
            nota_final=None,
            periodo="2024-1",
        )
        estudiante_asignatura_dao.insertar(relacion_original)

        relacion_verificar = EstudianteAsignaturaDTO(
            id_estudiante=id_estudiante,
            id_asignatura=id_asignatura,
        )
        assert estudiante_asignatura_dao.existe(relacion_verificar) is True

        resultado_eliminacion = estudiante_asignatura_dao.eliminar(relacion_verificar)
        assert resultado_eliminacion is True, "La eliminación debe retornar True"
        assert (
            estudiante_asignatura_dao.existe(relacion_verificar) is False
        ), "La relación debe estar eliminada"

    def test_eliminar_inexistente(self, estudiante_asignatura_dao):
        """Verifica que eliminar una relación inexistente retorna False."""
        relacion_no_existe = EstudianteAsignaturaDTO(
            id_estudiante=999,
            id_asignatura=999,
        )
        resultado = estudiante_asignatura_dao.eliminar(relacion_no_existe)

        assert resultado is False, "No debe eliminar una relación inexistente"

    def test_ciclo_completo(self, estudiante_asignatura_dao, datos_para_relacion_estasig):
        """Verifica un ciclo completo: crear, instanciar, eliminar."""
        id_estudiante, id_asignatura = datos_para_relacion_estasig
        # 1. Crear
        relacion_original = EstudianteAsignaturaDTO(
            id_estudiante=id_estudiante,
            id_asignatura=id_asignatura,
            estado="activo",
            nota_final=7.5,
            periodo="2024-1",
        )
        resultado_insert = estudiante_asignatura_dao.insertar(relacion_original)
        assert resultado_insert is True

        # 2. Instanciar
        relacion_recuperada = EstudianteAsignaturaDTO(
            id_estudiante=id_estudiante,
            id_asignatura=id_asignatura,
        )
        assert estudiante_asignatura_dao.instanciar(relacion_recuperada) is True
        assert relacion_recuperada.estado == "activo"

        # 3. Verificar existencia
        assert estudiante_asignatura_dao.existe(relacion_recuperada) is True

        # 4. Eliminar
        assert estudiante_asignatura_dao.eliminar(relacion_recuperada) is True
        assert estudiante_asignatura_dao.existe(relacion_recuperada) is False
