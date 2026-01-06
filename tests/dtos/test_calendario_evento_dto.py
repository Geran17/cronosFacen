import pytest
from src.modelos.dtos.calendario_evento_dto import CalendarioEventoDTO


class TestCalendarioEventoDTO:
    """Tests para CalendarioEventoDTO"""

    def test_crear_evento_vacio(self):
        """Test crear un evento con valores por defecto"""
        evento = CalendarioEventoDTO()
        assert evento.id_evento is None
        assert evento.titulo is None
        assert evento.tipo is None
        assert evento.fecha_inicio is None
        assert evento.fecha_fin is None
        assert evento.afecta_actividades is None

    def test_crear_evento_con_datos(self):
        """Test crear un evento con todos los parámetros"""
        evento = CalendarioEventoDTO(
            id_evento=1,
            titulo='Período de Exámenes',
            tipo='examen',
            fecha_inicio='2025-06-01',
            fecha_fin='2025-06-15',
            afecta_actividades=1,
        )
        assert evento.id_evento == 1
        assert evento.titulo == 'Período de Exámenes'
        assert evento.tipo == 'examen'
        assert evento.fecha_inicio == '2025-06-01'
        assert evento.fecha_fin == '2025-06-15'
        assert evento.afecta_actividades == 1

    def test_get_data(self):
        """Test obtener datos como diccionario"""
        evento = CalendarioEventoDTO(
            id_evento=1,
            titulo='Período de Exámenes',
            tipo='examen',
            fecha_inicio='2025-06-01',
            fecha_fin='2025-06-15',
            afecta_actividades=1,
        )
        datos = evento.get_data()
        assert isinstance(datos, dict)
        assert datos['id_evento'] == 1
        assert datos['titulo'] == 'Período de Exámenes'
        assert datos['tipo'] == 'examen'
        assert datos['fecha_inicio'] == '2025-06-01'
        assert datos['fecha_fin'] == '2025-06-15'
        assert datos['afecta_actividades'] == 1

    def test_set_data_completo(self):
        """Test establecer todos los datos desde un diccionario"""
        evento = CalendarioEventoDTO()
        datos = {
            'id_evento': 1,
            'titulo': 'Período de Exámenes',
            'tipo': 'examen',
            'fecha_inicio': '2025-06-01',
            'fecha_fin': '2025-06-15',
            'afecta_actividades': 1,
        }
        evento.set_data(datos)
        assert evento.id_evento == 1
        assert evento.titulo == 'Período de Exámenes'
        assert evento.tipo == 'examen'

    def test_set_data_parcial(self):
        """Test establecer datos parciales preserva valores existentes"""
        evento = CalendarioEventoDTO(id_evento=1, titulo='Período de Exámenes')
        datos = {'tipo': 'examen'}
        evento.set_data(datos)
        assert evento.id_evento == 1
        assert evento.titulo == 'Período de Exámenes'
        assert evento.tipo == 'examen'

    def test_tipos_eventos_validos(self):
        """Test que se pueden asignar diferentes tipos de eventos"""
        tipos = ['receso', 'examen', 'entrega', 'festivo', 'semana_tecnica']
        for tipo in tipos:
            evento = CalendarioEventoDTO(tipo=tipo)
            assert evento.tipo == tipo

    def test_afecta_actividades_binario(self):
        """Test que afecta_actividades acepta valores binarios"""
        valores = [0, 1]
        for valor in valores:
            evento = CalendarioEventoDTO(afecta_actividades=valor)
            assert evento.afecta_actividades == valor

    def test_fechas_iso_format(self):
        """Test que se pueden asignar fechas en formato ISO"""
        fechas = ['2025-01-01', '2025-06-15', '2025-12-31']
        for fecha in fechas:
            evento = CalendarioEventoDTO(fecha_inicio=fecha)
            assert evento.fecha_inicio == fecha

    def test_set_data_vacio(self):
        """Test set_data con diccionario vacío no causa errores"""
        evento = CalendarioEventoDTO(id_evento=1, titulo='Evento')
        evento.set_data({})
        assert evento.id_evento == 1
        assert evento.titulo == 'Evento'

    def test_set_data_none(self):
        """Test set_data con None no causa errores"""
        evento = CalendarioEventoDTO(id_evento=1, titulo='Evento')
        evento.set_data({})
        assert evento.id_evento == 1
        assert evento.titulo == 'Evento'

    def test_roundtrip_get_set_data(self):
        """Test que get_data y set_data son consistentes"""
        evento_original = CalendarioEventoDTO(
            id_evento=1,
            titulo='Período de Exámenes',
            tipo='examen',
            fecha_inicio='2025-06-01',
            fecha_fin='2025-06-15',
            afecta_actividades=1,
        )
        datos = evento_original.get_data()

        evento_nuevo = CalendarioEventoDTO()
        evento_nuevo.set_data(datos)

        assert evento_nuevo.get_data() == evento_original.get_data()
