"""
Diálogos de la aplicación CronosFacen

Este paquete contiene todos los diálogos modales de la interfaz gráfica.
"""

from .dialogo_administrar_carrera import DialogoAdministrarCarrera
from .dialogo_administrar_estudiante import DialogoAdministrarEstudiante
from .dialogo_administrar_estudiante_carrera import DialogoAdministrarEstudianteCarrera
from .dialogo_administrar_asignatura import DialogoAdministrarAsignatura
from .dialogo_administrar_eje_tematico import DialogoAdministrarEjeTemático
from .dialogo_administrar_tipo_actividad import DialogoAdministrarTipoActividad
from .dialogo_administrar_actividad import DialogoAdministrarActividad
from .dialogo_administrar_calendario import DialogoAdministrarCalendario
from .dialogo_acerca_de import DialogoAcercaDe

__all__ = [
    "DialogoAdministrarCarrera",
    "DialogoAdministrarEstudiante",
    "DialogoAdministrarEstudianteCarrera",
    "DialogoAdministrarAsignatura",
    "DialogoAdministrarEjeTemático",
    "DialogoAdministrarTipoActividad",
    "DialogoAdministrarActividad",
    "DialogoAdministrarCalendario",
    "DialogoAcercaDe",
]
