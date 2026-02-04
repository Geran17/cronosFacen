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
from ui.ttk.styles.icons import ICON_ESTUDIANTE
from ui.ttk.utils.layout import build_header
from ui.ttk.utils.validation import bind_required
from ui.ttk.styles.estilos import PADDING_MD, PADDING_SM
from controladores.controlar_administrar_estudiante import ControlarAdministrarEstudiante

logger = obtener_logger_modulo(__name__)


class FrameAdministrarEstudiante(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        self.map_widgets: Dict[str, Any] = {}
        self.map_vars: Dict[str, Any] = {}

        # Variables
        self.var_id = IntVar(value=0)
        self.map_vars['var_id'] = self.var_id

        self.var_nombre = StringVar()
        self.map_vars['var_nombre'] = self.var_nombre

        self.var_correo = StringVar()
        self.map_vars['var_correo'] = self.var_correo

        # creamos los widgets
        self._crear_widgets()

        # Cargamos el controlador
        ControlarAdministrarEstudiante(
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
            titulo="👤 Administrador de Estudiantes",
            subtitulo="Gestión de estudiantes y datos personales",
        )

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Central
    # └────────────────────────────────────────────────────────────┘
    def _frame_central(self, frame: Frame):
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        # Crear Notebook (tabs)
        self.notebook = Notebook(frame)
        self.notebook.grid(row=0, column=0, sticky=NSEW, padx=PADDING_SM, pady=PADDING_SM)

        # Tab 1: Tabla
        frame_tabla_tab = Frame(self.notebook, padding=10)
        self.notebook.add(frame_tabla_tab, text="👥 Lista de Estudiantes")
        self._frame_tabla(frame_tabla_tab)

        # Tab 2: Formulario
        frame_formulario_tab = Frame(self.notebook, padding=10)
        self.notebook.add(frame_formulario_tab, text="📝 Detalles del Estudiante")
        self._frame_formulario(frame_formulario_tab)

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

        self.tabla_estudiante = Tableview(
            frame,
            searchable=TRUE,
            paginated=TRUE,
            coldata=[
                {'text': 'Id', 'stretch': False, 'anchor': 'e'},
                {'text': 'Nombre', 'stretch': True, 'anchor': 'w'},
                {'text': 'Correo', 'stretch': True, 'anchor': 'w'},
                {'text': 'Carreras', 'stretch': True, 'anchor': 'w'},
            ],
            bootstyle="primary",
        )
        self.tabla_estudiante.pack(side=TOP, fill=BOTH, padx=PADDING_SM, pady=PADDING_SM, expand=TRUE)
        self.map_widgets['tabla_estudiante'] = self.tabla_estudiante

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Formulario
    # └────────────────────────────────────────────────────────────┘
    def _frame_formulario(self, frame: Frame):
        # Sección de campos del formulario
        frame_campos = Frame(frame)
        frame_campos.pack(fill=BOTH, expand=True, pady=(0, 10))

        # Configuraciones de las columnas
        frame_campos.columnconfigure(0, weight=1)

        # Id
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

        # Nombre
        lbl_nombre = Label(
            frame_campos, text="👤 Nombre Completo:", anchor=W, style="FormLabel.TLabel"
        )
        lbl_nombre.grid(column=0, row=2, sticky=W, padx=PADDING_SM, pady=(5, 2))

        self.entry_nombre = Entry(
            frame_campos,
            textvariable=self.var_nombre,
            bootstyle="info",
        )
        self.entry_nombre.grid(column=0, row=3, padx=PADDING_SM, pady=(0, 8), sticky=EW)
        self.map_widgets['entry_nombre'] = self.entry_nombre
        bind_required(self.entry_nombre, "info")

        # Correo
        lbl_correo = Label(
            frame_campos, text="📧 Correo Electrónico:", anchor=W, style="FormLabel.TLabel"
        )
        lbl_correo.grid(column=0, row=4, sticky=W, padx=PADDING_SM, pady=(5, 2))

        self.entry_correo = Entry(
            frame_campos,
            textvariable=self.var_correo,
            bootstyle="info",
        )
        self.entry_correo.grid(column=0, row=5, padx=PADDING_SM, pady=(0, 8), sticky=EW)
        self.map_widgets['entry_correo'] = self.entry_correo
        bind_required(self.entry_correo, "info")

        # Sección de Carreras
        lbl_carreras = Label(
            frame_campos,
            text="🎓 Carreras del Estudiante:",
            anchor=W,
            style="FormLabel.TLabel",
        )
        lbl_carreras.grid(column=0, row=6, sticky=W, padx=PADDING_SM, pady=(5, 2))

        # Frame para mostrar carreras y botón
        frame_carreras = Frame(frame_campos)
        frame_carreras.grid(column=0, row=7, padx=PADDING_SM, pady=(0, 8), sticky=EW)
        frame_carreras.columnconfigure(0, weight=1)

        self.lbl_info_carreras = Label(
            frame_carreras,
            text="Seleccione un estudiante para ver sus carreras",
            bootstyle="secondary",
            style="Hint.TLabel",
            anchor=W,
        )
        self.lbl_info_carreras.grid(column=0, row=0, sticky=EW, pady=(0, 5))
        self.map_widgets['lbl_info_carreras'] = self.lbl_info_carreras

        self.btn_gestionar_carreras = Button(
            frame_carreras,
            text="🎓 Gestionar Carreras",
            bootstyle="info-outline",
            state=DISABLED)
        self.btn_gestionar_carreras.grid(column=0, row=1, sticky=EW)
        self.map_widgets['btn_gestionar_carreras'] = self.btn_gestionar_carreras
        ToolTip(self.btn_gestionar_carreras, text="Administrar las carreras del estudiante")

        # Separador
        Separator(frame_campos, bootstyle="secondary").grid(
            column=0, row=8, sticky=EW, padx=PADDING_SM, pady=PADDING_MD
        )

        # Botones de acción principales
        frame_acciones = Frame(frame_campos)
        frame_acciones.grid(column=0, row=9, sticky=EW, padx=PADDING_SM, pady=(0, 5))

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
        frame_navegacion.grid(column=0, row=10, sticky=EW, padx=PADDING_SM, pady=(5, 0))

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
