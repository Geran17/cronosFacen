import uuid
import pytest
from pathlib import Path
from src.modelos.services.estudiante_actividad_service import EstudianteActividadService
from src.modelos.services.estudiante_service import EstudianteService
from src.modelos.services.actividad_service import ActividadService
from src.modelos.services.carrera_service import CarreraService
from src.modelos.services.asignatura_service import AsignaturaService
from src.modelos.services.eje_tematico_service import EjeTematicoService
from src.modelos.services.tipo_actividad_service import TipoActividadService


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
def estudiante_service(test_db_path):
    """Fixture para crear un servicio de estudiante para las pruebas."""
    db_path = test_db_path
    service = EstudianteService(ruta_db=db_path)
    service.crear_tabla()
    yield service


@pytest.fixture
def estudiante_id(estudiante_service, carrera_id):
    """Fixture para crear un estudiante y retornar su ID."""
    estudiante_service.nombre = f"Juan-{uuid.uuid4()}"
    estudiante_service.correo = f"juan.{uuid.uuid4()}@example.com"
    estudiante_service.id_carrera = carrera_id
    estudiante_id = estudiante_service.insertar()
    assert estudiante_id is not None
    yield estudiante_id


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


@pytest.fixture
def actividad_id(actividad_service, eje_tematico_id, tipo_actividad_id):
    """Fixture para crear una actividad y retornar su ID."""
    actividad_service.titulo = f"Ejercicio-{uuid.uuid4()}"
    actividad_service.id_eje_tematico = eje_tematico_id
    actividad_service.id_tipo_actividad = tipo_actividad_id
    actividad_id = actividad_service.insertar()
    assert actividad_id is not None
    yield actividad_id


@pytest.fixture
def estudiante_actividad_service(test_db_path):
    """Fixture para crear un servicio de estudiante actividad para las pruebas."""
    db_path = test_db_path
    service = EstudianteActividadService(ruta_db=db_path)
    service.crear_tabla()
    yield service


class TestEstudianteActividadService:
    """Pruebas para el servicio de Estudiante Actividad."""

    def test_crear_tabla(self, estudiante_actividad_service):
        """Verifica que la tabla de estudiante actividad se cree correctamente."""
        assert Path(estudiante_actividad_service.dao.ruta_db).exists()

    def test_insertar_valido(self, estudiante_actividad_service, estudiante_id, actividad_id):
        """Verifica que se puede insertar una relación estudiante actividad válida."""
        estudiante_actividad_service.id_estudiante = estudiante_id
        estudiante_actividad_service.id_actividad = actividad_id

        id_insertado = estudiante_actividad_service.insertar()
        assert id_insertado is not None
        assert isinstance(id_insertado, int)

    def test_eliminar_valido(self, estudiante_actividad_service, estudiante_id, actividad_id):
        """Verifica que se puede eliminar una relación estudiante actividad válida."""
        estudiante_actividad_service.id_estudiante = estudiante_id
        estudiante_actividad_service.id_actividad = actividad_id
        id_insertado = estudiante_actividad_service.insertar()

        estudiante_actividad_service.id_estudiante_actividad = id_insertado
        resultado = estudiante_actividad_service.eliminar()
        assert resultado is True

    def test_instanciar_valido(self, estudiante_actividad_service, estudiante_id, actividad_id):
        """Verifica que se puede instanciar una relación estudiante actividad desde la BD."""
        estudiante_actividad_service.id_estudiante = estudiante_id
        estudiante_actividad_service.id_actividad = actividad_id
        id_insertado = estudiante_actividad_service.insertar()

        estudiante_actividad_service.id_estudiante_actividad = id_insertado
        resultado = estudiante_actividad_service.instanciar()
        assert resultado is True

    def test_existe_true(self, estudiante_actividad_service, estudiante_id, actividad_id):
        """Verifica que existe() retorna True para una relación que existe."""
        estudiante_actividad_service.id_estudiante = estudiante_id
        estudiante_actividad_service.id_actividad = actividad_id
        id_insertado = estudiante_actividad_service.insertar()

        estudiante_actividad_service.id_estudiante_actividad = id_insertado
        resultado = estudiante_actividad_service.existe()
        assert resultado is True

    def test_existe_false(self, estudiante_actividad_service):
        """Verifica que existe() retorna False para una relación que no existe."""
        estudiante_actividad_service.id_estudiante_actividad = 9999
        resultado = estudiante_actividad_service.existe()
        assert resultado is False

    def test_es_valida_true(self, estudiante_actividad_service, estudiante_id, actividad_id):
        """Verifica que es_valida() retorna True para una relación válida."""
        estudiante_actividad_service.id_estudiante = estudiante_id
        estudiante_actividad_service.id_actividad = actividad_id

        resultado = estudiante_actividad_service.es_valida()
        assert resultado is True

    def test_es_valida_estudiante_none(self, estudiante_actividad_service, actividad_id):
        """Verifica que es_valida() retorna False si id_estudiante es None."""
        estudiante_actividad_service.id_estudiante = None
        estudiante_actividad_service.id_actividad = actividad_id

        resultado = estudiante_actividad_service.es_valida()
        assert resultado is False

    def test_es_valida_actividad_none(self, estudiante_actividad_service, estudiante_id):
        """Verifica que es_valida() retorna False si id_actividad es None."""
        estudiante_actividad_service.id_estudiante = estudiante_id
        estudiante_actividad_service.id_actividad = None

        resultado = estudiante_actividad_service.es_valida()
        assert resultado is False

    def test_str_representation(self, estudiante_actividad_service, estudiante_id, actividad_id):
        """Verifica que __str__() funciona correctamente."""
        estudiante_actividad_service.id_estudiante_actividad = 1
        estudiante_actividad_service.id_estudiante = estudiante_id
        estudiante_actividad_service.id_actividad = actividad_id
        estudiante_actividad_service.completada = True

        resultado = str(estudiante_actividad_service)
        assert "EstudianteActividadService" in resultado

    def test_repr_representation(self, estudiante_actividad_service, estudiante_id, actividad_id):
        """Verifica que __repr__() funciona correctamente."""
        estudiante_actividad_service.id_estudiante_actividad = 1
        estudiante_actividad_service.id_estudiante = estudiante_id
        estudiante_actividad_service.id_actividad = actividad_id

        resultado = repr(estudiante_actividad_service)
        assert "EstudianteActividadService" in resultado

    def test_insertar_multiples(self, estudiante_actividad_service, estudiante_id, actividad_id):
        """Verifica que se pueden insertar múltiples relaciones."""
        ids = []
        for i in range(1, 4):
            estudiante_actividad_service.id_estudiante = estudiante_id
            estudiante_actividad_service.id_actividad = actividad_id + (i - 1)
            id_insertado = estudiante_actividad_service.insertar()
            assert id_insertado is not None
            ids.append(id_insertado)

        assert len(ids) == 3

    def test_flujo_completo(self, estudiante_actividad_service, estudiante_id, actividad_id):
        """Verifica el flujo completo: insertar, existe, instanciar, eliminar."""
        estudiante_actividad_service.id_estudiante = estudiante_id
        estudiante_actividad_service.id_actividad = actividad_id

        # Insertar
        id_insertado = estudiante_actividad_service.insertar()
        assert id_insertado is not None

        # Existe
        estudiante_actividad_service.id_estudiante_actividad = id_insertado
        assert estudiante_actividad_service.existe() is True

        # Instanciar
        assert estudiante_actividad_service.instanciar() is True

        # Eliminar
        assert estudiante_actividad_service.eliminar() is True
        assert estudiante_actividad_service.existe() is False
