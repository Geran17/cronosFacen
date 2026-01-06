from ttkbootstrap import Toplevel
from ttkbootstrap.constants import *
from ui.ttk.frames.frame_administrar_asignatura import FrameAdministrarAsignatura
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class DialogoAdministrarAsignatura(Toplevel):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.title("Administrador de Asignaturas")
        self.geometry("900x650+10+10")

        frame = FrameAdministrarAsignatura(master=self)
        frame.pack(side=TOP, fill=BOTH, expand=TRUE)
