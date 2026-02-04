"""
Diálogo Acerca De - Información sobre CronosFacen

Este módulo contiene la clase Dialog que integra el FrameAcercaDe
en una ventana modal independiente para mostrar información de la aplicación.
"""

from ttkbootstrap import Frame, Button, Separator
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from ui.ttk.frames.frame_acerca_de import FrameAcercaDe
from scripts.logging_config import obtener_logger_modulo
from ui.ttk.dialogos.base_dialog import BaseDialog

logger = obtener_logger_modulo(__name__)


class DialogoAcercaDe(BaseDialog):
    """
    Diálogo Modal para Información sobre la Aplicación.

    Proporciona una ventana modal que integra el FrameAcercaDe,
    permitiendo al usuario ver información sobre CronosFacen.

    Características:
    - Ventana modal (bloquea interacción con ventana padre)
    - Frame de información integrado
    - Botón de cerrar
    - Gestión de ciclo de vida de la ventana
    - Logging de eventos

    Atributos:
        parent: Ventana padre que abre el diálogo
        frame_acerca_de: Instancia del FrameAcercaDe
    """

    def __init__(self, parent=None, **kwargs):
        """
        Inicializa el diálogo de acerca de.

        Args:
            parent: Ventana padre (típicamente la ventana principal)
            **kwargs: Argumentos adicionales para Toplevel

        Ejemplo:
            dialogo = DialogoAcercaDe(parent=ventana_principal)
            dialogo.wait_window()
        """
        super().__init__(
            parent,
            title="Acerca de CronosFacen",
            geometry="800x600",
            minsize=(800, 600),
            modal=True,
            **kwargs,
        )

        self.resizable(True, True)
        self.parent = parent

        # Inicializar logging
        logger.info("Diálogo de acerca de abierto")

        # Crear estructura de widgets
        self._crear_widgets()

        # Enlazar evento de cierre (BaseDialog ya maneja cierre seguro)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _crear_widgets(self):
        """Crea la estructura principal de widgets del diálogo"""

        # Frame principal con padding
        frame_principal = Frame(self, padding=10)
        frame_principal.pack(fill=BOTH, expand=True)

        # Integrar el FrameAcercaDe
        self.frame_acerca_de = FrameAcercaDe(master=frame_principal)
        self.frame_acerca_de.pack(fill=BOTH, expand=True, pady=(0, 10))

        # Separador
        Separator(frame_principal, orient=HORIZONTAL).pack(fill=X, pady=10)

        # Frame de botones inferiores
        self._crear_botones_control(frame_principal)

    def _crear_botones_control(self, parent):
        """
        Crea los botones de control del diálogo.

        Args:
            parent: Frame padre donde colocar los botones
        """

        frame_botones = Frame(parent)
        frame_botones.pack(fill=X, pady=10)

        # Espacio flexible
        Frame(frame_botones).pack(side=LEFT, fill=X, expand=True)

        # Botón: Cerrar
        btn_cerrar = Button(
            frame_botones,
            text="✅ Cerrar",
            bootstyle="primary",
            command=self._on_closing,
        )
        btn_cerrar.pack(side=RIGHT, padx=5)

        ToolTip(btn_cerrar, "Cierra la ventana de información")

    def _on_closing(self):
        """
        Manejador del evento de cierre de la ventana.

        Realiza limpieza, logging y destruye la ventana.
        """

        try:
            logger.info("Diálogo de acerca de cerrado")

            # Realizar limpieza si es necesaria
            self._limpiar_recursos()

            # Destruir la ventana
            self.destroy()

        except Exception as e:
            logger.error(f"Error al cerrar el diálogo: {e}")
            self.destroy()

    def _limpiar_recursos(self):
        """
        Realiza limpieza de recursos utilizados por el diálogo.

        Esto incluye cerrar conexiones, cancelar timers, etc.
        """

        try:
            logger.debug("Limpieza de recursos del diálogo completada")

        except Exception as e:
            logger.warning(f"Error durante la limpieza de recursos: {e}")
