from __future__ import annotations

import hashlib
from typing import Optional

from ttkbootstrap import Frame, Label, Entry, Button, StringVar
from ttkbootstrap.constants import *

from ui.ttk.dialogos.base_dialog import BaseDialog
from ui.ttk.styles.estilos import PADDING_SM
from configuracion.config_app import get_pin_hash, set_pin_hash
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


def _hash_pin(pin: str) -> str:
    return hashlib.sha256(pin.encode("utf-8")).hexdigest()


class DialogoPin(BaseDialog):
    def __init__(self, parent=None, mode: str = "verify", **kwargs):
        self.mode = mode
        self._autenticado = False
        super().__init__(
            parent,
            title="Acceso" if mode == "verify" else "Configurar PIN",
            geometry="420x220",
            minsize=(420, 220),
            modal=True,
            **kwargs,
        )
        self.var_pin = StringVar()
        self.var_pin2 = StringVar()
        self.var_mensaje = StringVar(value="")
        self._crear_widgets()

    @property
    def autenticado(self) -> bool:
        return self._autenticado

    def _crear_widgets(self):
        frame = Frame(self, padding=PADDING_SM)
        frame.pack(side=TOP, fill=BOTH, expand=TRUE)

        if self.mode == "verify":
            Label(frame, text="Ingrese su PIN:", style="FormLabel.TLabel").pack(anchor=W)
            entry = Entry(frame, textvariable=self.var_pin, show="*")
            entry.pack(fill=X, pady=(0, PADDING_SM))
            entry.bind("<Return>", lambda _e: self._verificar())
        else:
            Label(frame, text="Nuevo PIN:", style="FormLabel.TLabel").pack(anchor=W)
            Entry(frame, textvariable=self.var_pin, show="*").pack(fill=X, pady=(0, PADDING_SM))
            Label(frame, text="Confirmar PIN:", style="FormLabel.TLabel").pack(anchor=W)
            Entry(frame, textvariable=self.var_pin2, show="*").pack(fill=X, pady=(0, PADDING_SM))

        lbl_msg = Label(frame, textvariable=self.var_mensaje, bootstyle="danger")
        lbl_msg.pack(anchor=W, pady=(0, PADDING_SM))

        frame_btn = Frame(frame)
        frame_btn.pack(fill=X)

        if self.mode == "verify":
            Button(frame_btn, text="Ingresar", bootstyle=SUCCESS, command=self._verificar).pack(
                side=RIGHT, padx=(PADDING_SM, 0)
            )
            Button(frame_btn, text="Salir", bootstyle=SECONDARY, command=self._salir).pack(
                side=RIGHT
            )
        else:
            Button(frame_btn, text="Guardar", bootstyle=SUCCESS, command=self._guardar).pack(
                side=RIGHT, padx=(PADDING_SM, 0)
            )
            Button(frame_btn, text="Cancelar", bootstyle=SECONDARY, command=self.destroy).pack(
                side=RIGHT
            )

    def _verificar(self):
        pin = self.var_pin.get().strip()
        if not pin:
            self.var_mensaje.set("Debe ingresar el PIN.")
            return
        pin_hash = get_pin_hash()
        if not pin_hash:
            self._autenticado = True
            self.destroy()
            return
        if _hash_pin(pin) == pin_hash:
            self._autenticado = True
            self.destroy()
        else:
            self.var_mensaje.set("PIN incorrecto.")

    def _guardar(self):
        pin = self.var_pin.get().strip()
        pin2 = self.var_pin2.get().strip()
        if not pin:
            self.var_mensaje.set("Ingrese un PIN.")
            return
        if pin != pin2:
            self.var_mensaje.set("El PIN no coincide.")
            return
        set_pin_hash(_hash_pin(pin))
        logger.info("PIN actualizado")
        self.destroy()

    def _salir(self):
        self._autenticado = False
        self.destroy()
