from ui.ttk.dialogos.base_dialog import BaseDialog
from ttkbootstrap.constants import *
from ui.ttk.frames.frame_administrar_carrera import FrameAdministrarCarrera
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class DialogoAdministrarCarrera(BaseDialog):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, title="Administrador de Carreras", geometry="800x600", minsize=(800, 600), **kwargs)

        frame = FrameAdministrarCarrera(master=self)
        frame.pack(side=TOP, fill=BOTH, expand=TRUE)
