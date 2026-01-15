"""
Frame Principal - Contenedor principal de la aplicación CronosFacen

Este módulo contiene la estructura principal de la interfaz gráfica,
incluyendo menú superior, panel lateral con tabs y área central de contenido.
"""

from ttkbootstrap import Frame, Button, Separator, Panedwindow, Notebook, Label, Style
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from typing import Dict, Any

from ui.ttk.styles.icons import (
    ICON_MENU,
    ICON_CARRERA,
    ICON_ESTUDIANTE,
    ICON_ASIGNATURA,
    ICON_ACERCA_DE,
    ICON_CRUZ_ROJA,
    ICON_TIPO_ACTIVIDAD,
    ICON_ACTIVIDAD,
    ICON_EJE_TEMATICO,
    ICON_CALENDARIO,
    ICON_DATOS,
    ICON_ASOCIACIONES,
    ICON_PREREQUISITO,
    ICON_CONFIGURACIONES,
    ICON_TEMA,
    ICON_CASA,
    ICON_ESTADISTICAS,
)
from ui.ttk.frames.frame_bienvenidad import FrameBienvenidad
from ui.ttk.frames.frame_calendario import FrameCalendario
from ui.ttk.frames.frame_actividades import FrameActividades
from scripts.logging_config import obtener_logger_modulo
from controladores.controlar_frame_principal import ControlarFramePrincipal

logger = obtener_logger_modulo(__name__)


class FramePrincipal(Frame):
    """
    Frame principal de la aplicación.

    Estructura:
    - Frame Superior: Menú y botones de navegación rápida
    - Frame Central: Panel lateral (navegación) + Área de contenido (Notebook central)
    - Frame Inferior: Información de estado (reservado para futuros usos)
    """

    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        # Configurar estilo del notebook lateral
        style = Style()
        style.configure('custom.TNotebook', tabposition=SW)

        # Crear estructura de widgets
        self._crear_widgets()

        # Diccionario de referencia a widgets para acceso externo
        self.map_widgets: Dict[str, Any] = {
            # Botones del menú superior
            'btn_menu': self.btn_menu,
            'btn_carrera': self.btn_carrera,
            'btn_estudiante': self.btn_estudiante,
            'btn_asignatura': self.btn_asignatura,
            'btn_eje_tematico': self.btn_eje_tematico,
            'btn_tipo_actividad': self.btn_tipo_actividad,
            'btn_actividad': self.btn_actividad,
            'btn_calendario': self.btn_calendario,
            'btn_salir': self.btn_salir,
            'btn_acerca_de': self.btn_acerca_de,
            # Botones del panel lateral - Datos
            'btn_admin_carrera': self.btn_admin_carrera,
            'btn_admin_estudiante': self.btn_admin_estudiante,
            'btn_admin_asignatura': self.btn_admin_asignatura,
            'btn_admin_eje_tematico': self.btn_admin_eje_tematico,
            'btn_admin_tipo_actividad': self.btn_admin_tipo_actividad,
            'btn_admin_actividad': self.btn_admin_actividad,
            'btn_admin_calendario': self.btn_admin_calendario,
            # Botones del panel lateral - Asociaciones
            'btn_prerequisito': self.btn_prerequisito,
            'btn_estudiante_asignatura': self.btn_estudiante_asignatura,
            'btn_estudiante_actividad': self.btn_estudiante_actividad,
            'btn_estudiante_carrera': self.btn_estudiante_carrera,
            # Botones del panel lateral - Configuraciones
            'btn_tema': self.btn_tema,
            # Frames del Notebook central
            'frame_bienvenidad': self.frame_bienvenidad,
            'frame_calendario': self.frame_calendario,
        }

        # Controlador del Frame Principal
        ControlarFramePrincipal(master=self, map_widgets=self.map_widgets)

    def _crear_widgets(self):
        """Crea la estructura principal de widgets"""

        # Frame Superior - Menú y botones principales
        self.frame_superior = Frame(self, padding=(0, 0), bootstyle="primary")
        self._frame_superior(frame=self.frame_superior)
        self.frame_superior.pack(side=TOP, fill=X, padx=0, pady=0)

        # Frame Central - Contenido principal (panel lateral + notebook central)
        self.frame_central = Frame(self, padding=(0, 0))
        self._frame_central(frame=self.frame_central)
        self.frame_central.pack(side=TOP, fill=BOTH, padx=0, pady=0, expand=TRUE)

        # Frame Inferior - Barra de estado (opcional)
        self.frame_inferior = Frame(self, padding=(1, 1))
        self._frame_inferior(frame=self.frame_inferior)
        self.frame_inferior.pack(side=TOP, fill=X, padx=1, pady=1)

    def _frame_superior(self, frame: Frame):
        """Construye el menú superior con botones de navegación"""
        self._frame_menu(frame=frame)

    def _frame_central(self, frame: Frame):
        """Construye el contenido central: panel lateral + área de contenido"""

        # PanedWindow para permitir redimensionamiento entre panel lateral y central
        self.paned_window = Panedwindow(frame, orient=HORIZONTAL)
        self.paned_window.pack(side=TOP, fill=BOTH, expand=TRUE)

        # Panel Lateral - Navegación y opciones
        self.frame_lateral = Frame(self.paned_window, width=200, padding=(1, 1))
        self._frame_lateral(frame=self.frame_lateral)
        self.paned_window.add(self.frame_lateral, weight=0)

        # Área Central - Contenido principal con tabs
        self.frame_tab = Frame(self.paned_window)
        self._frame_tab(frame=self.frame_tab)
        self.paned_window.add(self.frame_tab, weight=1)

    def _frame_inferior(self, frame: Frame):
        """
        Frame inferior reservado para barra de estado.
        Actualmente vacío, disponible para expansión futura.
        """
        pass

    def _frame_menu(self, frame: Frame):
        """
        Construye el menú superior con botones principales.

        Botones (izquierda -> derecha):
        - Menú (mostrar/ocultar panel lateral)
        - Botones de acceso rápido (Carrera, Estudiante, Asignatura, etc.)
        - Botones de utilidad (Acerca de, Salir)
        """

        # Botón Menú (mostrar/ocultar panel lateral)
        self.btn_menu = Button(frame, text=ICON_MENU, bootstyle="primary")
        self.btn_menu.pack(side=LEFT, fill=X)
        ToolTip(self.btn_menu, "Muestra o oculta el panel lateral")

        Separator(frame, orient=VERTICAL).pack(side=LEFT)

        # ========== BOTONES DE NAVEGACIÓN RÁPIDA ==========

        self.btn_carrera = Button(frame, text=f"{ICON_CARRERA} Carrera", bootstyle="primary")
        self.btn_carrera.pack(side=LEFT)
        ToolTip(self.btn_carrera, "Abre el administrador de carreras")

        self.btn_estudiante = Button(
            frame, text=f"{ICON_ESTUDIANTE} Estudiante", bootstyle="primary"
        )
        self.btn_estudiante.pack(side=LEFT)
        ToolTip(self.btn_estudiante, "Abre el administrador de estudiantes")

        self.btn_asignatura = Button(
            frame, text=f"{ICON_ASIGNATURA} Asignatura", bootstyle="primary"
        )
        self.btn_asignatura.pack(side=LEFT)
        ToolTip(self.btn_asignatura, "Abre el administrador de asignaturas")

        self.btn_eje_tematico = Button(
            frame, text=f"{ICON_EJE_TEMATICO} Eje temático", bootstyle="primary"
        )
        self.btn_eje_tematico.pack(side=LEFT)
        ToolTip(self.btn_eje_tematico, "Abre el administrador de ejes temáticos o unidades")

        self.btn_tipo_actividad = Button(
            frame, text=f"{ICON_TIPO_ACTIVIDAD} Tipo actividad", bootstyle="primary"
        )
        self.btn_tipo_actividad.pack(side=LEFT)
        ToolTip(self.btn_tipo_actividad, "Abre el administrador de tipos de actividades")

        self.btn_actividad = Button(frame, text=f"{ICON_ACTIVIDAD} Actividad", bootstyle="primary")
        self.btn_actividad.pack(side=LEFT)
        ToolTip(self.btn_actividad, "Abre el administrador de actividades")

        self.btn_calendario = Button(
            frame, text=f"{ICON_CALENDARIO} Calendario", bootstyle="primary"
        )
        self.btn_calendario.pack(side=LEFT)
        ToolTip(self.btn_calendario, "Abre el administrador de eventos en el calendario")

        # ========== BOTONES DE UTILIDAD (lado derecho) ==========

        self.btn_salir = Button(frame, text=ICON_CRUZ_ROJA, bootstyle="primary")
        self.btn_salir.pack(side=RIGHT)
        ToolTip(self.btn_salir, "Cierra la aplicación")

        Separator(frame, orient=VERTICAL).pack(side=RIGHT)

        self.btn_acerca_de = Button(frame, text=f"Acerca de {ICON_ACERCA_DE}", bootstyle="primary")
        self.btn_acerca_de.pack(side=RIGHT)
        ToolTip(self.btn_acerca_de, "Muestra información sobre la aplicación")

    def _frame_lateral(self, frame: Frame):
        """
        Construye el panel lateral con dos tabs:
        1. Datos: Administración de entidades principales
        2. Configuraciones: Ajustes de la aplicación
        """

        # Notebook Lateral con tabs
        notebook_lateral = Notebook(frame, bootstyle="primary")
        notebook_lateral.pack(side=TOP, fill=BOTH, expand=TRUE, padx=1, pady=1)

        # Tab 1: Administración de Datos
        frame_datos = Frame(notebook_lateral, padding=(1, 1))
        self._frame_datos(frame=frame_datos)
        notebook_lateral.add(frame_datos, text=f"{ICON_DATOS} Datos")

        # Tab 2: Configuraciones
        frame_configuraciones = Frame(notebook_lateral, padding=(1, 1))
        self._frame_configuraciones(frame=frame_configuraciones)
        notebook_lateral.add(frame_configuraciones, text=f"{ICON_CONFIGURACIONES} Config.")

    def _frame_configuraciones(self, frame: Frame):
        """
        Tab de Configuraciones.

        Opciones:
        - Seleccionar tema de la aplicación
        """

        # Encabezado
        lbl_configuracion = Label(
            frame, text=f"{ICON_CONFIGURACIONES} Configuraciones", bootstyle="info"
        )
        lbl_configuracion.pack(side=TOP, fill=X, padx=5, pady=5)

        Separator(frame, orient=HORIZONTAL).pack(side=TOP, fill=X, padx=2, pady=2)

        # Botón Seleccionar Tema
        self.btn_tema = Button(
            frame,
            text=f"{ICON_TEMA} Seleccione el tema",
            style='primary.success-link',
        )
        self.btn_tema.pack(side=TOP, fill=X, padx=1, pady=1)
        ToolTip(self.btn_tema, "Abre el diálogo para seleccionar el tema de la aplicación")

    def _frame_datos(self, frame: Frame):
        """
        Tab de Administración de Datos.

        Secciones:
        1. Administrar Entidades (Carreras, Estudiantes, Asignaturas, etc.)
        2. Asociaciones de Datos (Prerrequisitos, Estudiante-Asignatura, etc.)
        """

        # ========== SECCIÓN 1: ADMINISTRAR DATOS ==========

        lbl_datos = Label(frame, text=f"{ICON_DATOS} Administrar Datos", bootstyle="info")
        lbl_datos.pack(side=TOP, fill=X, padx=5, pady=5)

        Separator(frame, orient=HORIZONTAL).pack(side=TOP, fill=X, padx=2, pady=2)

        # Botón Administrar Carreras
        self.btn_admin_carrera = Button(
            frame,
            text=f"{ICON_CARRERA} Administrar Carreras",
            style='primary.success-link',
        )
        self.btn_admin_carrera.pack(side=TOP, fill=X, padx=1, pady=1)
        ToolTip(self.btn_admin_carrera, "Abre el administrador de carreras")

        # Botón Administrar Estudiantes
        self.btn_admin_estudiante = Button(
            frame,
            text=f"{ICON_ESTUDIANTE} Administrar Estudiantes",
            style='primary.success-link',
        )
        self.btn_admin_estudiante.pack(side=TOP, fill=X, padx=1, pady=1)
        ToolTip(self.btn_admin_estudiante, "Abre el administrador de estudiantes")

        # Botón Administrar Asignaturas
        self.btn_admin_asignatura = Button(
            frame,
            text=f"{ICON_ASIGNATURA} Administrar Asignaturas",
            style='primary.success-link',
        )
        self.btn_admin_asignatura.pack(side=TOP, fill=X, padx=1, pady=1)
        ToolTip(self.btn_admin_asignatura, "Abre el administrador de asignaturas")

        # Botón Administrar Eje Temático
        self.btn_admin_eje_tematico = Button(
            frame,
            text=f"{ICON_EJE_TEMATICO} Administrar Eje temático",
            style='primary.success-link',
        )
        self.btn_admin_eje_tematico.pack(side=TOP, fill=X, padx=1, pady=1)
        ToolTip(self.btn_admin_eje_tematico, "Abre el administrador de ejes temáticos o unidades")

        # Botón Administrar Tipo de Actividad
        self.btn_admin_tipo_actividad = Button(
            frame,
            text=f"{ICON_TIPO_ACTIVIDAD} Administrar Tipo Actividad",
            style='primary.success-link',
        )
        self.btn_admin_tipo_actividad.pack(side=TOP, fill=X, padx=1, pady=1)
        ToolTip(self.btn_admin_tipo_actividad, "Abre el administrador de tipos de actividades")

        # Botón Administrar Actividad
        self.btn_admin_actividad = Button(
            frame,
            text=f"{ICON_ACTIVIDAD} Administrar Actividad",
            style='primary.success-link',
        )
        self.btn_admin_actividad.pack(side=TOP, fill=X, padx=1, pady=1)
        ToolTip(self.btn_admin_actividad, "Abre el administrador de actividades")

        # Botón Administrar Calendario
        self.btn_admin_calendario = Button(
            frame,
            text=f"{ICON_CALENDARIO} Administrar Calendario",
            style='primary.success-link',
        )
        self.btn_admin_calendario.pack(side=TOP, fill=X, padx=1, pady=1)
        ToolTip(self.btn_admin_calendario, "Abre el administrador de eventos")

        # ========== SECCIÓN 2: ASOCIACIONES DE DATOS ==========

        lbl_asociacion_datos = Label(
            frame, text=f"{ICON_ASOCIACIONES} Asociaciones de Datos", bootstyle="info"
        )
        lbl_asociacion_datos.pack(side=TOP, fill=X, padx=5, pady=5)

        Separator(frame, orient=HORIZONTAL).pack(side=TOP, fill=X, padx=2, pady=2)

        # Botón Asociar Prerrequisitos
        self.btn_prerequisito = Button(
            frame,
            text=f"{ICON_PREREQUISITO} Asociar Prerrequisitos",
            style='primary.success-link',
        )
        self.btn_prerequisito.pack(side=TOP, fill=X, padx=1, pady=1)
        ToolTip(self.btn_prerequisito, "Abre el administrador de asociaciones de prerrequisitos")

        # Botón Estudiante-Asignatura
        self.btn_estudiante_asignatura = Button(
            frame,
            text=f"{ICON_ESTUDIANTE} ↔ {ICON_ASIGNATURA} Estudiante-Asignatura",
            style='primary.success-link',
        )
        self.btn_estudiante_asignatura.pack(side=TOP, fill=X, padx=1, pady=1)
        ToolTip(
            self.btn_estudiante_asignatura,
            "Abre el administrador de asociaciones entre estudiantes y asignaturas",
        )

        # Botón Estudiante-Actividad
        self.btn_estudiante_actividad = Button(
            frame,
            text=f"{ICON_ESTUDIANTE} ↔ {ICON_ACTIVIDAD} Estudiante-Actividad",
            style='primary.success-link',
        )
        self.btn_estudiante_actividad.pack(side=TOP, fill=X, padx=1, pady=1)
        ToolTip(
            self.btn_estudiante_actividad,
            "Abre el administrador de asociaciones entre estudiantes y actividades",
        )

        # Botón Estudiante-Carrera
        self.btn_estudiante_carrera = Button(
            frame,
            text=f"{ICON_ESTUDIANTE} ↔ {ICON_CARRERA} Estudiante-Carrera",
            style='primary.success-link',
        )
        self.btn_estudiante_carrera.pack(side=TOP, fill=X, padx=1, pady=1)
        ToolTip(
            self.btn_estudiante_carrera,
            "Abre el administrador de inscripciones de estudiantes en carreras",
        )

    def _frame_tab(self, frame: Frame):
        """
        Construye el área central con un Notebook.

        Tabs:
        1. Bienvenida: Panel introductorio con características y accesos rápidos
        2. Dashboard: Resumen académico general y estadísticas
        3. Reportes: Generación y exportación de reportes
        4. (Adicionales según necesidad: Actividades, Progreso, etc.)
        """

        # Notebook Central para tabs de contenido
        self.notebook_central = Notebook(frame, bootstyle="primary")
        self.notebook_central.pack(side=TOP, fill=BOTH, padx=1, pady=1, expand=True)

        # Tab Bienvenida
        self.frame_bienvenidad = FrameBienvenidad(master=self.notebook_central)
        self.notebook_central.add(self.frame_bienvenidad, text=f"{ICON_CASA} Bienvenida")

        # Tab Calendario
        self.frame_calendario = FrameCalendario(master=self.notebook_central)
        self.notebook_central.add(self.frame_calendario, text=f"{ICON_CALENDARIO} Calendario")

        # Tab Actividades
        self.frame_actividades = FrameActividades(master=self.notebook_central)
        self.notebook_central.add(self.frame_actividades, text=f"{ICON_ACTIVIDAD} Actividades")
