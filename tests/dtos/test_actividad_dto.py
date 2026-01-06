import pytest
from src.modelos.dtos.actividad_dto import ActividadDTO


class TestActividadDTO:
    """Tests para ActividadDTO"""

    def test_crear_actividad_vacia(self):
        """Test crear una actividad con valores por defecto"""
        actividad = ActividadDTO()
        assert actividad.id_actividad is None
        assert actividad.titulo is None
        assert actividad.descripcion is None
        assert actividad.fecha_inicio is None
        assert actividad.fecha_fin is None
        assert actividad.id_eje is None
        assert actividad.id_tipo_actividad is None

    def test_crear_actividad_con_datos(self):
        """Test crear una actividad con todos los parámetros"""
        actividad = ActividadDTO(
            id_actividad=1,
            titulo='Tarea 1 - Algoritmos',
            descripcion='Implementar tres algoritmos de ordenamiento',
            fecha_inicio='2025-01-15',
            fecha_fin='2025-01-22',
            id_eje=1,
            id_tipo_actividad=1,
        )
        assert actividad.id_actividad == 1
        assert actividad.titulo == 'Tarea 1 - Algoritmos'
        assert actividad.descripcion == 'Implementar tres algoritmos de ordenamiento'
        assert actividad.fecha_inicio == '2025-01-15'
        assert actividad.fecha_fin == '2025-01-22'
        assert actividad.id_eje == 1
        assert actividad.id_tipo_actividad == 1

    def test_get_data(self):
        """Test obtener datos como diccionario"""
        actividad = ActividadDTO(
            id_actividad=1,
            titulo='Tarea 1',
            descripcion='Descripción',
            fecha_inicio='2025-01-15',
            fecha_fin='2025-01-22',
            id_eje=1,
            id_tipo_actividad=1,
        )
        datos = actividad.get_data()
        assert isinstance(datos, dict)
        assert datos['id_actividad'] == 1
        assert datos['titulo'] == 'Tarea 1'
        assert datos['descripcion'] == 'Descripción'
        assert datos['fecha_inicio'] == '2025-01-15'
        assert datos['fecha_fin'] == '2025-01-22'
        assert datos['id_eje'] == 1
        assert datos['id_tipo_actividad'] == 1

    def test_set_data_completo(self):
        """Test establecer todos los datos desde un diccionario"""
        actividad = ActividadDTO()
        datos = {
            'id_actividad': 1,
            'titulo': 'Tarea 1',
            'descripcion': 'Descripción',
            'fecha_inicio': '2025-01-15',
            'fecha_fin': '2025-01-22',
            'id_eje': 1,
            'id_tipo_actividad': 1,
        }
        actividad.set_data(datos)
        assert actividad.id_actividad == 1
        assert actividad.titulo == 'Tarea 1'
        assert actividad.descripcion == 'Descripción'

    def test_set_data_parcial(self):
        """Test establecer datos parciales preserva valores existentes"""
        actividad = ActividadDTO(id_actividad=1, titulo='Tarea Original')
        datos = {'descripcion': 'Nueva descripción'}
        actividad.set_data(datos)
        assert actividad.id_actividad == 1
        assert actividad.titulo == 'Tarea Original'
        assert actividad.descripcion == 'Nueva descripción'

    def test_set_data_vacio(self):
        """Test set_data con diccionario vacío no causa errores"""
        actividad = ActividadDTO(id_actividad=1, titulo='Tarea')
        actividad.set_data({})
        assert actividad.id_actividad == 1
        assert actividad.titulo == 'Tarea'

    def test_set_data_none(self):
        """Test set_data con None no causa errores"""
        actividad = ActividadDTO(id_actividad=1, titulo='Tarea')
        actividad.set_data({})
        assert actividad.id_actividad == 1
        assert actividad.titulo == 'Tarea'

    def test_roundtrip_get_set_data(self):
        """Test que get_data y set_data son consistentes"""
        actividad_original = ActividadDTO(
            id_actividad=1,
            titulo='Tarea 1',
            descripcion='Descripción',
            fecha_inicio='2025-01-15',
            fecha_fin='2025-01-22',
            id_eje=1,
            id_tipo_actividad=1,
        )
        datos = actividad_original.get_data()

        actividad_nueva = ActividadDTO()
        actividad_nueva.set_data(datos)

        assert actividad_nueva.get_data() == actividad_original.get_data()
