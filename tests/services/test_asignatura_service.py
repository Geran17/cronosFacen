import uuid
import pytest
from pathlib import Path
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


class TestAsignaturaService:
    """Pruebas para el servicio de Asignatura."""

    def test_crear_tabla(self, asignatura_service):
        """Verifica que la tabla de asignaturas se cree correctamente."""
        assert Path(asignatura_service.dao.ruta_db).exists()

    def test_insertar_valido(self, asignatura_service, carrera_id):
        """Verifica que se puede insertar una asignatura válida."""
        asignatura_service.nombre = f"Matemática-{uuid.uuid4()}"
        asignatura_service.codigo = f"MAT-{uuid.uuid4().hex[:4].upper()}"
        asignatura_service.tipo = "Obligatoria"
        asignatura_service.creditos = 4
        asignatura_service.id_carrera = carrera_id

        id_insertado = asignatura_service.insertar()
        assert id_insertado is not None
        assert isinstance(id_insertado, int)

    def test_eliminar_valido(self, asignatura_service, carrera_id):
        """Verifica que se puede eliminar una asignatura válida."""
        asignatura_service.nombre = f"Física-{uuid.uuid4()}"
        asignatura_service.codigo = f"FIS-{uuid.uuid4().hex[:4].upper()}"
        asignatura_service.tipo = "Optativa"
        asignatura_service.creditos = 3
        asignatura_service.id_carrera = carrera_id
        id_insertado = asignatura_service.insertar()

        asignatura_service.id_asignatura = id_insertado
        resultado = asignatura_service.eliminar()
        assert resultado is True

    def test_instanciar_valido(self, asignatura_service, carrera_id):
        """Verifica que se puede instanciar una asignatura desde la BD."""
        asignatura_service.nombre = f"Química-{uuid.uuid4()}"
        asignatura_service.codigo = f"QUI-{uuid.uuid4().hex[:4].upper()}"
        asignatura_service.tipo = "Obligatoria"
        asignatura_service.creditos = 5
        asignatura_service.id_carrera = carrera_id
        id_insertado = asignatura_service.insertar()

        asignatura_service.id_asignatura = id_insertado
        resultado = asignatura_service.instanciar()
        assert resultado is True

    def test_existe_true(self, asignatura_service, carrera_id):
        """Verifica que existe() retorna True para una asignatura que existe."""
        asignatura_service.nombre = f"Biología-{uuid.uuid4()}"
        asignatura_service.codigo = f"BIO-{uuid.uuid4().hex[:4].upper()}"
        asignatura_service.tipo = "Obligatoria"
        asignatura_service.creditos = 4
        asignatura_service.id_carrera = carrera_id
        id_insertado = asignatura_service.insertar()

        asignatura_service.id_asignatura = id_insertado
        resultado = asignatura_service.existe()
        assert resultado is True

    def test_existe_false(self, asignatura_service):
        """Verifica que existe() retorna False para una asignatura que no existe."""
        asignatura_service.id_asignatura = 9999
        resultado = asignatura_service.existe()
        assert resultado is False

    def test_es_valida_true(self, asignatura_service, carrera_id):
        """Verifica que es_valida() retorna True para una asignatura válida."""
        asignatura_service.nombre = f"Historia-{uuid.uuid4()}"
        asignatura_service.codigo = f"HIS-{uuid.uuid4().hex[:4].upper()}"
        asignatura_service.tipo = "Obligatoria"
        asignatura_service.creditos = 3
        asignatura_service.id_carrera = carrera_id

        resultado = asignatura_service.es_valida()
        assert resultado is True

    def test_es_valida_nombre_vacio(self, asignatura_service, carrera_id):
        """Verifica que es_valida() retorna False si el nombre está vacío."""
        asignatura_service.nombre = ""
        asignatura_service.codigo = f"TST-{uuid.uuid4().hex[:4].upper()}"
        asignatura_service.tipo = "Obligatoria"
        asignatura_service.creditos = 3
        asignatura_service.id_carrera = carrera_id

        resultado = asignatura_service.es_valida()
        assert resultado is False

    def test_es_valida_codigo_vacio(self, asignatura_service, carrera_id):
        """Verifica que es_valida() retorna False si el código está vacío."""
        asignatura_service.nombre = f"Test-{uuid.uuid4()}"
        asignatura_service.codigo = ""
        asignatura_service.tipo = "Obligatoria"
        asignatura_service.creditos = 3
        asignatura_service.id_carrera = carrera_id

        resultado = asignatura_service.es_valida()
        assert resultado is False

    def test_es_valida_tipo_vacio(self, asignatura_service, carrera_id):
        """Verifica que es_valida() retorna False si el tipo está vacío."""
        asignatura_service.nombre = f"Test-{uuid.uuid4()}"
        asignatura_service.codigo = f"TST-{uuid.uuid4().hex[:4].upper()}"
        asignatura_service.tipo = ""
        asignatura_service.creditos = 3
        asignatura_service.id_carrera = carrera_id

        resultado = asignatura_service.es_valida()
        assert resultado is False

    def test_es_valida_creditos_cero(self, asignatura_service, carrera_id):
        """Verifica que es_valida() retorna False si los créditos son cero o negativos."""
        asignatura_service.nombre = f"Test-{uuid.uuid4()}"
        asignatura_service.codigo = f"TST-{uuid.uuid4().hex[:4].upper()}"
        asignatura_service.tipo = "Obligatoria"
        asignatura_service.creditos = 0
        asignatura_service.id_carrera = carrera_id

        resultado = asignatura_service.es_valida()
        assert resultado is False

    def test_es_valida_carrera_none(self, asignatura_service):
        """Verifica que es_valida() retorna False si id_carrera es None."""
        asignatura_service.nombre = f"Test-{uuid.uuid4()}"
        asignatura_service.codigo = f"TST-{uuid.uuid4().hex[:4].upper()}"
        asignatura_service.tipo = "Obligatoria"
        asignatura_service.creditos = 3
        asignatura_service.id_carrera = None

        resultado = asignatura_service.es_valida()
        assert resultado is False

    def test_str_representation(self, asignatura_service, carrera_id):
        """Verifica que __str__() funciona correctamente."""
        asignatura_service.id_asignatura = 1
        asignatura_service.nombre = "Test"
        asignatura_service.codigo = "TST"
        asignatura_service.tipo = "Obligatoria"
        asignatura_service.creditos = 3
        asignatura_service.id_carrera = carrera_id

        resultado = str(asignatura_service)
        assert "AsignaturaService" in resultado
        assert "Test" in resultado
        assert "TST" in resultado

    def test_repr_representation(self, asignatura_service, carrera_id):
        """Verifica que __repr__() funciona correctamente."""
        asignatura_service.id_asignatura = 1
        asignatura_service.nombre = "Test"
        asignatura_service.codigo = "TST"
        asignatura_service.tipo = "Obligatoria"
        asignatura_service.creditos = 3
        asignatura_service.id_carrera = carrera_id

        resultado = repr(asignatura_service)
        assert "AsignaturaService" in resultado

    def test_insertar_multiples(self, asignatura_service, carrera_id):
        """Verifica que se pueden insertar múltiples asignaturas."""
        ids = []
        for i in range(3):
            asignatura_service.nombre = f"Asignatura-{uuid.uuid4()}"
            asignatura_service.codigo = f"ASG-{i}"
            asignatura_service.tipo = "Obligatoria"
            asignatura_service.creditos = 3 + i
            asignatura_service.id_carrera = carrera_id
            id_insertado = asignatura_service.insertar()
            assert id_insertado is not None
            ids.append(id_insertado)

        assert len(ids) == 3
        assert len(set(ids)) == 3  # Todos deben ser únicos

    def test_flujo_completo(self, asignatura_service, carrera_id):
        """Verifica el flujo completo: insertar, existe, instanciar, eliminar."""
        asignatura_service.nombre = f"Completo-{uuid.uuid4()}"
        asignatura_service.codigo = f"CMP-{uuid.uuid4().hex[:4].upper()}"
        asignatura_service.tipo = "Obligatoria"
        asignatura_service.creditos = 4
        asignatura_service.id_carrera = carrera_id

        # Insertar
        id_insertado = asignatura_service.insertar()
        assert id_insertado is not None

        # Existe
        asignatura_service.id_asignatura = id_insertado
        assert asignatura_service.existe() is True

        # Instanciar
        assert asignatura_service.instanciar() is True

        # Eliminar
        assert asignatura_service.eliminar() is True
        assert asignatura_service.existe() is False
