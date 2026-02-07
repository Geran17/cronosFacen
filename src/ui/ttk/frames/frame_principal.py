"""
Frame Principal - Contenedor principal de la aplicación CronosFacen

Este módulo contiene la estructura principal de la interfaz gráfica,
incluyendo menú superior, panel lateral con tabs y área central de contenido.
"""

from ttkbootstrap import (
    Frame,
    Button,
    Separator,
    Panedwindow,
    Notebook,
    Label,
    Style,
    BooleanVar,
    StringVar,
    Checkbutton,
    Labelframe,
    Entry,
)
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from typing import Dict, Any

from ui.ttk.styles.estilos import PADDING_SM
from ui.ttk.styles.icons import (
    ICON_MENU,
    ICON_CARRERA,
    ICON_ESTUDIANTE,
    ICON_ASIGNATURA,
    ICON_ACERCA_DE,
    ICON_CRUZ_ROJA,
    ICON_TIPO_ACTIVIDAD,
    ICON_ETIQUETA,
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
    ICON_ALERTA,
    ICON_CUELLOS,
)
from configuracion.config_app import (
    get_tabs_visibility,
    set_tabs_visibility,
    get_pin_hash,
    get_backup_settings,
    get_notificaciones_config,
)
from ui.ttk.frames.frame_bienvenidad import FrameBienvenidad
from ui.ttk.frames.frame_calendario import FrameCalendario
from ui.ttk.frames.frame_actividades import FrameActividades
from ui.ttk.frames.frame_carreras import FrameCarreras
from ui.ttk.frames.frame_alertas import FrameAlertas
from ui.ttk.frames.frame_dashboard import FrameDashboard
from ui.ttk.frames.frame_cuellos import FrameCuellos
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

        self.auto_menu = True
        self.tab_vars = {
            "dashboard": BooleanVar(value=True),
            "bienvenida": BooleanVar(value=True),
            "calendario": BooleanVar(value=True),
            "actividades": BooleanVar(value=True),
            "alertas": BooleanVar(value=True),
            "carreras": BooleanVar(value=True),
            "cuellos": BooleanVar(value=True),
            "configuraciones": BooleanVar(value=True),
        }
        self.var_backup_dir = StringVar()
        self.var_backup_keep_days = StringVar()
        self.var_backup_keep_last = StringVar()
        self.var_notif_habilitadas = BooleanVar(value=True)
        self.var_notif_umbral = StringVar()
        self.var_notif_intervalo = StringVar()
        self.var_notif_incluir_hoy = BooleanVar(value=True)

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
            'btn_dashboard': self.btn_dashboard,
            'btn_alertas': self.btn_alertas,
            'btn_cuellos': self.btn_cuellos,
            'btn_configuraciones': self.btn_configuraciones,
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
            'btn_admin_etiqueta': self.btn_admin_etiqueta,
            # Botones del panel lateral - Asociaciones
            'btn_prerequisito': self.btn_prerequisito,
            'btn_estudiante_asignatura': self.btn_estudiante_asignatura,
            'btn_estudiante_actividad': self.btn_estudiante_actividad,
            'btn_estudiante_carrera': self.btn_estudiante_carrera,
            # Botones del panel lateral - Configuraciones
            'btn_tema': self.btn_tema,
            'btn_pin_config': self.btn_pin_config,
            'btn_pin_clear': self.btn_pin_clear,
            'btn_backup_dir': self.btn_backup_dir,
            'btn_backup_save': self.btn_backup_save,
            'btn_backup_now': self.btn_backup_now,
            'entry_backup_dir': self.entry_backup_dir,
            'entry_backup_keep_days': self.entry_backup_keep_days,
            'entry_backup_keep_last': self.entry_backup_keep_last,
            'var_backup_dir': self.var_backup_dir,
            'var_backup_keep_days': self.var_backup_keep_days,
            'var_backup_keep_last': self.var_backup_keep_last,
            'var_notif_habilitadas': self.var_notif_habilitadas,
            'var_notif_umbral': self.var_notif_umbral,
            'var_notif_intervalo': self.var_notif_intervalo,
            'var_notif_incluir_hoy': self.var_notif_incluir_hoy,
            'btn_notif_save': self.btn_notif_save,
            'btn_notif_test': self.btn_notif_test,
            # Frames del Notebook central
            'frame_bienvenidad': self.frame_bienvenidad,
            'frame_dashboard': self.frame_dashboard,
            'frame_calendario': self.frame_calendario,
            'frame_carreras': self.frame_carreras,
            'frame_alertas': self.frame_alertas,
            'frame_cuellos': self.frame_cuellos,
            'frame_configuraciones': self.frame_configuraciones,
            'notebook_central': self.notebook_central,
        }

        # Controlador del Frame Principal
        ControlarFramePrincipal(master=self, map_widgets=self.map_widgets)

        # Aplicar visibilidad de pestañas desde config
        # Ajuste automático de menú lateral según tamaño
        self.bind("<Configure>", self._auto_adjust_layout)

    def _auto_adjust_layout(self, _event=None):
        if not self.auto_menu:
            return
        try:
            width = self.winfo_width()
            # Ocultar menú en pantallas pequeñas
            if width < 1000 and str(self.frame_lateral) in self.paned_window.panes():
                self.paned_window.remove(self.frame_lateral)
            elif width >= 1100 and str(self.frame_lateral) not in self.paned_window.panes():
                self.paned_window.insert(0, self.frame_lateral, weight=0)
        except Exception:
            pass

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
        self.frame_inferior = Frame(self, padding=(PADDING_SM, PADDING_SM))
        self._frame_inferior(frame=self.frame_inferior)
        self.frame_inferior.pack(side=TOP, fill=X, padx=PADDING_SM, pady=PADDING_SM)

    def _frame_superior(self, frame: Frame):
        """Construye el menú superior con botones de navegación"""
        self._frame_menu(frame=frame)

    def _frame_central(self, frame: Frame):
        """Construye el contenido central: panel lateral + área de contenido"""

        # PanedWindow para permitir redimensionamiento entre panel lateral y central
        self.paned_window = Panedwindow(frame, orient=HORIZONTAL)
        self.paned_window.pack(side=TOP, fill=BOTH, expand=TRUE)

        # Panel Lateral - Navegación y opciones
        self.frame_lateral = Frame(self.paned_window, padding=(PADDING_SM, PADDING_SM))
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

        # Orden Académico: Dashboard → Carreras → Actividades → Calendario → Alertas
        self.btn_dashboard = Button(frame, text=ICON_ESTADISTICAS, bootstyle="primary")
        self.btn_dashboard.pack(side=LEFT)
        ToolTip(self.btn_dashboard, "Abre la vista de dashboard")

        self.btn_cuellos = Button(frame, text=ICON_CUELLOS, bootstyle="primary")
        self.btn_cuellos.pack(side=LEFT)
        ToolTip(self.btn_cuellos, "Abre la vista de cuellos de botella")

        self.btn_carrera = Button(frame, text=ICON_CARRERA, bootstyle="primary")
        self.btn_carrera.pack(side=LEFT)
        ToolTip(self.btn_carrera, "Abre la vista de carreras")

        self.btn_actividad = Button(frame, text=ICON_ACTIVIDAD, bootstyle="primary")
        self.btn_actividad.pack(side=LEFT)
        ToolTip(self.btn_actividad, "Abre la vista de actividades")

        self.btn_calendario = Button(frame, text=ICON_CALENDARIO, bootstyle="primary")
        self.btn_calendario.pack(side=LEFT)
        ToolTip(self.btn_calendario, "Abre la vista de calendario")

        self.btn_alertas = Button(frame, text=ICON_ALERTA, bootstyle="primary")
        self.btn_alertas.pack(side=LEFT)
        ToolTip(self.btn_alertas, "Abre la vista de alertas de actividades")

        self.btn_configuraciones = Button(
            frame, text=ICON_CONFIGURACIONES, bootstyle="primary"
        )
        self.btn_configuraciones.pack(side=LEFT)
        ToolTip(self.btn_configuraciones, "Abre la vista de configuraciones")

        self.sep_nav = Separator(frame, orient=VERTICAL)
        self.sep_nav.pack(side=LEFT, padx=2)

        self.btn_estudiante = Button(frame, text=ICON_ESTUDIANTE, bootstyle="primary")
        self.btn_estudiante.pack(side=LEFT)
        ToolTip(self.btn_estudiante, "Abre el administrador de estudiantes")

        self.btn_asignatura = Button(frame, text=ICON_ASIGNATURA, bootstyle="primary")
        self.btn_asignatura.pack(side=LEFT)
        ToolTip(self.btn_asignatura, "Abre el administrador de asignaturas")

        self.btn_eje_tematico = Button(
            frame, text=ICON_EJE_TEMATICO, bootstyle="primary")
        self.btn_eje_tematico.pack(side=LEFT)
        ToolTip(self.btn_eje_tematico, "Abre el administrador de ejes temáticos o unidades")

        self.btn_tipo_actividad = Button(
            frame, text=ICON_TIPO_ACTIVIDAD, bootstyle="primary")
        self.btn_tipo_actividad.pack(side=LEFT)
        ToolTip(self.btn_tipo_actividad, "Abre el administrador de tipos de actividades")

        # ========== BOTONES DE UTILIDAD (lado derecho) ==========

        self.btn_salir = Button(frame, text=ICON_CRUZ_ROJA, bootstyle="primary")
        self.btn_salir.pack(side=RIGHT)
        ToolTip(self.btn_salir, "Cierra la aplicación")

        Separator(frame, orient=VERTICAL).pack(side=RIGHT)

        self.btn_acerca_de = Button(
            frame, text=ICON_ACERCA_DE, bootstyle="primary")
        self.btn_acerca_de.pack(side=RIGHT)
        ToolTip(self.btn_acerca_de, "Muestra información sobre la aplicación")

    def _frame_lateral(self, frame: Frame):
        """
        Construye el panel lateral con menú de administración de datos.
        """
        frame_datos = Frame(frame, padding=(PADDING_SM, PADDING_SM))
        self._frame_datos(frame=frame_datos)
        frame_datos.pack(side=TOP, fill=BOTH, expand=TRUE)

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
        lbl_configuracion.pack(side=TOP, fill=X, padx=PADDING_SM, pady=PADDING_SM)

        Separator(frame, orient=HORIZONTAL).pack(side=TOP, fill=X, padx=2, pady=2)

        # Botón Seleccionar Tema
        self.btn_tema = Button(
            frame,
            text=f"{ICON_TEMA} Seleccione el tema",
            style='primary.success-link')
        self.btn_tema.pack(side=TOP, fill=X, padx=PADDING_SM, pady=PADDING_SM)
        ToolTip(self.btn_tema, "Abre el diálogo para seleccionar el tema de la aplicación")

        # Configuración de PIN
        lf_pin = Labelframe(frame, text="Seguridad", padding=(PADDING_SM, PADDING_SM))
        lf_pin.pack(side=TOP, fill=X, padx=PADDING_SM, pady=PADDING_SM)

        self.btn_pin_config = Button(
            lf_pin,
            text="Configurar PIN",
            bootstyle="secondary",
        )
        self.btn_pin_config.pack(fill=X, pady=(0, PADDING_SM))
        ToolTip(self.btn_pin_config, "Define un PIN para abrir la aplicación")

        self.btn_pin_clear = Button(
            lf_pin,
            text="Quitar PIN",
            bootstyle="warning",
        )
        self.btn_pin_clear.pack(fill=X)
        ToolTip(self.btn_pin_clear, "Elimina el PIN guardado")
        if not get_pin_hash():
            self.btn_pin_clear.config(state=DISABLED)

        self.lbl_pin_estado = Label(
            lf_pin,
            text="🔒 PIN activo" if get_pin_hash() else "🔓 PIN no configurado",
            bootstyle="secondary",
            style="Small.TLabel",
        )
        self.lbl_pin_estado.pack(anchor=W, pady=(PADDING_SM, 0))

        # Configuración de pestañas
        lf_tabs = Labelframe(frame, text="Pestañas visibles", padding=(PADDING_SM, PADDING_SM))
        lf_tabs.pack(side=TOP, fill=X, padx=PADDING_SM, pady=PADDING_SM)

        self.chk_bienvenida = Checkbutton(
            lf_tabs, text="Bienvenida", variable=self.tab_vars["bienvenida"]
        )
        self.chk_bienvenida.pack(anchor=W, pady=2)

        self.chk_dashboard = Checkbutton(
            lf_tabs, text="Dashboard", variable=self.tab_vars["dashboard"]
        )
        self.chk_dashboard.pack(anchor=W, pady=2)

        self.chk_calendario = Checkbutton(
            lf_tabs, text="Calendario", variable=self.tab_vars["calendario"]
        )
        self.chk_calendario.pack(anchor=W, pady=2)

        self.chk_actividades = Checkbutton(
            lf_tabs, text="Actividades", variable=self.tab_vars["actividades"]
        )
        self.chk_actividades.pack(anchor=W, pady=2)

        self.chk_alertas = Checkbutton(
            lf_tabs, text="Alertas", variable=self.tab_vars["alertas"]
        )
        self.chk_alertas.pack(anchor=W, pady=2)

        self.chk_carreras = Checkbutton(
            lf_tabs, text="Carreras", variable=self.tab_vars["carreras"]
        )
        self.chk_carreras.pack(anchor=W, pady=2)

        self.chk_cuellos = Checkbutton(
            lf_tabs, text="Cuellos", variable=self.tab_vars["cuellos"]
        )
        self.chk_cuellos.pack(anchor=W, pady=2)

        self.chk_configuraciones = Checkbutton(
            lf_tabs, text="Configuraciones", variable=self.tab_vars["configuraciones"]
        )
        self.chk_configuraciones.pack(anchor=W, pady=2)

        btn_guardar_tabs = Button(
            lf_tabs,
            text="Guardar pestañas",
            bootstyle="info",
            command=self._guardar_config_tabs,
        )
        btn_guardar_tabs.pack(fill=X, pady=(PADDING_SM, 0))

        # Configuración de backups
        lf_backups = Labelframe(frame, text="Backups de Base de Datos", padding=(PADDING_SM, PADDING_SM))
        lf_backups.pack(side=TOP, fill=X, padx=PADDING_SM, pady=PADDING_SM)
        lf_backups.columnconfigure(1, weight=1)
        lf_backups.columnconfigure(3, weight=1)

        lbl_backup_dir = Label(lf_backups, text="Carpeta:")
        lbl_backup_dir.grid(row=0, column=0, padx=PADDING_SM, pady=2, sticky=W)
        self.entry_backup_dir = Entry(
            lf_backups,
            textvariable=self.var_backup_dir,
            state=READONLY,
        )
        self.entry_backup_dir.grid(row=0, column=1, columnspan=2, padx=PADDING_SM, pady=2, sticky=EW)

        self.btn_backup_dir = Button(
            lf_backups,
            text="Seleccionar",
            bootstyle="secondary",
        )
        self.btn_backup_dir.grid(row=0, column=3, padx=PADDING_SM, pady=2, sticky=E)
        ToolTip(self.btn_backup_dir, "Selecciona la carpeta donde se guardarán los backups")

        lbl_keep_days = Label(lf_backups, text="Retención (días):")
        lbl_keep_days.grid(row=1, column=0, padx=PADDING_SM, pady=2, sticky=W)
        self.entry_backup_keep_days = Entry(
            lf_backups,
            textvariable=self.var_backup_keep_days,
        )
        self.entry_backup_keep_days.grid(row=1, column=1, padx=PADDING_SM, pady=2, sticky=EW)

        lbl_keep_last = Label(lf_backups, text="Mantener últimos:")
        lbl_keep_last.grid(row=1, column=2, padx=PADDING_SM, pady=2, sticky=W)
        self.entry_backup_keep_last = Entry(
            lf_backups,
            textvariable=self.var_backup_keep_last,
        )
        self.entry_backup_keep_last.grid(row=1, column=3, padx=PADDING_SM, pady=2, sticky=EW)

        self.btn_backup_save = Button(
            lf_backups,
            text="Guardar Backup",
            bootstyle="info",
        )
        self.btn_backup_save.grid(row=2, column=0, columnspan=4, padx=PADDING_SM, pady=(PADDING_SM, 0), sticky=EW)
        ToolTip(self.btn_backup_save, "Guarda la configuración de backups")

        self.btn_backup_now = Button(
            lf_backups,
            text="Crear backup ahora",
            bootstyle="success",
        )
        self.btn_backup_now.grid(row=3, column=0, columnspan=4, padx=PADDING_SM, pady=(PADDING_SM, 0), sticky=EW)
        ToolTip(self.btn_backup_now, "Crea un backup inmediato con la configuración actual")

        backup_cfg = get_backup_settings()
        self.var_backup_dir.set(backup_cfg.get("dir", ""))
        self.var_backup_keep_days.set(str(backup_cfg.get("keep_days", 30)))
        self.var_backup_keep_last.set(str(backup_cfg.get("keep_last", 5)))

        # Configuración de notificaciones
        lf_notif = Labelframe(frame, text="Notificaciones", padding=(PADDING_SM, PADDING_SM))
        lf_notif.pack(side=TOP, fill=X, padx=PADDING_SM, pady=PADDING_SM)
        lf_notif.columnconfigure(1, weight=1)
        lf_notif.columnconfigure(3, weight=1)

        chk_habilitadas = Checkbutton(
            lf_notif, text="Habilitar notificaciones", variable=self.var_notif_habilitadas
        )
        chk_habilitadas.grid(row=0, column=0, columnspan=2, sticky=W, padx=PADDING_SM, pady=2)

        chk_incluir_hoy = Checkbutton(
            lf_notif, text="Incluir actividades de hoy", variable=self.var_notif_incluir_hoy
        )
        chk_incluir_hoy.grid(row=0, column=2, columnspan=2, sticky=W, padx=PADDING_SM, pady=2)

        lbl_umbral = Label(lf_notif, text="Umbral (días):")
        lbl_umbral.grid(row=1, column=0, padx=PADDING_SM, pady=2, sticky=W)
        self.entry_notif_umbral = Entry(lf_notif, textvariable=self.var_notif_umbral)
        self.entry_notif_umbral.grid(row=1, column=1, padx=PADDING_SM, pady=2, sticky=EW)

        lbl_intervalo = Label(lf_notif, text="Intervalo (min):")
        lbl_intervalo.grid(row=1, column=2, padx=PADDING_SM, pady=2, sticky=W)
        self.entry_notif_intervalo = Entry(lf_notif, textvariable=self.var_notif_intervalo)
        self.entry_notif_intervalo.grid(row=1, column=3, padx=PADDING_SM, pady=2, sticky=EW)

        self.btn_notif_save = Button(
            lf_notif,
            text="Guardar notificaciones",
            bootstyle="info",
        )
        self.btn_notif_save.grid(
            row=2, column=0, columnspan=2, padx=PADDING_SM, pady=(PADDING_SM, 0), sticky=EW
        )

        self.btn_notif_test = Button(
            lf_notif,
            text="Probar ahora",
            bootstyle="secondary",
        )
        self.btn_notif_test.grid(
            row=2, column=2, columnspan=2, padx=PADDING_SM, pady=(PADDING_SM, 0), sticky=EW
        )

        notif_cfg = get_notificaciones_config()
        self.var_notif_habilitadas.set(bool(notif_cfg.get("habilitado", True)))
        self.var_notif_incluir_hoy.set(bool(notif_cfg.get("incluir_hoy", True)))
        self.var_notif_umbral.set(str(notif_cfg.get("umbral_dias", 1)))
        self.var_notif_intervalo.set(str(notif_cfg.get("intervalo_min", 60)))

    def _frame_datos(self, frame: Frame):
        """
        Tab de Administración de Datos.

        Secciones:
        1. Administrar Entidades (Carreras, Estudiantes, Asignaturas, etc.)
        2. Asociaciones de Datos (Prerrequisitos, Estudiante-Asignatura, etc.)
        """

        # ========== SECCIÓN 1: ADMINISTRAR DATOS ==========

        lbl_datos = Label(frame, text=f"{ICON_DATOS} Administrar Datos", bootstyle="info")
        lbl_datos.pack(side=TOP, fill=X, padx=PADDING_SM, pady=(PADDING_SM, 2))

        Separator(frame, orient=HORIZONTAL).pack(side=TOP, fill=X, padx=2, pady=2)

        grid_datos = Frame(frame, padding=(2, 2))
        grid_datos.pack(side=TOP, fill=X, padx=PADDING_SM, pady=(2, PADDING_SM))
        for col in range(2):
            grid_datos.columnconfigure(col, weight=1)

        self.btn_admin_carrera = Button(
            grid_datos,
            text=f"{ICON_CARRERA} Carreras",
            style='primary.success-link')
        self.btn_admin_carrera.grid(row=0, column=0, sticky=EW, padx=2, pady=2)
        ToolTip(self.btn_admin_carrera, "Abre el administrador de carreras")

        self.btn_admin_estudiante = Button(
            grid_datos,
            text=f"{ICON_ESTUDIANTE} Estudiantes",
            style='primary.success-link')
        self.btn_admin_estudiante.grid(row=0, column=1, sticky=EW, padx=2, pady=2)
        ToolTip(self.btn_admin_estudiante, "Abre el administrador de estudiantes")

        self.btn_admin_asignatura = Button(
            grid_datos,
            text=f"{ICON_ASIGNATURA} Asignaturas",
            style='primary.success-link')
        self.btn_admin_asignatura.grid(row=1, column=0, sticky=EW, padx=2, pady=2)
        ToolTip(self.btn_admin_asignatura, "Abre el administrador de asignaturas")

        self.btn_admin_eje_tematico = Button(
            grid_datos,
            text=f"{ICON_EJE_TEMATICO} Ejes temáticos",
            style='primary.success-link')
        self.btn_admin_eje_tematico.grid(row=1, column=1, sticky=EW, padx=2, pady=2)
        ToolTip(self.btn_admin_eje_tematico, "Abre el administrador de ejes temáticos o unidades")

        self.btn_admin_tipo_actividad = Button(
            grid_datos,
            text=f"{ICON_TIPO_ACTIVIDAD} Tipos actividad",
            style='primary.success-link')
        self.btn_admin_tipo_actividad.grid(row=2, column=0, sticky=EW, padx=2, pady=2)
        ToolTip(self.btn_admin_tipo_actividad, "Abre el administrador de tipos de actividades")

        self.btn_admin_actividad = Button(
            grid_datos,
            text=f"{ICON_ACTIVIDAD} Actividades",
            style='primary.success-link')
        self.btn_admin_actividad.grid(row=2, column=1, sticky=EW, padx=2, pady=2)
        ToolTip(self.btn_admin_actividad, "Abre el administrador de actividades")

        self.btn_admin_calendario = Button(
            grid_datos,
            text=f"{ICON_CALENDARIO} Calendario",
            style='primary.success-link')
        self.btn_admin_calendario.grid(row=3, column=0, sticky=EW, padx=2, pady=2)
        ToolTip(self.btn_admin_calendario, "Abre el administrador de eventos")

        self.btn_admin_etiqueta = Button(
            grid_datos,
            text=f"{ICON_ETIQUETA} Etiquetas",
            style='primary.success-link')
        self.btn_admin_etiqueta.grid(row=3, column=1, sticky=EW, padx=2, pady=2)
        ToolTip(self.btn_admin_etiqueta, "Abre el administrador de etiquetas")

        # ========== SECCIÓN 2: ASOCIACIONES DE DATOS ==========

        lbl_asociacion_datos = Label(
            frame, text=f"{ICON_ASOCIACIONES} Asociaciones de Datos", bootstyle="info"
        )
        lbl_asociacion_datos.pack(side=TOP, fill=X, padx=PADDING_SM, pady=(PADDING_SM, 2))

        Separator(frame, orient=HORIZONTAL).pack(side=TOP, fill=X, padx=2, pady=2)

        grid_assoc = Frame(frame, padding=(2, 2))
        grid_assoc.pack(side=TOP, fill=X, padx=PADDING_SM, pady=(2, PADDING_SM))
        for col in range(1):
            grid_assoc.columnconfigure(col, weight=1)

        self.btn_prerequisito = Button(
            grid_assoc,
            text=f"{ICON_PREREQUISITO} Prerrequisitos",
            style='primary.success-link')
        self.btn_prerequisito.grid(row=0, column=0, sticky=EW, padx=2, pady=2)
        ToolTip(self.btn_prerequisito, "Abre el administrador de asociaciones de prerrequisitos")

        self.btn_estudiante_asignatura = Button(
            grid_assoc,
            text=f"{ICON_ESTUDIANTE} ↔ {ICON_ASIGNATURA} Estudiante-Asignatura",
            style='primary.success-link')
        self.btn_estudiante_asignatura.grid(row=1, column=0, sticky=EW, padx=2, pady=2)
        ToolTip(
            self.btn_estudiante_asignatura,
            "Abre el administrador de asociaciones entre estudiantes y asignaturas",
        )

        self.btn_estudiante_actividad = Button(
            grid_assoc,
            text=f"{ICON_ESTUDIANTE} ↔ {ICON_ACTIVIDAD} Estudiante-Actividad",
            style='primary.success-link')
        self.btn_estudiante_actividad.grid(row=2, column=0, sticky=EW, padx=2, pady=2)
        ToolTip(
            self.btn_estudiante_actividad,
            "Abre el administrador de asociaciones entre estudiantes y actividades",
        )

        self.btn_estudiante_carrera = Button(
            grid_assoc,
            text=f"{ICON_ESTUDIANTE} ↔ {ICON_CARRERA} Estudiante-Carrera",
            style='primary.success-link')
        self.btn_estudiante_carrera.grid(row=3, column=0, sticky=EW, padx=2, pady=2)
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
        self.notebook_central.pack(
            side=TOP, fill=BOTH, padx=PADDING_SM, pady=PADDING_SM, expand=True
        )

        # Tab Bienvenida
        self.frame_bienvenidad = FrameBienvenidad(master=self.notebook_central)
        self.notebook_central.add(self.frame_bienvenidad, text=f"{ICON_CASA} Bienvenida")

        # Tab Dashboard
        self.frame_dashboard = FrameDashboard(master=self.notebook_central)
        self.notebook_central.add(self.frame_dashboard, text=f"{ICON_ESTADISTICAS} Dashboard")

        # Tab Calendario
        self.frame_calendario = FrameCalendario(master=self.notebook_central)
        self.notebook_central.add(self.frame_calendario, text=f"{ICON_CALENDARIO} Calendario")

        # Tab Actividades
        self.frame_actividades = FrameActividades(master=self.notebook_central)
        self.notebook_central.add(self.frame_actividades, text=f"{ICON_ACTIVIDAD} Actividades")

        # Tab Alertas
        self.frame_alertas = FrameAlertas(master=self.notebook_central)
        self.notebook_central.add(self.frame_alertas, text=f"{ICON_ALERTA} Alertas")

        # Tab Carreras
        self.frame_carreras = FrameCarreras(master=self.notebook_central)
        self.notebook_central.add(self.frame_carreras, text=f"{ICON_CARRERA} Carreras")

        # Tab Cuellos de botella
        self.frame_cuellos = FrameCuellos(master=self.notebook_central)
        self.notebook_central.add(self.frame_cuellos, text=f"{ICON_CUELLOS} Cuellos")

        # Tab Configuraciones
        self.frame_configuraciones = Frame(self.notebook_central)
        self._frame_configuraciones(frame=self.frame_configuraciones)
        self.notebook_central.add(
            self.frame_configuraciones,
            text=f"{ICON_CONFIGURACIONES} Configuraciones",
        )

        self.tab_defs = {
            "dashboard": (self.frame_dashboard, f"{ICON_ESTADISTICAS} Dashboard"),
            "bienvenida": (self.frame_bienvenidad, f"{ICON_CASA} Bienvenida"),
            "calendario": (self.frame_calendario, f"{ICON_CALENDARIO} Calendario"),
            "actividades": (self.frame_actividades, f"{ICON_ACTIVIDAD} Actividades"),
            "alertas": (self.frame_alertas, f"{ICON_ALERTA} Alertas"),
            "carreras": (self.frame_carreras, f"{ICON_CARRERA} Carreras"),
            "cuellos": (self.frame_cuellos, f"{ICON_CUELLOS} Cuellos"),
            "configuraciones": (
                self.frame_configuraciones,
                f"{ICON_CONFIGURACIONES} Configuraciones",
            ),
        }

        self._cargar_config_tabs()

    def _cargar_config_tabs(self):
        vis = get_tabs_visibility()
        for key, var in self.tab_vars.items():
            var.set(vis.get(key, True))
        self._aplicar_visibilidad_tabs()

    def _guardar_config_tabs(self):
        vis = {k: v.get() for k, v in self.tab_vars.items()}
        if not any(vis.values()):
            vis["bienvenida"] = True
            self.tab_vars["bienvenida"].set(True)
        set_tabs_visibility(vis)
        self._aplicar_visibilidad_tabs()

    def _aplicar_visibilidad_tabs(self):
        if not hasattr(self, "notebook_central"):
            return
        current = None
        try:
            current = self.notebook_central.select()
        except Exception:
            current = None
        actuales = set(self.notebook_central.tabs())
        for key, (frame, text) in getattr(self, "tab_defs", {}).items():
            visible = self.tab_vars.get(key).get()
            frame_id = str(frame)
            if visible and frame_id not in actuales:
                self.notebook_central.add(frame, text=text)
            elif not visible and frame_id in actuales:
                self.notebook_central.hide(frame)

        if current and current not in self.notebook_central.tabs():
            if self.tab_vars.get("dashboard").get():
                self.notebook_central.select(self.frame_dashboard)
            else:
                for key, (frame, _text) in getattr(self, "tab_defs", {}).items():
                    if self.tab_vars.get(key).get():
                        self.notebook_central.select(frame)
                        break

        if hasattr(self, "btn_configuraciones"):
            visible_cfg = self.tab_vars.get("configuraciones").get()
            if visible_cfg:
                if not self.btn_configuraciones.winfo_ismapped():
                    self.btn_configuraciones.pack(side=LEFT, before=self.sep_nav)
            else:
                if self.btn_configuraciones.winfo_ismapped():
                    self.btn_configuraciones.pack_forget()
