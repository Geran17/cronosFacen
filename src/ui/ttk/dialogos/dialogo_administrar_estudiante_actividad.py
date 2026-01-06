from ttkbootstrap import Toplevel
from ttkbootstrap.constants import *
from ui.ttk.frames.frame_administrar_estudiante_actividad import FrameAdministrarEstudianteActividad
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class DialogoAdministrarEstudianteActividad(Toplevel):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.title("Administrador de Estudiante-Actividad")
        self.geometry("1000x650+10+10")

        frame = FrameAdministrarEstudianteActividad(master=self)
        frame.pack(side=TOP, fill=BOTH, expand=TRUE)
