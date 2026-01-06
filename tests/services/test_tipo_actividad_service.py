import uuid
import pytest
from pathlib import Path
from src.modelos.services.tipo_actividad_service import TipoActividadService


@pytest.fixture
def tipo_actividad_service(test_db_path):
    """Fixture para crear un servicio de tipo de actividad para las pruebas."""
    db_path = test_db_path
    service = TipoActividadService(ruta_db=db_path)
    service.crear_tabla()
    yield service


class TestTipoActividadService:
    """Pruebas para el servicio de Tipo de Actividad."""

    def test_crear_tabla(self, tipo_actividad_service):
        """Verifica que la tabla de tipos de actividad se cree correctamente."""
        assert Path(tipo_actividad_service.dao.ruta_db).exists()

    def test_insertar_valido(self, tipo_actividad_service):
        """Verifica que se puede insertar un tipo de actividad válido."""
        tipo_actividad_service.nombre = f"Taller-{uuid.uuid4()}"
        tipo_actividad_service.siglas = f"TAL-{uuid.uuid4().hex[:2].upper()}"

        id_insertado = tipo_actividad_service.insertar()
        assert id_insertado is not None
        assert isinstance(id_insertado, int)

    def test_eliminar_valido(self, tipo_actividad_service):
        """Verifica que se puede eliminar un tipo de actividad válido."""
        tipo_actividad_service.nombre = f"Conferencia-{uuid.uuid4()}"
        tipo_actividad_service.siglas = f"CONF-{uuid.uuid4().hex[:2].upper()}"
        id_insertado = tipo_actividad_service.insertar()

        tipo_actividad_service.id_tipo_actividad = id_insertado
        resultado = tipo_actividad_service.eliminar()
        assert resultado is True

    def test_instanciar_valido(self, tipo_actividad_service):
        """Verifica que se puede instanciar un tipo de actividad desde la BD."""
        tipo_actividad_service.nombre = f"Práctica-{uuid.uuid4()}"
        tipo_actividad_service.siglas = f"PRAC-{uuid.uuid4().hex[:2].upper()}"
        id_insertado = tipo_actividad_service.insertar()

        tipo_actividad_service.id_tipo_actividad = id_insertado
        resultado = tipo_actividad_service.instanciar()
        assert resultado is True

    def test_existe_true(self, tipo_actividad_service):
        """Verifica que existe() retorna True para un tipo de actividad que existe."""
        tipo_actividad_service.nombre = f"Seminario-{uuid.uuid4()}"
        tipo_actividad_service.siglas = f"SEM-{uuid.uuid4().hex[:2].upper()}"
        id_insertado = tipo_actividad_service.insertar()

        tipo_actividad_service.id_tipo_actividad = id_insertado
        resultado = tipo_actividad_service.existe()
        assert resultado is True

    def test_existe_false(self, tipo_actividad_service):
        """Verifica que existe() retorna False para un tipo de actividad que no existe."""
        tipo_actividad_service.id_tipo_actividad = 9999
        resultado = tipo_actividad_service.existe()
        assert resultado is False

    def test_es_valida_true(self, tipo_actividad_service):
        """Verifica que es_valida() retorna True para un tipo de actividad válido."""
        tipo_actividad_service.nombre = f"Clase-{uuid.uuid4()}"
        tipo_actividad_service.siglas = f"CLA-{uuid.uuid4().hex[:2].upper()}"

        resultado = tipo_actividad_service.es_valida()
        assert resultado is True

    def test_es_valida_nombre_vacio(self, tipo_actividad_service):
        """Verifica que es_valida() retorna False si el nombre está vacío."""
        tipo_actividad_service.nombre = ""
        tipo_actividad_service.siglas = f"TST-{uuid.uuid4().hex[:2].upper()}"

        resultado = tipo_actividad_service.es_valida()
        assert resultado is False

    def test_es_valida_siglas_vacio(self, tipo_actividad_service):
        """Verifica que es_valida() retorna False si las siglas están vacías."""
        tipo_actividad_service.nombre = f"Test-{uuid.uuid4()}"
        tipo_actividad_service.siglas = ""

        resultado = tipo_actividad_service.es_valida()
        assert resultado is False

    def test_str_representation(self, tipo_actividad_service):
        """Verifica que __str__() funciona correctamente."""
        tipo_actividad_service.id_tipo_actividad = 1
        tipo_actividad_service.nombre = "Test"
        tipo_actividad_service.siglas = f"TST-{uuid.uuid4().hex[:2].upper()}"

        resultado = str(tipo_actividad_service)
        assert "TipoActividadService" in resultado
        assert "Test" in resultado
        assert "TST" in resultado

    def test_repr_representation(self, tipo_actividad_service):
        """Verifica que __repr__() funciona correctamente."""
        tipo_actividad_service.id_tipo_actividad = 1
        tipo_actividad_service.nombre = "Test"
        tipo_actividad_service.siglas = f"TST-{uuid.uuid4().hex[:2].upper()}"

        resultado = repr(tipo_actividad_service)
        assert "TipoActividadService" in resultado

    def test_insertar_multiples(self, tipo_actividad_service):
        """Verifica que se pueden insertar múltiples tipos de actividad."""
        ids = []
        for i in range(3):
            tipo_actividad_service.nombre = f"Tipo-{uuid.uuid4()}"
            tipo_actividad_service.siglas = f"TP{i}"
            id_insertado = tipo_actividad_service.insertar()
            assert id_insertado is not None
            ids.append(id_insertado)

        assert len(ids) == 3
        assert len(set(ids)) == 3  # Todos deben ser únicos

    def test_flujo_completo(self, tipo_actividad_service):
        """Verifica el flujo completo: insertar, existe, instanciar, eliminar."""
        tipo_actividad_service.nombre = f"Completo-{uuid.uuid4()}"
        tipo_actividad_service.siglas = f"CMP-{uuid.uuid4().hex[:2].upper()}"

        # Insertar
        id_insertado = tipo_actividad_service.insertar()
        assert id_insertado is not None

        # Existe
        tipo_actividad_service.id_tipo_actividad = id_insertado
        assert tipo_actividad_service.existe() is True

        # Instanciar
        assert tipo_actividad_service.instanciar() is True

        # Eliminar
        assert tipo_actividad_service.eliminar() is True
        assert tipo_actividad_service.existe() is False
