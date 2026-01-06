import pytest
import os
import sqlite3
import uuid
from pathlib import Path
from src.modelos.daos.actividad_dao import ActividadDAO
from src.modelos.daos.eje_tematico_dao import EjeTematicoDAO
from src.modelos.daos.tipo_actividad_dao import TipoActividadDAO
from src.modelos.daos.asignatura_dao import AsignaturaDAO
from src.modelos.daos.carrera_dao import CarreraDAO
from src.modelos.dtos.actividad_dto import ActividadDTO
from src.modelos.dtos.eje_tematico_dto import EjeTematicoDTO
from src.modelos.dtos.tipo_actividad_dto import TipoActividadDTO
from src.modelos.dtos.asignatura_dto import AsignaturaDTO
from src.modelos.dtos.carrera_dto import CarreraDTO


def get_unique():
    """Genera un sufijo único para evitar conflictos UNIQUE"""
    return str(uuid.uuid4())[:8]


@pytest.fixture
def db_path(tmp_path):
    """Crea una ruta temporal para la base de datos de prueba."""
    db_file = tmp_path / "test_actividad.db"
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
def datos_para_actividades(carrera_dao, asignatura_dao, eje_tematico_dao, tipo_actividad_dao):
    """Crea toda la cadena de dependencias: Carrera → Asignatura → EjeTemático, TipoActividad.
    Retorna (id_eje, id_tipo)."""

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

    yield (id_eje, id_tipo)


class TestActividadDAO:
    """Suite de pruebas para la clase ActividadDAO."""

    def test_crear_tabla(self, actividad_dao):
        """Verifica que la tabla se crea correctamente."""
        with actividad_dao.get_conexion() as con:
            cursor = con.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='actividad'")
            resultado = cursor.fetchone()
            assert resultado is not None, "La tabla 'actividad' no fue creada"

    def test_insertar(self, actividad_dao, datos_para_actividades):
        """Verifica que se inserta correctamente un registro."""
        id_eje, id_tipo = datos_para_actividades
        uid = get_unique()
        actividad_dto = ActividadDTO(
            titulo=f"Actividad-{uid}",
            descripcion="Descripción de prueba",
            id_eje=id_eje,
            id_tipo_actividad=id_tipo,
        )

        id_insertado = actividad_dao.insertar(actividad_dto)

        assert id_insertado is not None, "No se obtuvo ID después de insertar"
        assert id_insertado > 0, "El ID insertado debe ser mayor a 0"

    def test_insertar_multiples(self, actividad_dao, datos_para_actividades):
        """Verifica que se pueden insertar múltiples registros."""
        id_eje, id_tipo = datos_para_actividades
        u1, u2, u3 = get_unique(), get_unique(), get_unique()
        actividades = [
            ActividadDTO(
                titulo=f"Act-{u1}", descripcion="Desc", id_eje=id_eje, id_tipo_actividad=id_tipo
            ),
            ActividadDTO(
                titulo=f"Act-{u2}", descripcion="Desc", id_eje=id_eje, id_tipo_actividad=id_tipo
            ),
            ActividadDTO(
                titulo=f"Act-{u3}", descripcion="Desc", id_eje=id_eje, id_tipo_actividad=id_tipo
            ),
        ]

        ids = [actividad_dao.insertar(act) for act in actividades]

        assert all(id is not None for id in ids), "Todos los IDs deben ser válidos"
        assert len(ids) == 3, "Debe insertar 3 registros"

    def test_instanciar_existente(self, actividad_dao, datos_para_actividades):
        """Verifica que se instancia correctamente una actividad existente."""
        id_eje, id_tipo = datos_para_actividades
        uid = get_unique()
        actividad_original = ActividadDTO(
            titulo=f"Actividad-{uid}",
            descripcion="Descripción de prueba",
            id_eje=id_eje,
            id_tipo_actividad=id_tipo,
        )
        id_creado = actividad_dao.insertar(actividad_original)

        actividad_recuperada = ActividadDTO(id_actividad=id_creado)
        resultado = actividad_dao.instanciar(actividad_recuperada)

        assert resultado is True, "Debería encontrar la actividad"
        assert actividad_recuperada.titulo == actividad_original.titulo, "El título debe coincidir"

    def test_instanciar_inexistente(self, actividad_dao):
        """Verifica que no se instancia un ID que no existe."""
        actividad_inexistente = ActividadDTO(id_actividad=999)
        resultado = actividad_dao.instanciar(actividad_inexistente)

        assert resultado is False, "No debería encontrar una actividad inexistente"

    def test_instanciar_id_invalido(self, actividad_dao):
        """Verifica el manejo de ID inválido."""
        actividad_invalida = ActividadDTO(id_actividad=None)
        resultado = actividad_dao.instanciar(actividad_invalida)

        assert resultado is False, "No debería instanciar con ID None"

    def test_existe_verdadero(self, actividad_dao, datos_para_actividades):
        """Verifica que existe() retorna True para un registro insertado."""
        id_eje, id_tipo = datos_para_actividades
        uid = get_unique()
        actividad_original = ActividadDTO(
            titulo=f"Actividad-{uid}",
            descripcion="Descripción de prueba",
            id_eje=id_eje,
            id_tipo_actividad=id_tipo,
        )
        id_creado = actividad_dao.insertar(actividad_original)

        actividad_verificar = ActividadDTO(id_actividad=id_creado)
        existe = actividad_dao.existe(actividad_verificar)

        assert existe is True, "Debería confirmar que la actividad existe"

    def test_existe_falso(self, actividad_dao):
        """Verifica que existe() retorna False para un ID inexistente."""
        actividad_no_existe = ActividadDTO(id_actividad=999)
        existe = actividad_dao.existe(actividad_no_existe)

        assert existe is False, "No debería encontrar una actividad inexistente"

    def test_existe_id_invalido(self, actividad_dao):
        """Verifica el manejo de ID inválido en existe()."""
        actividad_invalida = ActividadDTO(id_actividad=None)
        existe = actividad_dao.existe(actividad_invalida)

        assert existe is False, "No debería confirmar existencia con ID None"

    def test_eliminar(self, actividad_dao, datos_para_actividades):
        """Verifica que se elimina correctamente un registro."""
        id_eje, id_tipo = datos_para_actividades
        uid = get_unique()
        actividad_original = ActividadDTO(
            titulo=f"Actividad-{uid}",
            descripcion="Descripción de prueba",
            id_eje=id_eje,
            id_tipo_actividad=id_tipo,
        )
        id_creado = actividad_dao.insertar(actividad_original)

        actividad_verificar = ActividadDTO(id_actividad=id_creado)
        assert actividad_dao.existe(actividad_verificar) is True

        resultado_eliminacion = actividad_dao.eliminar(actividad_verificar)
        assert resultado_eliminacion is True, "La eliminación debe retornar True"
        assert (
            actividad_dao.existe(actividad_verificar) is False
        ), "El registro debe estar eliminado"

    def test_eliminar_inexistente(self, actividad_dao):
        """Verifica que eliminar un registro inexistente retorna False."""
        actividad_no_existe = ActividadDTO(id_actividad=999)
        resultado = actividad_dao.eliminar(actividad_no_existe)

        assert resultado is False, "No debe eliminar un registro inexistente"

    def test_ciclo_completo(self, actividad_dao, datos_para_actividades):
        """Verifica un ciclo completo: crear, instanciar, eliminar."""
        id_eje, id_tipo = datos_para_actividades
        uid = get_unique()
        # 1. Crear
        actividad_original = ActividadDTO(
            titulo=f"Actividad-{uid}",
            descripcion="Descripción de prueba",
            id_eje=id_eje,
            id_tipo_actividad=id_tipo,
        )
        id_creado = actividad_dao.insertar(actividad_original)
        assert id_creado is not None

        # 2. Instanciar
        actividad_recuperada = ActividadDTO(id_actividad=id_creado)
        assert actividad_dao.instanciar(actividad_recuperada) is True
        assert actividad_recuperada.titulo == actividad_original.titulo

        # 3. Verificar existencia
        assert actividad_dao.existe(actividad_recuperada) is True

        # 4. Eliminar
        assert actividad_dao.eliminar(actividad_recuperada) is True
        assert actividad_dao.existe(actividad_recuperada) is False
