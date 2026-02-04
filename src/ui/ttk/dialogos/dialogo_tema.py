from ttkbootstrap import Frame, Label, Combobox, Button, StringVar, Style
from ttkbootstrap.constants import *

from ui.ttk.dialogos.base_dialog import BaseDialog
from ui.ttk.styles.estilos import PADDING_SM, apply_styles
from configuracion.config_app import get_tema, set_tema
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class DialogoTema(BaseDialog):
    def __init__(self, parent=None, **kwargs):
        super().__init__(
            parent,
            title="Seleccionar tema",
            geometry="420x220",
            minsize=(420, 220),
            **kwargs,
        )
        self._style = Style()
        tema_actual = get_tema() or self._style.theme_use()
        self.var_tema = StringVar(value=tema_actual)
        self._crear_widgets()

    def _crear_widgets(self):
        frame = Frame(self, padding=PADDING_SM)
        frame.pack(side=TOP, fill=BOTH, expand=TRUE)

        Label(frame, text="Tema:", style="FormLabel.TLabel").pack(anchor=W)

        temas = sorted(self.style.theme_names())
        cbx = Combobox(frame, state=READONLY, textvariable=self.var_tema, values=temas)
        cbx.pack(fill=X, pady=(0, PADDING_SM))

        frame_botones = Frame(frame)
        frame_botones.pack(fill=X, pady=PADDING_SM)

        Button(frame_botones, text="Aplicar", bootstyle=SUCCESS, command=self._aplicar).pack(
            side=RIGHT, padx=(PADDING_SM, 0)
        )
        Button(
            frame_botones,
            text="Restablecer",
            bootstyle=WARNING,
            command=self._restablecer,
        ).pack(side=RIGHT, padx=(PADDING_SM, 0))
        Button(frame_botones, text="Cerrar", bootstyle=SECONDARY, command=self.destroy).pack(
            side=RIGHT
        )

    def _aplicar(self):
        tema = self.var_tema.get()
        try:
            if tema:
                self._style.theme_use(tema)
                apply_styles(self.winfo_toplevel())
                set_tema(tema)
                logger.info(f"Tema aplicado: {tema}")
        except Exception as e:
            logger.error(f"Error al aplicar tema: {e}", exc_info=True)

    def _restablecer(self):
        try:
            tema = "darkly"
            self.var_tema.set(tema)
            self._style.theme_use(tema)
            apply_styles(self.winfo_toplevel())
            set_tema(tema)
            logger.info("Tema restablecido a darkly")
        except Exception as e:
            logger.error(f"Error al restablecer tema: {e}", exc_info=True)
