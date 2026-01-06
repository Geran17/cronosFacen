import uuid
import pytest
from pathlib import Path
from src.modelos.services.estudiante_asignatura_service import EstudianteAsignaturaService
from src.modelos.services.estudiante_service import EstudianteService
from src.modelos.services.asignatura_service import AsignaturaService
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
def estudiante_asignatura_service(test_db_path):
    """Fixture para crear un servicio de estudiante asignatura para las pruebas."""
    db_path = test_db_path
    service = EstudianteAsignaturaService(ruta_db=db_path)
    service.crear_tabla()
    yield service


class TestEstudianteAsignaturaService:
    """Pruebas para el servicio de Estudiante Asignatura."""

    def test_crear_tabla(self, estudiante_asignatura_service):
        """Verifica que la tabla de estudiante asignatura se cree correctamente."""
        assert Path(estudiante_asignatura_service.dao.ruta_db).exists()

    def test_insertar_valido(self, estudiante_asignatura_service, estudiante_id, asignatura_id):
        """Verifica que se puede insertar una relación estudiante asignatura válida."""
        estudiante_asignatura_service.id_estudiante = estudiante_id
        estudiante_asignatura_service.id_asignatura = asignatura_id

        id_insertado = estudiante_asignatura_service.insertar()
        assert id_insertado is not None
        assert isinstance(id_insertado, int)

    def test_eliminar_valido(self, estudiante_asignatura_service, estudiante_id, asignatura_id):
        """Verifica que se puede eliminar una relación estudiante asignatura válida."""
        estudiante_asignatura_service.id_estudiante = estudiante_id
        estudiante_asignatura_service.id_asignatura = asignatura_id
        id_insertado = estudiante_asignatura_service.insertar()

        estudiante_asignatura_service.id_estudiante_asignatura = id_insertado
        resultado = estudiante_asignatura_service.eliminar()
        assert resultado is True

    def test_instanciar_valido(self, estudiante_asignatura_service, estudiante_id, asignatura_id):
        """Verifica que se puede instanciar una relación estudiante asignatura desde la BD."""
        estudiante_asignatura_service.id_estudiante = estudiante_id
        estudiante_asignatura_service.id_asignatura = asignatura_id
        id_insertado = estudiante_asignatura_service.insertar()

        estudiante_asignatura_service.id_estudiante_asignatura = id_insertado
        resultado = estudiante_asignatura_service.instanciar()
        assert resultado is True

    def test_existe_true(self, estudiante_asignatura_service, estudiante_id, asignatura_id):
        """Verifica que existe() retorna True para una relación que existe."""
        estudiante_asignatura_service.id_estudiante = estudiante_id
        estudiante_asignatura_service.id_asignatura = asignatura_id
        id_insertado = estudiante_asignatura_service.insertar()

        estudiante_asignatura_service.id_estudiante_asignatura = id_insertado
        resultado = estudiante_asignatura_service.existe()
        assert resultado is True

    def test_existe_false(self, estudiante_asignatura_service):
        """Verifica que existe() retorna False para una relación que no existe."""
        estudiante_asignatura_service.id_estudiante_asignatura = 9999
        resultado = estudiante_asignatura_service.existe()
        assert resultado is False

    def test_es_valida_true(self, estudiante_asignatura_service, estudiante_id, asignatura_id):
        """Verifica que es_valida() retorna True para una relación válida."""
        estudiante_asignatura_service.id_estudiante = estudiante_id
        estudiante_asignatura_service.id_asignatura = asignatura_id

        resultado = estudiante_asignatura_service.es_valida()
        assert resultado is True

    def test_es_valida_estudiante_none(self, estudiante_asignatura_service, asignatura_id):
        """Verifica que es_valida() retorna False si id_estudiante es None."""
        estudiante_asignatura_service.id_estudiante = None
        estudiante_asignatura_service.id_asignatura = asignatura_id

        resultado = estudiante_asignatura_service.es_valida()
        assert resultado is False

    def test_es_valida_asignatura_none(self, estudiante_asignatura_service, estudiante_id):
        """Verifica que es_valida() retorna False si id_asignatura es None."""
        estudiante_asignatura_service.id_estudiante = estudiante_id
        estudiante_asignatura_service.id_asignatura = None

        resultado = estudiante_asignatura_service.es_valida()
        assert resultado is False

    def test_str_representation(self, estudiante_asignatura_service, estudiante_id, asignatura_id):
        """Verifica que __str__() funciona correctamente."""
        estudiante_asignatura_service.id_estudiante_asignatura = 1
        estudiante_asignatura_service.id_estudiante = estudiante_id
        estudiante_asignatura_service.id_asignatura = asignatura_id
        estudiante_asignatura_service.calificacion = 4.5

        resultado = str(estudiante_asignatura_service)
        assert "EstudianteAsignaturaService" in resultado

    def test_repr_representation(self, estudiante_asignatura_service, estudiante_id, asignatura_id):
        """Verifica que __repr__() funciona correctamente."""
        estudiante_asignatura_service.id_estudiante_asignatura = 1
        estudiante_asignatura_service.id_estudiante = estudiante_id
        estudiante_asignatura_service.id_asignatura = asignatura_id

        resultado = repr(estudiante_asignatura_service)
        assert "EstudianteAsignaturaService" in resultado

    def test_insertar_multiples(self, estudiante_asignatura_service, estudiante_id, asignatura_id):
        """Verifica que se pueden insertar múltiples relaciones."""
        # Crear más asignaturas con ID incremental
        ids = []
        for i in range(1, 4):
            estudiante_asignatura_service.id_estudiante = estudiante_id
            estudiante_asignatura_service.id_asignatura = asignatura_id + (i - 1)
            id_insertado = estudiante_asignatura_service.insertar()
            assert id_insertado is not None
            ids.append(id_insertado)

        assert len(ids) == 3

    def test_flujo_completo(self, estudiante_asignatura_service, estudiante_id, asignatura_id):
        """Verifica el flujo completo: insertar, existe, instanciar, eliminar."""
        estudiante_asignatura_service.id_estudiante = estudiante_id
        estudiante_asignatura_service.id_asignatura = asignatura_id

        # Insertar
        id_insertado = estudiante_asignatura_service.insertar()
        assert id_insertado is not None

        # Existe
        estudiante_asignatura_service.id_estudiante_asignatura = id_insertado
        assert estudiante_asignatura_service.existe() is True

        # Instanciar
        assert estudiante_asignatura_service.instanciar() is True

        # Eliminar
        assert estudiante_asignatura_service.eliminar() is True
        assert estudiante_asignatura_service.existe() is False
