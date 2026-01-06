import uuid
import pytest
from pathlib import Path
from src.modelos.services.estudiante_service import EstudianteService
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


class TestEstudianteService:
    """Pruebas para el servicio de Estudiante."""

    def test_crear_tabla(self, estudiante_service):
        """Verifica que la tabla de estudiantes se cree correctamente."""
        assert Path(estudiante_service.dao.ruta_db).exists()

    def test_insertar_valido(self, estudiante_service, carrera_id):
        """Verifica que se puede insertar un estudiante válido."""
        estudiante_service.nombre = f"Juan-{uuid.uuid4()}"
        estudiante_service.correo = f"juan.{uuid.uuid4()}@example.com"
        estudiante_service.id_carrera = carrera_id

        id_insertado = estudiante_service.insertar()
        assert id_insertado is not None
        assert isinstance(id_insertado, int)

    def test_eliminar_valido(self, estudiante_service, carrera_id):
        """Verifica que se puede eliminar un estudiante válido."""
        estudiante_service.nombre = f"Maria-{uuid.uuid4()}"
        estudiante_service.correo = f"maria.{uuid.uuid4()}@example.com"
        estudiante_service.id_carrera = carrera_id
        id_insertado = estudiante_service.insertar()

        estudiante_service.id_estudiante = id_insertado
        resultado = estudiante_service.eliminar()
        assert resultado is True

    def test_instanciar_valido(self, estudiante_service, carrera_id):
        """Verifica que se puede instanciar un estudiante desde la BD."""
        estudiante_service.nombre = f"Pedro-{uuid.uuid4()}"
        estudiante_service.correo = f"pedro.{uuid.uuid4()}@example.com"
        estudiante_service.id_carrera = carrera_id
        id_insertado = estudiante_service.insertar()

        estudiante_service.id_estudiante = id_insertado
        resultado = estudiante_service.instanciar()
        assert resultado is True

    def test_existe_true(self, estudiante_service, carrera_id):
        """Verifica que existe() retorna True para un estudiante que existe."""
        estudiante_service.nombre = f"Ana-{uuid.uuid4()}"
        estudiante_service.correo = f"ana.{uuid.uuid4()}@example.com"
        estudiante_service.id_carrera = carrera_id
        id_insertado = estudiante_service.insertar()

        estudiante_service.id_estudiante = id_insertado
        resultado = estudiante_service.existe()
        assert resultado is True

    def test_existe_false(self, estudiante_service):
        """Verifica que existe() retorna False para un estudiante que no existe."""
        estudiante_service.id_estudiante = 9999
        resultado = estudiante_service.existe()
        assert resultado is False

    def test_es_valida_true(self, estudiante_service, carrera_id):
        """Verifica que es_valida() retorna True para un estudiante válido."""
        estudiante_service.nombre = f"Luis-{uuid.uuid4()}"
        estudiante_service.correo = f"luis.{uuid.uuid4()}@example.com"
        estudiante_service.id_carrera = carrera_id

        resultado = estudiante_service.es_valida()
        assert resultado is True

    def test_es_valida_nombre_vacio(self, estudiante_service, carrera_id):
        """Verifica que es_valida() retorna False si el nombre está vacío."""
        estudiante_service.nombre = ""
        estudiante_service.correo = f"test.{uuid.uuid4()}@example.com"
        estudiante_service.id_carrera = carrera_id

        resultado = estudiante_service.es_valida()
        assert resultado is False

    def test_es_valida_correo_vacio(self, estudiante_service, carrera_id):
        """Verifica que es_valida() retorna False si el correo está vacío."""
        estudiante_service.nombre = f"Test-{uuid.uuid4()}"
        estudiante_service.correo = ""
        estudiante_service.id_carrera = carrera_id

        resultado = estudiante_service.es_valida()
        assert resultado is False

    def test_es_valida_correo_invalido(self, estudiante_service, carrera_id):
        """Verifica que es_valida() retorna False si el correo es inválido."""
        estudiante_service.nombre = f"Test-{uuid.uuid4()}"
        estudiante_service.correo = "correo_invalido"
        estudiante_service.id_carrera = carrera_id

        resultado = estudiante_service.es_valida()
        assert resultado is False

    def test_es_valida_carrera_none(self, estudiante_service):
        """Verifica que es_valida() retorna False si id_carrera es None."""
        estudiante_service.nombre = f"Test-{uuid.uuid4()}"
        estudiante_service.correo = f"test.{uuid.uuid4()}@example.com"
        estudiante_service.id_carrera = None

        resultado = estudiante_service.es_valida()
        assert resultado is False

    def test_str_representation(self, estudiante_service, carrera_id):
        """Verifica que __str__() funciona correctamente."""
        estudiante_service.id_estudiante = 1
        estudiante_service.nombre = "Test"
        estudiante_service.correo = "test@example.com"
        estudiante_service.id_carrera = carrera_id

        resultado = str(estudiante_service)
        assert "EstudianteService" in resultado
        assert "Test" in resultado
        assert "test@example.com" in resultado

    def test_repr_representation(self, estudiante_service, carrera_id):
        """Verifica que __repr__() funciona correctamente."""
        estudiante_service.id_estudiante = 1
        estudiante_service.nombre = "Test"
        estudiante_service.correo = "test@example.com"
        estudiante_service.id_carrera = carrera_id

        resultado = repr(estudiante_service)
        assert "EstudianteService" in resultado
