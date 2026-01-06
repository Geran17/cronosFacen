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
from ui.ttk.styles.icons import ICON_ASIGNATURA
from controladores.controlar_administrar_asignatura import ControlarAdministrarAsignatura

logger = obtener_logger_modulo(__name__)


class FrameAdministrarAsignatura(Frame):
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

        self.var_creditos = IntVar(value=0)
        self.map_vars['var_creditos'] = self.var_creditos

        self.var_horas_semanales = IntVar(value=0)
        self.map_vars['var_horas_semanales'] = self.var_horas_semanales

        self.var_tipo = StringVar()
        self.map_vars['var_tipo'] = self.var_tipo

        self.var_carrera = StringVar()
        self.map_vars['var_carrera'] = self.var_carrera

        # creamos los widgets
        self._crear_widgets()

        # Cargamos el controlador
        ControlarAdministrarAsignatura(
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
            text=f"{ICON_ASIGNATURA} Administrador de Asignaturas",
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

        # Panel Izquierdo: Tabla de Asignaturas
        frame_izquierdo = Labelframe(
            frame,
            text="📚 Lista de Asignaturas",
            padding=10,
            bootstyle="primary",
        )
        frame_izquierdo.grid(row=0, column=0, sticky=NSEW, padx=(0, 5))
        self._frame_tabla(frame_izquierdo)

        # Panel Derecho: Formulario
        frame_derecho = Labelframe(
            frame,
            text="📝 Detalles de Asignatura",
            padding=10,
            bootstyle="info",
        )
        frame_derecho.grid(row=0, column=1, sticky=NSEW, padx=(5, 0))
        self._frame_formulario(frame_derecho)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Tabla
    # └────────────────────────────────────────────────────────────┘
    def _frame_tabla(self, frame: Frame):
        # Frame para información
        frame_busqueda = Frame(frame)
        frame_busqueda.pack(fill=X, pady=(0, 10))

        lbl_info = Label(
            frame_busqueda,
            text="💡 Haz doble clic en una fila para editar",
            bootstyle="secondary",
            font=("Helvetica", 9, "italic"),
        )
        lbl_info.pack(side=LEFT, padx=5)

        self.tabla_asignatura = Tableview(
            frame,
            searchable=TRUE,
            paginated=TRUE,
            coldata=[
                {'text': 'Id', 'stretch': False, 'anchor': 'e'},  # Derecha (east)
                {'text': 'Codigo', 'stretch': False, 'anchor': 'center'},  # Centro
                {'text': 'Nombre', 'stretch': True, 'anchor': 'w'},  # Izquierda (west)
                {'text': 'Creditos', 'stretch': False, 'anchor': 'e'},  # Derecha
                {'text': 'Horas', 'stretch': False, 'anchor': 'e'},  # Derecha
                {'text': 'Tipo', 'stretch': False, 'anchor': 'center'},  # Centro
                {'text': 'Carrera', 'stretch': True, 'anchor': 'w'},  # Izquierda
            ],
            bootstyle="primary",
        )
        self.tabla_asignatura.pack(side=TOP, fill=BOTH, padx=1, pady=1, expand=TRUE)
        self.map_widgets['tabla_asignatura'] = self.tabla_asignatura

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

        self.entry_id = Entry(
            frame_campos,
            textvariable=self.var_id,
            state=READONLY,
            justify=RIGHT,
            bootstyle="secondary",
        )
        self.entry_id.grid(column=0, row=1, padx=5, pady=(0, 8), sticky=EW)
        self.map_widgets['entry_id'] = self.entry_id

        # Codigo
        lbl_codigo = Label(
            frame_campos, text="📋 Código:", anchor=W, font=("Helvetica", 10, "bold")
        )
        lbl_codigo.grid(column=1, row=0, sticky=W, padx=5, pady=(5, 2))

        self.entry_codigo = Entry(
            frame_campos,
            textvariable=self.var_codigo,
            bootstyle="info",
        )
        self.entry_codigo.grid(column=1, row=1, padx=5, pady=(0, 8), sticky=EW)
        self.map_widgets['entry_codigo'] = self.entry_codigo

        # Creditos
        lbl_creditos = Label(
            frame_campos, text="🎓 Créditos:", anchor=W, font=("Helvetica", 10, "bold")
        )
        lbl_creditos.grid(column=0, row=2, sticky=W, padx=5, pady=(5, 2))

        self.entry_creditos = Entry(
            frame_campos, textvariable=self.var_creditos, justify=RIGHT, bootstyle="info"
        )
        self.entry_creditos.grid(column=0, row=3, padx=5, pady=(0, 8), sticky=EW)
        self.map_widgets['entry_creditos'] = self.entry_creditos

        # Horas Semanales
        lbl_horas = Label(
            frame_campos, text="⏰ Horas Semanales:", anchor=W, font=("Helvetica", 10, "bold")
        )
        lbl_horas.grid(column=1, row=2, padx=5, pady=(5, 2), sticky=W)

        self.entry_horas = Entry(
            frame_campos, textvariable=self.var_horas_semanales, justify=RIGHT, bootstyle="info"
        )
        self.entry_horas.grid(column=1, row=3, pady=(0, 8), sticky=EW, padx=5)
        self.map_widgets['entry_horas'] = self.entry_horas

        # Nombre (ocupa todo el ancho)
        lbl_nombre = Label(
            frame_campos,
            text="📚 Nombre de la Asignatura:",
            anchor=W,
            font=("Helvetica", 10, "bold"),
        )
        lbl_nombre.grid(column=0, row=4, sticky=W, padx=5, pady=(5, 2), columnspan=2)

        self.entry_nombre = Entry(
            frame_campos,
            textvariable=self.var_nombre,
            bootstyle="info",
        )
        self.entry_nombre.grid(column=0, row=5, padx=5, pady=(0, 8), sticky=EW, columnspan=2)
        self.map_widgets['entry_nombre'] = self.entry_nombre

        # Tipo (ocupa todo el ancho)
        lbl_tipo = Label(frame_campos, text="📖 Tipo:", anchor=W, font=("Helvetica", 10, "bold"))
        lbl_tipo.grid(column=0, row=6, padx=5, pady=(5, 2), sticky=W, columnspan=2)

        self.cbx_tipo = Combobox(
            frame_campos,
            textvariable=self.var_tipo,
            state=READONLY,
            values=("Obligatoria", "Electiva"),
            bootstyle="info",
        )
        self.cbx_tipo.grid(column=0, row=7, pady=(0, 8), sticky=EW, padx=5, columnspan=2)
        self.map_widgets['cbx_tipo'] = self.cbx_tipo

        # Carrera (ocupa todo el ancho)
        lbl_carrera = Label(
            frame_campos, text="🏫 Carrera:", anchor=W, font=("Helvetica", 10, "bold")
        )
        lbl_carrera.grid(column=0, row=8, sticky=W, padx=5, pady=(5, 2), columnspan=2)

        self.cbx_carrera = Combobox(
            frame_campos,
            textvariable=self.var_carrera,
            state=READONLY,
            bootstyle="info",
        )
        self.cbx_carrera.grid(column=0, row=9, pady=(0, 10), sticky=EW, columnspan=2, padx=5)
        self.map_widgets['cbx_carrera'] = self.cbx_carrera

        # Separador
        Separator(frame_campos, bootstyle="secondary").grid(
            column=0, row=10, columnspan=2, sticky=EW, padx=5, pady=10
        )

        # Botones de acción principales
        frame_acciones = Frame(frame_campos)
        frame_acciones.grid(column=0, row=11, columnspan=2, sticky=EW, padx=5, pady=(0, 10))
        frame_acciones.columnconfigure(0, weight=1)
        frame_acciones.columnconfigure(1, weight=1)
        frame_acciones.columnconfigure(2, weight=1)

        self.btn_nuevo = Button(
            frame_acciones, text="➕ Nuevo", bootstyle="success-outline", width=8
        )
        self.btn_nuevo.grid(row=0, column=0, padx=2, sticky=EW)
        self.map_widgets['btn_nuevo'] = self.btn_nuevo

        self.btn_aplicar = Button(frame_acciones, text="💾 Guardar", bootstyle="primary", width=8)
        self.btn_aplicar.grid(row=0, column=1, padx=2, sticky=EW)
        self.map_widgets['btn_aplicar'] = self.btn_aplicar

        self.btn_eliminar = Button(
            frame_acciones, text="🗑️ Eliminar", bootstyle="danger-outline", width=8
        )
        self.btn_eliminar.grid(row=0, column=2, padx=2, sticky=EW)
        self.map_widgets['btn_eliminar'] = self.btn_eliminar

        # Separador antes de navegación
        Separator(frame_campos, bootstyle="secondary").grid(
            column=0, row=12, columnspan=2, sticky=EW, padx=5, pady=10
        )

        # Botones de navegación
        frame_navegacion = Frame(frame_campos)
        frame_navegacion.grid(column=0, row=13, columnspan=2, sticky=EW, padx=5)

        Label(
            frame_navegacion,
            text="Navegación:",
            font=("Helvetica", 9, "bold"),
            bootstyle="secondary",
        ).pack(side=LEFT, padx=(0, 10))

        self.btn_primero = Button(
            frame_navegacion, text="⏮️", bootstyle="secondary-outline", width=3
        )
        self.btn_primero.pack(side=LEFT, padx=2)
        self.map_widgets['btn_primero'] = self.btn_primero

        self.btn_anterior = Button(
            frame_navegacion, text="◀️", bootstyle="secondary-outline", width=3
        )
        self.btn_anterior.pack(side=LEFT, padx=2)
        self.map_widgets['btn_anterior'] = self.btn_anterior

        self.btn_siguiente = Button(
            frame_navegacion, text="▶️", bootstyle="secondary-outline", width=3
        )
        self.btn_siguiente.pack(side=LEFT, padx=2)
        self.map_widgets['btn_siguiente'] = self.btn_siguiente

        self.btn_ultimo = Button(frame_navegacion, text="⏭️", bootstyle="secondary-outline", width=3)
        self.btn_ultimo.pack(side=LEFT, padx=2)
        self.map_widgets['btn_ultimo'] = self.btn_ultimo

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Inferior
    # └────────────────────────────────────────────────────────────┘
    def _frame_inferior(self, frame: Frame):
        self.lbl_estadisticas = Label(frame, text="", bootstyle="secondary", anchor=W)
        self.lbl_estadisticas.pack(side=TOP, fill=X, padx=1, pady=1)
        self.map_widgets['lbl_estadisticas'] = self.lbl_estadisticas
