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
from ui.ttk.styles.icons import ICON_EJE_TEMATICO
from ui.ttk.utils.layout import build_header
from ui.ttk.utils.validation import bind_required
from ui.ttk.styles.estilos import PADDING_MD, PADDING_SM
from controladores.controlar_administrar_eje_tematico import ControlarAdministrarEjeTematico

logger = obtener_logger_modulo(__name__)


class FrameAdministrarEjeTematico(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        self.map_widgets: Dict[str, Any] = {}
        self.map_vars: Dict[str, Any] = {}

        # Variables
        self.var_id_eje = IntVar(value=0)
        self.map_vars['var_id_eje'] = self.var_id_eje

        self.var_nombre = StringVar()
        self.map_vars['var_nombre'] = self.var_nombre

        self.var_orden = IntVar(value=0)
        self.map_vars['var_orden'] = self.var_orden

        self.var_id_asignatura = IntVar(value=0)
        self.map_vars['var_id_asignatura'] = self.var_id_asignatura

        self.var_nombre_asignatura = StringVar()
        self.map_vars['var_nombre_asignatura'] = self.var_nombre_asignatura

        # Variables para filtros
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
        ControlarAdministrarEjeTematico(
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
            titulo=f"{ICON_EJE_TEMATICO} Administrador de Ejes Temáticos",
            subtitulo="Gestión de ejes temáticos y unidades",
        )

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Central
    # └────────────────────────────────────────────────────────────┘
    def _frame_central(self, frame: Frame):
        # Frame de filtros
        frame_filtros = Frame(frame, padding=(PADDING_SM, PADDING_SM))
        self._frame_filtros(frame=frame_filtros)
        frame_filtros.pack(side=TOP, fill=X, padx=PADDING_SM, pady=PADDING_SM)

        note_book = Notebook(frame, bootstyle="primary")
        note_book.pack(side=TOP, fill=BOTH, padx=PADDING_SM, pady=PADDING_SM, expand=TRUE)

        frame_tabla = Frame(note_book, padding=(PADDING_SM, PADDING_SM))
        self._frame_tabla(frame=frame_tabla)
        note_book.add(frame_tabla, text="Ejes Temáticos")

        frame_formulario = Frame(note_book, padding=(PADDING_SM, PADDING_SM))
        self._frame_formulario(frame=frame_formulario)
        note_book.add(frame_formulario, text="Formulario")

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Filtros
    # └────────────────────────────────────────────────────────────┘
    def _frame_filtros(self, frame: Frame):
        lf_filtros = Labelframe(
            frame,
            text="🔍 Filtros",
            bootstyle="secondary",
            padding=(5, 5),
        )
        lf_filtros.pack(side=TOP, fill=X, padx=PADDING_SM, pady=PADDING_SM)

        # Configuraciones de las columnas
        lf_filtros.columnconfigure(0, weight=1)
        lf_filtros.columnconfigure(1, weight=1)
        lf_filtros.columnconfigure(2, weight=1)

        # Filtro por Carrera
        lbl_carrera_filtro = Label(lf_filtros, text="Carrera:", anchor=W)
        lbl_carrera_filtro.grid(column=0, row=0, sticky=W, padx=PADDING_SM, pady=2)

        self.cbx_carrera_filtro = Combobox(
            lf_filtros,
            textvariable=self.var_nombre_carrera_filtro,
            state=READONLY,
        )
        self.cbx_carrera_filtro.grid(column=0, row=1, pady=2, padx=PADDING_SM, sticky=EW)
        self.map_widgets['cbx_carrera_filtro'] = self.cbx_carrera_filtro
        ToolTip(self.cbx_carrera_filtro, "Seleccione una carrera para filtrar")

        # Filtro por Asignatura
        lbl_asignatura_filtro = Label(lf_filtros, text="Asignatura:", anchor=W)
        lbl_asignatura_filtro.grid(column=1, row=0, sticky=W, padx=PADDING_SM, pady=2)

        self.cbx_asignatura_filtro = Combobox(
            lf_filtros,
            textvariable=self.var_nombre_asignatura_filtro,
            state=READONLY,
        )
        self.cbx_asignatura_filtro.grid(column=1, row=1, pady=2, padx=PADDING_SM, sticky=EW)
        self.map_widgets['cbx_asignatura_filtro'] = self.cbx_asignatura_filtro
        ToolTip(self.cbx_asignatura_filtro, "Seleccione una asignatura para filtrar")

        # Botón Limpiar Filtros
        self.btn_limpiar_filtros = Button(
            lf_filtros, text="🔄 Limpiar Filtros", bootstyle="secondary-outline"
        )
        self.btn_limpiar_filtros.grid(column=2, row=1, pady=2, padx=PADDING_SM, sticky=EW)
        self.map_widgets['btn_limpiar_filtros'] = self.btn_limpiar_filtros
        ToolTip(self.btn_limpiar_filtros, "Mostrar todos los ejes temáticos")

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Tabla
    # └────────────────────────────────────────────────────────────┘
    def _frame_tabla(self, frame: Frame):
        self.tabla_eje_tematico = Tableview(
            frame,
            searchable=TRUE,
            paginated=TRUE,
            coldata=[
                {'text': 'Id', 'stretch': False, 'anchor': 'e'},
                {'text': 'Nombre', 'stretch': True, 'anchor': 'w'},
                {'text': 'Orden', 'stretch': False, 'anchor': 'center'},
                {'text': 'Id Asignatura', 'stretch': False, 'anchor': 'e'},
                {'text': 'Asignatura', 'stretch': True, 'anchor': 'w'},
            ],
            bootstyle="primary",
        )
        self.tabla_eje_tematico.pack(side=TOP, fill=BOTH, padx=PADDING_SM, pady=PADDING_SM, expand=TRUE)
        self.map_widgets['tabla_eje_tematico'] = self.tabla_eje_tematico
        ToolTip(
            self.tabla_eje_tematico,
            "Doble click sobre una fila, para cargar los datos en el formulario",
        )

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Formulario
    # └────────────────────────────────────────────────────────────┘
    def _frame_formulario(self, frame: Frame):
        # Labelframe principal
        lf_datos = Labelframe(
            frame,
            text="📋 Datos del Eje Temático",
            bootstyle="primary",
            padding=(10, 10),
        )
        lf_datos.pack(side=TOP, fill=BOTH, padx=PADDING_SM, pady=PADDING_SM, expand=TRUE)

        # Configuraciones de las columnas
        lf_datos.columnconfigure(0, weight=1)
        lf_datos.columnconfigure(1, weight=1)
        lf_datos.columnconfigure(2, weight=1)

        # Id Eje
        lbl_id_eje = Label(lf_datos, text="Id:", anchor=W)
        lbl_id_eje.grid(column=0, row=0, sticky=W, padx=PADDING_SM, pady=2)

        self.entry_id_eje = Entry(
            lf_datos,
            textvariable=self.var_id_eje,
            state=READONLY,
            justify=RIGHT,
        )
        self.entry_id_eje.grid(column=0, row=1, padx=PADDING_SM, pady=2, sticky=EW)
        self.map_widgets['entry_id_eje'] = self.entry_id_eje

        # Orden
        lbl_orden = Label(lf_datos, text="Orden:", anchor=W)
        lbl_orden.grid(column=1, row=0, sticky=W, padx=PADDING_SM, pady=2)

        self.entry_orden = Entry(
            lf_datos,
            textvariable=self.var_orden,
            justify=RIGHT,
        )
        self.entry_orden.grid(column=1, row=1, padx=PADDING_SM, pady=2, sticky=EW)
        self.map_widgets['entry_orden'] = self.entry_orden
        ToolTip(self.entry_orden, "Orden de visualización del eje temático")

        # Id Asignatura
        lbl_id_asignatura = Label(lf_datos, text="Id Asignatura:", anchor=W)
        lbl_id_asignatura.grid(column=2, row=0, sticky=W, padx=PADDING_SM, pady=2)

        self.entry_id_asignatura = Entry(
            lf_datos,
            textvariable=self.var_id_asignatura,
            state=READONLY,
            justify=RIGHT,
        )
        self.entry_id_asignatura.grid(column=2, row=1, padx=PADDING_SM, pady=2, sticky=EW)
        self.map_widgets['entry_id_asignatura'] = self.entry_id_asignatura

        # Nombre
        lbl_nombre = Label(lf_datos, text="Nombre del Eje Temático:", anchor=W)
        lbl_nombre.grid(column=0, row=2, sticky=W, padx=PADDING_SM, pady=(10, 2), columnspan=3)

        self.entry_nombre = Entry(
            lf_datos,
            textvariable=self.var_nombre,
        )
        self.entry_nombre.grid(column=0, row=3, padx=PADDING_SM, pady=2, sticky=EW, columnspan=3)
        self.map_widgets['entry_nombre'] = self.entry_nombre
        ToolTip(self.entry_nombre, "Ingrese el nombre del eje temático")
        bind_required(self.entry_nombre, "info")

        # Asignatura (Combobox)
        lbl_asignatura = Label(lf_datos, text="Asignatura:", anchor=W)
        lbl_asignatura.grid(column=0, row=4, padx=PADDING_SM, pady=(10, 2), sticky=W, columnspan=3)

        self.cbx_asignatura = Combobox(
            lf_datos,
            textvariable=self.var_nombre_asignatura,
            state=READONLY,
        )
        self.cbx_asignatura.grid(column=0, row=5, pady=2, padx=PADDING_SM, sticky=EW, columnspan=3)
        self.map_widgets['cbx_asignatura'] = self.cbx_asignatura
        ToolTip(self.cbx_asignatura, "Seleccione la asignatura a la que pertenece este eje")

        # Labelframe de acciones
        lf_acciones = Labelframe(
            frame,
            text="⚙️ Acciones",
            bootstyle="secondary",
            padding=(10, 10),
        )
        lf_acciones.pack(side=TOP, fill=X, padx=PADDING_SM, pady=PADDING_SM)

        # Frame para botones principales
        frame_buttons_main = Frame(lf_acciones)
        frame_buttons_main.pack(side=TOP, fill=X, pady=2)

        self.btn_aplicar = Button(frame_buttons_main, text="✓ Aplicar", bootstyle="success")
        self.btn_aplicar.pack(side=LEFT, fill=X, padx=2, pady=2, expand=TRUE)
        self.map_widgets['btn_aplicar'] = self.btn_aplicar
        ToolTip(self.btn_aplicar, "Guardar cambios")

        self.btn_nuevo = Button(frame_buttons_main, text="+ Nuevo", bootstyle="info")
        self.btn_nuevo.pack(side=LEFT, fill=X, padx=2, pady=2, expand=TRUE)
        self.map_widgets['btn_nuevo'] = self.btn_nuevo
        ToolTip(self.btn_nuevo, "Crear nuevo eje temático")

        self.btn_eliminar = Button(frame_buttons_main, text="🗑 Eliminar", bootstyle="danger")
        self.btn_eliminar.pack(side=LEFT, fill=X, padx=2, pady=2, expand=TRUE)
        self.map_widgets['btn_eliminar'] = self.btn_eliminar
        ToolTip(self.btn_eliminar, "Eliminar eje temático seleccionado")

        # Separador
        Separator(lf_acciones, bootstyle="secondary").pack(side=TOP, fill=X, pady=PADDING_SM)

        # Frame para navegación
        frame_nav = Frame(lf_acciones)
        frame_nav.pack(side=TOP, fill=X, pady=2)

        Label(frame_nav, text="Navegación:", anchor=W).pack(side=LEFT, padx=PADDING_SM)

        self.btn_primero = Button(
            frame_nav, text="⏮ Primero", bootstyle="secondary-outline")
        self.btn_primero.pack(side=LEFT, padx=2)
        self.map_widgets['btn_primero'] = self.btn_primero
        ToolTip(self.btn_primero, "Ir al primer registro")

        self.btn_anterior = Button(
            frame_nav, text="◀ Anterior", bootstyle="secondary-outline")
        self.btn_anterior.pack(side=LEFT, padx=2)
        self.map_widgets['btn_anterior'] = self.btn_anterior
        ToolTip(self.btn_anterior, "Ir al registro anterior")

        self.btn_siguiente = Button(
            frame_nav, text="Siguiente ▶", bootstyle="secondary-outline")
        self.btn_siguiente.pack(side=LEFT, padx=2)
        self.map_widgets['btn_siguiente'] = self.btn_siguiente
        ToolTip(self.btn_siguiente, "Ir al siguiente registro")

        self.btn_ultimo = Button(
            frame_nav, text="Último ⏭", bootstyle="secondary-outline")
        self.btn_ultimo.pack(side=LEFT, padx=2)
        self.map_widgets['btn_ultimo'] = self.btn_ultimo
        ToolTip(self.btn_ultimo, "Ir al último registro")

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Inferior
    # └────────────────────────────────────────────────────────────┘
    def _frame_inferior(self, frame: Frame):
        self.lbl_estadisticas = Label(frame, text="", bootstyle="secondary", anchor=W, style="Small.TLabel")
        self.lbl_estadisticas.pack(side=TOP, fill=X, padx=PADDING_SM, pady=PADDING_SM)
        self.map_widgets['lbl_estadisticas'] = self.lbl_estadisticas
