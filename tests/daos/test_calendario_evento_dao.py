import pytest
import os
import sqlite3
from pathlib import Path
from src.modelos.daos.calendario_evento_dao import CalendarioEventoDAO
from src.modelos.dtos.calendario_evento_dto import CalendarioEventoDTO


@pytest.fixture
def db_path(tmp_path):
    """Crea una ruta temporal para la base de datos de prueba."""
    db_file = tmp_path / "test_calendario_evento.db"
    yield str(db_file)
    # Cleanup
    if db_file.exists():
        db_file.unlink()


@pytest.fixture
def calendario_evento_dao(db_path):
    """Crea una instancia del DAO con base de datos temporal."""
    dao = CalendarioEventoDAO(ruta_db=db_path)
    yield dao


class TestCalendarioEventoDAO:
    """Suite de pruebas para la clase CalendarioEventoDAO."""

    def test_crear_tabla(self, calendario_evento_dao):
        """Verifica que la tabla se crea correctamente."""
        calendario_evento_dao.crear_tabla()

        with calendario_evento_dao.get_conexion() as con:
            cursor = con.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='calendario_evento'"
            )
            resultado = cursor.fetchone()
            assert resultado is not None, "La tabla 'calendario_evento' no fue creada"

    def test_insertar(self, calendario_evento_dao):
        """Verifica que se inserta correctamente un registro de evento."""
        evento_dto = CalendarioEventoDTO(
            titulo="Período de Exámenes",
            tipo="examen",
            fecha_inicio="2025-06-01",
            fecha_fin="2025-06-15",
            afecta_actividades=1,
        )

        id_insertado = calendario_evento_dao.insertar(evento_dto)

        assert id_insertado is not None, "No se obtuvo ID después de insertar"
        assert id_insertado > 0, "El ID insertado debe ser mayor a 0"

    def test_insertar_multiples(self, calendario_evento_dao):
        """Verifica que se pueden insertar múltiples registros."""
        eventos = [
            CalendarioEventoDTO(
                titulo="Período de Exámenes",
                tipo="examen",
                fecha_inicio="2025-06-01",
                fecha_fin="2025-06-15",
                afecta_actividades=1,
            ),
            CalendarioEventoDTO(
                titulo="Receso Académico",
                tipo="receso",
                fecha_inicio="2025-07-01",
                fecha_fin="2025-07-31",
                afecta_actividades=1,
            ),
        ]

        ids = [calendario_evento_dao.insertar(evento) for evento in eventos]

        assert len(ids) == 2, "Deberían haberse insertado 2 registros"
        assert all(id is not None for id in ids), "Todos los IDs deben ser válidos"

    def test_instanciar_existente(self, calendario_evento_dao):
        """Verifica que se puede obtener un registro existente."""
        evento_original = CalendarioEventoDTO(
            titulo="Período de Exámenes",
            tipo="examen",
            fecha_inicio="2025-06-01",
            fecha_fin="2025-06-15",
            afecta_actividades=1,
        )
        id_insertado = calendario_evento_dao.insertar(evento_original)

        evento_consultado = CalendarioEventoDTO(id_evento=id_insertado)
        resultado = calendario_evento_dao.instanciar(evento_consultado)

        assert resultado is True, "Debería encontrar el evento"
        assert evento_consultado.id_evento == id_insertado
        assert evento_consultado.titulo == "Período de Exámenes"
        assert evento_consultado.tipo == "examen"
        assert evento_consultado.afecta_actividades == 1

    def test_instanciar_inexistente(self, calendario_evento_dao):
        """Verifica que retorna False cuando no existe el registro."""
        evento_consultado = CalendarioEventoDTO(id_evento=999)
        resultado = calendario_evento_dao.instanciar(evento_consultado)

        assert resultado is False, "Debería retornar False para evento inexistente"

    def test_instanciar_id_invalido(self, calendario_evento_dao):
        """Verifica que retorna False para IDs inválidos."""
        evento = CalendarioEventoDTO(id_evento=0)
        resultado = calendario_evento_dao.instanciar(evento)
        assert resultado is False, "Debería retornar False para ID = 0"

        evento = CalendarioEventoDTO(id_evento=None)
        resultado = calendario_evento_dao.instanciar(evento)
        assert resultado is False, "Debería retornar False para ID = None"

    def test_existe_verdadero(self, calendario_evento_dao):
        """Verifica que existe retorna True para un registro existente."""
        evento_original = CalendarioEventoDTO(
            titulo="Período de Exámenes",
            tipo="examen",
            fecha_inicio="2025-06-01",
            fecha_fin="2025-06-15",
            afecta_actividades=1,
        )
        id_insertado = calendario_evento_dao.insertar(evento_original)

        evento_verificar = CalendarioEventoDTO(id_evento=id_insertado)
        existe = calendario_evento_dao.existe(evento_verificar)

        assert existe is True, "Debería confirmar que el evento existe"

    def test_existe_falso(self, calendario_evento_dao):
        """Verifica que existe retorna False para un registro inexistente."""
        evento_verificar = CalendarioEventoDTO(id_evento=999)
        existe = calendario_evento_dao.existe(evento_verificar)

        assert existe is False, "Debería retornar False para evento inexistente"

    def test_existe_id_invalido(self, calendario_evento_dao):
        """Verifica que existe retorna False para IDs inválidos."""
        evento = CalendarioEventoDTO(id_evento=0)
        resultado = calendario_evento_dao.existe(evento)
        assert resultado is False, "Debería retornar False para ID = 0"

        evento = CalendarioEventoDTO(id_evento=None)
        resultado = calendario_evento_dao.existe(evento)
        assert resultado is False, "Debería retornar False para ID = None"

    def test_eliminar(self, calendario_evento_dao):
        """Verifica que se puede eliminar un registro."""
        evento_original = CalendarioEventoDTO(
            titulo="Período de Exámenes",
            tipo="examen",
            fecha_inicio="2025-06-01",
            fecha_fin="2025-06-15",
            afecta_actividades=1,
        )
        id_insertado = calendario_evento_dao.insertar(evento_original)

        evento_verificar = CalendarioEventoDTO(id_evento=id_insertado)
        assert calendario_evento_dao.existe(evento_verificar) is True

        evento_eliminar = CalendarioEventoDTO(id_evento=id_insertado)
        resultado = calendario_evento_dao.eliminar(evento_eliminar)

        assert resultado is True, "Debería eliminar correctamente"
        assert (
            calendario_evento_dao.existe(evento_verificar) is False
        ), "El evento no debería existir después de eliminar"

    def test_eliminar_inexistente(self, calendario_evento_dao):
        """Verifica que eliminar un registro inexistente retorna False."""
        evento_eliminar = CalendarioEventoDTO(id_evento=999)
        resultado = calendario_evento_dao.eliminar(evento_eliminar)

        assert resultado is False, "Debería retornar False al eliminar registro inexistente"

    def test_ciclo_completo(self, calendario_evento_dao):
        """Prueba completa del ciclo CRUD."""
        evento = CalendarioEventoDTO(
            titulo="Entrega de Proyectos",
            tipo="entrega",
            fecha_inicio="2025-05-01",
            fecha_fin="2025-05-15",
            afecta_actividades=1,
        )
        id_creado = calendario_evento_dao.insertar(evento)
        assert id_creado is not None

        evento_leido = CalendarioEventoDTO(id_evento=id_creado)
        resultado_lectura = calendario_evento_dao.instanciar(evento_leido)
        assert resultado_lectura is True
        assert evento_leido.titulo == "Entrega de Proyectos"

        evento_verificar = CalendarioEventoDTO(id_evento=id_creado)
        assert calendario_evento_dao.existe(evento_verificar) is True

        evento_eliminar = CalendarioEventoDTO(id_evento=id_creado)
        resultado_eliminacion = calendario_evento_dao.eliminar(evento_eliminar)
        assert resultado_eliminacion is True

        evento_verificar_final = CalendarioEventoDTO(id_evento=id_creado)
        assert calendario_evento_dao.existe(evento_verificar_final) is False
