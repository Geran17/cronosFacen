from ttkbootstrap import Toplevel
from ttkbootstrap.constants import *
from ui.ttk.frames.frame_administrar_eje_tematico import FrameAdministrarEjeTematico
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class DialogoAdministrarEjeTemático(Toplevel):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.title("Administrador de Ejes Temáticos")
        self.geometry("950x700+10+10")

        frame = FrameAdministrarEjeTematico(master=self)
        frame.pack(side=TOP, fill=BOTH, expand=TRUE)
