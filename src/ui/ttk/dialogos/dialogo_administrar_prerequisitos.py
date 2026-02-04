from ui.ttk.dialogos.base_dialog import BaseDialog
from ttkbootstrap.constants import *
from ui.ttk.frames.frame_administrar_prerequisitos import FrameAdministrarPrerequisitos
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class DialogoAdministrarPrerequisitos(BaseDialog):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, title="Administrador de Prerequisitos", geometry="1100x650", minsize=(1100, 650), **kwargs)
        frame = FrameAdministrarPrerequisitos(master=self)
        frame.pack(side=TOP, fill=BOTH, expand=TRUE)
