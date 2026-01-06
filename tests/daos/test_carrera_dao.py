import pytest
import os
import sqlite3
from pathlib import Path
from src.modelos.daos.carrera_dao import CarreraDAO
from src.modelos.dtos.carrera_dto import CarreraDTO


@pytest.fixture
def db_path(tmp_path):
    """Crea una ruta temporal para la base de datos de prueba."""
    db_file = tmp_path / "test_carrera.db"
    yield str(db_file)
    # Cleanup
    if db_file.exists():
        db_file.unlink()


@pytest.fixture
def carrera_dao(db_path):
    """Crea una instancia del DAO con base de datos temporal."""
    dao = CarreraDAO(ruta_db=db_path)
    yield dao


class TestCarreraDAO:
    """Suite de pruebas para la clase CarreraDAO."""

    def test_crear_tabla(self, carrera_dao):
        """Verifica que la tabla se crea correctamente."""
        # La tabla se crea en __init__, verificamos que existe
        carrera_dao.crear_tabla()

        # Verificar que la tabla existe consultando el esquema
        with carrera_dao.get_conexion() as con:
            cursor = con.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='carrera'")
            resultado = cursor.fetchone()
            assert resultado is not None, "La tabla 'carrera' no fue creada"

    def test_insertar(self, carrera_dao):
        """Verifica que se inserta correctamente un registro de carrera."""
        carrera_dto = CarreraDTO(
            nombre="Ingeniería en Sistemas",
            plan="Plan 2023",
            modalidad="Presencial",
            creditos_totales=240,
        )

        id_insertado = carrera_dao.insertar(carrera_dto)

        assert id_insertado is not None, "No se obtuvo ID después de insertar"
        assert id_insertado > 0, "El ID insertado debe ser mayor a 0"

    def test_insertar_multiples(self, carrera_dao):
        """Verifica que se pueden insertar múltiples registros."""
        carreras = [
            CarreraDTO(
                nombre="Ingeniería en Sistemas",
                plan="Plan 2023",
                modalidad="Presencial",
                creditos_totales=240,
            ),
            CarreraDTO(
                nombre="Licenciatura en Matemática",
                plan="Plan 2022",
                modalidad="Virtual",
                creditos_totales=200,
            ),
            CarreraDTO(
                nombre="Licenciatura en Física",
                plan="Plan 2023",
                modalidad="Híbrida",
                creditos_totales=220,
            ),
        ]

        ids = [carrera_dao.insertar(carrera) for carrera in carreras]

        assert len(ids) == 3, "Deberían haberse insertado 3 registros"
        assert all(id is not None for id in ids), "Todos los IDs deben ser válidos"
        # Verificar que los IDs son únicos y incrementales
        assert len(set(ids)) == 3, "Los IDs deben ser únicos"
        assert ids == sorted(ids), "Los IDs deben ser incrementales"

    def test_instanciar_existente(self, carrera_dao):
        """Verifica que se puede obtener un registro existente."""
        # Insertar una carrera
        carrera_original = CarreraDTO(
            nombre="Ingeniería en Sistemas",
            plan="Plan 2023",
            modalidad="Presencial",
            creditos_totales=240,
        )
        id_insertado = carrera_dao.insertar(carrera_original)

        # Consultar la carrera
        carrera_consultada = CarreraDTO(id_carrera=id_insertado)
        resultado = carrera_dao.instanciar(carrera_consultada)

        assert resultado is True, "Debería encontrar la carrera"
        assert carrera_consultada.id_carrera == id_insertado
        assert carrera_consultada.nombre == "Ingeniería en Sistemas"
        assert carrera_consultada.plan == "Plan 2023"
        assert carrera_consultada.modalidad == "Presencial"
        assert carrera_consultada.creditos_totales == 240

    def test_instanciar_inexistente(self, carrera_dao):
        """Verifica que retorna False cuando no existe el registro."""
        carrera_consultada = CarreraDTO(id_carrera=999)
        resultado = carrera_dao.instanciar(carrera_consultada)

        assert resultado is False, "Debería retornar False para carrera inexistente"

    def test_instanciar_id_invalido(self, carrera_dao):
        """Verifica que retorna False para IDs inválidos."""
        # ID = 0
        carrera = CarreraDTO(id_carrera=0)
        resultado = carrera_dao.instanciar(carrera)
        assert resultado is False, "Debería retornar False para ID = 0"

        # ID = None
        carrera = CarreraDTO(id_carrera=None)
        resultado = carrera_dao.instanciar(carrera)
        assert resultado is False, "Debería retornar False para ID = None"

    def test_existe_verdadero(self, carrera_dao):
        """Verifica que existe retorna True para un registro existente."""
        # Insertar una carrera
        carrera_original = CarreraDTO(
            nombre="Ingeniería en Sistemas",
            plan="Plan 2023",
            modalidad="Presencial",
            creditos_totales=240,
        )
        id_insertado = carrera_dao.insertar(carrera_original)

        # Verificar existencia
        carrera_a_verificar = CarreraDTO(id_carrera=id_insertado)
        existe = carrera_dao.existe(carrera_a_verificar)

        assert existe is True, "Debería confirmar que la carrera existe"

    def test_existe_falso(self, carrera_dao):
        """Verifica que existe retorna False para un registro inexistente."""
        carrera_a_verificar = CarreraDTO(id_carrera=999)
        existe = carrera_dao.existe(carrera_a_verificar)

        assert existe is False, "Debería retornar False para carrera inexistente"

    def test_existe_id_invalido(self, carrera_dao):
        """Verifica que existe retorna False para IDs inválidos."""
        # ID = 0
        carrera = CarreraDTO(id_carrera=0)
        resultado = carrera_dao.existe(carrera)
        assert resultado is False, "Debería retornar False para ID = 0"

        # ID = None
        carrera = CarreraDTO(id_carrera=None)
        resultado = carrera_dao.existe(carrera)
        assert resultado is False, "Debería retornar False para ID = None"

    def test_eliminar(self, carrera_dao):
        """Verifica que se puede eliminar un registro."""
        # Insertar una carrera
        carrera_original = CarreraDTO(
            nombre="Ingeniería en Sistemas",
            plan="Plan 2023",
            modalidad="Presencial",
            creditos_totales=240,
        )
        id_insertado = carrera_dao.insertar(carrera_original)

        # Verificar que existe
        carrera_verificar = CarreraDTO(id_carrera=id_insertado)
        assert carrera_dao.existe(carrera_verificar) is True

        # Eliminar
        carrera_a_eliminar = CarreraDTO(id_carrera=id_insertado)
        resultado = carrera_dao.eliminar(carrera_a_eliminar)

        assert resultado is True, "Debería eliminar correctamente"
        assert (
            carrera_dao.existe(carrera_verificar) is False
        ), "La carrera no debería existir después de eliminar"

    def test_eliminar_inexistente(self, carrera_dao):
        """Verifica que eliminar un registro inexistente retorna False."""
        carrera_a_eliminar = CarreraDTO(id_carrera=999)
        resultado = carrera_dao.eliminar(carrera_a_eliminar)

        assert resultado is False, "Debería retornar False al eliminar registro inexistente"

    def test_ciclo_completo(self, carrera_dao):
        """Prueba completa del ciclo CRUD."""
        # CREATE
        carrera = CarreraDTO(
            nombre="Ingeniería en Informática",
            plan="Plan 2024",
            modalidad="Presencial",
            creditos_totales=250,
        )
        id_creado = carrera_dao.insertar(carrera)
        assert id_creado is not None

        # READ
        carrera_leida = CarreraDTO(id_carrera=id_creado)
        resultado_lectura = carrera_dao.instanciar(carrera_leida)
        assert resultado_lectura is True
        assert carrera_leida.nombre == "Ingeniería en Informática"

        # VERIFY EXISTS
        carrera_verificar = CarreraDTO(id_carrera=id_creado)
        assert carrera_dao.existe(carrera_verificar) is True

        # DELETE
        carrera_eliminar = CarreraDTO(id_carrera=id_creado)
        resultado_eliminacion = carrera_dao.eliminar(carrera_eliminar)
        assert resultado_eliminacion is True

        # VERIFY NOT EXISTS
        carrera_verificar_final = CarreraDTO(id_carrera=id_creado)
        assert carrera_dao.existe(carrera_verificar_final) is False
