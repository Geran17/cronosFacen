from ttkbootstrap import Toplevel
from ttkbootstrap.constants import *
from ui.ttk.frames.frame_administrar_prerequisitos import FrameAdministrarPrerequisitos
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class DialogoAdministrarPrerequisitos(Toplevel):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.title("Administrador de Prerequisitos")
        self.geometry("1000x650+10+10")

        frame = FrameAdministrarPrerequisitos(master=self)
        frame.pack(side=TOP, fill=BOTH, expand=TRUE)
