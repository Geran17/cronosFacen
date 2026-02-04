from ui.ttk.dialogos.base_dialog import BaseDialog
from ttkbootstrap.constants import *
from ui.ttk.frames.frame_administrar_estudiante import FrameAdministrarEstudiante
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class DialogoAdministrarEstudiante(BaseDialog):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, title="Administrador de Estudiantes", geometry="900x650", minsize=(900, 650), **kwargs)

        frame = FrameAdministrarEstudiante(master=self)
        frame.pack(side=TOP, fill=BOTH, expand=TRUE)
