from ttkbootstrap import Toplevel
from ttkbootstrap.constants import *
from ui.ttk.frames.frame_administrar_estudiante_carrera import FrameAdministrarEstudianteCarrera
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class DialogoAdministrarEstudianteCarrera(Toplevel):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.title("Administrador de Inscripciones Estudiante-Carrera")
        self.geometry("1200x700+50+50")

        frame = FrameAdministrarEstudianteCarrera(master=self)
        frame.pack(side=TOP, fill=BOTH, expand=TRUE)
