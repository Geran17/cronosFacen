from ttkbootstrap import Frame, Label, Button, Separator
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from ui.ttk.styles.estilos import PADDING_SM, PADDING_MD, PADDING_LG, PADDING_XL
from ui.ttk.styles.icons import (
    ICON_CARRERA,
    ICON_ESTUDIANTE,
    ICON_ASIGNATURA,
    ICON_ACTIVIDAD,
    ICON_CALENDARIO,
    ICON_ESTADISTICAS,
    ICON_ALERTA,
)
from ui.ttk.dialogos.dialogo_administrar_estudiante import DialogoAdministrarEstudiante
from ui.ttk.dialogos.dialogo_administrar_asignatura import DialogoAdministrarAsignatura
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class FrameBienvenidad(Frame):
    """
    Frame de bienvenida de la aplicación cronosFacen.
    Muestra un panel introductorio con características principales y accesos rápidos.
    """

    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        # Configurar estilo
        self.config(padding=PADDING_XL)

        # Crear widgets
        self._crear_widgets()

    def _crear_widgets(self):
        """Crea todos los widgets del frame de bienvenida"""

        # Encabezado principal
        self._crear_encabezado()

        # Separador
        Separator(self, orient=HORIZONTAL).pack(fill=X, pady=PADDING_LG)

        # Descripción
        self._crear_descripcion()

        # Separador
        Separator(self, orient=HORIZONTAL).pack(fill=X, pady=PADDING_LG)

        # Características principales
        self._crear_caracteristicas()

        # Separador
        Separator(self, orient=HORIZONTAL).pack(fill=X, pady=PADDING_LG)

        # Accesos rápidos
        self._crear_accesos_rapidos()

        # Separador
        Separator(self, orient=HORIZONTAL).pack(fill=X, pady=PADDING_LG)

        # Información de versión
        self._crear_pie_pagina()

    def _crear_encabezado(self):
        """Crea el encabezado de bienvenida"""
        frame_encabezado = Frame(self)  # bootstyle="secondary"
        frame_encabezado.pack(fill=X, pady=PADDING_MD)

        # Título principal
        label_titulo = Label(
            frame_encabezado,
            text="🎓 Bienvenido a CronosFacen",
            bootstyle="info",
            style="Title.TLabel",
        )
        label_titulo.pack(pady=PADDING_MD)

        # Subtítulo
        label_subtitulo = Label(
            frame_encabezado,
            text="Sistema de Organización Académica",
            bootstyle="info",
            style="Subtitle.TLabel",
        )
        label_subtitulo.pack(pady=PADDING_SM)

    def _crear_descripcion(self):
        """Crea la descripción de la aplicación"""
        frame_descripcion = Frame(self)
        frame_descripcion.pack(fill=X, pady=PADDING_MD)

        label_descripcion = Label(
            frame_descripcion,
            text=(
                "CronosFacen es una aplicación completa para gestionar y organizar "
                "información académica de estudiantes,\n"
                "asignaturas, actividades y eventos. Optimizada con una base de datos "
                "eficiente e índices para máximo rendimiento."
            ),
            style="Body.TLabel",
            justify=CENTER,
            wraplength=600,
        )
        label_descripcion.pack(pady=PADDING_MD)

    def _crear_caracteristicas(self):
        """Crea la sección de características principales"""
        frame_caracteristicas = Frame(self)
        frame_caracteristicas.pack(fill=BOTH, expand=TRUE, pady=PADDING_MD)

        label_caracteristicas = Label(
            frame_caracteristicas,
            text="✨ Características Principales",
            style="Section.TLabel",
        )
        label_caracteristicas.pack(anchor=W, pady=(0, PADDING_LG))

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
            label = Label(frame_col1, text=caracteristica, style="Body.TLabel", justify=LEFT)
            label.pack(anchor=W, pady=PADDING_SM)

        # Características columna 2
        caracteristicas_col2 = [
            "✓ Calendarios de Eventos",
            "✓ Dashboards Interactivos",
            "✓ Base de Datos Optimizada",
            "✓ 11 VIEWS SQL avanzadas",
        ]

        for caracteristica in caracteristicas_col2:
            label = Label(frame_col2, text=caracteristica, style="Body.TLabel", justify=LEFT)
            label.pack(anchor=W, pady=PADDING_SM)

    def _crear_accesos_rapidos(self):
        """Crea los botones de acceso rápido"""
        frame_accesos = Frame(self)
        frame_accesos.pack(fill=X, pady=PADDING_MD)

        label_accesos = Label(
            frame_accesos, text="⚡ Accesos Rápidos", style="Section.TLabel"
        )
        label_accesos.pack(anchor=W, pady=(0, PADDING_LG))

        # Frame de botones
        frame_botones = Frame(frame_accesos)
        frame_botones.pack(fill=X, pady=PADDING_MD)
        for col in range(3):
            frame_botones.columnconfigure(col, weight=1)

        # Botones de acceso rápido
        botones = [
            (f"{ICON_CARRERA} Carreras", "Gestiona las carreras académicas", self._ir_carreras),
            (f"{ICON_ESTUDIANTE} Estudiantes", "Administra los estudiantes", self._abrir_estudiantes),
            (f"{ICON_ASIGNATURA} Asignaturas", "Organiza las asignaturas", self._abrir_asignaturas),
            (f"{ICON_ACTIVIDAD} Actividades", "Crea y asigna actividades", self._ir_actividades),
            (f"{ICON_CALENDARIO} Calendario", "Visualiza el calendario académico", self._ir_calendario),
            (f"{ICON_ALERTA} Alertas", "Revisa actividades próximas a vencer", self._ir_alertas),
            (f"{ICON_ESTADISTICAS} Dashboard", "Resumen de progreso y próximos eventos", self._ir_dashboard),
        ]

        for i, (texto, tooltip, command) in enumerate(botones):
            row = i // 3
            col = i % 3
            btn = Button(frame_botones, text=texto, bootstyle="info", command=command)
            btn.grid(row=row, column=col, padx=PADDING_SM, pady=PADDING_SM, sticky=EW)
            ToolTip(btn, tooltip)

    def _get_frame_principal(self):
        root = self.winfo_toplevel()
        return getattr(root, "frame_prinicipal", None)

    def _select_tab(self, key: str):
        frame_principal = self._get_frame_principal()
        if not frame_principal:
            return
        try:
            notebook = frame_principal.map_widgets.get("notebook_central")
            target = frame_principal.map_widgets.get(key)
            if notebook and target:
                notebook.select(target)
        except Exception as e:
            logger.error(f"Error al seleccionar tab {key}: {e}")

    def _ir_carreras(self):
        self._select_tab("frame_carreras")

    def _ir_actividades(self):
        self._select_tab("frame_actividades")

    def _ir_calendario(self):
        self._select_tab("frame_calendario")

    def _ir_alertas(self):
        self._select_tab("frame_alertas")

    def _ir_dashboard(self):
        self._select_tab("frame_dashboard")

    def _abrir_estudiantes(self):
        try:
            DialogoAdministrarEstudiante(parent=self.winfo_toplevel())
        except Exception as e:
            logger.error(f"Error al abrir Estudiantes: {e}")

    def _abrir_asignaturas(self):
        try:
            DialogoAdministrarAsignatura(parent=self.winfo_toplevel())
        except Exception as e:
            logger.error(f"Error al abrir Asignaturas: {e}")

    def _crear_pie_pagina(self):
        """Crea la información de pie de página"""
        frame_pie = Frame(self)
        frame_pie.pack(fill=X, pady=PADDING_MD)

        label_version = Label(
            frame_pie,
            text="CronosFacen v1.0 • Desarrollado con Python y ttkbootstrap",
            bootstyle="secondary",
            style="Small.TLabel",
        )
        label_version.pack()

        label_info = Label(
            frame_pie,
            text="© 2025 Sistema de Organización Académica | Para más información consulta la documentación",
            bootstyle="secondary",
            style="Small.TLabel",
        )
        label_info.pack()
