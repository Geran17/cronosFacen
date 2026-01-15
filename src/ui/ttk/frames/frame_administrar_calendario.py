from ttkbootstrap import (
    Frame,
    Label,
    Button,
    Separator,
    Entry,
    Combobox,
    Notebook,
    StringVar,
    IntVar,
    Checkbutton,
)
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.tableview import Tableview
from typing import Dict, Any
from scripts.logging_config import obtener_logger_modulo
from ui.ttk.styles.icons import ICON_CALENDARIO
from controladores.controlar_administrar_calendario import ControlarAdministrarCalendario

logger = obtener_logger_modulo(__name__)


class FrameAdministrarCalendario(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        self.map_widgets: Dict[str, Any] = {}
        self.map_vars: Dict[str, Any] = {}

        # Variables
        self.var_id_evento = IntVar(value=0)
        self.map_vars['var_id_evento'] = self.var_id_evento

        self.var_titulo = StringVar()
        self.map_vars['var_titulo'] = self.var_titulo

        self.var_tipo = StringVar()
        self.map_vars['var_tipo'] = self.var_tipo

        self.var_fecha_inicio = StringVar()
        self.map_vars['var_fecha_inicio'] = self.var_fecha_inicio

        self.var_fecha_fin = StringVar()
        self.map_vars['var_fecha_fin'] = self.var_fecha_fin

        self.var_afecta_actividades = IntVar(value=0)
        self.map_vars['var_afecta_actividades'] = self.var_afecta_actividades

        # creamos los widgets
        self._crear_widgets()

        # Cargamos el controlador
        ControlarAdministrarCalendario(
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
            text=f"{ICON_CALENDARIO} Administrador de Calendario de Eventos",
            bootstyle="info",
            font=("Helvetica", 16, "bold"),
        )
        label_info.pack(side=TOP, fill=X, padx=1, pady=1, expand=TRUE)

        Separator(frame).pack(side=TOP, fill=X, expand=TRUE, padx=1, pady=1)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Central
    # └────────────────────────────────────────────────────────────┘
    def _frame_central(self, frame: Frame):
        # Configurar el frame para usar todo el espacio disponible
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        # Crear Notebook para las pestañas
        notebook = Notebook(frame)
        notebook.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)

        # Pestaña 1: Tabla de Eventos
        tab_tabla = Frame(notebook)
        notebook.add(tab_tabla, text="📋 Lista de Eventos")
        self._frame_tabla(tab_tabla)

        # Pestaña 2: Formulario
        tab_formulario = Frame(notebook)
        notebook.add(tab_formulario, text="📝 Detalles del Evento")
        self._frame_formulario(tab_formulario)

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

        self.tabla_evento = Tableview(
            frame,
            searchable=TRUE,
            paginated=TRUE,
            coldata=[
                {'text': 'Id', 'stretch': False, 'anchor': 'e'},
                {'text': 'Título', 'stretch': True, 'anchor': 'w'},
                {'text': 'Tipo', 'stretch': False, 'anchor': 'w'},
                {'text': 'Fecha Inicio', 'stretch': False, 'anchor': 'center'},
                {'text': 'Fecha Fin', 'stretch': False, 'anchor': 'center'},
                {'text': 'Afecta', 'stretch': False, 'anchor': 'center'},
            ],
            bootstyle="primary",
        )
        self.tabla_evento.pack(side=TOP, fill=BOTH, padx=1, pady=1, expand=TRUE)
        self.map_widgets['tabla_evento'] = self.tabla_evento

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

        self.entry_id_evento = Entry(
            frame_campos,
            textvariable=self.var_id_evento,
            state=READONLY,
            justify=RIGHT,
            bootstyle="secondary",
        )
        self.entry_id_evento.grid(column=0, row=1, padx=5, pady=(0, 8), sticky=EW)
        self.map_widgets['entry_id_evento'] = self.entry_id_evento

        # Tipo
        lbl_tipo = Label(frame_campos, text="🏷️ Tipo:", anchor=W, font=("Helvetica", 10, "bold"))
        lbl_tipo.grid(column=1, row=0, sticky=W, padx=5, pady=(5, 2))

        self.cbx_tipo = Combobox(
            frame_campos,
            textvariable=self.var_tipo,
            state=NORMAL,
            values=[
                "Feriando",
                "Asueto",
                "Administrativo",
                "Conmemorativo",
                "Evalución",
                "Académico",
            ],
            bootstyle="info",
        )
        self.cbx_tipo.grid(column=1, row=1, padx=5, pady=(0, 8), sticky=EW)
        self.map_widgets['cbx_tipo'] = self.cbx_tipo

        # Título
        lbl_titulo = Label(
            frame_campos, text="📝 Título del Evento:", anchor=W, font=("Helvetica", 10, "bold")
        )
        lbl_titulo.grid(column=0, row=2, sticky=W, padx=5, pady=(5, 2), columnspan=2)

        self.entry_titulo = Entry(
            frame_campos,
            textvariable=self.var_titulo,
            bootstyle="info",
        )
        self.entry_titulo.grid(column=0, row=3, padx=5, pady=(0, 8), sticky=EW, columnspan=2)
        self.map_widgets['entry_titulo'] = self.entry_titulo

        # Fecha Inicio
        lbl_fecha_inicio = Label(
            frame_campos, text="📅 Fecha Inicio:", anchor=W, font=("Helvetica", 10, "bold")
        )
        lbl_fecha_inicio.grid(column=0, row=4, sticky=W, padx=5, pady=(5, 2))

        self.entry_fecha_inicio = Entry(
            frame_campos,
            textvariable=self.var_fecha_inicio,
            justify=CENTER,
            bootstyle="info",
        )
        self.entry_fecha_inicio.grid(column=0, row=5, padx=5, pady=(0, 8), sticky=EW)
        self.map_widgets['entry_fecha_inicio'] = self.entry_fecha_inicio

        # Fecha Fin
        lbl_fecha_fin = Label(
            frame_campos, text="📅 Fecha Fin:", anchor=W, font=("Helvetica", 10, "bold")
        )
        lbl_fecha_fin.grid(column=1, row=4, sticky=W, padx=5, pady=(5, 2))

        self.entry_fecha_fin = Entry(
            frame_campos,
            textvariable=self.var_fecha_fin,
            justify=CENTER,
            bootstyle="info",
        )
        self.entry_fecha_fin.grid(column=1, row=5, padx=5, pady=(0, 8), sticky=EW)
        self.map_widgets['entry_fecha_fin'] = self.entry_fecha_fin

        # Afecta Actividades
        lbl_config = Label(
            frame_campos, text="⚙️ Configuración:", anchor=W, font=("Helvetica", 10, "bold")
        )
        lbl_config.grid(column=0, row=6, sticky=W, padx=5, pady=(5, 2), columnspan=2)

        self.chk_afecta_actividades = Checkbutton(
            frame_campos,
            text="Afecta a las actividades programadas",
            variable=self.var_afecta_actividades,
            bootstyle="round-toggle",
        )
        self.chk_afecta_actividades.grid(
            column=0, row=7, padx=5, pady=(0, 10), sticky=W, columnspan=2
        )
        self.map_widgets['chk_afecta_actividades'] = self.chk_afecta_actividades
        ToolTip(
            self.chk_afecta_actividades,
            "Marcar si este evento afecta las fechas de entrega de actividades",
        )

        # Separador
        Separator(frame_campos, bootstyle="secondary").grid(
            column=0, row=8, columnspan=2, sticky=EW, padx=5, pady=10
        )

        # Botones de acción principales
        frame_acciones = Frame(frame_campos)
        frame_acciones.grid(column=0, row=9, columnspan=2, sticky=EW, padx=5, pady=(0, 5))

        self.btn_nuevo = Button(frame_acciones, text="➕ Nuevo", bootstyle="success", width=12)
        self.btn_nuevo.pack(side=LEFT, padx=2)
        self.map_widgets['btn_nuevo'] = self.btn_nuevo

        self.btn_aplicar = Button(frame_acciones, text="💾 Guardar", bootstyle="primary", width=12)
        self.btn_aplicar.pack(side=LEFT, padx=2)
        self.map_widgets['btn_aplicar'] = self.btn_aplicar

        self.btn_importar = Button(frame_acciones, text="📥 Importar", bootstyle="info", width=12)
        self.btn_importar.pack(side=LEFT, padx=2)
        self.map_widgets['btn_importar'] = self.btn_importar

        self.btn_eliminar = Button(frame_acciones, text="🗑️ Eliminar", bootstyle="danger", width=12)
        self.btn_eliminar.pack(side=LEFT, padx=2)
        self.map_widgets['btn_eliminar'] = self.btn_eliminar

        # Botones de navegación
        frame_navegacion = Frame(frame_campos)
        frame_navegacion.grid(column=0, row=10, columnspan=2, sticky=EW, padx=5)

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
