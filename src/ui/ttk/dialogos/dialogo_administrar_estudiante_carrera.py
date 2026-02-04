from ui.ttk.dialogos.base_dialog import BaseDialog
from ttkbootstrap.constants import *
from ui.ttk.frames.frame_administrar_estudiante_carrera import FrameAdministrarEstudianteCarrera
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class DialogoAdministrarEstudianteCarrera(BaseDialog):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        frame = FrameAdministrarEstudianteCarrera(master=self)
        frame.pack(side=TOP, fill=BOTH, expand=TRUE)
