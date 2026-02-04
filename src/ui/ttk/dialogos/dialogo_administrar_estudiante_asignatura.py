from ui.ttk.dialogos.base_dialog import BaseDialog
from ttkbootstrap.constants import *
from ui.ttk.frames.frame_administrar_estudiante_asignatura import FrameAdministrarEstudianteAsignatura
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class DialogoAdministrarEstudianteAsignatura(BaseDialog):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, title="Administrador de Estudiante-Asignatura", geometry="1000x650", minsize=(1000, 650), **kwargs)

        frame = FrameAdministrarEstudianteAsignatura(master=self)
        frame.pack(side=TOP, fill=BOTH, expand=TRUE)
