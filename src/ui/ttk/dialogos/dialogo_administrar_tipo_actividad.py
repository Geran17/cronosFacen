from ttkbootstrap import Toplevel
from ttkbootstrap.constants import *
from ui.ttk.frames.frame_administrar_tipo_actividad import FrameAdministrarTipoActividad
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class DialogoAdministrarTipoActividad(Toplevel):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.title("Administrador de Tipos de Actividad")
        self.geometry("800x600+10+10")

        frame = FrameAdministrarTipoActividad(master=self)
        frame.pack(side=TOP, fill=BOTH, expand=TRUE)
