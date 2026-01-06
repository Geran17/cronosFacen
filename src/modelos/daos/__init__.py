"""
Módulo de Data Access Objects (DAOs) para acceso a la base de datos.

Contiene clases DAO para cada tabla del modelo de datos, proporcionando
operaciones CRUD y consultas específicas de negocio.
"""

from .conexion_sqlite import ConexionSQLite
from .base_dao import DAO

__all__ = ["ConexionSQLite", "DAO"]

__all__ = [
    "ConexionSQLite",
    "DAOBase",
    "SchemaDAO",
    "CarreraDAO",
    "AsignaturaDAO",
    "PrerrequisiteDAO",
    "EjeTematicoDAO",
    "TipoActividadDAO",
    "ActividadDAO",
    "CalendarioEventoDAO",
    "EstudianteDAO",
    "EstudianteAsignaturaDAO",
    "EstudianteActividadDAO",
]
