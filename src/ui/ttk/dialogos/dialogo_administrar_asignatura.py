from ui.ttk.dialogos.base_dialog import BaseDialog
from ttkbootstrap.constants import *
from ui.ttk.frames.frame_administrar_asignatura import FrameAdministrarAsignatura
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class DialogoAdministrarAsignatura(BaseDialog):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, title="Administrador de Asignaturas", geometry="900x650", minsize=(900, 650), **kwargs)

        frame = FrameAdministrarAsignatura(master=self)
        frame.pack(side=TOP, fill=BOTH, expand=TRUE)
