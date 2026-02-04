from ttkbootstrap import (
    Frame,
    Label,
    Button,
    Separator,
    Entry,
    Combobox,
    Labelframe,
    Scrollbar,
    StringVar,
    IntVar,
)
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.tableview import Tableview
from tkinter import Listbox
from typing import Dict, Any
from scripts.logging_config import obtener_logger_modulo
from ui.ttk.styles.icons import ICON_PREREQUISITO
from ui.ttk.utils.layout import build_header
from ui.ttk.styles.estilos import PADDING_MD, PADDING_SM
from controladores.controlar_administrar_prerequisitos import ControlarAdministrarPrerequisitos

logger = obtener_logger_modulo(__name__)


class FrameAdministrarPrerequisitos(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        self.map_widgets: Dict[str, Any] = {}
        self.map_vars: Dict[str, Any] = {}

        # Variables
        self.var_id_asignatura_seleccionada = IntVar(value=0)
        self.map_vars['var_id_asignatura_seleccionada'] = self.var_id_asignatura_seleccionada

        self.var_nombre_asignatura_seleccionada = StringVar()
        self.map_vars['var_nombre_asignatura_seleccionada'] = (
            self.var_nombre_asignatura_seleccionada
        )

        self.var_id_carrera_filtro = IntVar(value=0)
        self.map_vars['var_id_carrera_filtro'] = self.var_id_carrera_filtro

        self.var_nombre_carrera_filtro = StringVar()
        self.map_vars['var_nombre_carrera_filtro'] = self.var_nombre_carrera_filtro

        self.var_prerequisito_seleccionado = StringVar()
        self.map_vars['var_prerequisito_seleccionado'] = self.var_prerequisito_seleccionado

        # creamos los widgets
        self._crear_widgets()

        # Cargamos el controlador
        ControlarAdministrarPrerequisitos(
            master=self,
            map_vars=self.map_vars,
            map_widgets=self.map_widgets,
        )

    # ┌────────────────────────────────────────────────────────────┐
    # │ Creamos los widgets
    # └────────────────────────────────────────────────────────────┘
    def _crear_widgets(self):
        frame_superior = Frame(self, padding=(5, 5))
        self._frame_superior(frame=frame_superior)
        frame_superior.pack(side=TOP, fill=X, padx=PADDING_SM, pady=PADDING_SM)

        frame_filtro = Frame(self, padding=(5, 5))
        self._frame_filtro(frame=frame_filtro)
        frame_filtro.pack(side=TOP, fill=X, padx=PADDING_SM, pady=PADDING_SM)

        frame_central = Frame(self, padding=(5, 5))
        self._frame_central(frame=frame_central)
        frame_central.pack(side=TOP, fill=BOTH, padx=PADDING_SM, pady=PADDING_SM, expand=True)

        frame_inferior = Frame(self, padding=(5, 5))
        self._frame_inferior(frame=frame_inferior)
        frame_inferior.pack(side=TOP, fill=X, padx=PADDING_SM, pady=PADDING_SM)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Superior
    # └────────────────────────────────────────────────────────────┘
    def _frame_superior(self, frame: Frame):
        build_header(
            frame,
            titulo=f"{ICON_PREREQUISITO} Administrador de Prerequisitos",
            subtitulo="Gestión de asociaciones y requisitos previos",
        )

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Filtro
    # └────────────────────────────────────────────────────────────┘
    def _frame_filtro(self, frame: Frame):
        frame.columnconfigure(1, weight=1)

        lbl_filtro = Label(frame, text="Filtrar por Carrera:", anchor=W)
        lbl_filtro.grid(row=0, column=0, sticky=W, padx=PADDING_SM, pady=PADDING_SM)

        self.cbx_carrera_filtro = Combobox(
            frame,
            textvariable=self.var_nombre_carrera_filtro,
            state=READONLY,
        )
        self.cbx_carrera_filtro.grid(
            row=0, column=1, sticky=EW, padx=PADDING_SM, pady=PADDING_SM
        )
        self.map_widgets['cbx_carrera_filtro'] = self.cbx_carrera_filtro
        ToolTip(
            self.cbx_carrera_filtro,
            "Selecciona una carrera para filtrar las asignaturas",
        )

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Central - Panel Dividido
    # └────────────────────────────────────────────────────────────┘
    def _frame_central(self, frame: Frame):
        # Configurar columnas: panel izquierdo (30%) y derecho (70%)
        frame.columnconfigure(0, weight=3, minsize=250)
        frame.columnconfigure(1, weight=7, minsize=500)
        frame.rowconfigure(0, weight=1)

        # Panel Izquierdo: Lista de Asignaturas
        frame_izquierdo = Labelframe(
            frame,
            text="📚 Asignaturas",
            padding=10,
            bootstyle="primary",
        )
        frame_izquierdo.grid(row=0, column=0, sticky=NSEW, padx=(0, 5))
        self._panel_asignaturas(frame_izquierdo)

        # Panel Derecho: Prerequisitos
        frame_derecho = Labelframe(
            frame,
            text="📋 Gestión de Prerequisitos",
            padding=10,
            bootstyle="info",
        )
        frame_derecho.grid(row=0, column=1, sticky=NSEW, padx=(5, 0))
        self._panel_prerequisitos(frame_derecho)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Izquierdo - Lista de Asignaturas
    # └────────────────────────────────────────────────────────────┘
    def _panel_asignaturas(self, frame: Frame):
        # Frame para búsqueda rápida
        frame_busqueda = Frame(frame)
        frame_busqueda.pack(fill=X, pady=(0, 5))

        lbl_buscar = Label(frame_busqueda, text="🔎 Buscar:", anchor=W)
        lbl_buscar.pack(side=LEFT, padx=(0, 5))

        self.entry_buscar_asignatura = Entry(frame_busqueda)
        self.entry_buscar_asignatura.pack(side=LEFT, fill=X, expand=True)
        self.map_widgets['entry_buscar_asignatura'] = self.entry_buscar_asignatura
        ToolTip(
            self.entry_buscar_asignatura,
            "Buscar asignatura por código o nombre",
        )

        # Frame para Listbox con scrollbar
        frame_lista = Frame(frame)
        frame_lista.pack(fill=BOTH, expand=True)

        scrollbar = Scrollbar(frame_lista, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox_asignaturas = Listbox(
            frame_lista,
            yscrollcommand=scrollbar.set,
            selectmode=SINGLE,
        )
        self.listbox_asignaturas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.listbox_asignaturas.yview)
        self.map_widgets['listbox_asignaturas'] = self.listbox_asignaturas
        ToolTip(
            self.listbox_asignaturas,
            "Click en una asignatura para ver/gestionar sus prerequisitos",
        )

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Derecho - Gestión de Prerequisitos
    # └────────────────────────────────────────────────────────────┘
    def _panel_prerequisitos(self, frame: Frame):
        # Asignatura seleccionada
        frame_seleccionada = Frame(frame)
        frame_seleccionada.pack(fill=X, pady=(0, 10))

        lbl_titulo = Label(
            frame_seleccionada,
            text="Asignatura Seleccionada:",
            style="FormLabel.TLabel",
            anchor=W,
        )
        lbl_titulo.pack(side=TOP, fill=X)

        self.lbl_asignatura_seleccionada = Label(
            frame_seleccionada,
            textvariable=self.var_nombre_asignatura_seleccionada,
            style="Body.TLabel",
            foreground="blue",
            anchor=W,
        )
        self.lbl_asignatura_seleccionada.pack(side=TOP, fill=X, pady=(2, 0))
        self.map_widgets['lbl_asignatura_seleccionada'] = self.lbl_asignatura_seleccionada

        Separator(frame, orient=HORIZONTAL).pack(fill=X, pady=PADDING_MD)

        # Sección: Prerequisitos Actuales
        frame_actuales = Labelframe(
            frame,
            text="✓ Prerequisitos Actuales (Requiere estas asignaturas)",
            padding=10,
            bootstyle="success",
        )
        frame_actuales.pack(fill=BOTH, expand=True, pady=(0, 10))

        self.tabla_prerequisitos_actuales = Tableview(
            frame_actuales,
            searchable=False,
            paginated=False,
            coldata=[
                {'text': 'Código', 'stretch': False, 'anchor': 'w'},
                {'text': 'Asignatura Prerequisito', 'stretch': True, 'anchor': 'w'},
                {'text': '', 'stretch': False, 'anchor': 'center'},
            ],
            bootstyle="success",
            height=8,
        )
        self.tabla_prerequisitos_actuales.pack(fill=BOTH, expand=True)
        self.map_widgets['tabla_prerequisitos_actuales'] = self.tabla_prerequisitos_actuales
        ToolTip(
            self.tabla_prerequisitos_actuales,
            "Lista de asignaturas que se deben aprobar antes de cursar esta",
        )

        # Sección: Agregar Prerequisito
        frame_agregar = Labelframe(
            frame,
            text="➕ Agregar Nuevo Prerequisito",
            padding=10,
            bootstyle="warning",
        )
        frame_agregar.pack(fill=X, pady=(0, 10))

        lbl_instruccion = Label(
            frame_agregar,
            text="Selecciona una asignatura para agregarla como prerequisito:",
            anchor=W,
        )
        lbl_instruccion.pack(fill=X, pady=(0, 5))

        frame_combo = Frame(frame_agregar)
        frame_combo.pack(fill=X, pady=(0, 5))

        self.cbx_prerequisito_agregar = Combobox(
            frame_combo,
            textvariable=self.var_prerequisito_seleccionado,
            state=READONLY,
        )
        self.cbx_prerequisito_agregar.pack(side=LEFT, fill=X, expand=True, padx=(0, 5))
        self.map_widgets['cbx_prerequisito_agregar'] = self.cbx_prerequisito_agregar
        ToolTip(
            self.cbx_prerequisito_agregar,
            "Selecciona la asignatura que será prerequisito",
        )

        self.btn_agregar_prerequisito = Button(
            frame_combo,
            text="✅ Agregar",
            bootstyle="success")
        self.btn_agregar_prerequisito.pack(side=LEFT)
        self.map_widgets['btn_agregar_prerequisito'] = self.btn_agregar_prerequisito

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Inferior - Estadísticas
    # └────────────────────────────────────────────────────────────┘
    def _frame_inferior(self, frame: Frame):
        self.lbl_estadisticas = Label(frame, text="", bootstyle="secondary", anchor=W, style="Small.TLabel")
        self.lbl_estadisticas.pack(side=TOP, fill=X, padx=PADDING_SM, pady=PADDING_SM)
        self.map_widgets['lbl_estadisticas'] = self.lbl_estadisticas
