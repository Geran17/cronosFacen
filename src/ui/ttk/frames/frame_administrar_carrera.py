from ttkbootstrap import (
    Frame,
    Label,
    Button,
    Separator,
    Entry,
    Combobox,
    Labelframe,
    Notebook,
    StringVar,
    IntVar,
)
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.tableview import Tableview
from typing import Dict, Any
from scripts.logging_config import obtener_logger_modulo
from ui.ttk.styles.icons import ICON_CARRERA
from ui.ttk.utils.layout import build_header
from ui.ttk.utils.validation import bind_required
from ui.ttk.styles.estilos import PADDING_MD, PADDING_SM
from controladores.controlar_administrar_carrera import ControlarAdministrarCarrera

logger = obtener_logger_modulo(__name__)


class FrameAdministrarCarrera(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        self.map_widgets: Dict[str, Any] = {}
        self.map_vars: Dict[str, Any] = {}

        # Variables
        self.var_id = IntVar(value=0)
        self.map_vars['var_id'] = self.var_id

        self.var_codigo = StringVar()
        self.map_vars['var_codigo'] = self.var_codigo

        self.var_nombre = StringVar()
        self.map_vars['var_nombre'] = self.var_nombre

        self.var_plan = StringVar()
        self.map_vars['var_plan'] = self.var_plan

        self.var_modalidad = StringVar()
        self.map_vars['var_modalidad'] = self.var_modalidad

        self.var_credito = IntVar(value=0)
        self.map_vars['var_credito'] = self.var_credito

        # creamos los widgets
        self._crear_widgets()

        # Cargamos el controlador
        ControlarAdministrarCarrera(
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
            titulo=f"{ICON_CARRERA} Administrador de Carreras",
            subtitulo="Gestión de carreras, planes y modalidades",
        )

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Central
    # └────────────────────────────────────────────────────────────┘
    def _frame_central(self, frame: Frame):
        # Configurar columnas: panel izquierdo (60%) y derecho (40%)
        frame.columnconfigure(0, weight=6, minsize=400)
        frame.columnconfigure(1, weight=4, minsize=300)
        frame.rowconfigure(0, weight=1)

        # Panel Izquierdo: Tabla de Carreras
        frame_izquierdo = Labelframe(
            frame,
            text="📚 Lista de Carreras",
            padding=10,
            bootstyle="primary",
        )
        frame_izquierdo.grid(row=0, column=0, sticky=NSEW, padx=(0, 5))
        self._frame_tabla(frame_izquierdo)

        # Panel Derecho: Formulario
        frame_derecho = Labelframe(
            frame,
            text="📝 Detalles de Carrera",
            padding=10,
            bootstyle="info",
        )
        frame_derecho.grid(row=0, column=1, sticky=NSEW, padx=(5, 0))
        self._frame_formulario(frame_derecho)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Tabla
    # └────────────────────────────────────────────────────────────┘
    def _frame_tabla(self, frame: Frame):
        # Frame para búsqueda
        frame_busqueda = Frame(frame)
        frame_busqueda.pack(fill=X, pady=(0, 10))

        lbl_info = Label(
            frame_busqueda,
            text="💡 Haz doble clic en una fila para editar",
            bootstyle="secondary",
            style="Hint.TLabel",
        )
        lbl_info.pack(side=LEFT, padx=PADDING_SM)

        self.tabla_carrera = Tableview(
            frame,
            searchable=TRUE,
            paginated=TRUE,
            coldata=[
                {'text': 'Id', 'stretch': False, 'anchor': 'e'},
                {'text': 'Codigo', 'stretch': False, 'anchor': 'center'},
                {'text': 'Nombre', 'stretch': True, 'anchor': 'w'},
                {'text': 'Plan', 'stretch': False, 'anchor': 'center'},
                {'text': 'Modalidad', 'stretch': True, 'anchor': 'w'},
                {'text': 'Creditos', 'stretch': False, 'anchor': 'e'},
            ],
            bootstyle="primary",
        )
        self.tabla_carrera.pack(side=TOP, fill=BOTH, padx=PADDING_SM, pady=PADDING_SM, expand=TRUE)
        self.map_widgets['tabla_carrera'] = self.tabla_carrera

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Formulario
    # └────────────────────────────────────────────────────────────┘
    def _frame_formulario(self, frame: Frame):
        # Sección de campos del formulario
        frame_campos = Frame(frame)
        frame_campos.pack(fill=BOTH, expand=True, pady=(0, 10))

        # Configuraciones de las columnas
        frame_campos.columnconfigure(0, weight=1)
        frame_campos.columnconfigure(1, weight=1)

        # Id (oculto visualmente pero presente)
        lbl_id = Label(frame_campos, text="ID:", anchor=W, style="Small.TLabel")
        lbl_id.grid(column=0, row=0, sticky=W, padx=PADDING_SM, pady=(5, 2))

        self.entry_id = Entry(
            frame_campos,
            textvariable=self.var_id,
            state=READONLY,
            justify=RIGHT,
            bootstyle="secondary",
        )
        self.entry_id.grid(column=0, row=1, padx=PADDING_SM, pady=(0, 8), sticky=EW)
        self.map_widgets['entry_id'] = self.entry_id

        # Codigo
        lbl_codigo = Label(
            frame_campos, text="📋 Código:", anchor=W, style="FormLabel.TLabel"
        )
        lbl_codigo.grid(column=1, row=0, sticky=W, padx=PADDING_SM, pady=(5, 2))

        self.entry_codigo = Entry(
            frame_campos,
            textvariable=self.var_codigo,
            bootstyle="info",
        )
        self.entry_codigo.grid(column=1, row=1, padx=PADDING_SM, pady=(0, 8), sticky=EW)
        self.map_widgets['entry_codigo'] = self.entry_codigo
        bind_required(self.entry_codigo, "info")

        # Plan
        lbl_plan = Label(frame_campos, text="📅 Plan:", anchor=W, style="FormLabel.TLabel")
        lbl_plan.grid(column=0, row=2, sticky=W, padx=PADDING_SM, pady=(5, 2))

        self.entry_plan = Entry(
            frame_campos, textvariable=self.var_plan, justify=CENTER, bootstyle="info"
        )
        self.entry_plan.grid(column=0, row=3, padx=PADDING_SM, pady=(0, 8), sticky=EW)
        self.map_widgets['entry_plan'] = self.entry_plan

        # Créditos
        lbl_credito = Label(
            frame_campos, text="🎓 Créditos:", anchor=W, style="FormLabel.TLabel"
        )
        lbl_credito.grid(column=1, row=2, padx=PADDING_SM, pady=(5, 2), sticky=W)

        self.entry_credito = Entry(
            frame_campos, textvariable=self.var_credito, justify=RIGHT, bootstyle="info"
        )
        self.entry_credito.grid(column=1, row=3, sticky=EW, padx=PADDING_SM, pady=(0, 8))
        self.map_widgets['entry_credito'] = self.entry_credito

        # Nombre (ocupa todo el ancho)
        lbl_nombre = Label(
            frame_campos, text="📚 Nombre de la Carrera:", anchor=W, style="FormLabel.TLabel"
        )
        lbl_nombre.grid(column=0, row=4, sticky=W, padx=PADDING_SM, pady=(5, 2), columnspan=2)

        self.entry_nombre = Entry(
            frame_campos,
            textvariable=self.var_nombre,
            bootstyle="info",
        )
        self.entry_nombre.grid(column=0, row=5, padx=PADDING_SM, pady=(0, 8), sticky=EW, columnspan=2)
        self.map_widgets['entry_nombre'] = self.entry_nombre
        bind_required(self.entry_nombre, "info")

        # Modalidad (ocupa todo el ancho)
        lbl_modalidad = Label(
            frame_campos, text="🏫 Modalidad:", anchor=W, style="FormLabel.TLabel"
        )
        lbl_modalidad.grid(column=0, row=6, padx=PADDING_SM, pady=(5, 2), sticky=W, columnspan=2)

        self.cbx_modalidad = Combobox(
            frame_campos,
            textvariable=self.var_modalidad,
            state=READONLY,
            values=("Presencial", "Virtual", "Simi-Presencial"),
            bootstyle="info",
        )
        self.cbx_modalidad.grid(column=0, row=7, pady=(0, 10), sticky=EW, columnspan=2, padx=PADDING_SM)
        self.map_widgets['cbx_modalidad'] = self.cbx_modalidad

        # Separador
        Separator(frame_campos, bootstyle="secondary").grid(
            column=0, row=8, columnspan=2, sticky=EW, padx=PADDING_SM, pady=PADDING_MD
        )

        # Botones de acción principales
        frame_acciones = Frame(frame_campos)
        frame_acciones.grid(column=0, row=9, columnspan=2, sticky=EW, padx=PADDING_SM, pady=(0, 5))

        self.btn_nuevo = Button(
            frame_acciones,
            text="➕ Nuevo",
            bootstyle="success-outline")
        self.btn_nuevo.pack(side=LEFT, padx=2, fill=X, expand=True)
        self.map_widgets['btn_nuevo'] = self.btn_nuevo

        self.btn_aplicar = Button(
            frame_acciones,
            text="💾 Guardar",
            bootstyle="primary")
        self.btn_aplicar.pack(side=LEFT, padx=2, fill=X, expand=True)
        self.map_widgets['btn_aplicar'] = self.btn_aplicar

        self.btn_eliminar = Button(
            frame_acciones,
            text="🗑️ Eliminar",
            bootstyle="danger-outline")
        self.btn_eliminar.pack(side=LEFT, padx=2, fill=X, expand=True)
        self.map_widgets['btn_eliminar'] = self.btn_eliminar

        # Botones de navegación
        frame_navegacion = Frame(frame_campos)
        frame_navegacion.grid(column=0, row=10, columnspan=2, sticky=EW, padx=PADDING_SM, pady=(5, 0))

        Label(frame_navegacion, text="Navegación:", style="Small.TLabel").pack(
            side=LEFT, padx=PADDING_SM
        )

        self.btn_primero = Button(
            frame_navegacion, text="⏮️", bootstyle="secondary-outline")
        self.btn_primero.pack(side=LEFT, padx=PADDING_SM)
        self.map_widgets['btn_primero'] = self.btn_primero

        self.btn_anterior = Button(
            frame_navegacion, text="◀️", bootstyle="secondary-outline")
        self.btn_anterior.pack(side=LEFT, padx=PADDING_SM)
        self.map_widgets['btn_anterior'] = self.btn_anterior

        self.btn_siguiente = Button(
            frame_navegacion, text="▶️", bootstyle="secondary-outline")
        self.btn_siguiente.pack(side=LEFT, padx=PADDING_SM)
        self.map_widgets['btn_siguiente'] = self.btn_siguiente

        self.btn_ultimo = Button(frame_navegacion, text="⏭️", bootstyle="secondary-outline")
        self.btn_ultimo.pack(side=LEFT, padx=PADDING_SM)
        self.map_widgets['btn_ultimo'] = self.btn_ultimo

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Inferior
    # └────────────────────────────────────────────────────────────┘
    def _frame_inferior(self, frame: Frame):
        self.lbl_estadisticas = Label(frame, text="", bootstyle="secondary", anchor=W, style="Small.TLabel")
        self.lbl_estadisticas.pack(side=TOP, fill=X, padx=PADDING_SM, pady=PADDING_SM)
        self.map_widgets['lbl_estadisticas'] = self.lbl_estadisticas
