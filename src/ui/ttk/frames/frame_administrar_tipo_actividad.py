from ttkbootstrap import (
    Frame,
    Label,
    Button,
    Separator,
    Entry,
    Labelframe,
    Notebook,
    StringVar,
    IntVar,
    Text,
    Scrollbar,
)
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.tableview import Tableview
from typing import Dict, Any
from scripts.logging_config import obtener_logger_modulo
from ui.ttk.styles.icons import ICON_TIPO_ACTIVIDAD
from controladores.controlar_administrar_tipo_actividad import ControlarAdministrarTipoActividad

logger = obtener_logger_modulo(__name__)


class FrameAdministrarTipoActividad(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        self.map_widgets: Dict[str, Any] = {}
        self.map_vars: Dict[str, Any] = {}

        # Variables
        self.var_id_tipo_actividad = IntVar(value=0)
        self.map_vars['var_id_tipo_actividad'] = self.var_id_tipo_actividad

        self.var_nombre = StringVar()
        self.map_vars['var_nombre'] = self.var_nombre

        self.var_siglas = StringVar()
        self.map_vars['var_siglas'] = self.var_siglas

        self.var_descripcion = StringVar()
        self.map_vars['var_descripcion'] = self.var_descripcion

        # creamos los widgets
        self._crear_widgets()

        # Cargamos el controlador
        ControlarAdministrarTipoActividad(
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
        frame_superior.pack(side=TOP, fill=X, padx=1, pady=1)

        frame_central = Frame(self, padding=(5, 5))
        self._frame_central(frame=frame_central)
        frame_central.pack(side=TOP, fill=BOTH, padx=1, pady=1, expand=True)

        frame_inferior = Frame(self, padding=(5, 5))
        self._frame_inferior(frame=frame_inferior)
        frame_inferior.pack(side=TOP, fill=X, padx=1, pady=1)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Superior
    # └────────────────────────────────────────────────────────────┘
    def _frame_superior(self, frame: Frame):
        label_info = Label(
            frame,
            text=f"{ICON_TIPO_ACTIVIDAD} Administrador de Tipos de Actividad",
            bootstyle="info",
            font=("Helvetica", 16, "bold"),
        )
        label_info.pack(side=TOP, fill=X, padx=1, pady=1, expand=TRUE)

        Separator(frame).pack(side=TOP, fill=X, expand=TRUE, padx=1, pady=1)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Central
    # └────────────────────────────────────────────────────────────┘
    def _frame_central(self, frame: Frame):
        # Configurar columnas: panel izquierdo (60%) y derecho (40%)
        frame.columnconfigure(0, weight=6, minsize=400)
        frame.columnconfigure(1, weight=4, minsize=300)
        frame.rowconfigure(0, weight=1)

        # Panel Izquierdo: Tabla
        frame_izquierdo = Labelframe(
            frame,
            text="📋 Lista de Tipos de Actividad",
            padding=10,
            bootstyle="primary",
        )
        frame_izquierdo.grid(row=0, column=0, sticky=NSEW, padx=(0, 5))
        self._frame_tabla(frame_izquierdo)

        # Panel Derecho: Formulario
        frame_derecho = Labelframe(
            frame,
            text="📝 Detalles del Tipo",
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
            font=("Helvetica", 9, "italic"),
        )
        lbl_info.pack(side=LEFT, padx=5)

        self.tabla_tipo_actividad = Tableview(
            frame,
            searchable=TRUE,
            paginated=TRUE,
            coldata=[
                {'text': 'Id', 'stretch': False, 'anchor': 'e'},
                {'text': 'Nombre', 'stretch': True, 'anchor': 'w'},
                {'text': 'Siglas', 'stretch': False, 'anchor': 'center'},
                {'text': 'Descripción', 'stretch': True, 'anchor': 'w'},
            ],
            bootstyle="primary",
        )
        self.tabla_tipo_actividad.pack(side=TOP, fill=BOTH, padx=1, pady=1, expand=TRUE)
        self.map_widgets['tabla_tipo_actividad'] = self.tabla_tipo_actividad

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
        lbl_id = Label(frame_campos, text="ID:", anchor=W, font=("Helvetica", 9))
        lbl_id.grid(column=0, row=0, sticky=W, padx=5, pady=(5, 2))

        self.entry_id_tipo_actividad = Entry(
            frame_campos,
            textvariable=self.var_id_tipo_actividad,
            state=READONLY,
            justify=RIGHT,
            bootstyle="secondary",
        )
        self.entry_id_tipo_actividad.grid(column=0, row=1, padx=5, pady=(0, 8), sticky=EW)
        self.map_widgets['entry_id_tipo_actividad'] = self.entry_id_tipo_actividad

        # Siglas
        lbl_siglas = Label(
            frame_campos, text="🔤 Siglas:", anchor=W, font=("Helvetica", 10, "bold")
        )
        lbl_siglas.grid(column=1, row=0, sticky=W, padx=5, pady=(5, 2))

        self.entry_siglas = Entry(
            frame_campos,
            textvariable=self.var_siglas,
            justify=CENTER,
            bootstyle="info",
        )
        self.entry_siglas.grid(column=1, row=1, padx=5, pady=(0, 8), sticky=EW)
        self.map_widgets['entry_siglas'] = self.entry_siglas

        # Nombre
        lbl_nombre = Label(
            frame_campos, text="📝 Nombre del Tipo:", anchor=W, font=("Helvetica", 10, "bold")
        )
        lbl_nombre.grid(column=0, row=2, sticky=W, padx=5, pady=(5, 2), columnspan=2)

        self.entry_nombre = Entry(
            frame_campos,
            textvariable=self.var_nombre,
            bootstyle="info",
        )
        self.entry_nombre.grid(column=0, row=3, padx=5, pady=(0, 8), sticky=EW, columnspan=2)
        self.map_widgets['entry_nombre'] = self.entry_nombre

        # Descripción
        lbl_descripcion = Label(
            frame_campos, text="📄 Descripción:", anchor=W, font=("Helvetica", 10, "bold")
        )
        lbl_descripcion.grid(column=0, row=4, padx=5, pady=(5, 2), sticky=W, columnspan=2)

        frame_descripcion = Frame(frame_campos)
        frame_descripcion.grid(column=0, row=5, padx=5, pady=(0, 8), sticky=NSEW, columnspan=2)
        frame_descripcion.columnconfigure(0, weight=1)
        frame_descripcion.rowconfigure(0, weight=1)

        self.text_descripcion = Text(
            frame_descripcion,
            height=5,
            wrap=WORD,
        )
        self.text_descripcion.grid(column=0, row=0, sticky=NSEW)
        self.map_widgets['text_descripcion'] = self.text_descripcion

        scrollbar_descripcion = Scrollbar(
            frame_descripcion,
            orient=VERTICAL,
            command=self.text_descripcion.yview,
        )
        scrollbar_descripcion.grid(column=1, row=0, sticky=NS)
        self.text_descripcion.configure(yscrollcommand=scrollbar_descripcion.set)

        # Separador
        Separator(frame_campos, bootstyle="secondary").grid(
            column=0, row=6, columnspan=2, sticky=EW, padx=5, pady=10
        )

        # Botones de acción principales
        frame_acciones = Frame(frame_campos)
        frame_acciones.grid(column=0, row=7, columnspan=2, sticky=EW, padx=5, pady=(0, 5))

        self.btn_nuevo = Button(frame_acciones, text="➕ Nuevo", bootstyle="success", width=12)
        self.btn_nuevo.pack(side=LEFT, padx=2)
        self.map_widgets['btn_nuevo'] = self.btn_nuevo

        self.btn_aplicar = Button(frame_acciones, text="💾 Guardar", bootstyle="primary", width=12)
        self.btn_aplicar.pack(side=LEFT, padx=2)
        self.map_widgets['btn_aplicar'] = self.btn_aplicar

        self.btn_eliminar = Button(frame_acciones, text="🗑️ Eliminar", bootstyle="danger", width=12)
        self.btn_eliminar.pack(side=LEFT, padx=2)
        self.map_widgets['btn_eliminar'] = self.btn_eliminar

        # Botones de navegación
        frame_navegacion = Frame(frame_campos)
        frame_navegacion.grid(column=0, row=8, columnspan=2, sticky=EW, padx=5)

        self.btn_primero = Button(frame_navegacion, text="⏮️", bootstyle="secondary", width=6)
        self.btn_primero.pack(side=LEFT, padx=1, expand=True, fill=X)
        self.map_widgets['btn_primero'] = self.btn_primero

        self.btn_anterior = Button(frame_navegacion, text="◀️", bootstyle="secondary", width=6)
        self.btn_anterior.pack(side=LEFT, padx=1, expand=True, fill=X)
        self.map_widgets['btn_anterior'] = self.btn_anterior

        self.btn_siguiente = Button(frame_navegacion, text="▶️", bootstyle="secondary", width=6)
        self.btn_siguiente.pack(side=LEFT, padx=1, expand=True, fill=X)
        self.map_widgets['btn_siguiente'] = self.btn_siguiente

        self.btn_ultimo = Button(frame_navegacion, text="⏭️", bootstyle="secondary", width=6)
        self.btn_ultimo.pack(side=LEFT, padx=1, expand=True, fill=X)
        self.map_widgets['btn_ultimo'] = self.btn_ultimo

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Inferior
    # └────────────────────────────────────────────────────────────┘
    def _frame_inferior(self, frame: Frame):
        self.lbl_estadisticas = Label(frame, text="", bootstyle="secondary", anchor=W)
        self.lbl_estadisticas.pack(side=TOP, fill=X, padx=1, pady=1)
        self.map_widgets['lbl_estadisticas'] = self.lbl_estadisticas
