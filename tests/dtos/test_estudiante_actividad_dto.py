import pytest
from src.modelos.dtos.estudiante_actividad_dto import EstudianteActividadDTO


class TestEstudianteActividadDTO:
    """Tests para EstudianteActividadDTO"""

    def test_crear_estudiante_actividad_vacio(self):
        """Test crear un registro estudiante-actividad con valores por defecto"""
        reg = EstudianteActividadDTO()
        assert reg.id_estudiante is None
        assert reg.id_actividad is None
        assert reg.estado is None
        assert reg.fecha_entrega is None

    def test_crear_estudiante_actividad_con_datos(self):
        """Test crear un registro estudiante-actividad con todos los parámetros"""
        reg = EstudianteActividadDTO(
            id_estudiante=1, id_actividad=1, estado='entregada', fecha_entrega='2025-01-20'
        )
        assert reg.id_estudiante == 1
        assert reg.id_actividad == 1
        assert reg.estado == 'entregada'
        assert reg.fecha_entrega == '2025-01-20'

    def test_get_data(self):
        """Test obtener datos como diccionario"""
        reg = EstudianteActividadDTO(
            id_estudiante=1, id_actividad=1, estado='entregada', fecha_entrega='2025-01-20'
        )
        datos = reg.get_data()
        assert isinstance(datos, dict)
        assert datos['id_estudiante'] == 1
        assert datos['id_actividad'] == 1
        assert datos['estado'] == 'entregada'
        assert datos['fecha_entrega'] == '2025-01-20'

    def test_set_data_completo(self):
        """Test establecer todos los datos desde un diccionario"""
        reg = EstudianteActividadDTO()
        datos = {
            'id_estudiante': 1,
            'id_actividad': 1,
            'estado': 'entregada',
            'fecha_entrega': '2025-01-20',
        }
        reg.set_data(datos)
        assert reg.id_estudiante == 1
        assert reg.id_actividad == 1
        assert reg.estado == 'entregada'
        assert reg.fecha_entrega == '2025-01-20'

    def test_set_data_parcial(self):
        """Test establecer datos parciales preserva valores existentes"""
        reg = EstudianteActividadDTO(id_estudiante=1, id_actividad=1)
        datos = {'estado': 'entregada'}
        reg.set_data(datos)
        assert reg.id_estudiante == 1
        assert reg.id_actividad == 1
        assert reg.estado == 'entregada'

    def test_estados_validos(self):
        """Test que se pueden asignar diferentes estados"""
        estados = ['pendiente', 'en_progreso', 'entregada', 'vencida']
        for estado in estados:
            reg = EstudianteActividadDTO(estado=estado)
            assert reg.estado == estado

    def test_multiples_actividades_estudiante(self):
        """Test que un estudiante puede tener múltiples actividades"""
        actividades = [(1, 2, 'pendiente'), (1, 3, 'entregada'), (1, 4, 'vencida')]
        for id_est, id_act, estado in actividades:
            reg = EstudianteActividadDTO(id_estudiante=id_est, id_actividad=id_act, estado=estado)
            assert reg.id_estudiante == id_est
            assert reg.id_actividad == id_act
            assert reg.estado == estado

    def test_set_data_vacio(self):
        """Test set_data con diccionario vacío no causa errores"""
        reg = EstudianteActividadDTO(id_estudiante=1, id_actividad=1)
        reg.set_data({})
        assert reg.id_estudiante == 1
        assert reg.id_actividad == 1

    def test_set_data_none(self):
        """Test set_data con None no causa errores"""
        reg = EstudianteActividadDTO(id_estudiante=1, id_actividad=1)
        reg.set_data(None)
        assert reg.id_estudiante == 1
        assert reg.id_actividad == 1

    def test_roundtrip_get_set_data(self):
        """Test que get_data y set_data son consistentes"""
        reg_original = EstudianteActividadDTO(
            id_estudiante=1, id_actividad=1, estado='entregada', fecha_entrega='2025-01-20'
        )
        datos = reg_original.get_data()

        reg_nuevo = EstudianteActividadDTO()
        reg_nuevo.set_data(datos)

        assert reg_nuevo.get_data() == reg_original.get_data()
