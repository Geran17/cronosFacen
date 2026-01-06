import pytest
from src.modelos.dtos.prerequisito_dto import PrerrequisiteDTO


class TestPrerrequisiteDTO:
    """Tests para PrerrequisiteDTO"""

    def test_crear_prerequisito_vacio(self):
        """Test crear un prerequisito con valores por defecto"""
        prerequisito = PrerrequisiteDTO()
        assert prerequisito.id_asignatura is None
        assert prerequisito.id_asignatura_prerequisito is None

    def test_crear_prerequisito_con_datos(self):
        """Test crear un prerequisito con todos los parámetros"""
        prerequisito = PrerrequisiteDTO(id_asignatura=2, id_asignatura_prerequisito=1)
        assert prerequisito.id_asignatura == 2
        assert prerequisito.id_asignatura_prerequisito == 1

    def test_get_data(self):
        """Test obtener datos como diccionario"""
        prerequisito = PrerrequisiteDTO(id_asignatura=2, id_asignatura_prerequisito=1)
        datos = prerequisito.get_data()
        assert isinstance(datos, dict)
        assert datos['id_asignatura'] == 2
        assert datos['id_asignatura_prerequisito'] == 1

    def test_set_data_completo(self):
        """Test establecer todos los datos desde un diccionario"""
        prerequisito = PrerrequisiteDTO()
        datos = {'id_asignatura': 2, 'id_asignatura_prerequisito': 1}
        prerequisito.set_data(datos)
        assert prerequisito.id_asignatura == 2
        assert prerequisito.id_asignatura_prerequisito == 1

    def test_set_data_parcial(self):
        """Test establecer datos parciales preserva valores existentes"""
        prerequisito = PrerrequisiteDTO(id_asignatura=2)
        datos = {'id_asignatura_prerequisito': 1}
        prerequisito.set_data(datos)
        assert prerequisito.id_asignatura == 2
        assert prerequisito.id_asignatura_prerequisito == 1

    def test_prerequisitos_multiples(self):
        """Test crear múltiples relaciones de prerequisitos"""
        pares = [(2, 1), (3, 1), (3, 2), (4, 3), (5, 3)]
        for id_asig, id_prereq in pares:
            prerequisito = PrerrequisiteDTO(
                id_asignatura=id_asig, id_asignatura_prerequisito=id_prereq
            )
            assert prerequisito.id_asignatura == id_asig
            assert prerequisito.id_asignatura_prerequisito == id_prereq

    def test_set_data_vacio(self):
        """Test set_data con diccionario vacío no causa errores"""
        prerequisito = PrerrequisiteDTO(id_asignatura=2)
        prerequisito.set_data({})
        assert prerequisito.id_asignatura == 2

    def test_set_data_none(self):
        """Test set_data con None no causa errores"""
        prerequisito = PrerrequisiteDTO(id_asignatura=2)
        prerequisito.set_data({})
        assert prerequisito.id_asignatura == 2

    def test_roundtrip_get_set_data(self):
        """Test que get_data y set_data son consistentes"""
        prerequisito_original = PrerrequisiteDTO(id_asignatura=2, id_asignatura_prerequisito=1)
        datos = prerequisito_original.get_data()

        prerequisito_nuevo = PrerrequisiteDTO()
        prerequisito_nuevo.set_data(datos)

        assert prerequisito_nuevo.get_data() == prerequisito_original.get_data()
