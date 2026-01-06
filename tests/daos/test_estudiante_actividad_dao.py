import pytest
import os
import sqlite3
import uuid
from pathlib import Path
from src.modelos.daos.estudiante_actividad_dao import EstudianteActividadDAO
from src.modelos.daos.actividad_dao import ActividadDAO
from src.modelos.daos.eje_tematico_dao import EjeTematicoDAO
from src.modelos.daos.tipo_actividad_dao import TipoActividadDAO
from src.modelos.daos.asignatura_dao import AsignaturaDAO
from src.modelos.daos.carrera_dao import CarreraDAO
from src.modelos.daos.estudiante_dao import EstudianteDAO
from src.modelos.dtos.estudiante_actividad_dto import EstudianteActividadDTO
from src.modelos.dtos.actividad_dto import ActividadDTO
from src.modelos.dtos.eje_tematico_dto import EjeTematicoDTO
from src.modelos.dtos.tipo_actividad_dto import TipoActividadDTO
from src.modelos.dtos.asignatura_dto import AsignaturaDTO
from src.modelos.dtos.carrera_dto import CarreraDTO
from src.modelos.dtos.estudiante_dto import EstudianteDTO


def get_unique():
    """Genera un sufijo único para evitar conflictos UNIQUE"""
    return str(uuid.uuid4())[:8]


@pytest.fixture
def db_path(tmp_path):
    """Crea una ruta temporal para la base de datos de prueba."""
    db_file = tmp_path / "test_estudiante_actividad.db"
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
def eje_tematico_dao(db_path, asignatura_dao):
    """Crea una instancia del EjeTematicoDAO con tabla creada."""
    dao = EjeTematicoDAO(ruta_db=db_path)
    dao.crear_tabla()
    yield dao


@pytest.fixture
def tipo_actividad_dao(db_path):
    """Crea una instancia del TipoActividadDAO con tabla creada."""
    dao = TipoActividadDAO(ruta_db=db_path)
    dao.crear_tabla()
    yield dao


@pytest.fixture
def actividad_dao(db_path, carrera_dao, asignatura_dao, eje_tematico_dao, tipo_actividad_dao):
    """Crea una instancia del ActividadDAO con tabla creada."""
    dao = ActividadDAO(ruta_db=db_path)
    dao.crear_tabla()
    yield dao


@pytest.fixture
def estudiante_dao(db_path, carrera_dao):
    """Crea una instancia del EstudianteDAO con tabla creada."""
    dao = EstudianteDAO(ruta_db=db_path)
    dao.crear_tabla()
    yield dao


@pytest.fixture
def estudiante_actividad_dao(
    db_path,
    carrera_dao,
    asignatura_dao,
    eje_tematico_dao,
    tipo_actividad_dao,
    actividad_dao,
    estudiante_dao,
):
    """Crea una instancia del EstudianteActividadDAO con tabla creada."""
    dao = EstudianteActividadDAO(ruta_db=db_path)
    dao.crear_tabla()
    yield dao


@pytest.fixture
def datos_para_relacion_estact(
    carrera_dao, asignatura_dao, eje_tematico_dao, tipo_actividad_dao, actividad_dao, estudiante_dao
):
    """Crea toda la cadena: Carrera → Asignatura → EjeTemático, TipoActividad → Actividad, Y Carrera → Estudiante.
    Retorna (id_estudiante, id_actividad)."""

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

    # EjeTemático
    u_eje = get_unique()
    eje = EjeTematicoDTO(
        nombre=f"Tema-{u_eje}",
        orden=1,
        id_asignatura=id_asignatura,
    )
    id_eje = eje_tematico_dao.insertar(eje)

    # TipoActividad
    u_tipo = get_unique()
    tipo = TipoActividadDTO(
        nombre=f"Tipo-{u_tipo}",
        siglas=f"TIP{u_tipo[:3]}",
        descripcion="Tipo de prueba",
    )
    id_tipo = tipo_actividad_dao.insertar(tipo)

    # Actividad
    u_act = get_unique()
    actividad = ActividadDTO(
        titulo=f"Actividad-{u_act}",
        descripcion="Descripción",
        id_eje=id_eje,
        id_tipo_actividad=id_tipo,
    )
    id_actividad = actividad_dao.insertar(actividad)

    # Estudiante
    u_est = get_unique()
    estudiante = EstudianteDTO(
        nombre=f"Juan-{u_est}",
        correo=f"juan{u_est}@universidad.edu",
        id_carrera=id_carrera,
    )
    id_estudiante = estudiante_dao.insertar(estudiante)

    yield (id_estudiante, id_actividad)


class TestEstudianteActividadDAO:
    """Suite de pruebas para la clase EstudianteActividadDAO."""

    def test_crear_tabla(self, estudiante_actividad_dao):
        """Verifica que la tabla se crea correctamente."""
        with estudiante_actividad_dao.get_conexion() as con:
            cursor = con.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='estudiante_actividad'"
            )
            resultado = cursor.fetchone()
            assert resultado is not None, "La tabla 'estudiante_actividad' no fue creada"

    def test_insertar(self, estudiante_actividad_dao, datos_para_relacion_estact):
        """Verifica que se inserta correctamente una relación."""
        id_estudiante, id_actividad = datos_para_relacion_estact
        relacion_dto = EstudianteActividadDTO(
            id_estudiante=id_estudiante,
            id_actividad=id_actividad,
            estado="pendiente",
            fecha_entrega=None,
        )

        resultado = estudiante_actividad_dao.insertar(relacion_dto)

        assert resultado is True, "Debería insertar correctamente"

    def test_insertar_multiples(self, estudiante_actividad_dao, datos_para_relacion_estact):
        """Para relaciones compuestas, solo permite UNA fila por clave compuesta."""
        id_estudiante, id_actividad = datos_para_relacion_estact
        relacion1 = EstudianteActividadDTO(
            id_estudiante=id_estudiante,
            id_actividad=id_actividad,
            estado="pendiente",
            fecha_entrega=None,
        )

        resultado1 = estudiante_actividad_dao.insertar(relacion1)
        assert resultado1 is True, "Primera inserción debe ser exitosa"

    def test_instanciar_existente(self, estudiante_actividad_dao, datos_para_relacion_estact):
        """Verifica que se instancia correctamente una relación existente."""
        id_estudiante, id_actividad = datos_para_relacion_estact
        relacion_original = EstudianteActividadDTO(
            id_estudiante=id_estudiante,
            id_actividad=id_actividad,
            estado="en_progreso",
            fecha_entrega=None,
        )
        estudiante_actividad_dao.insertar(relacion_original)

        relacion_recuperada = EstudianteActividadDTO(
            id_estudiante=id_estudiante,
            id_actividad=id_actividad,
        )
        resultado = estudiante_actividad_dao.instanciar(relacion_recuperada)

        assert resultado is True, "Debería encontrar la relación"
        assert relacion_recuperada.estado == "en_progreso", "El estado debe coincidir"

    def test_instanciar_inexistente(self, estudiante_actividad_dao):
        """Verifica que no se instancia una relación inexistente."""
        relacion_inexistente = EstudianteActividadDTO(
            id_estudiante=999,
            id_actividad=999,
        )
        resultado = estudiante_actividad_dao.instanciar(relacion_inexistente)

        assert resultado is False, "No debería encontrar una relación inexistente"

    def test_instanciar_ids_invalidos(self, estudiante_actividad_dao):
        """Verifica el manejo de IDs inválidos."""
        relacion_invalida = EstudianteActividadDTO(
            id_estudiante=None,
            id_actividad=None,
        )
        resultado = estudiante_actividad_dao.instanciar(relacion_invalida)

        assert resultado is False, "No debería instanciar con IDs None"

    def test_existe_verdadero(self, estudiante_actividad_dao, datos_para_relacion_estact):
        """Verifica que existe() retorna True para una relación insertada."""
        id_estudiante, id_actividad = datos_para_relacion_estact
        relacion_original = EstudianteActividadDTO(
            id_estudiante=id_estudiante,
            id_actividad=id_actividad,
            estado="pendiente",
            fecha_entrega=None,
        )
        estudiante_actividad_dao.insertar(relacion_original)

        relacion_verificar = EstudianteActividadDTO(
            id_estudiante=id_estudiante,
            id_actividad=id_actividad,
        )
        existe = estudiante_actividad_dao.existe(relacion_verificar)

        assert existe is True, "Debería confirmar que la relación existe"

    def test_existe_falso(self, estudiante_actividad_dao):
        """Verifica que existe() retorna False para una relación inexistente."""
        relacion_no_existe = EstudianteActividadDTO(
            id_estudiante=999,
            id_actividad=999,
        )
        existe = estudiante_actividad_dao.existe(relacion_no_existe)

        assert existe is False, "No debería encontrar una relación inexistente"

    def test_existe_ids_invalidos(self, estudiante_actividad_dao):
        """Verifica el manejo de IDs inválidos en existe()."""
        relacion_invalida = EstudianteActividadDTO(
            id_estudiante=None,
            id_actividad=None,
        )
        existe = estudiante_actividad_dao.existe(relacion_invalida)

        assert existe is False, "No debería confirmar existencia con IDs None"

    def test_eliminar(self, estudiante_actividad_dao, datos_para_relacion_estact):
        """Verifica que se elimina correctamente una relación."""
        id_estudiante, id_actividad = datos_para_relacion_estact
        relacion_original = EstudianteActividadDTO(
            id_estudiante=id_estudiante,
            id_actividad=id_actividad,
            estado="pendiente",
            fecha_entrega=None,
        )
        estudiante_actividad_dao.insertar(relacion_original)

        relacion_verificar = EstudianteActividadDTO(
            id_estudiante=id_estudiante,
            id_actividad=id_actividad,
        )
        assert estudiante_actividad_dao.existe(relacion_verificar) is True

        resultado_eliminacion = estudiante_actividad_dao.eliminar(relacion_verificar)
        assert resultado_eliminacion is True, "La eliminación debe retornar True"
        assert (
            estudiante_actividad_dao.existe(relacion_verificar) is False
        ), "La relación debe estar eliminada"

    def test_eliminar_inexistente(self, estudiante_actividad_dao):
        """Verifica que eliminar una relación inexistente retorna False."""
        relacion_no_existe = EstudianteActividadDTO(
            id_estudiante=999,
            id_actividad=999,
        )
        resultado = estudiante_actividad_dao.eliminar(relacion_no_existe)

        assert resultado is False, "No debe eliminar una relación inexistente"

    def test_ciclo_completo(self, estudiante_actividad_dao, datos_para_relacion_estact):
        """Verifica un ciclo completo: crear, instanciar, eliminar."""
        id_estudiante, id_actividad = datos_para_relacion_estact
        # 1. Crear
        relacion_original = EstudianteActividadDTO(
            id_estudiante=id_estudiante,
            id_actividad=id_actividad,
            estado="pendiente",
            fecha_entrega=None,
        )
        resultado_insert = estudiante_actividad_dao.insertar(relacion_original)
        assert resultado_insert is True

        # 2. Instanciar
        relacion_recuperada = EstudianteActividadDTO(
            id_estudiante=id_estudiante,
            id_actividad=id_actividad,
        )
        assert estudiante_actividad_dao.instanciar(relacion_recuperada) is True
        assert relacion_recuperada.estado == "pendiente"

        # 3. Verificar existencia
        assert estudiante_actividad_dao.existe(relacion_recuperada) is True

        # 4. Eliminar
        assert estudiante_actividad_dao.eliminar(relacion_recuperada) is True
        assert estudiante_actividad_dao.existe(relacion_recuperada) is False
