from ttkbootstrap import Frame, Label, Button, Separator
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from ui.ttk.styles.icons import (
    ICON_CARRERA,
    ICON_ESTUDIANTE,
    ICON_ASIGNATURA,
    ICON_ACTIVIDAD,
    ICON_CALENDARIO,
    ICON_ESTADISTICAS,
)


class FrameBienvenidad(Frame):
    """
    Frame de bienvenida de la aplicación cronosFacen.
    Muestra un panel introductorio con características principales y accesos rápidos.
    """

    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        # Configurar estilo
        self.config(padding=20)

        # Crear widgets
        self._crear_widgets()

    def _crear_widgets(self):
        """Crea todos los widgets del frame de bienvenida"""

        # Encabezado principal
        self._crear_encabezado()

        # Separador
        Separator(self, orient=HORIZONTAL).pack(fill=X, pady=20)

        # Descripción
        self._crear_descripcion()

        # Separador
        Separator(self, orient=HORIZONTAL).pack(fill=X, pady=20)

        # Características principales
        self._crear_caracteristicas()

        # Separador
        Separator(self, orient=HORIZONTAL).pack(fill=X, pady=20)

        # Accesos rápidos
        self._crear_accesos_rapidos()

        # Separador
        Separator(self, orient=HORIZONTAL).pack(fill=X, pady=20)

        # Información de versión
        self._crear_pie_pagina()

    def _crear_encabezado(self):
        """Crea el encabezado de bienvenida"""
        frame_encabezado = Frame(self)  # bootstyle="secondary"
        frame_encabezado.pack(fill=X, pady=10)

        # Título principal
        label_titulo = Label(
            frame_encabezado,
            text="🎓 Bienvenido a CronosFacen",
            font=("Helvetica", 24, "bold"),
            bootstyle="info",
        )
        label_titulo.pack(pady=10)

        # Subtítulo
        label_subtitulo = Label(
            frame_encabezado,
            text="Sistema de Organización Académica",
            font=("Helvetica", 12),
            bootstyle="info",
        )
        label_subtitulo.pack(pady=5)

    def _crear_descripcion(self):
        """Crea la descripción de la aplicación"""
        frame_descripcion = Frame(self)
        frame_descripcion.pack(fill=X, pady=10)

        label_descripcion = Label(
            frame_descripcion,
            text=(
                "CronosFacen es una aplicación completa para gestionar y organizar "
                "información académica de estudiantes,\n"
                "asignaturas, actividades y eventos. Optimizada con una base de datos "
                "eficiente e índices para máximo rendimiento."
            ),
            font=("Helvetica", 10),
            justify=CENTER,
            wraplength=600,
        )
        label_descripcion.pack(pady=10)

    def _crear_caracteristicas(self):
        """Crea la sección de características principales"""
        frame_caracteristicas = Frame(self)
        frame_caracteristicas.pack(fill=BOTH, expand=TRUE, pady=10)

        label_caracteristicas = Label(
            frame_caracteristicas,
            text="✨ Características Principales",
            font=("Helvetica", 14, "bold"),
        )
        label_caracteristicas.pack(anchor=W, pady=(0, 15))

        # Crear dos columnas
        frame_col1 = Frame(frame_caracteristicas)
        frame_col1.pack(side=LEFT, fill=BOTH, expand=TRUE, padx=(0, 10))

        frame_col2 = Frame(frame_caracteristicas)
        frame_col2.pack(side=LEFT, fill=BOTH, expand=TRUE, padx=(10, 0))

        # Características columna 1
        caracteristicas_col1 = [
            "✓ Gestión de Carreras y Asignaturas",
            "✓ Seguimiento del Progreso Académico",
            "✓ Administración de Actividades",
            "✓ Alertas Personalizadas",
        ]

        for caracteristica in caracteristicas_col1:
            label = Label(frame_col1, text=caracteristica, font=("Helvetica", 10), justify=LEFT)
            label.pack(anchor=W, pady=5)

        # Características columna 2
        caracteristicas_col2 = [
            "✓ Calendarios de Eventos",
            "✓ Dashboards Interactivos",
            "✓ Base de Datos Optimizada",
            "✓ 11 VIEWS SQL avanzadas",
        ]

        for caracteristica in caracteristicas_col2:
            label = Label(frame_col2, text=caracteristica, font=("Helvetica", 10), justify=LEFT)
            label.pack(anchor=W, pady=5)

    def _crear_accesos_rapidos(self):
        """Crea los botones de acceso rápido"""
        frame_accesos = Frame(self)
        frame_accesos.pack(fill=X, pady=10)

        label_accesos = Label(
            frame_accesos, text="⚡ Accesos Rápidos", font=("Helvetica", 14, "bold")
        )
        label_accesos.pack(anchor=W, pady=(0, 15))

        # Frame de botones
        frame_botones = Frame(frame_accesos)
        frame_botones.pack(fill=X, pady=10)

        # Botones de acceso rápido
        botones = [
            (f"{ICON_CARRERA} Carreras", "Gestiona las carreras académicas"),
            (f"{ICON_ESTUDIANTE} Estudiantes", "Administra los estudiantes"),
            (f"{ICON_ASIGNATURA} Asignaturas", "Organiza las asignaturas"),
            (f"{ICON_ACTIVIDAD} Actividades", "Crea y asigna actividades"),
            (f"{ICON_CALENDARIO} Calendario", "Visualiza el calendario académico"),
        ]

        for i, (texto, tooltip) in enumerate(botones):
            btn = Button(frame_botones, text=texto, bootstyle="info", width=20)
            btn.pack(side=LEFT, padx=5, pady=5)
            ToolTip(btn, tooltip)

    def _crear_pie_pagina(self):
        """Crea la información de pie de página"""
        frame_pie = Frame(self)
        frame_pie.pack(fill=X, pady=10)

        label_version = Label(
            frame_pie,
            text="CronosFacen v1.0 • Desarrollado con Python y ttkbootstrap",
            font=("Helvetica", 9),
            bootstyle="secondary",
        )
        label_version.pack()

        label_info = Label(
            frame_pie,
            text="© 2025 Sistema de Organización Académica | Para más información consulta la documentación",
            font=("Helvetica", 8),
            bootstyle="secondary",
        )
        label_info.pack()
