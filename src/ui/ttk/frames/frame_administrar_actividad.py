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
    Text,
    Scrollbar,
)
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.tableview import Tableview
from typing import Dict, Any
from scripts.logging_config import obtener_logger_modulo
from ui.ttk.styles.icons import ICON_ACTIVIDAD
from ui.ttk.utils.layout import build_header
from ui.ttk.utils.validation import bind_required
from ui.ttk.styles.estilos import PADDING_MD, PADDING_SM
from controladores.controlar_administrar_actividad import ControlarAdministrarActividad

logger = obtener_logger_modulo(__name__)


class FrameAdministrarActividad(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        self.map_widgets: Dict[str, Any] = {}
        self.map_vars: Dict[str, Any] = {}

        # Variables
        self.var_id_actividad = IntVar(value=0)
        self.map_vars['var_id_actividad'] = self.var_id_actividad

        self.var_titulo = StringVar()
        self.map_vars['var_titulo'] = self.var_titulo

        self.var_descripcion = StringVar()
        self.map_vars['var_descripcion'] = self.var_descripcion

        self.var_fecha_inicio = StringVar()
        self.map_vars['var_fecha_inicio'] = self.var_fecha_inicio

        self.var_fecha_fin = StringVar()
        self.map_vars['var_fecha_fin'] = self.var_fecha_fin

        self.var_id_eje = IntVar(value=0)
        self.map_vars['var_id_eje'] = self.var_id_eje

        self.var_nombre_eje = StringVar()
        self.map_vars['var_nombre_eje'] = self.var_nombre_eje

        self.var_id_tipo_actividad = IntVar(value=0)
        self.map_vars['var_id_tipo_actividad'] = self.var_id_tipo_actividad

        self.var_nombre_tipo_actividad = StringVar()
        self.map_vars['var_nombre_tipo_actividad'] = self.var_nombre_tipo_actividad

        self.var_nota = IntVar(value=0)
        self.map_vars['var_nota'] = self.var_nota

        self.var_id_carrera_filtro = IntVar(value=0)
        self.map_vars['var_id_carrera_filtro'] = self.var_id_carrera_filtro

        self.var_nombre_carrera_filtro = StringVar()
        self.map_vars['var_nombre_carrera_filtro'] = self.var_nombre_carrera_filtro

        self.var_id_asignatura_filtro = IntVar(value=0)
        self.map_vars['var_id_asignatura_filtro'] = self.var_id_asignatura_filtro

        self.var_nombre_asignatura_filtro = StringVar()
        self.map_vars['var_nombre_asignatura_filtro'] = self.var_nombre_asignatura_filtro

        # creamos los widgets
        self._crear_widgets()

        # Cargamos el controlador
        ControlarAdministrarActividad(
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
            titulo=f"{ICON_ACTIVIDAD} Administrador de Actividades",
            subtitulo="Gestión de actividades académicas",
        )

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Central
    # └────────────────────────────────────────────────────────────┘
    def _frame_central(self, frame: Frame):
        # Configurar el notebook (tabs)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        notebook = Notebook(frame, bootstyle="primary")
        notebook.grid(row=0, column=0, sticky=NSEW, padx=PADDING_SM, pady=PADDING_SM)
        self.map_widgets['notebook'] = notebook

        # Tab 1: Tabla
        tab_tabla = Frame(notebook, padding=10)
        notebook.add(tab_tabla, text="📋 Lista de Actividades")
        self._frame_tabla(tab_tabla)

        # Tab 2: Formulario
        tab_formulario = Frame(notebook, padding=10)
        notebook.add(tab_formulario, text="📝 Detalles de la Actividad")
        self._frame_formulario(tab_formulario)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Tabla
    # └────────────────────────────────────────────────────────────┘
    def _frame_tabla(self, frame: Frame):
        # Frame para filtros
        frame_filtros = Frame(frame)
        frame_filtros.pack(fill=X, pady=(0, PADDING_MD))
        frame_filtros.columnconfigure(1, weight=1)
        frame_filtros.columnconfigure(3, weight=1)

        # Filtro por carrera
        lbl_carrera = Label(
            frame_filtros,
            text="🎓 Filtrar por Carrera:",
            style="FormLabel.TLabel",
        )
        lbl_carrera.grid(row=0, column=0, sticky=W, padx=PADDING_SM, pady=PADDING_SM)

        self.cbx_carrera_filtro = Combobox(
            frame_filtros,
            textvariable=self.var_nombre_carrera_filtro,
            state=READONLY,
            bootstyle="primary",
        )
        self.cbx_carrera_filtro.grid(
            row=0, column=1, sticky=EW, padx=PADDING_SM, pady=PADDING_SM
        )
        self.map_widgets['cbx_carrera_filtro'] = self.cbx_carrera_filtro
        ToolTip(self.cbx_carrera_filtro, text="Filtra las actividades por carrera")

        # Filtro por asignatura
        lbl_asignatura = Label(
            frame_filtros,
            text="📚 Filtrar por Asignatura:",
            style="FormLabel.TLabel",
        )
        lbl_asignatura.grid(row=0, column=2, sticky=W, padx=PADDING_SM, pady=PADDING_SM)

        self.cbx_asignatura_filtro = Combobox(
            frame_filtros,
            textvariable=self.var_nombre_asignatura_filtro,
            state=READONLY,
            bootstyle="info",
        )
        self.cbx_asignatura_filtro.grid(
            row=0, column=3, sticky=EW, padx=PADDING_SM, pady=PADDING_SM
        )
        self.map_widgets['cbx_asignatura_filtro'] = self.cbx_asignatura_filtro
        ToolTip(self.cbx_asignatura_filtro, text="Filtra las actividades por asignatura")

        lbl_info = Label(
            frame_filtros,
            text="💡 Haz doble clic en una fila para editar",
            bootstyle="secondary",
            style="Hint.TLabel",
        )
        lbl_info.grid(row=1, column=0, columnspan=4, sticky=E, padx=PADDING_SM)

        self.tabla_actividad = Tableview(
            frame,
            searchable=TRUE,
            paginated=TRUE,
            coldata=[
                {'text': 'Id', 'stretch': False, 'anchor': 'e'},
                {'text': 'Título', 'stretch': True, 'anchor': 'w'},
                {'text': 'Carrera', 'stretch': True, 'anchor': 'w'},
                {'text': 'Fecha Inicio', 'stretch': False, 'anchor': 'center'},
                {'text': 'Fecha Fin', 'stretch': False, 'anchor': 'center'},
                {'text': 'Eje Temático', 'stretch': True, 'anchor': 'w'},
                {'text': 'Tipo', 'stretch': False, 'anchor': 'center'},
            ],
            bootstyle="primary",
        )
        self.tabla_actividad.pack(side=TOP, fill=BOTH, padx=PADDING_SM, pady=PADDING_SM, expand=TRUE)
        self.map_widgets['tabla_actividad'] = self.tabla_actividad

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
        frame_campos.columnconfigure(2, weight=1)

        # Fila 0: IDs
        lbl_id = Label(frame_campos, text="ID:", anchor=W, style="Small.TLabel")
        lbl_id.grid(column=0, row=0, sticky=W, padx=PADDING_SM, pady=(5, 2))

        self.entry_id_actividad = Entry(
            frame_campos,
            textvariable=self.var_id_actividad,
            state=READONLY,
            justify=RIGHT,
            bootstyle="secondary",
        )
        self.entry_id_actividad.grid(column=0, row=1, padx=PADDING_SM, pady=(0, 8), sticky=EW)
        self.map_widgets['entry_id_actividad'] = self.entry_id_actividad

        lbl_id_eje = Label(frame_campos, text="ID Eje:", anchor=W, style="Small.TLabel")
        lbl_id_eje.grid(column=1, row=0, sticky=W, padx=PADDING_SM, pady=(5, 2))

        self.entry_id_eje = Entry(
            frame_campos,
            textvariable=self.var_id_eje,
            state=READONLY,
            justify=RIGHT,
            bootstyle="secondary",
        )
        self.entry_id_eje.grid(column=1, row=1, padx=PADDING_SM, pady=(0, 8), sticky=EW)
        self.map_widgets['entry_id_eje'] = self.entry_id_eje

        lbl_id_tipo = Label(frame_campos, text="ID Tipo:", anchor=W, style="Small.TLabel")
        lbl_id_tipo.grid(column=2, row=0, sticky=W, padx=PADDING_SM, pady=(5, 2))

        self.entry_id_tipo_actividad = Entry(
            frame_campos,
            textvariable=self.var_id_tipo_actividad,
            state=READONLY,
            justify=RIGHT,
            bootstyle="secondary",
        )
        self.entry_id_tipo_actividad.grid(column=2, row=1, padx=PADDING_SM, pady=(0, 8), sticky=EW)
        self.map_widgets['entry_id_tipo_actividad'] = self.entry_id_tipo_actividad

        # Título
        lbl_titulo = Label(
            frame_campos,
            text="📝 Título de la Actividad:",
            anchor=W,
            style="FormLabel.TLabel",
        )
        lbl_titulo.grid(column=0, row=2, sticky=W, padx=PADDING_SM, pady=(5, 2), columnspan=3)

        self.entry_titulo = Entry(
            frame_campos,
            textvariable=self.var_titulo,
            bootstyle="info",
        )
        self.entry_titulo.grid(column=0, row=3, padx=PADDING_SM, pady=(0, 8), sticky=EW, columnspan=3)
        self.map_widgets['entry_titulo'] = self.entry_titulo
        bind_required(self.entry_titulo, "info")

        # Fechas
        lbl_fecha_inicio = Label(
            frame_campos, text="📅 Fecha Inicio:", anchor=W, style="FormLabel.TLabel"
        )
        lbl_fecha_inicio.grid(column=0, row=4, sticky=W, padx=PADDING_SM, pady=(5, 2))

        self.entry_fecha_inicio = Entry(
            frame_campos,
            textvariable=self.var_fecha_inicio,
            justify=CENTER,
            bootstyle="info",
        )
        self.entry_fecha_inicio.grid(column=0, row=5, padx=PADDING_SM, pady=(0, 8), sticky=EW)
        self.map_widgets['entry_fecha_inicio'] = self.entry_fecha_inicio

        lbl_fecha_fin = Label(
            frame_campos, text="📅 Fecha Fin:", anchor=W, style="FormLabel.TLabel"
        )
        lbl_fecha_fin.grid(column=1, row=4, sticky=W, padx=PADDING_SM, pady=(5, 2), columnspan=2)

        self.entry_fecha_fin = Entry(
            frame_campos,
            textvariable=self.var_fecha_fin,
            justify=CENTER,
            bootstyle="info",
        )
        self.entry_fecha_fin.grid(column=1, row=5, padx=PADDING_SM, pady=(0, 8), sticky=EW, columnspan=2)
        self.map_widgets['entry_fecha_fin'] = self.entry_fecha_fin

        # Eje Temático
        lbl_eje = Label(
            frame_campos, text="📚 Eje Temático:", anchor=W, style="FormLabel.TLabel"
        )
        lbl_eje.grid(column=0, row=6, padx=PADDING_SM, pady=(5, 2), sticky=W, columnspan=3)

        self.cbx_eje = Combobox(
            frame_campos,
            textvariable=self.var_nombre_eje,
            state=READONLY,
            bootstyle="info",
        )
        self.cbx_eje.grid(column=0, row=7, pady=(0, 8), padx=PADDING_SM, sticky=EW, columnspan=3)
        self.map_widgets['cbx_eje'] = self.cbx_eje

        # Tipo Actividad
        lbl_tipo = Label(
            frame_campos, text="🏷️ Tipo de Actividad:", anchor=W, style="FormLabel.TLabel"
        )
        lbl_tipo.grid(column=0, row=8, padx=PADDING_SM, pady=(5, 2), sticky=W, columnspan=3)

        self.cbx_tipo_actividad = Combobox(
            frame_campos,
            textvariable=self.var_nombre_tipo_actividad,
            state=READONLY,
            bootstyle="info",
        )
        self.cbx_tipo_actividad.grid(column=0, row=9, pady=(0, 8), padx=PADDING_SM, sticky=EW, columnspan=3)
        self.map_widgets['cbx_tipo_actividad'] = self.cbx_tipo_actividad

        # Nota
        lbl_nota = Label(frame_campos, text="⭐ Nota:", anchor=W, style="FormLabel.TLabel")
        lbl_nota.grid(column=0, row=10, padx=PADDING_SM, pady=(5, 2), sticky=W)

        self.entry_nota = Entry(
            frame_campos,
            textvariable=self.var_nota,
            justify=CENTER,
            bootstyle="info",
        )
        self.entry_nota.grid(column=0, row=11, padx=PADDING_SM, pady=(0, 8), sticky=EW)
        self.map_widgets['entry_nota'] = self.entry_nota

        # Descripción
        lbl_descripcion = Label(
            frame_campos, text="📄 Descripción:", anchor=W, style="FormLabel.TLabel"
        )
        lbl_descripcion.grid(column=0, row=12, padx=PADDING_SM, pady=(5, 2), sticky=W, columnspan=3)

        frame_descripcion = Frame(frame_campos)
        frame_descripcion.grid(column=0, row=13, padx=PADDING_SM, pady=(0, 8), sticky=NSEW, columnspan=3)
        frame_descripcion.columnconfigure(0, weight=1)
        frame_descripcion.rowconfigure(0, weight=1)

        self.text_descripcion = Text(
            frame_descripcion,
            height=4,
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
            column=0, row=14, columnspan=3, sticky=EW, padx=PADDING_SM, pady=PADDING_MD
        )

        # Botones de acción principales
        frame_acciones = Frame(frame_campos)
        frame_acciones.grid(column=0, row=15, columnspan=3, sticky=EW, padx=PADDING_SM, pady=(0, 5))

        self.btn_nuevo = Button(frame_acciones, text="➕ Nuevo", bootstyle="success")
        self.btn_nuevo.pack(side=LEFT, padx=2)
        self.map_widgets['btn_nuevo'] = self.btn_nuevo

        self.btn_aplicar = Button(frame_acciones, text="💾 Guardar", bootstyle="primary")
        self.btn_aplicar.pack(side=LEFT, padx=2)
        self.map_widgets['btn_aplicar'] = self.btn_aplicar

        self.btn_eliminar = Button(frame_acciones, text="🗑️ Eliminar", bootstyle="danger")
        self.btn_eliminar.pack(side=LEFT, padx=2)
        self.map_widgets['btn_eliminar'] = self.btn_eliminar

        # Botones de navegación
        frame_navegacion = Frame(frame_campos)
        frame_navegacion.grid(column=0, row=16, columnspan=3, sticky=EW, padx=PADDING_SM)

        self.btn_primero = Button(frame_navegacion, text="⏮️", bootstyle="secondary")
        self.btn_primero.pack(side=LEFT, padx=PADDING_SM, expand=True, fill=X)
        self.map_widgets['btn_primero'] = self.btn_primero

        self.btn_anterior = Button(frame_navegacion, text="◀️", bootstyle="secondary")
        self.btn_anterior.pack(side=LEFT, padx=PADDING_SM, expand=True, fill=X)
        self.map_widgets['btn_anterior'] = self.btn_anterior

        self.btn_siguiente = Button(frame_navegacion, text="▶️", bootstyle="secondary")
        self.btn_siguiente.pack(side=LEFT, padx=PADDING_SM, expand=True, fill=X)
        self.map_widgets['btn_siguiente'] = self.btn_siguiente

        self.btn_ultimo = Button(frame_navegacion, text="⏭️", bootstyle="secondary")
        self.btn_ultimo.pack(side=LEFT, padx=PADDING_SM, expand=True, fill=X)
        self.map_widgets['btn_ultimo'] = self.btn_ultimo

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Inferior
    # └────────────────────────────────────────────────────────────┘
    def _frame_inferior(self, frame: Frame):
        self.lbl_estadisticas = Label(frame, text="", bootstyle="secondary", anchor=W, style="Small.TLabel")
        self.lbl_estadisticas.pack(side=TOP, fill=X, padx=PADDING_SM, pady=PADDING_SM)
        self.map_widgets['lbl_estadisticas'] = self.lbl_estadisticas
