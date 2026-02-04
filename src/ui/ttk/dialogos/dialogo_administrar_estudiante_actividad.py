from ui.ttk.dialogos.base_dialog import BaseDialog
from ttkbootstrap.constants import *
from ui.ttk.frames.frame_administrar_estudiante_actividad import FrameAdministrarEstudianteActividad
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class DialogoAdministrarEstudianteActividad(BaseDialog):
    def __init__(self, parent=None, preselect=None, **kwargs):
        super().__init__(
            parent,
            title="Administrador de Estudiante-Actividad",
            geometry="1200x700",
            minsize=(1200, 700),
            **kwargs,
        )
        frame = FrameAdministrarEstudianteActividad(master=self, preselect=preselect)
        frame.pack(side=TOP, fill=BOTH, expand=TRUE)
