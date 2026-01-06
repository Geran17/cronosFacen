import pytest
from src.modelos.dtos.asignatura_dto import AsignaturaDTO


class TestAsignaturaDTO:
    """Tests para AsignaturaDTO"""

    def test_crear_asignatura_vacia(self):
        """Test crear una asignatura con valores por defecto"""
        asignatura = AsignaturaDTO()
        assert asignatura.id_asignatura is None
        assert asignatura.codigo is None
        assert asignatura.nombre is None
        assert asignatura.creditos is None
        assert asignatura.horas_semanales is None
        assert asignatura.tipo is None
        assert asignatura.id_carrera is None

    def test_crear_asignatura_con_datos(self):
        """Test crear una asignatura con todos los parámetros"""
        asignatura = AsignaturaDTO(
            id_asignatura=1,
            codigo='SIS101',
            nombre='Programación I',
            creditos=4,
            horas_semanales=5,
            tipo='obligatoria',
            id_carrera=1,
        )
        assert asignatura.id_asignatura == 1
        assert asignatura.codigo == 'SIS101'
        assert asignatura.nombre == 'Programación I'
        assert asignatura.creditos == 4
        assert asignatura.horas_semanales == 5
        assert asignatura.tipo == 'obligatoria'
        assert asignatura.id_carrera == 1

    def test_get_data(self):
        """Test obtener datos como diccionario"""
        asignatura = AsignaturaDTO(
            id_asignatura=1,
            codigo='SIS101',
            nombre='Programación I',
            creditos=4,
            horas_semanales=5,
            tipo='obligatoria',
            id_carrera=1,
        )
        datos = asignatura.get_data()
        assert isinstance(datos, dict)
        assert datos['id_asignatura'] == 1
        assert datos['codigo'] == 'SIS101'
        assert datos['nombre'] == 'Programación I'
        assert datos['creditos'] == 4
        assert datos['horas_semanales'] == 5
        assert datos['tipo'] == 'obligatoria'
        assert datos['id_carrera'] == 1

    def test_set_data_completo(self):
        """Test establecer todos los datos desde un diccionario"""
        asignatura = AsignaturaDTO()
        datos = {
            'id_asignatura': 1,
            'codigo': 'SIS101',
            'nombre': 'Programación I',
            'creditos': 4,
            'horas_semanales': 5,
            'tipo': 'obligatoria',
            'id_carrera': 1,
        }
        asignatura.set_data(datos)
        assert asignatura.id_asignatura == 1
        assert asignatura.codigo == 'SIS101'
        assert asignatura.nombre == 'Programación I'

    def test_set_data_parcial(self):
        """Test establecer datos parciales preserva valores existentes"""
        asignatura = AsignaturaDTO(id_asignatura=1, codigo='SIS101', nombre='Programación I')
        datos = {'creditos': 4}
        asignatura.set_data(datos)
        assert asignatura.id_asignatura == 1
        assert asignatura.codigo == 'SIS101'
        assert asignatura.nombre == 'Programación I'
        assert asignatura.creditos == 4

    def test_tipo_asignatura_validos(self):
        """Test que se pueden asignar diferentes tipos de asignaturas"""
        tipos = ['obligatoria', 'electiva', 'optativa']
        for tipo in tipos:
            asignatura = AsignaturaDTO(tipo=tipo)
            assert asignatura.tipo == tipo

    def test_creditos_positivo(self):
        """Test que se pueden asignar créditos positivos"""
        creditos_validos = [1, 2, 3, 4, 5, 10]
        for creditos in creditos_validos:
            asignatura = AsignaturaDTO(creditos=creditos)
            assert asignatura.creditos == creditos

    def test_horas_semanales_positivo(self):
        """Test que se pueden asignar horas semanales positivas"""
        horas = [2, 3, 4, 5, 6]
        for h in horas:
            asignatura = AsignaturaDTO(horas_semanales=h)
            assert asignatura.horas_semanales == h

    def test_roundtrip_get_set_data(self):
        """Test que get_data y set_data son consistentes"""
        asignatura_original = AsignaturaDTO(
            id_asignatura=1,
            codigo='SIS101',
            nombre='Programación I',
            creditos=4,
            horas_semanales=5,
            tipo='obligatoria',
            id_carrera=1,
        )
        datos = asignatura_original.get_data()

        asignatura_nueva = AsignaturaDTO()
        asignatura_nueva.set_data(datos)

        assert asignatura_nueva.get_data() == asignatura_original.get_data()
