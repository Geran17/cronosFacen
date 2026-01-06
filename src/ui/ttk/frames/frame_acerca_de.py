"""
Frame Acerca De - Información sobre la aplicación CronosFacen

Este módulo contiene la interfaz para mostrar información sobre
la aplicación, incluyendo versión, autor, licencia, etc.
"""

from ttkbootstrap import Frame, Label, Button, Separator, Scrollbar, Text
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class FrameAcercaDe(Frame):
    """
    Frame de Información sobre la Aplicación.

    Muestra detalles sobre CronosFacen incluyendo:
    - Nombre y versión de la aplicación
    - Descripción y propósito
    - Autor y contacto
    - Licencia
    - Información técnica
    """

    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)
        self.config(padding=20)

        self._crear_widgets()

    def _crear_widgets(self):
        """Crea la estructura principal de widgets"""

        # Encabezado
        self._crear_encabezado()

        Separator(self, orient=HORIZONTAL).pack(fill=X, pady=15)

        # Contenido principal
        self._crear_contenido()

        Separator(self, orient=HORIZONTAL).pack(fill=X, pady=15)

        # Footer
        self._crear_footer()

    def _crear_encabezado(self):
        """Crea el encabezado con logo e información principal"""
        frame_header = Frame(self)
        frame_header.pack(fill=X, pady=10)

        # Logo/Icono
        Label(
            frame_header,
            text="🎓",
            font=("Helvetica", 48),
        ).pack(side=LEFT, padx=20)

        # Información principal
        frame_info = Frame(frame_header)
        frame_info.pack(side=LEFT, fill=BOTH, expand=True)

        Label(
            frame_info,
            text="CronosFacen",
            font=("Helvetica", 24, "bold"),
        ).pack(anchor=W)

        Label(
            frame_info,
            text="Sistema de Gestión de Cronograma Académico",
            font=("Helvetica", 12),
            foreground="gray",
        ).pack(anchor=W)

        Label(
            frame_info,
            text="Versión 1.0.0",
            font=("Helvetica", 10),
            foreground="darkblue",
        ).pack(anchor=W, pady=(5, 0))

    def _crear_contenido(self):
        """Crea el contenido principal con información de la aplicación"""
        frame_content = Frame(self)
        frame_content.pack(fill=BOTH, expand=True)

        # Descripción
        Label(
            frame_content,
            text="Descripción",
            font=("Helvetica", 12, "bold"),
        ).pack(anchor=W, pady=(10, 5))

        texto_descripcion = """CronosFacen es una aplicación de gestión académica diseñada para
facilitar la administración de cronogramas, estudiantes, asignaturas y
actividades académicas. Permite a los administradores educativos mantener
un control centralizado de las entidades académicas y los eventos del calendario."""

        Label(
            frame_content,
            text=texto_descripcion,
            font=("Helvetica", 10),
            justify=LEFT,
            wraplength=500,
        ).pack(anchor=W, pady=10, padx=20)

        # Características
        Label(
            frame_content,
            text="Características Principales",
            font=("Helvetica", 12, "bold"),
        ).pack(anchor=W, pady=(15, 5))

        caracteristicas = [
            "✓ Gestión completa de carreras académicas",
            "✓ Administración de estudiantes y asignaturas",
            "✓ Control de ejes temáticos y actividades",
            "✓ Gestión del calendario académico",
            "✓ Interfaz intuitiva y responsiva",
            "✓ Base de datos SQLite integrada",
        ]

        for caracteristica in caracteristicas:
            Label(
                frame_content,
                text=caracteristica,
                font=("Helvetica", 10),
                justify=LEFT,
            ).pack(anchor=W, padx=40, pady=2)

        # Información técnica
        Label(
            frame_content,
            text="Información Técnica",
            font=("Helvetica", 12, "bold"),
        ).pack(anchor=W, pady=(15, 5))

        info_tecnica = [
            "Framework: ttkbootstrap (Tkinter)",
            "Base de Datos: SQLite 3",
            "Lenguaje: Python 3.10+",
            "Patrón Arquitectónico: MVC (Modelo-Vista-Controlador)",
            "Logging: Sistema de logging integrado",
        ]

        for info in info_tecnica:
            Label(
                frame_content,
                text=info,
                font=("Helvetica", 10),
                justify=LEFT,
            ).pack(anchor=W, padx=40, pady=2)

        # Autor
        Label(
            frame_content,
            text="Autor",
            font=("Helvetica", 12, "bold"),
        ).pack(anchor=W, pady=(15, 5))

        Label(
            frame_content,
            text="German Cespedes",
            font=("Helvetica", 10),
            foreground="gray",
        ).pack(anchor=W, padx=40)

        Label(
            frame_content,
            text="Correo: gapurzel@gmail.com",
            font=("Helvetica", 10),
            foreground="gray",
        ).pack(anchor=W, padx=40)

        # Licencia
        Label(
            frame_content,
            text="Licencia",
            font=("Helvetica", 12, "bold"),
        ).pack(anchor=W, pady=(15, 5))

        Label(
            frame_content,
            text="Este software es proporcionado bajo licencia académica.",
            font=("Helvetica", 10),
            foreground="gray",
        ).pack(anchor=W, padx=40)

    def _crear_footer(self):
        """Crea el footer con información de copyright"""
        frame_footer = Frame(self)
        frame_footer.pack(fill=X)

        Label(
            frame_footer,
            text="© 2025-2026 CronosFacen. Todos los derechos reservados.",
            font=("Helvetica", 9),
            foreground="gray",
        ).pack(anchor=CENTER)

        Label(
            frame_footer,
            text="Gracias por usar CronosFacen",
            font=("Helvetica", 9, "italic"),
            foreground="darkgray",
        ).pack(anchor=CENTER, pady=(5, 0))
