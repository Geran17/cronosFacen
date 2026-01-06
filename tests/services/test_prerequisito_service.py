import uuid
import pytest
from pathlib import Path
from src.modelos.services.prerequisito_service import PrerrequisitoService
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
def asignatura_service(test_db_path):
    """Fixture para crear un servicio de asignatura para las pruebas."""
    db_path = test_db_path
    service = AsignaturaService(ruta_db=db_path)
    service.crear_tabla()
    yield service


@pytest.fixture
def asignatura_ids(asignatura_service, carrera_id):
    """Fixture para crear dos asignaturas y retornar sus IDs."""
    asignatura_ids = []
    for i in range(2):
        asignatura_service.nombre = f"Asignatura-{uuid.uuid4()}"
        asignatura_service.codigo = f"ASI-{uuid.uuid4().hex[:4].upper()}"
        asignatura_service.tipo = "Obligatoria"
        asignatura_service.creditos = 4
        asignatura_service.id_carrera = carrera_id
        asignatura_id = asignatura_service.insertar()
        assert asignatura_id is not None
        asignatura_ids.append(asignatura_id)
    yield asignatura_ids


@pytest.fixture
def prerequisito_service(test_db_path):
    """Fixture para crear un servicio de prerequisito para las pruebas."""
    db_path = test_db_path
    service = PrerrequisitoService(ruta_db=db_path)
    service.crear_tabla()
    yield service


class TestPrerrequisitoService:
    """Pruebas para el servicio de Prerrequisito."""

    def test_crear_tabla(self, prerequisito_service):
        """Verifica que la tabla de prerrequisitos se cree correctamente."""
        assert Path(prerequisito_service.dao.ruta_db).exists()

    def test_insertar_valido(self, prerequisito_service, asignatura_ids):
        """Verifica que se puede insertar un prerrequisito válido."""
        prerequisito_service.id_asignatura = asignatura_ids[0]
        prerequisito_service.id_asignatura_prerrequisito = asignatura_ids[1]

        id_insertado = prerequisito_service.insertar()
        assert id_insertado is not None
        assert isinstance(id_insertado, int)

    def test_eliminar_valido(self, prerequisito_service, asignatura_ids):
        """Verifica que se puede eliminar un prerrequisito válido."""
        prerequisito_service.id_asignatura = asignatura_ids[0]
        prerequisito_service.id_asignatura_prerrequisito = asignatura_ids[1]
        id_insertado = prerequisito_service.insertar()

        prerequisito_service.id_prerequisito = id_insertado
        resultado = prerequisito_service.eliminar()
        assert resultado is True

    def test_instanciar_valido(self, prerequisito_service, asignatura_ids):
        """Verifica que se puede instanciar un prerrequisito desde la BD."""
        prerequisito_service.id_asignatura = asignatura_ids[0]
        prerequisito_service.id_asignatura_prerrequisito = asignatura_ids[1]
        id_insertado = prerequisito_service.insertar()

        prerequisito_service.id_prerequisito = id_insertado
        resultado = prerequisito_service.instanciar()
        assert resultado is True

    def test_existe_true(self, prerequisito_service, asignatura_ids):
        """Verifica que existe() retorna True para un prerrequisito que existe."""
        prerequisito_service.id_asignatura = asignatura_ids[0]
        prerequisito_service.id_asignatura_prerrequisito = asignatura_ids[1]
        id_insertado = prerequisito_service.insertar()

        prerequisito_service.id_prerequisito = id_insertado
        resultado = prerequisito_service.existe()
        assert resultado is True

    def test_existe_false(self, prerequisito_service):
        """Verifica que existe() retorna False para un prerrequisito que no existe."""
        prerequisito_service.id_prerequisito = 9999
        resultado = prerequisito_service.existe()
        assert resultado is False

    def test_es_valida_true(self, prerequisito_service, asignatura_ids):
        """Verifica que es_valida() retorna True para un prerrequisito válido."""
        prerequisito_service.id_asignatura = asignatura_ids[0]
        prerequisito_service.id_asignatura_prerrequisito = asignatura_ids[1]

        resultado = prerequisito_service.es_valida()
        assert resultado is True

    def test_es_valida_asignatura_none(self, prerequisito_service, asignatura_ids):
        """Verifica que es_valida() retorna False si id_asignatura es None."""
        prerequisito_service.id_asignatura = None
        prerequisito_service.id_asignatura_prerrequisito = asignatura_ids[1]

        resultado = prerequisito_service.es_valida()
        assert resultado is False

    def test_es_valida_prerequisito_none(self, prerequisito_service, asignatura_ids):
        """Verifica que es_valida() retorna False si id_asignatura_prerrequisito es None."""
        prerequisito_service.id_asignatura = asignatura_ids[0]
        prerequisito_service.id_asignatura_prerrequisito = None

        resultado = prerequisito_service.es_valida()
        assert resultado is False

    def test_es_valida_mismo_id(self, prerequisito_service, asignatura_ids):
        """Verifica que es_valida() retorna False si ambas asignaturas son iguales."""
        prerequisito_service.id_asignatura = asignatura_ids[0]
        prerequisito_service.id_asignatura_prerrequisito = asignatura_ids[0]

        resultado = prerequisito_service.es_valida()
        assert resultado is False

    def test_str_representation(self, prerequisito_service, asignatura_ids):
        """Verifica que __str__() funciona correctamente."""
        prerequisito_service.id_prerequisito = 1
        prerequisito_service.id_asignatura = asignatura_ids[0]
        prerequisito_service.id_asignatura_prerrequisito = asignatura_ids[1]

        resultado = str(prerequisito_service)
        assert "PrerrequisitoService" in resultado

    def test_repr_representation(self, prerequisito_service, asignatura_ids):
        """Verifica que __repr__() funciona correctamente."""
        prerequisito_service.id_prerequisito = 1
        prerequisito_service.id_asignatura = asignatura_ids[0]
        prerequisito_service.id_asignatura_prerrequisito = asignatura_ids[1]

        resultado = repr(prerequisito_service)
        assert "PrerrequisitoService" in resultado

    def test_flujo_completo(self, prerequisito_service, asignatura_ids):
        """Verifica el flujo completo: insertar, existe, instanciar, eliminar."""
        prerequisito_service.id_asignatura = asignatura_ids[0]
        prerequisito_service.id_asignatura_prerrequisito = asignatura_ids[1]

        # Insertar
        id_insertado = prerequisito_service.insertar()
        assert id_insertado is not None

        # Existe
        prerequisito_service.id_prerequisito = id_insertado
        assert prerequisito_service.existe() is True

        # Instanciar
        assert prerequisito_service.instanciar() is True

        # Eliminar
        assert prerequisito_service.eliminar() is True
        assert prerequisito_service.existe() is False
