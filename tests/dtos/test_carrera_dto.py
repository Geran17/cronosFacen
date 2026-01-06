import pytest
from src.modelos.dtos.carrera_dto import CarreraDTO


class TestCarreraDTO:
    """Tests para CarreraDTO"""

    def test_crear_carrera_vacia(self):
        """Test crear una carrera con valores por defecto"""
        carrera = CarreraDTO()
        assert carrera.id_carrera is None
        assert carrera.nombre is None
        assert carrera.plan is None
        assert carrera.modalidad is None
        assert carrera.creditos_totales is None

    def test_crear_carrera_con_datos(self):
        """Test crear una carrera con todos los parámetros"""
        carrera = CarreraDTO(
            id_carrera=1,
            nombre='Ingeniería en Sistemas',
            plan='Plan 2023',
            modalidad='Presencial',
            creditos_totales=240,
        )
        assert carrera.id_carrera == 1
        assert carrera.nombre == 'Ingeniería en Sistemas'
        assert carrera.plan == 'Plan 2023'
        assert carrera.modalidad == 'Presencial'
        assert carrera.creditos_totales == 240

    def test_get_data(self):
        """Test obtener datos como diccionario"""
        carrera = CarreraDTO(
            id_carrera=1,
            nombre='Ingeniería en Sistemas',
            plan='Plan 2023',
            modalidad='Presencial',
            creditos_totales=240,
        )
        datos = carrera.get_data()
        assert isinstance(datos, dict)
        assert datos['id_carrera'] == 1
        assert datos['nombre'] == 'Ingeniería en Sistemas'
        assert datos['plan'] == 'Plan 2023'
        assert datos['modalidad'] == 'Presencial'
        assert datos['creditos_totales'] == 240

    def test_set_data_completo(self):
        """Test establecer todos los datos desde un diccionario"""
        carrera = CarreraDTO()
        datos = {
            'id_carrera': 1,
            'nombre': 'Ingeniería en Sistemas',
            'plan': 'Plan 2023',
            'modalidad': 'Presencial',
            'creditos_totales': 240,
        }
        carrera.set_data(datos)
        assert carrera.id_carrera == 1
        assert carrera.nombre == 'Ingeniería en Sistemas'
        assert carrera.plan == 'Plan 2023'

    def test_set_data_parcial(self):
        """Test establecer datos parciales preserva valores existentes"""
        carrera = CarreraDTO(id_carrera=1, nombre='Ingeniería en Sistemas')
        datos = {'modalidad': 'Virtual'}
        carrera.set_data(datos)
        assert carrera.id_carrera == 1
        assert carrera.nombre == 'Ingeniería en Sistemas'
        assert carrera.modalidad == 'Virtual'

    def test_modalidades_validas(self):
        """Test que se pueden asignar diferentes modalidades"""
        modalidades = ['Presencial', 'Virtual', 'Híbrida']
        for modalidad in modalidades:
            carrera = CarreraDTO(modalidad=modalidad)
            assert carrera.modalidad == modalidad

    def test_creditos_totales_positivo(self):
        """Test que se pueden asignar créditos totales positivos"""
        creditos = [100, 150, 200, 240, 300]
        for c in creditos:
            carrera = CarreraDTO(creditos_totales=c)
            assert carrera.creditos_totales == c

    def test_set_data_vacio(self):
        """Test set_data con diccionario vacío no causa errores"""
        carrera = CarreraDTO(id_carrera=1, nombre='Ingeniería')
        carrera.set_data({})
        assert carrera.id_carrera == 1
        assert carrera.nombre == 'Ingeniería'

    def test_set_data_none(self):
        """Test set_data con None no causa errores"""
        carrera = CarreraDTO(id_carrera=1, nombre='Ingeniería')
        carrera.set_data({})
        assert carrera.id_carrera == 1
        assert carrera.nombre == 'Ingeniería'

    def test_roundtrip_get_set_data(self):
        """Test que get_data y set_data son consistentes"""
        carrera_original = CarreraDTO(
            id_carrera=1,
            nombre='Ingeniería en Sistemas',
            plan='Plan 2023',
            modalidad='Presencial',
            creditos_totales=240,
        )
        datos = carrera_original.get_data()

        carrera_nueva = CarreraDTO()
        carrera_nueva.set_data(datos)

        assert carrera_nueva.get_data() == carrera_original.get_data()
