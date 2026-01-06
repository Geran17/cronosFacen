import pytest
import os
from pathlib import Path
from src.modelos.services.carrera_service import CarreraService
from src.modelos.dtos.carrera_dto import CarreraDTO


@pytest.fixture
def db_path(tmp_path):
    """Crea una ruta temporal para la base de datos de prueba."""
    db_file = tmp_path / "test_carrera_service.db"
    yield str(db_file)
    # Cleanup
    if db_file.exists():
        db_file.unlink()


@pytest.fixture
def carrera_service(db_path):
    """Crea una instancia de CarreraService con base de datos temporal."""
    service = CarreraService(ruta_db=db_path)
    service.crear_tabla()
    yield service


class TestCarreraService:
    """Suite de pruebas para la clase CarreraService."""

    def test_crear_tabla(self, db_path):
        """Verifica que la tabla se crea correctamente."""
        service = CarreraService(ruta_db=db_path)
        service.crear_tabla()

        with service.dao.get_conexion() as con:
            cursor = con.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='carrera'")
            resultado = cursor.fetchone()
            assert resultado is not None, "La tabla 'carrera' no fue creada"

    def test_insertar_carrera(self, carrera_service):
        """Verifica que se puede insertar una carrera."""
        carrera_service.nombre = "Ingeniería en Sistemas"
        carrera_service.plan = "Plan 2023"
        carrera_service.modalidad = "Presencial"

        id_insertado = carrera_service.insertar()

        assert id_insertado is not None, "No se obtuvo ID después de insertar"
        assert id_insertado > 0, "El ID debe ser mayor a 0"
        assert carrera_service.id_carrera == id_insertado, "El ID debe estar en el objeto"

    def test_carrera_es_valida(self, carrera_service):
        """Verifica validación de carrera."""
        # Carrera válida
        carrera_service.nombre = "Ingeniería"
        carrera_service.plan = "Plan 2023"
        carrera_service.modalidad = "Presencial"
        assert carrera_service.es_valida() is True

        # Carrera sin nombre
        carrera_service.nombre = None
        assert carrera_service.es_valida() is False

        # Carrera sin plan
        carrera_service.nombre = "Ingeniería"
        carrera_service.plan = None
        assert carrera_service.es_valida() is False

        # Carrera sin modalidad
        carrera_service.plan = "Plan 2023"
        carrera_service.modalidad = None
        assert carrera_service.es_valida() is False

    def test_instanciar_carrera(self, carrera_service):
        """Verifica que se puede cargar una carrera desde BD."""
        # Insertar una carrera
        carrera_service.nombre = "Ingeniería en Sistemas"
        carrera_service.plan = "Plan 2023"
        carrera_service.modalidad = "Presencial"
        id_creado = carrera_service.insertar()

        # Crear nuevo servicio y cargar los datos
        carrera_nueva = CarreraService(ruta_db=carrera_service.dao.ruta_db)
        carrera_nueva.id_carrera = id_creado

        resultado = carrera_nueva.instanciar()

        assert resultado is True, "Debería instanciar correctamente"
        assert carrera_nueva.nombre == "Ingeniería en Sistemas", "El nombre debe coincidir"
        assert carrera_nueva.plan == "Plan 2023", "El plan debe coincidir"
        assert carrera_nueva.modalidad == "Presencial", "La modalidad debe coincidir"

    def test_instanciar_inexistente(self, carrera_service):
        """Verifica que instanciar una carrera inexistente retorna False."""
        carrera_service.id_carrera = 999
        resultado = carrera_service.instanciar()

        assert resultado is False, "No debería instanciar carrera inexistente"

    def test_existe_verdadero(self, carrera_service):
        """Verifica que existe() retorna True para carrera insertada."""
        carrera_service.nombre = "Ingeniería en Sistemas"
        carrera_service.plan = "Plan 2023"
        carrera_service.modalidad = "Presencial"
        id_creado = carrera_service.insertar()

        carrera_verificar = CarreraService(ruta_db=carrera_service.dao.ruta_db)
        carrera_verificar.id_carrera = id_creado

        existe = carrera_verificar.existe()

        assert existe is True, "Debería confirmar que la carrera existe"

    def test_existe_falso(self, carrera_service):
        """Verifica que existe() retorna False para carrera inexistente."""
        carrera_service.id_carrera = 999
        existe = carrera_service.existe()

        assert existe is False, "No debería encontrar carrera inexistente"

    def test_eliminar_carrera(self, carrera_service):
        """Verifica que se puede eliminar una carrera."""
        carrera_service.nombre = "Ingeniería en Sistemas"
        carrera_service.plan = "Plan 2023"
        carrera_service.modalidad = "Presencial"
        id_creado = carrera_service.insertar()

        # Verificar que existe
        carrera_verificar = CarreraService(ruta_db=carrera_service.dao.ruta_db)
        carrera_verificar.id_carrera = id_creado
        assert carrera_verificar.existe() is True

        # Eliminar
        resultado_eliminacion = carrera_service.eliminar()
        assert resultado_eliminacion is True, "La eliminación debe retornar True"
        assert carrera_verificar.existe() is False, "La carrera debe estar eliminada"

    def test_eliminar_inexistente(self, carrera_service):
        """Verifica que eliminar una carrera inexistente retorna False."""
        carrera_service.id_carrera = 999
        resultado = carrera_service.eliminar()

        assert resultado is False, "No debe eliminar carrera inexistente"

    def test_eliminar_sin_id(self, carrera_service):
        """Verifica que eliminar sin ID retorna False."""
        carrera_service.id_carrera = None
        resultado = carrera_service.eliminar()

        assert resultado is False, "No debe eliminar sin ID"

    def test_instanciar_sin_id(self, carrera_service):
        """Verifica que instanciar sin ID retorna False."""
        carrera_service.id_carrera = None
        resultado = carrera_service.instanciar()

        assert resultado is False, "No debe instanciar sin ID"

    def test_existe_sin_id(self, carrera_service):
        """Verifica que existe sin ID retorna False."""
        carrera_service.id_carrera = None
        resultado = carrera_service.existe()

        assert resultado is False, "No debe verificar existencia sin ID"

    def test_str_representation(self, carrera_service):
        """Verifica la representación en string."""
        carrera_service.id_carrera = 1
        carrera_service.nombre = "Ingeniería"
        carrera_service.plan = "Plan 2023"
        carrera_service.modalidad = "Presencial"

        str_rep = str(carrera_service)

        assert "CarreraService" in str_rep, "Debe contener nombre de clase"
        assert "Ingeniería" in str_rep, "Debe contener nombre de carrera"
        assert "Plan 2023" in str_rep, "Debe contener plan"

    def test_ciclo_completo(self, carrera_service):
        """Verifica un ciclo completo: crear, cargar, eliminar."""
        # 1. Crear
        carrera_service.nombre = "Ingeniería en Sistemas"
        carrera_service.plan = "Plan 2023"
        carrera_service.modalidad = "Presencial"

        assert carrera_service.es_valida() is True
        id_creado = carrera_service.insertar()
        assert id_creado is not None

        # 2. Cargar
        carrera_cargada = CarreraService(ruta_db=carrera_service.dao.ruta_db)
        carrera_cargada.id_carrera = id_creado
        assert carrera_cargada.instanciar() is True
        assert carrera_cargada.nombre == "Ingeniería en Sistemas"

        # 3. Verificar existencia
        assert carrera_cargada.existe() is True

        # 4. Eliminar
        assert carrera_cargada.eliminar() is True
        assert carrera_cargada.existe() is False
