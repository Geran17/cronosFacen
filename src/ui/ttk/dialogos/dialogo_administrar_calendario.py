from ttkbootstrap import Toplevel
from ttkbootstrap.constants import *
from ui.ttk.frames.frame_administrar_calendario import FrameAdministrarCalendario
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class DialogoAdministrarCalendario(Toplevel):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.title("Administrador de Calendario")
        self.geometry("1200x700+10+10")

        frame = FrameAdministrarCalendario(master=self)
        frame.pack(side=TOP, fill=BOTH, expand=TRUE)
