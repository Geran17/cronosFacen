import pytest
import os
import sqlite3
import uuid
from pathlib import Path
from src.modelos.daos.tipo_actividad_dao import TipoActividadDAO
from src.modelos.dtos.tipo_actividad_dto import TipoActividadDTO


def get_unique():
    """Genera un sufijo único para evitar conflictos UNIQUE"""
    return str(uuid.uuid4())[:8]


@pytest.fixture
def db_path(tmp_path):
    """Crea una ruta temporal para la base de datos de prueba."""
    db_file = tmp_path / "test_tipo_actividad.db"
    yield str(db_file)
    # Cleanup
    if db_file.exists():
        db_file.unlink()


@pytest.fixture
def tipo_actividad_dao(db_path):
    """Crea una instancia del DAO con base de datos temporal."""
    dao = TipoActividadDAO(ruta_db=db_path)
    yield dao


class TestTipoActividadDAO:
    """Suite de pruebas para la clase TipoActividadDAO."""

    def test_crear_tabla(self, tipo_actividad_dao):
        """Verifica que la tabla se crea correctamente."""
        tipo_actividad_dao.crear_tabla()

        with tipo_actividad_dao.get_conexion() as con:
            cursor = con.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='tipo_actividad'"
            )
            resultado = cursor.fetchone()
            assert resultado is not None, "La tabla 'tipo_actividad' no fue creada"

    def test_insertar(self, tipo_actividad_dao):
        """Verifica que se inserta correctamente un registro de tipo de actividad."""
        uid = get_unique()
        tipo_dto = TipoActividadDTO(
            nombre=f"Tarea-{uid}",
            siglas=f"TAR{uid[:3]}",
            descripcion="Actividad de refuerzo",
        )

        id_insertado = tipo_actividad_dao.insertar(tipo_dto)

        assert id_insertado is not None, "No se obtuvo ID después de insertar"
        assert id_insertado > 0, "El ID insertado debe ser mayor a 0"

    def test_insertar_multiples(self, tipo_actividad_dao):
        """Verifica que se pueden insertar múltiples registros."""
        u1, u2, u3 = get_unique(), get_unique(), get_unique()
        tipos = [
            TipoActividadDTO(nombre=f"Tarea-{u1}", siglas=f"TAR{u1[:3]}", descripcion="Tarea"),
            TipoActividadDTO(nombre=f"Quiz-{u2}", siglas=f"QZ{u2[:3]}", descripcion="Quiz"),
            TipoActividadDTO(nombre=f"Examen-{u3}", siglas=f"EXN{u3[:3]}", descripcion="Examen"),
        ]

        ids = [tipo_actividad_dao.insertar(tipo) for tipo in tipos]

        assert all(id is not None for id in ids), "Todos los IDs deben ser válidos"
        assert len(ids) == 3, "Debe insertar 3 registros"

    def test_instanciar_existente(self, tipo_actividad_dao):
        """Verifica que se instancia correctamente un tipo existente."""
        uid = get_unique()
        tipo_original = TipoActividadDTO(
            nombre=f"Tarea-{uid}",
            siglas=f"TAR{uid[:3]}",
            descripcion="Actividad de refuerzo",
        )
        id_creado = tipo_actividad_dao.insertar(tipo_original)

        tipo_recuperado = TipoActividadDTO(id_tipo_actividad=id_creado)
        resultado = tipo_actividad_dao.instanciar(tipo_recuperado)

        assert resultado is True, "Debería encontrar el tipo de actividad"
        assert tipo_recuperado.nombre == tipo_original.nombre, "El nombre debe coincidir"

    def test_instanciar_inexistente(self, tipo_actividad_dao):
        """Verifica que no se instancia un ID que no existe."""
        tipo_inexistente = TipoActividadDTO(id_tipo_actividad=999)
        resultado = tipo_actividad_dao.instanciar(tipo_inexistente)

        assert resultado is False, "No debería encontrar un tipo inexistente"

    def test_instanciar_id_invalido(self, tipo_actividad_dao):
        """Verifica el manejo de ID inválido."""
        tipo_invalido = TipoActividadDTO(id_tipo_actividad=None)
        resultado = tipo_actividad_dao.instanciar(tipo_invalido)

        assert resultado is False, "No debería instanciar con ID None"

    def test_existe_verdadero(self, tipo_actividad_dao):
        """Verifica que existe() retorna True para un registro insertado."""
        uid = get_unique()
        tipo_original = TipoActividadDTO(
            nombre=f"Tarea-{uid}",
            siglas=f"TAR{uid[:3]}",
            descripcion="Actividad de refuerzo",
        )
        id_creado = tipo_actividad_dao.insertar(tipo_original)

        tipo_verificar = TipoActividadDTO(id_tipo_actividad=id_creado)
        existe = tipo_actividad_dao.existe(tipo_verificar)

        assert existe is True, "Debería confirmar que el tipo existe"

    def test_existe_falso(self, tipo_actividad_dao):
        """Verifica que existe() retorna False para un ID inexistente."""
        tipo_no_existe = TipoActividadDTO(id_tipo_actividad=999)
        existe = tipo_actividad_dao.existe(tipo_no_existe)

        assert existe is False, "No debería encontrar un tipo inexistente"

    def test_existe_id_invalido(self, tipo_actividad_dao):
        """Verifica el manejo de ID inválido en existe()."""
        tipo_invalido = TipoActividadDTO(id_tipo_actividad=None)
        existe = tipo_actividad_dao.existe(tipo_invalido)

        assert existe is False, "No debería confirmar existencia con ID None"

    def test_eliminar(self, tipo_actividad_dao):
        """Verifica que se elimina correctamente un registro."""
        uid = get_unique()
        tipo_original = TipoActividadDTO(
            nombre=f"Tarea-{uid}",
            siglas=f"TAR{uid[:3]}",
            descripcion="Actividad de refuerzo",
        )
        id_creado = tipo_actividad_dao.insertar(tipo_original)

        tipo_verificar = TipoActividadDTO(id_tipo_actividad=id_creado)
        assert tipo_actividad_dao.existe(tipo_verificar) is True

        resultado_eliminacion = tipo_actividad_dao.eliminar(tipo_verificar)
        assert resultado_eliminacion is True, "La eliminación debe retornar True"
        assert (
            tipo_actividad_dao.existe(tipo_verificar) is False
        ), "El registro debe estar eliminado"

    def test_eliminar_inexistente(self, tipo_actividad_dao):
        """Verifica que eliminar un registro inexistente retorna False."""
        tipo_no_existe = TipoActividadDTO(id_tipo_actividad=999)
        resultado = tipo_actividad_dao.eliminar(tipo_no_existe)

        assert resultado is False, "No debe eliminar un registro inexistente"

    def test_ciclo_completo(self, tipo_actividad_dao):
        """Verifica un ciclo completo: crear, instanciar, modificar, eliminar."""
        uid = get_unique()
        # 1. Crear
        tipo_original = TipoActividadDTO(
            nombre=f"Tarea-{uid}",
            siglas=f"TAR{uid[:3]}",
            descripcion="Actividad de refuerzo",
        )
        id_creado = tipo_actividad_dao.insertar(tipo_original)
        assert id_creado is not None

        # 2. Instanciar
        tipo_recuperado = TipoActividadDTO(id_tipo_actividad=id_creado)
        assert tipo_actividad_dao.instanciar(tipo_recuperado) is True
        assert tipo_recuperado.nombre == tipo_original.nombre

        # 3. Verificar existencia
        assert tipo_actividad_dao.existe(tipo_recuperado) is True

        # 4. Eliminar
        assert tipo_actividad_dao.eliminar(tipo_recuperado) is True
        assert tipo_actividad_dao.existe(tipo_recuperado) is False
