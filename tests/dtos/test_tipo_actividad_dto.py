import pytest
from src.modelos.dtos.tipo_actividad_dto import TipoActividadDTO


class TestTipoActividadDTO:
    """Tests para TipoActividadDTO"""

    def test_crear_tipo_actividad_vacio(self):
        """Test crear un tipo de actividad con valores por defecto"""
        tipo = TipoActividadDTO()
        assert tipo.id_tipo_actividad is None
        assert tipo.nombre is None
        assert tipo.siglas is None
        assert tipo.descripcion is None

    def test_crear_tipo_actividad_con_datos(self):
        """Test crear un tipo de actividad con todos los parámetros"""
        tipo = TipoActividadDTO(
            id_tipo_actividad=1,
            nombre='Tarea',
            siglas='TAR',
            descripcion='Actividad de refuerzo enviada a casa',
        )
        assert tipo.id_tipo_actividad == 1
        assert tipo.nombre == 'Tarea'
        assert tipo.siglas == 'TAR'
        assert tipo.descripcion == 'Actividad de refuerzo enviada a casa'

    def test_get_data(self):
        """Test obtener datos como diccionario"""
        tipo = TipoActividadDTO(
            id_tipo_actividad=1,
            nombre='Tarea',
            siglas='TAR',
            descripcion='Actividad de refuerzo enviada a casa',
        )
        datos = tipo.get_data()
        assert isinstance(datos, dict)
        assert datos['id_tipo_actividad'] == 1
        assert datos['nombre'] == 'Tarea'
        assert datos['siglas'] == 'TAR'
        assert datos['descripcion'] == 'Actividad de refuerzo enviada a casa'

    def test_set_data_completo(self):
        """Test establecer todos los datos desde un diccionario"""
        tipo = TipoActividadDTO()
        datos = {
            'id_tipo_actividad': 1,
            'nombre': 'Tarea',
            'siglas': 'TAR',
            'descripcion': 'Actividad de refuerzo enviada a casa',
        }
        tipo.set_data(datos)
        assert tipo.id_tipo_actividad == 1
        assert tipo.nombre == 'Tarea'
        assert tipo.siglas == 'TAR'
        assert tipo.descripcion == 'Actividad de refuerzo enviada a casa'

    def test_set_data_parcial(self):
        """Test establecer datos parciales preserva valores existentes"""
        tipo = TipoActividadDTO(id_tipo_actividad=1, nombre='Tarea')
        datos = {'siglas': 'TAR'}
        tipo.set_data(datos)
        assert tipo.id_tipo_actividad == 1
        assert tipo.nombre == 'Tarea'
        assert tipo.siglas == 'TAR'

    def test_tipos_actividades_validos(self):
        """Test que se pueden asignar diferentes tipos de actividades"""
        tipos_data = [
            {'id_tipo_actividad': 1, 'nombre': 'Tarea', 'siglas': 'TAR'},
            {'id_tipo_actividad': 2, 'nombre': 'Quiz', 'siglas': 'QZ'},
            {'id_tipo_actividad': 3, 'nombre': 'Examen', 'siglas': 'EXN'},
            {'id_tipo_actividad': 4, 'nombre': 'Proyecto', 'siglas': 'PRY'},
        ]
        for data in tipos_data:
            tipo = TipoActividadDTO(**data)
            assert tipo.nombre == data['nombre']
            assert tipo.siglas == data['siglas']

    def test_set_data_vacio(self):
        """Test set_data con diccionario vacío no causa errores"""
        tipo = TipoActividadDTO(id_tipo_actividad=1, nombre='Tarea')
        tipo.set_data({})
        assert tipo.id_tipo_actividad == 1
        assert tipo.nombre == 'Tarea'

    def test_set_data_none(self):
        """Test set_data con None no causa errores"""
        tipo = TipoActividadDTO(id_tipo_actividad=1, nombre='Tarea')
        tipo.set_data({})
        assert tipo.id_tipo_actividad == 1
        assert tipo.nombre == 'Tarea'

    def test_roundtrip_get_set_data(self):
        """Test que get_data y set_data son consistentes"""
        tipo_original = TipoActividadDTO(
            id_tipo_actividad=1,
            nombre='Tarea',
            siglas='TAR',
            descripcion='Actividad de refuerzo enviada a casa',
        )
        datos = tipo_original.get_data()

        tipo_nuevo = TipoActividadDTO()
        tipo_nuevo.set_data(datos)

        assert tipo_nuevo.get_data() == tipo_original.get_data()
