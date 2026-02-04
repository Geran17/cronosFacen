from ui.ttk.dialogos.base_dialog import BaseDialog
from ttkbootstrap.constants import *
from ui.ttk.frames.frame_administrar_calendario import FrameAdministrarCalendario
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class DialogoAdministrarCalendario(BaseDialog):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, title="Administrador de Calendario", geometry="1200x700", minsize=(1200, 700), **kwargs)
        frame = FrameAdministrarCalendario(master=self)
        frame.pack(side=TOP, fill=BOTH, expand=TRUE)
