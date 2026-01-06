import pytest
from modelos.dtos.estudiante_carrera_dto import EstudianteCarreraDTO


def test_crear_dto_con_valores_por_defecto():
    """Prueba crear DTO con valores por defecto"""
    dto = EstudianteCarreraDTO()

    assert dto.id_estudiante is None
    assert dto.id_carrera is None
    assert dto.estado == 'activa'
    assert dto.fecha_inscripcion is None
    assert dto.fecha_inicio is None
    assert dto.fecha_fin is None
    assert dto.es_carrera_principal == 1
    assert dto.periodo_ingreso is None
    assert dto.observaciones is None


def test_crear_dto_con_valores_iniciales():
    """Prueba crear DTO con valores iniciales"""
    dto = EstudianteCarreraDTO(
        id_estudiante=1,
        id_carrera=5,
        estado='activa',
        fecha_inscripcion='2024-03-01',
        es_carrera_principal=1,
        periodo_ingreso='2024-1',
    )

    assert dto.id_estudiante == 1
    assert dto.id_carrera == 5
    assert dto.estado == 'activa'
    assert dto.fecha_inscripcion == '2024-03-01'
    assert dto.es_carrera_principal == 1
    assert dto.periodo_ingreso == '2024-1'


def test_get_data():
    """Prueba obtener datos como diccionario"""
    dto = EstudianteCarreraDTO(
        id_estudiante=2,
        id_carrera=3,
        estado='completada',
        fecha_inscripcion='2020-03-01',
        fecha_fin='2024-12-20',
        es_carrera_principal=1,
        periodo_ingreso='2020-1',
        observaciones='Graduado con honores',
    )

    data = dto.get_data()

    assert data['id_estudiante'] == 2
    assert data['id_carrera'] == 3
    assert data['estado'] == 'completada'
    assert data['fecha_inscripcion'] == '2020-03-01'
    assert data['fecha_fin'] == '2024-12-20'
    assert data['es_carrera_principal'] == 1
    assert data['periodo_ingreso'] == '2020-1'
    assert data['observaciones'] == 'Graduado con honores'


def test_set_data():
    """Prueba establecer datos desde diccionario"""
    dto = EstudianteCarreraDTO()

    data = {
        'id_estudiante': 10,
        'id_carrera': 7,
        'estado': 'suspendida',
        'fecha_inscripcion': '2023-03-01',
        'fecha_inicio': '2023-03-15',
        'es_carrera_principal': 0,
        'periodo_ingreso': '2023-1',
        'observaciones': 'Suspensión temporal',
    }

    dto.set_data(data)

    assert dto.id_estudiante == 10
    assert dto.id_carrera == 7
    assert dto.estado == 'suspendida'
    assert dto.fecha_inscripcion == '2023-03-01'
    assert dto.fecha_inicio == '2023-03-15'
    assert dto.es_carrera_principal == 0
    assert dto.periodo_ingreso == '2023-1'
    assert dto.observaciones == 'Suspensión temporal'


def test_set_data_parcial():
    """Prueba establecer solo algunos datos"""
    dto = EstudianteCarreraDTO(
        id_estudiante=5, id_carrera=3, estado='activa', fecha_inscripcion='2024-01-01'
    )

    # Actualizar solo algunos campos
    data = {'estado': 'inactiva', 'observaciones': 'Receso temporal'}

    dto.set_data(data)

    assert dto.id_estudiante == 5  # No cambió
    assert dto.id_carrera == 3  # No cambió
    assert dto.estado == 'inactiva'  # Cambió
    assert dto.fecha_inscripcion == '2024-01-01'  # No cambió
    assert dto.observaciones == 'Receso temporal'  # Cambió


def test_estados_validos():
    """Prueba diferentes estados válidos"""
    estados = ['activa', 'inactiva', 'suspendida', 'completada', 'abandonada']

    for estado in estados:
        dto = EstudianteCarreraDTO(
            id_estudiante=1, id_carrera=1, estado=estado, fecha_inscripcion='2024-01-01'
        )
        assert dto.estado == estado


def test_carrera_principal_vs_secundaria():
    """Prueba distinción entre carrera principal y secundaria"""
    dto_principal = EstudianteCarreraDTO(id_estudiante=1, id_carrera=1, es_carrera_principal=1)

    dto_secundaria = EstudianteCarreraDTO(id_estudiante=1, id_carrera=2, es_carrera_principal=0)

    assert dto_principal.es_carrera_principal == 1
    assert dto_secundaria.es_carrera_principal == 0
