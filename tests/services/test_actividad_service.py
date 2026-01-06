import uuid
import pytest
from pathlib import Path
from src.modelos.services.actividad_service import ActividadService
from src.modelos.services.asignatura_service import AsignaturaService
from src.modelos.services.eje_tematico_service import EjeTematicoService
from src.modelos.services.tipo_actividad_service import TipoActividadService
from src.modelos.services.carrera_service import CarreraService


@pytest.fixture
def carrera_service(test_db_path):
    """Fixture para crear un servicio de carrera para las pruebas."""
    db_path = test_db_path
    service = CarreraService(ruta_db=db_path)
    service.crear_tabla()
    yield service


@pytest.fixture
def carrera_id(carrera_service):
    """Fixture para crear una carrera y retornar su ID."""
    carrera_service.nombre = f"Ingeniería-{uuid.uuid4()}"
    carrera_service.plan = f"Plan-{uuid.uuid4().hex[:4].upper()}"
    carrera_service.modalidad = "Presencial"
    carrera_id = carrera_service.insertar()
    assert carrera_id is not None
    yield carrera_id


@pytest.fixture
def asignatura_service(test_db_path):
    """Fixture para crear un servicio de asignatura para las pruebas."""
    db_path = test_db_path
    service = AsignaturaService(ruta_db=db_path)
    service.crear_tabla()
    yield service


@pytest.fixture
def asignatura_id(asignatura_service, carrera_id):
    """Fixture para crear una asignatura y retornar su ID."""
    asignatura_service.nombre = f"Matemática-{uuid.uuid4()}"
    asignatura_service.codigo = f"MAT-{uuid.uuid4().hex[:4].upper()}"
    asignatura_service.tipo = "Obligatoria"
    asignatura_service.creditos = 4
    asignatura_service.id_carrera = carrera_id
    asignatura_id = asignatura_service.insertar()
    assert asignatura_id is not None
    yield asignatura_id


@pytest.fixture
def eje_tematico_service(test_db_path):
    """Fixture para crear un servicio de eje temático para las pruebas."""
    db_path = test_db_path
    service = EjeTematicoService(ruta_db=db_path)
    service.crear_tabla()
    yield service


@pytest.fixture
def eje_tematico_id(eje_tematico_service, asignatura_id):
    """Fixture para crear un eje temático y retornar su ID."""
    eje_tematico_service.nombre = f"Conceptos-{uuid.uuid4()}"
    eje_tematico_service.orden = 1
    eje_tematico_service.id_asignatura = asignatura_id
    eje_tematico_id = eje_tematico_service.insertar()
    assert eje_tematico_id is not None
    yield eje_tematico_id


@pytest.fixture
def tipo_actividad_service(test_db_path):
    """Fixture para crear un servicio de tipo de actividad para las pruebas."""
    db_path = test_db_path
    service = TipoActividadService(ruta_db=db_path)
    service.crear_tabla()
    yield service


@pytest.fixture
def tipo_actividad_id(tipo_actividad_service):
    """Fixture para crear un tipo de actividad y retornar su ID."""
    tipo_actividad_service.nombre = f"Taller-{uuid.uuid4()}"
    tipo_actividad_service.siglas = "TAL"
    tipo_actividad_id = tipo_actividad_service.insertar()
    assert tipo_actividad_id is not None
    yield tipo_actividad_id


@pytest.fixture
def actividad_service(test_db_path):
    """Fixture para crear un servicio de actividad para las pruebas."""
    db_path = test_db_path
    service = ActividadService(ruta_db=db_path)
    service.crear_tabla()
    yield service


class TestActividadService:
    """Pruebas para el servicio de Actividad."""

    def test_crear_tabla(self, actividad_service):
        """Verifica que la tabla de actividades se cree correctamente."""
        assert Path(actividad_service.dao.ruta_db).exists()

    def test_insertar_valido(self, actividad_service, eje_tematico_id, tipo_actividad_id):
        """Verifica que se puede insertar una actividad válida."""
        actividad_service.titulo = f"Ejercicio-{uuid.uuid4()}"
        actividad_service.id_eje_tematico = eje_tematico_id
        actividad_service.id_tipo_actividad = tipo_actividad_id

        id_insertado = actividad_service.insertar()
        assert id_insertado is not None
        assert isinstance(id_insertado, int)

    def test_eliminar_valido(self, actividad_service, eje_tematico_id, tipo_actividad_id):
        """Verifica que se puede eliminar una actividad válida."""
        actividad_service.titulo = f"Tarea-{uuid.uuid4()}"
        actividad_service.id_eje_tematico = eje_tematico_id
        actividad_service.id_tipo_actividad = tipo_actividad_id
        id_insertado = actividad_service.insertar()

        actividad_service.id_actividad = id_insertado
        resultado = actividad_service.eliminar()
        assert resultado is True

    def test_instanciar_valido(self, actividad_service, eje_tematico_id, tipo_actividad_id):
        """Verifica que se puede instanciar una actividad desde la BD."""
        actividad_service.titulo = f"Proyecto-{uuid.uuid4()}"
        actividad_service.id_eje_tematico = eje_tematico_id
        actividad_service.id_tipo_actividad = tipo_actividad_id
        id_insertado = actividad_service.insertar()

        actividad_service.id_actividad = id_insertado
        resultado = actividad_service.instanciar()
        assert resultado is True

    def test_existe_true(self, actividad_service, eje_tematico_id, tipo_actividad_id):
        """Verifica que existe() retorna True para una actividad que existe."""
        actividad_service.titulo = f"Prueba-{uuid.uuid4()}"
        actividad_service.id_eje_tematico = eje_tematico_id
        actividad_service.id_tipo_actividad = tipo_actividad_id
        id_insertado = actividad_service.insertar()

        actividad_service.id_actividad = id_insertado
        resultado = actividad_service.existe()
        assert resultado is True

    def test_existe_false(self, actividad_service):
        """Verifica que existe() retorna False para una actividad que no existe."""
        actividad_service.id_actividad = 9999
        resultado = actividad_service.existe()
        assert resultado is False

    def test_es_valida_true(self, actividad_service, eje_tematico_id, tipo_actividad_id):
        """Verifica que es_valida() retorna True para una actividad válida."""
        actividad_service.titulo = f"Lección-{uuid.uuid4()}"
        actividad_service.id_eje_tematico = eje_tematico_id
        actividad_service.id_tipo_actividad = tipo_actividad_id

        resultado = actividad_service.es_valida()
        assert resultado is True

    def test_es_valida_titulo_vacio(self, actividad_service, eje_tematico_id, tipo_actividad_id):
        """Verifica que es_valida() retorna False si el título está vacío."""
        actividad_service.titulo = ""
        actividad_service.id_eje_tematico = eje_tematico_id
        actividad_service.id_tipo_actividad = tipo_actividad_id

        resultado = actividad_service.es_valida()
        assert resultado is False

    def test_es_valida_eje_none(self, actividad_service, tipo_actividad_id):
        """Verifica que es_valida() retorna False si id_eje_tematico es None."""
        actividad_service.titulo = f"Test-{uuid.uuid4()}"
        actividad_service.id_eje_tematico = None
        actividad_service.id_tipo_actividad = tipo_actividad_id

        resultado = actividad_service.es_valida()
        assert resultado is False

    def test_es_valida_tipo_none(self, actividad_service, eje_tematico_id):
        """Verifica que es_valida() retorna False si id_tipo_actividad es None."""
        actividad_service.titulo = f"Test-{uuid.uuid4()}"
        actividad_service.id_eje_tematico = eje_tematico_id
        actividad_service.id_tipo_actividad = None

        resultado = actividad_service.es_valida()
        assert resultado is False

    def test_str_representation(self, actividad_service, eje_tematico_id, tipo_actividad_id):
        """Verifica que __str__() funciona correctamente."""
        actividad_service.id_actividad = 1
        actividad_service.titulo = "Test"
        actividad_service.id_eje_tematico = eje_tematico_id
        actividad_service.id_tipo_actividad = tipo_actividad_id

        resultado = str(actividad_service)
        assert "ActividadService" in resultado
        assert "Test" in resultado

    def test_repr_representation(self, actividad_service, eje_tematico_id, tipo_actividad_id):
        """Verifica que __repr__() funciona correctamente."""
        actividad_service.id_actividad = 1
        actividad_service.titulo = "Test"
        actividad_service.id_eje_tematico = eje_tematico_id
        actividad_service.id_tipo_actividad = tipo_actividad_id

        resultado = repr(actividad_service)
        assert "ActividadService" in resultado
