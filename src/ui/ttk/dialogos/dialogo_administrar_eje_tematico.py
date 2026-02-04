from ui.ttk.dialogos.base_dialog import BaseDialog
from ttkbootstrap.constants import *
from ui.ttk.frames.frame_administrar_eje_tematico import FrameAdministrarEjeTematico
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class DialogoAdministrarEjeTemático(BaseDialog):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, title="Administrador de Ejes Temáticos", geometry="1000x650", minsize=(1000, 650), **kwargs)
        frame = FrameAdministrarEjeTematico(master=self)
        frame.pack(side=TOP, fill=BOTH, expand=TRUE)
