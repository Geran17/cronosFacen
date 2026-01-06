import uuid
import pytest
from pathlib import Path
from src.modelos.services.eje_tematico_service import EjeTematicoService
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


class TestEjeTematicoService:
    """Pruebas para el servicio de Eje Temático."""

    def test_crear_tabla(self, eje_tematico_service):
        """Verifica que la tabla de ejes temáticos se cree correctamente."""
        assert Path(eje_tematico_service.dao.ruta_db).exists()

    def test_insertar_valido(self, eje_tematico_service, asignatura_id):
        """Verifica que se puede insertar un eje temático válido."""
        eje_tematico_service.nombre = f"Conceptos Básicos-{uuid.uuid4()}"
        eje_tematico_service.orden = 1
        eje_tematico_service.id_asignatura = asignatura_id

        id_insertado = eje_tematico_service.insertar()
        assert id_insertado is not None
        assert isinstance(id_insertado, int)

    def test_eliminar_valido(self, eje_tematico_service, asignatura_id):
        """Verifica que se puede eliminar un eje temático válido."""
        eje_tematico_service.nombre = f"Definiciones-{uuid.uuid4()}"
        eje_tematico_service.orden = 2
        eje_tematico_service.id_asignatura = asignatura_id
        id_insertado = eje_tematico_service.insertar()

        eje_tematico_service.id_eje_tematico = id_insertado
        resultado = eje_tematico_service.eliminar()
        assert resultado is True

    def test_instanciar_valido(self, eje_tematico_service, asignatura_id):
        """Verifica que se puede instanciar un eje temático desde la BD."""
        eje_tematico_service.nombre = f"Aplicaciones-{uuid.uuid4()}"
        eje_tematico_service.orden = 3
        eje_tematico_service.id_asignatura = asignatura_id
        id_insertado = eje_tematico_service.insertar()

        eje_tematico_service.id_eje_tematico = id_insertado
        resultado = eje_tematico_service.instanciar()
        assert resultado is True

    def test_existe_true(self, eje_tematico_service, asignatura_id):
        """Verifica que existe() retorna True para un eje temático que existe."""
        eje_tematico_service.nombre = f"Ejercicios-{uuid.uuid4()}"
        eje_tematico_service.orden = 4
        eje_tematico_service.id_asignatura = asignatura_id
        id_insertado = eje_tematico_service.insertar()

        eje_tematico_service.id_eje_tematico = id_insertado
        resultado = eje_tematico_service.existe()
        assert resultado is True

    def test_existe_false(self, eje_tematico_service):
        """Verifica que existe() retorna False para un eje temático que no existe."""
        eje_tematico_service.id_eje_tematico = 9999
        resultado = eje_tematico_service.existe()
        assert resultado is False

    def test_es_valida_true(self, eje_tematico_service, asignatura_id):
        """Verifica que es_valida() retorna True para un eje temático válido."""
        eje_tematico_service.nombre = f"Problemas-{uuid.uuid4()}"
        eje_tematico_service.orden = 5
        eje_tematico_service.id_asignatura = asignatura_id

        resultado = eje_tematico_service.es_valida()
        assert resultado is True

    def test_es_valida_nombre_vacio(self, eje_tematico_service, asignatura_id):
        """Verifica que es_valida() retorna False si el nombre está vacío."""
        eje_tematico_service.nombre = ""
        eje_tematico_service.orden = 1
        eje_tematico_service.id_asignatura = asignatura_id

        resultado = eje_tematico_service.es_valida()
        assert resultado is False

    def test_es_valida_orden_negativo(self, eje_tematico_service, asignatura_id):
        """Verifica que es_valida() retorna False si orden es negativo."""
        eje_tematico_service.nombre = f"Test-{uuid.uuid4()}"
        eje_tematico_service.orden = -1
        eje_tematico_service.id_asignatura = asignatura_id

        resultado = eje_tematico_service.es_valida()
        assert resultado is False

    def test_es_valida_asignatura_none(self, eje_tematico_service):
        """Verifica que es_valida() retorna False si id_asignatura es None."""
        eje_tematico_service.nombre = f"Test-{uuid.uuid4()}"
        eje_tematico_service.orden = 1
        eje_tematico_service.id_asignatura = None

        resultado = eje_tematico_service.es_valida()
        assert resultado is False

    def test_str_representation(self, eje_tematico_service, asignatura_id):
        """Verifica que __str__() funciona correctamente."""
        eje_tematico_service.id_eje_tematico = 1
        eje_tematico_service.nombre = "Test"
        eje_tematico_service.orden = 1
        eje_tematico_service.id_asignatura = asignatura_id

        resultado = str(eje_tematico_service)
        assert "EjeTematicoService" in resultado
        assert "Test" in resultado

    def test_repr_representation(self, eje_tematico_service, asignatura_id):
        """Verifica que __repr__() funciona correctamente."""
        eje_tematico_service.id_eje_tematico = 1
        eje_tematico_service.nombre = "Test"
        eje_tematico_service.orden = 1
        eje_tematico_service.id_asignatura = asignatura_id

        resultado = repr(eje_tematico_service)
        assert "EjeTematicoService" in resultado
