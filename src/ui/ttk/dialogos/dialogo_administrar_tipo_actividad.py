from ui.ttk.dialogos.base_dialog import BaseDialog
from ttkbootstrap.constants import *
from ui.ttk.frames.frame_administrar_tipo_actividad import FrameAdministrarTipoActividad
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class DialogoAdministrarTipoActividad(BaseDialog):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, title="Administrador de Tipos de Actividad", geometry="900x650", minsize=(900, 650), **kwargs)
        frame = FrameAdministrarTipoActividad(master=self)
        frame.pack(side=TOP, fill=BOTH, expand=TRUE)
