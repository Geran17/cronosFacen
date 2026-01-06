from ttkbootstrap import Toplevel
from ttkbootstrap.constants import *
from ui.ttk.frames.frame_administrar_estudiante import FrameAdministrarEstudiante
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class DialogoAdministrarEstudiante(Toplevel):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.title("Administrador de Estudiantes")
        self.geometry("800x600+10+10")

        frame = FrameAdministrarEstudiante(master=self)
        frame.pack(side=TOP, fill=BOTH, expand=TRUE)
