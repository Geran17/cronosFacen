from datetime import date
from typing import Any, Dict, Callable, Optional

from ttkbootstrap import Frame, Label, Combobox, Button, StringVar
from ttkbootstrap.constants import *

from ui.ttk.dialogos.base_dialog import BaseDialog
from ui.ttk.styles.estilos import PADDING_SM
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class DialogoEstadoActividad(BaseDialog):
    def __init__(
        self,
        parent=None,
        actividad: Optional[Dict[str, Any]] = None,
        on_save: Optional[Callable[[Dict[str, Any], str, Optional[str]], None]] = None,
        **kwargs,
    ):
        super().__init__(
            parent,
            title="Cambiar estado de actividad",
            geometry="520x260",
            minsize=(520, 260),
            **kwargs,
        )
        self.actividad = actividad or {}
        self.on_save = on_save
        self.var_estado = StringVar(value=self.actividad.get("actividad_estado", "pendiente"))

        self._crear_widgets()

    def _crear_widgets(self):
        frame = Frame(self, padding=PADDING_SM)
        frame.pack(side=TOP, fill=BOTH, expand=TRUE)

        titulo = self.actividad.get("titulo", "Sin título")
        asignatura = self.actividad.get("nombre_asignatura", "Sin asignatura")
        carrera = self.actividad.get("carrera_nombre") or self.actividad.get("nombre_carrera")
        fecha_fin = self.actividad.get("fecha_fin", "-")
        estado_actual = self.actividad.get("actividad_estado", "pendiente")

        Label(frame, text="Actividad:", style="FormLabel.TLabel").pack(anchor=W)
        Label(frame, text=titulo).pack(anchor=W, pady=(0, PADDING_SM))

        Label(frame, text="Asignatura:", style="FormLabel.TLabel").pack(anchor=W)
        Label(frame, text=asignatura).pack(anchor=W, pady=(0, PADDING_SM))

        if carrera:
            Label(frame, text="Carrera:", style="FormLabel.TLabel").pack(anchor=W)
            Label(frame, text=carrera).pack(anchor=W, pady=(0, PADDING_SM))

        Label(frame, text="Fecha fin:", style="FormLabel.TLabel").pack(anchor=W)
        Label(frame, text=fecha_fin).pack(anchor=W, pady=(0, PADDING_SM))

        Label(frame, text="Estado actual:", style="FormLabel.TLabel").pack(anchor=W)
        Label(frame, text=estado_actual).pack(anchor=W, pady=(0, PADDING_SM))

        Label(frame, text="Nuevo estado:", style="FormLabel.TLabel").pack(anchor=W)
        cbx_estado = Combobox(
            frame,
            state=READONLY,
            textvariable=self.var_estado,
            values=["pendiente", "en_progreso", "entregada", "vencida"],
        )
        cbx_estado.pack(anchor=W, fill=X, pady=(0, PADDING_SM))

        frame_botones = Frame(frame)
        frame_botones.pack(side=TOP, fill=X, pady=PADDING_SM)

        Button(frame_botones, text="Guardar", bootstyle=SUCCESS, command=self._guardar).pack(
            side=RIGHT, padx=(PADDING_SM, 0)
        )
        Button(frame_botones, text="Cancelar", bootstyle=SECONDARY, command=self.destroy).pack(
            side=RIGHT
        )

    def _guardar(self):
        try:
            nuevo_estado = self.var_estado.get().strip() or "pendiente"
            fecha_entrega = self._resolver_fecha_entrega(nuevo_estado)
            if self.on_save:
                self.on_save(self.actividad, nuevo_estado, fecha_entrega)
        except Exception as e:
            logger.error(f"Error al guardar estado de actividad: {e}", exc_info=True)
        finally:
            self.destroy()

    def _resolver_fecha_entrega(self, nuevo_estado: str) -> Optional[str]:
        fecha_actual = self.actividad.get("fecha_entrega")
        if fecha_actual in (None, "-", ""):
            fecha_actual = None

        if nuevo_estado == "entregada":
            return fecha_actual or date.today().isoformat()
        return fecha_actual
