import uuid
import pytest
from pathlib import Path
from src.modelos.services.calendario_evento_service import CalendarioEventoService
from datetime import datetime


@pytest.fixture
def calendario_evento_service(test_db_path):
    """Fixture para crear un servicio de evento de calendario para las pruebas."""
    db_path = test_db_path
    service = CalendarioEventoService(ruta_db=db_path)
    service.crear_tabla()
    yield service


class TestCalendarioEventoService:
    """Pruebas para el servicio de Calendario Evento."""

    def test_crear_tabla(self, calendario_evento_service):
        """Verifica que la tabla de eventos de calendario se cree correctamente."""
        assert Path(calendario_evento_service.dao.ruta_db).exists()

    def test_insertar_valido(self, calendario_evento_service):
        """Verifica que se puede insertar un evento de calendario válido."""
        calendario_evento_service.nombre = f"Examen-{uuid.uuid4()}"
        calendario_evento_service.fecha_inicio = datetime(2024, 6, 1, 10, 0)

        id_insertado = calendario_evento_service.insertar()
        assert id_insertado is not None
        assert isinstance(id_insertado, int)

    def test_eliminar_valido(self, calendario_evento_service):
        """Verifica que se puede eliminar un evento de calendario válido."""
        calendario_evento_service.nombre = f"Conferencia-{uuid.uuid4()}"
        calendario_evento_service.fecha_inicio = datetime(2024, 7, 1, 14, 0)
        id_insertado = calendario_evento_service.insertar()

        calendario_evento_service.id_calendario_evento = id_insertado
        resultado = calendario_evento_service.eliminar()
        assert resultado is True

    def test_instanciar_valido(self, calendario_evento_service):
        """Verifica que se puede instanciar un evento de calendario desde la BD."""
        calendario_evento_service.nombre = f"Taller-{uuid.uuid4()}"
        calendario_evento_service.fecha_inicio = datetime(2024, 8, 1, 9, 0)
        id_insertado = calendario_evento_service.insertar()

        calendario_evento_service.id_calendario_evento = id_insertado
        resultado = calendario_evento_service.instanciar()
        assert resultado is True

    def test_existe_true(self, calendario_evento_service):
        """Verifica que existe() retorna True para un evento que existe."""
        calendario_evento_service.nombre = f"Seminario-{uuid.uuid4()}"
        calendario_evento_service.fecha_inicio = datetime(2024, 9, 1, 11, 0)
        id_insertado = calendario_evento_service.insertar()

        calendario_evento_service.id_calendario_evento = id_insertado
        resultado = calendario_evento_service.existe()
        assert resultado is True

    def test_existe_false(self, calendario_evento_service):
        """Verifica que existe() retorna False para un evento que no existe."""
        calendario_evento_service.id_calendario_evento = 9999
        resultado = calendario_evento_service.existe()
        assert resultado is False

    def test_es_valida_true(self, calendario_evento_service):
        """Verifica que es_valida() retorna True para un evento válido."""
        calendario_evento_service.nombre = f"Clase-{uuid.uuid4()}"
        calendario_evento_service.fecha_inicio = datetime(2024, 10, 1, 15, 0)

        resultado = calendario_evento_service.es_valida()
        assert resultado is True

    def test_es_valida_nombre_vacio(self, calendario_evento_service):
        """Verifica que es_valida() retorna False si el nombre está vacío."""
        calendario_evento_service.nombre = ""
        calendario_evento_service.fecha_inicio = datetime(2024, 11, 1, 16, 0)

        resultado = calendario_evento_service.es_valida()
        assert resultado is False

    def test_es_valida_fecha_none(self, calendario_evento_service):
        """Verifica que es_valida() retorna False si fecha_inicio es None."""
        calendario_evento_service.nombre = f"Test-{uuid.uuid4()}"
        calendario_evento_service.fecha_inicio = None

        resultado = calendario_evento_service.es_valida()
        assert resultado is False

    def test_str_representation(self, calendario_evento_service):
        """Verifica que __str__() funciona correctamente."""
        calendario_evento_service.id_calendario_evento = 1
        calendario_evento_service.nombre = "Test"
        calendario_evento_service.fecha_inicio = datetime(2024, 1, 1, 10, 0)
        calendario_evento_service.fecha_fin = datetime(2024, 1, 1, 12, 0)

        resultado = str(calendario_evento_service)
        assert "CalendarioEventoService" in resultado
        assert "Test" in resultado

    def test_repr_representation(self, calendario_evento_service):
        """Verifica que __repr__() funciona correctamente."""
        calendario_evento_service.id_calendario_evento = 1
        calendario_evento_service.nombre = "Test"
        calendario_evento_service.fecha_inicio = datetime(2024, 1, 1, 10, 0)

        resultado = repr(calendario_evento_service)
        assert "CalendarioEventoService" in resultado

    def test_insertar_multiples(self, calendario_evento_service):
        """Verifica que se pueden insertar múltiples eventos."""
        ids = []
        for i in range(3):
            calendario_evento_service.nombre = f"Evento-{uuid.uuid4()}"
            calendario_evento_service.fecha_inicio = datetime(2024, 12, i + 1, 10, 0)
            id_insertado = calendario_evento_service.insertar()
            assert id_insertado is not None
            ids.append(id_insertado)

        assert len(ids) == 3
        assert len(set(ids)) == 3  # Todos deben ser únicos

    def test_flujo_completo(self, calendario_evento_service):
        """Verifica el flujo completo: insertar, existe, instanciar, eliminar."""
        calendario_evento_service.nombre = f"Completo-{uuid.uuid4()}"
        calendario_evento_service.fecha_inicio = datetime(2025, 1, 1, 10, 0)

        # Insertar
        id_insertado = calendario_evento_service.insertar()
        assert id_insertado is not None

        # Existe
        calendario_evento_service.id_calendario_evento = id_insertado
        assert calendario_evento_service.existe() is True

        # Instanciar
        assert calendario_evento_service.instanciar() is True

        # Eliminar
        assert calendario_evento_service.eliminar() is True
        assert calendario_evento_service.existe() is False
