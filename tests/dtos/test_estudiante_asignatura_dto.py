import pytest
from src.modelos.dtos.estudiante_asignatura_dto import EstudianteAsignaturaDTO


class TestEstudianteAsignaturaDTO:
    """Tests para EstudianteAsignaturaDTO"""

    def test_crear_estudiante_asignatura_vacio(self):
        """Test crear un registro estudiante-asignatura con valores por defecto"""
        reg = EstudianteAsignaturaDTO()
        assert reg.id_estudiante is None
        assert reg.id_asignatura is None
        assert reg.estado is None
        assert reg.nota_final is None
        assert reg.periodo is None

    def test_crear_estudiante_asignatura_con_datos(self):
        """Test crear un registro estudiante-asignatura con todos los parámetros"""
        reg = EstudianteAsignaturaDTO(
            id_estudiante=1, id_asignatura=1, estado='aprobada', nota_final=85.5, periodo='2025-I'
        )
        assert reg.id_estudiante == 1
        assert reg.id_asignatura == 1
        assert reg.estado == 'aprobada'
        assert reg.nota_final == 85.5
        assert reg.periodo == '2025-I'

    def test_get_data(self):
        """Test obtener datos como diccionario"""
        reg = EstudianteAsignaturaDTO(
            id_estudiante=1, id_asignatura=1, estado='aprobada', nota_final=85.5, periodo='2025-I'
        )
        datos = reg.get_data()
        assert isinstance(datos, dict)
        assert datos['id_estudiante'] == 1
        assert datos['id_asignatura'] == 1
        assert datos['estado'] == 'aprobada'
        assert datos['nota_final'] == 85.5
        assert datos['periodo'] == '2025-I'

    def test_set_data_completo(self):
        """Test establecer todos los datos desde un diccionario"""
        reg = EstudianteAsignaturaDTO()
        datos = {
            'id_estudiante': 1,
            'id_asignatura': 1,
            'estado': 'aprobada',
            'nota_final': 85.5,
            'periodo': '2025-I',
        }
        reg.set_data(datos)
        assert reg.id_estudiante == 1
        assert reg.id_asignatura == 1
        assert reg.estado == 'aprobada'
        assert reg.nota_final == 85.5
        assert reg.periodo == '2025-I'

    def test_set_data_parcial(self):
        """Test establecer datos parciales preserva valores existentes"""
        reg = EstudianteAsignaturaDTO(id_estudiante=1, id_asignatura=1)
        datos = {'estado': 'aprobada', 'nota_final': 85.5}
        reg.set_data(datos)
        assert reg.id_estudiante == 1
        assert reg.id_asignatura == 1
        assert reg.estado == 'aprobada'
        assert reg.nota_final == 85.5

    def test_estados_validos(self):
        """Test que se pueden asignar diferentes estados"""
        estados = ['no_cursada', 'cursando', 'aprobada', 'reprobada']
        for estado in estados:
            reg = EstudianteAsignaturaDTO(estado=estado)
            assert reg.estado == estado

    def test_notas_validas(self):
        """Test que se pueden asignar diferentes notas"""
        notas = [0.0, 25.5, 50.0, 75.5, 100.0]
        for nota in notas:
            reg = EstudianteAsignaturaDTO(nota_final=nota)
            assert reg.nota_final == nota

    def test_periodos_academicos(self):
        """Test que se pueden asignar diferentes períodos académicos"""
        periodos = ['2024-I', '2024-II', '2025-I', '2025-II', '2025-Verano']
        for periodo in periodos:
            reg = EstudianteAsignaturaDTO(periodo=periodo)
            assert reg.periodo == periodo

    def test_multiples_asignaturas_estudiante(self):
        """Test que un estudiante puede estar en múltiples asignaturas"""
        registros = [(1, 1, 'aprobada', 85.5), (1, 2, 'cursando', None), (1, 3, 'reprobada', 45.0)]
        for id_est, id_asig, estado, nota in registros:
            reg = EstudianteAsignaturaDTO(
                id_estudiante=id_est, id_asignatura=id_asig, estado=estado, nota_final=nota
            )
            assert reg.id_estudiante == id_est
            assert reg.id_asignatura == id_asig
            assert reg.estado == estado
            assert reg.nota_final == nota

    def test_set_data_vacio(self):
        """Test set_data con diccionario vacío no causa errores"""
        reg = EstudianteAsignaturaDTO(id_estudiante=1, id_asignatura=1)
        reg.set_data({})
        assert reg.id_estudiante == 1
        assert reg.id_asignatura == 1

    def test_set_data_none(self):
        """Test set_data con None no causa errores"""
        reg = EstudianteAsignaturaDTO(id_estudiante=1, id_asignatura=1)
        reg.set_data({})
        assert reg.id_estudiante == 1
        assert reg.id_asignatura == 1

    def test_roundtrip_get_set_data(self):
        """Test que get_data y set_data son consistentes"""
        reg_original = EstudianteAsignaturaDTO(
            id_estudiante=1, id_asignatura=1, estado='aprobada', nota_final=85.5, periodo='2025-I'
        )
        datos = reg_original.get_data()

        reg_nuevo = EstudianteAsignaturaDTO()
        reg_nuevo.set_data(datos)

        assert reg_nuevo.get_data() == reg_original.get_data()
