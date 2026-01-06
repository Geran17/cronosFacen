import pytest
from src.modelos.dtos.estudiante_dto import EstudianteDTO


class TestEstudianteDTO:
    """Tests para EstudianteDTO"""

    def test_crear_estudiante_vacio(self):
        """Test crear un estudiante con valores por defecto"""
        estudiante = EstudianteDTO()
        assert estudiante.id_estudiante is None
        assert estudiante.nombre is None
        assert estudiante.correo is None
        assert estudiante.id_carrera is None

    def test_crear_estudiante_con_datos(self):
        """Test crear un estudiante con todos los parámetros"""
        estudiante = EstudianteDTO(
            id_estudiante=1, nombre='Juan Pérez', correo='juan.perez@universidad.edu', id_carrera=1
        )
        assert estudiante.id_estudiante == 1
        assert estudiante.nombre == 'Juan Pérez'
        assert estudiante.correo == 'juan.perez@universidad.edu'
        assert estudiante.id_carrera == 1

    def test_get_data(self):
        """Test obtener datos como diccionario"""
        estudiante = EstudianteDTO(
            id_estudiante=1, nombre='Juan Pérez', correo='juan.perez@universidad.edu', id_carrera=1
        )
        datos = estudiante.get_data()
        assert isinstance(datos, dict)
        assert datos['id_estudiante'] == 1
        assert datos['nombre'] == 'Juan Pérez'
        assert datos['correo'] == 'juan.perez@universidad.edu'
        assert datos['id_carrera'] == 1

    def test_set_data_completo(self):
        """Test establecer todos los datos desde un diccionario"""
        estudiante = EstudianteDTO()
        datos = {
            'id_estudiante': 1,
            'nombre': 'Juan Pérez',
            'correo': 'juan.perez@universidad.edu',
            'id_carrera': 1,
        }
        estudiante.set_data(datos)
        assert estudiante.id_estudiante == 1
        assert estudiante.nombre == 'Juan Pérez'
        assert estudiante.correo == 'juan.perez@universidad.edu'

    def test_set_data_parcial(self):
        """Test establecer datos parciales preserva valores existentes"""
        estudiante = EstudianteDTO(id_estudiante=1, nombre='Juan Pérez')
        datos = {'correo': 'nuevo@universidad.edu'}
        estudiante.set_data(datos)
        assert estudiante.id_estudiante == 1
        assert estudiante.nombre == 'Juan Pérez'
        assert estudiante.correo == 'nuevo@universidad.edu'

    def test_set_data_vacio(self):
        """Test set_data con diccionario vacío no causa errores"""
        estudiante = EstudianteDTO(id_estudiante=1, nombre='Juan')
        estudiante.set_data({})
        assert estudiante.id_estudiante == 1
        assert estudiante.nombre == 'Juan'

    def test_set_data_none(self):
        """Test set_data con None no causa errores"""
        estudiante = EstudianteDTO(id_estudiante=1, nombre='Juan')
        estudiante.set_data({})
        assert estudiante.id_estudiante == 1
        assert estudiante.nombre == 'Juan'

    def test_roundtrip_get_set_data(self):
        """Test que get_data y set_data son consistentes"""
        estudiante_original = EstudianteDTO(
            id_estudiante=1, nombre='Juan Pérez', correo='juan.perez@universidad.edu', id_carrera=1
        )
        datos = estudiante_original.get_data()

        estudiante_nuevo = EstudianteDTO()
        estudiante_nuevo.set_data(datos)

        assert estudiante_nuevo.get_data() == estudiante_original.get_data()

    def test_correo_valido(self):
        """Test que se pueden asignar correos válidos"""
        correos = [
            'juan@universidad.edu',
            'maria.lopez@university.com',
            'test.user+alias@example.org',
        ]
        for correo in correos:
            estudiante = EstudianteDTO(correo=correo)
            assert estudiante.correo == correo
