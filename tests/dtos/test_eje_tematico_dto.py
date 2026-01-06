import pytest
from src.modelos.dtos.eje_tematico_dto import EjeTematicoDTO


class TestEjeTematicoDTO:
    """Tests para EjeTematicoDTO"""

    def test_crear_eje_vacio(self):
        """Test crear un eje temático con valores por defecto"""
        eje = EjeTematicoDTO()
        assert eje.id_eje is None
        assert eje.nombre is None
        assert eje.orden is None
        assert eje.id_asignatura is None

    def test_crear_eje_con_datos(self):
        """Test crear un eje temático con todos los parámetros"""
        eje = EjeTematicoDTO(
            id_eje=1, nombre='Introducción a la Programación', orden=1, id_asignatura=1
        )
        assert eje.id_eje == 1
        assert eje.nombre == 'Introducción a la Programación'
        assert eje.orden == 1
        assert eje.id_asignatura == 1

    def test_get_data(self):
        """Test obtener datos como diccionario"""
        eje = EjeTematicoDTO(
            id_eje=1, nombre='Introducción a la Programación', orden=1, id_asignatura=1
        )
        datos = eje.get_data()
        assert isinstance(datos, dict)
        assert datos['id_eje'] == 1
        assert datos['nombre'] == 'Introducción a la Programación'
        assert datos['orden'] == 1
        assert datos['id_asignatura'] == 1

    def test_set_data_completo(self):
        """Test establecer todos los datos desde un diccionario"""
        eje = EjeTematicoDTO()
        datos = {
            'id_eje': 1,
            'nombre': 'Introducción a la Programación',
            'orden': 1,
            'id_asignatura': 1,
        }
        eje.set_data(datos)
        assert eje.id_eje == 1
        assert eje.nombre == 'Introducción a la Programación'
        assert eje.orden == 1
        assert eje.id_asignatura == 1

    def test_set_data_parcial(self):
        """Test establecer datos parciales preserva valores existentes"""
        eje = EjeTematicoDTO(id_eje=1, nombre='Introducción a la Programación')
        datos = {'orden': 1}
        eje.set_data(datos)
        assert eje.id_eje == 1
        assert eje.nombre == 'Introducción a la Programación'
        assert eje.orden == 1

    def test_orden_secuencial(self):
        """Test que se pueden asignar órdenes secuenciales"""
        ordenes = [1, 2, 3, 4, 5]
        for orden in ordenes:
            eje = EjeTematicoDTO(orden=orden)
            assert eje.orden == orden

    def test_set_data_vacio(self):
        """Test set_data con diccionario vacío no causa errores"""
        eje = EjeTematicoDTO(id_eje=1, nombre='Eje 1')
        eje.set_data({})
        assert eje.id_eje == 1
        assert eje.nombre == 'Eje 1'

    def test_set_data_none(self):
        """Test set_data con None no causa errores"""
        eje = EjeTematicoDTO(id_eje=1, nombre='Eje 1')
        eje.set_data({})
        assert eje.id_eje == 1
        assert eje.nombre == 'Eje 1'

    def test_roundtrip_get_set_data(self):
        """Test que get_data y set_data son consistentes"""
        eje_original = EjeTematicoDTO(
            id_eje=1, nombre='Introducción a la Programación', orden=1, id_asignatura=1
        )
        datos = eje_original.get_data()

        eje_nuevo = EjeTematicoDTO()
        eje_nuevo.set_data(datos)

        assert eje_nuevo.get_data() == eje_original.get_data()
