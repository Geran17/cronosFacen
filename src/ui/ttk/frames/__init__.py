"""
Frames de la aplicación CronosFacen

Este paquete contiene todos los frames (paneles) principales de la interfaz
gráfica de la aplicación.
"""

from .frame_principal import FramePrincipal
from .frame_administrar_carrera import FrameAdministrarCarrera
from .frame_administrar_estudiante import FrameAdministrarEstudiante
from .frame_administrar_asignatura import FrameAdministrarAsignatura
from .frame_administrar_eje_tematico import FrameAdministrarEjeTematico
from .frame_administrar_tipo_actividad import FrameAdministrarTipoActividad
from .frame_administrar_actividad import FrameAdministrarActividad
from .frame_administrar_calendario import FrameAdministrarCalendario
from .frame_acerca_de import FrameAcercaDe
from .frame_bienvenidad import FrameBienvenidad
from .frame_alertas import FrameAlertas
from .frame_dashboard import FrameDashboard
from .frame_cuellos import FrameCuellos

__all__ = [
    "FramePrincipal",
    "FrameAdministrarCarrera",
    "FrameAdministrarEstudiante",
    "FrameAdministrarAsignatura",
    "FrameAdministrarEjeTematico",
    "FrameAdministrarTipoActividad",
    "FrameAdministrarActividad",
    "FrameAdministrarCalendario",
    "FrameAcercaDe",
    "FrameAlertas",
    "FrameDashboard",
    "FrameCuellos",
    "FrameBienvenidad",
]
