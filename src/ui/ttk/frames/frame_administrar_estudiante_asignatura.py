from ttkbootstrap import (
    Frame,
    Label,
    Button,
    Separator,
    Entry,
    Combobox,
    Labelframe,
    Spinbox,
    StringVar,
    IntVar,
    DoubleVar,
)
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.tableview import Tableview
from typing import Dict, Any
from scripts.logging_config import obtener_logger_modulo
from ui.ttk.styles.icons import ICON_ESTUDIANTE
from controladores.controlar_administrar_estudiante_asignatura import (
    ControlarAdministrarEstudianteAsignatura,
)

logger = obtener_logger_modulo(__name__)


class FrameAdministrarEstudianteAsignatura(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        self.map_widgets: Dict[str, Any] = {}
        self.map_vars: Dict[str, Any] = {}

        # Variables
        self.var_id_estudiante = IntVar(value=0)
        self.map_vars['var_id_estudiante'] = self.var_id_estudiante

        self.var_nombre_estudiante = StringVar()
        self.map_vars['var_nombre_estudiante'] = self.var_nombre_estudiante

        self.var_id_asignatura_seleccionada = IntVar(value=0)
        self.map_vars['var_id_asignatura_seleccionada'] = self.var_id_asignatura_seleccionada

        self.var_nombre_asignatura_seleccionada = StringVar()
        self.map_vars['var_nombre_asignatura_seleccionada'] = (
            self.var_nombre_asignatura_seleccionada
        )

        self.var_estado = StringVar()
        self.map_vars['var_estado'] = self.var_estado

        self.var_nota = DoubleVar(value=0.0)
        self.map_vars['var_nota'] = self.var_nota

        self.var_periodo = StringVar()
        self.map_vars['var_periodo'] = self.var_periodo

        self.var_filtro_estado = StringVar(value="Todos")
        self.map_vars['var_filtro_estado'] = self.var_filtro_estado

        # creamos los widgets
        self._crear_widgets()

        # Cargamos el controlador
        ControlarAdministrarEstudianteAsignatura(
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

        frame_selector = Frame(self, padding=(5, 5))
        self._frame_selector_estudiante(frame=frame_selector)
        frame_selector.pack(side=TOP, fill=X, padx=1, pady=1)

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
            text=f"{ICON_ESTUDIANTE} Seguimiento Académico del Estudiante",
            bootstyle="info",
            font=("Helvetica", 16, "bold"),
        )
        label_info.pack(side=TOP, fill=X, padx=1, pady=1, expand=TRUE)

        Separator(frame).pack(side=TOP, fill=X, expand=TRUE, padx=1, pady=1)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Selector Estudiante
    # └────────────────────────────────────────────────────────────┘
    def _frame_selector_estudiante(self, frame: Frame):
        lbl_estudiante = Label(
            frame,
            text="Estudiante:",
            font=("Helvetica", 10, "bold"),
            anchor=W,
        )
        lbl_estudiante.pack(side=LEFT, padx=5)

        self.cbx_estudiante = Combobox(
            frame,
            textvariable=self.var_nombre_estudiante,
            state=READONLY,
            width=40,
        )
        self.cbx_estudiante.pack(side=LEFT, padx=5, fill=X, expand=True)
        self.map_widgets['cbx_estudiante'] = self.cbx_estudiante
        ToolTip(
            self.cbx_estudiante,
            "Selecciona un estudiante para ver su progreso académico",
        )

        self.btn_cargar_estudiante = Button(
            frame,
            text="📂 Cargar",
            bootstyle="info",
            width=12,
        )
        self.btn_cargar_estudiante.pack(side=LEFT, padx=5)
        self.map_widgets['btn_cargar_estudiante'] = self.btn_cargar_estudiante

        Separator(frame).pack(side=TOP, fill=X, expand=TRUE, padx=1, pady=10)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Central - Panel Dividido
    # └────────────────────────────────────────────────────────────┘
    def _frame_central(self, frame: Frame):
        # Configurar columnas: panel izquierdo (60%) y derecho (40%)
        frame.columnconfigure(0, weight=6, minsize=400)
        frame.columnconfigure(1, weight=4, minsize=300)
        frame.rowconfigure(0, weight=1)

        # Panel Izquierdo: Tabla de Asignaturas
        frame_izquierdo = Labelframe(
            frame,
            text="📚 Asignaturas del Estudiante",
            padding=10,
            bootstyle="primary",
        )
        frame_izquierdo.grid(row=0, column=0, sticky=NSEW, padx=(0, 5))
        self._panel_tabla_asignaturas(frame_izquierdo)

        # Panel Derecho: Formulario y Estadísticas
        frame_derecho = Frame(frame)
        frame_derecho.grid(row=0, column=1, sticky=NSEW, padx=(5, 0))
        self._panel_formulario_estadisticas(frame_derecho)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Izquierdo - Tabla de Asignaturas
    # └────────────────────────────────────────────────────────────┘
    def _panel_tabla_asignaturas(self, frame: Frame):
        # Frame para filtros
        frame_filtros = Frame(frame)
        frame_filtros.pack(fill=X, pady=(0, 10))

        # Campo de búsqueda
        lbl_buscar = Label(frame_filtros, text="🔎 Buscar:", anchor=W)
        lbl_buscar.pack(side=LEFT, padx=(0, 5))

        self.entry_buscar_asignatura = Entry(frame_filtros, width=20)
        self.entry_buscar_asignatura.pack(side=LEFT, padx=(0, 10), fill=X, expand=True)
        self.map_widgets['entry_buscar_asignatura'] = self.entry_buscar_asignatura
        ToolTip(
            self.entry_buscar_asignatura,
            "Buscar por código o nombre de asignatura",
        )

        # Filtro por estado
        lbl_estado = Label(frame_filtros, text="Estado:", anchor=W)
        lbl_estado.pack(side=LEFT, padx=(0, 5))

        self.cbx_filtro_estado = Combobox(
            frame_filtros,
            textvariable=self.var_filtro_estado,
            values=["Todos", "🔵 No cursada", "🟡 Cursando", "🟢 Aprobada", "🔴 Reprobada"],
            state=READONLY,
            width=15,
        )
        self.cbx_filtro_estado.pack(side=LEFT)
        self.map_widgets['cbx_filtro_estado'] = self.cbx_filtro_estado
        ToolTip(self.cbx_filtro_estado, "Filtrar asignaturas por estado")

        # Tabla de asignaturas
        self.tabla_asignaturas = Tableview(
            frame,
            searchable=False,
            paginated=True,
            pagesize=10,
            coldata=[
                {'text': 'Código', 'stretch': False, 'anchor': 'w'},
                {'text': 'Asignatura', 'stretch': True, 'anchor': 'w'},
                {'text': 'Créditos', 'stretch': False, 'anchor': 'center'},
                {'text': 'Estado', 'stretch': False, 'anchor': 'center'},
                {'text': 'Nota', 'stretch': False, 'anchor': 'e'},
                {'text': 'Período', 'stretch': False, 'anchor': 'center'},
            ],
            bootstyle="primary",
        )
        self.tabla_asignaturas.pack(fill=BOTH, expand=True)
        self.map_widgets['tabla_asignaturas'] = self.tabla_asignaturas
        ToolTip(
            self.tabla_asignaturas,
            "Click en una asignatura para actualizar su estado o nota",
        )

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Derecho - Formulario y Estadísticas
    # └────────────────────────────────────────────────────────────┘
    def _panel_formulario_estadisticas(self, frame: Frame):
        # Frame para formulario de actualización
        frame_formulario = Labelframe(
            frame,
            text="✏️ Actualizar Estado y Nota",
            padding=10,
            bootstyle="success",
        )
        frame_formulario.pack(fill=BOTH, expand=True, pady=(0, 10))
        self._crear_formulario(frame_formulario)

        # Frame para estadísticas
        frame_stats = Labelframe(
            frame,
            text="📊 Estadísticas del Estudiante",
            padding=10,
            bootstyle="info",
        )
        frame_stats.pack(fill=X)
        self._crear_estadisticas(frame_stats)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Formulario de Actualización
    # └────────────────────────────────────────────────────────────┘
    def _crear_formulario(self, frame: Frame):
        # Asignatura seleccionada
        lbl_asig = Label(
            frame,
            text="Asignatura Seleccionada:",
            font=("Helvetica", 9, "bold"),
            anchor=W,
        )
        lbl_asig.pack(fill=X, pady=(0, 3))

        self.lbl_asignatura_seleccionada = Label(
            frame,
            textvariable=self.var_nombre_asignatura_seleccionada,
            font=("Helvetica", 9),
            foreground="blue",
            anchor=W,
        )
        self.lbl_asignatura_seleccionada.pack(fill=X, pady=(0, 10))
        self.map_widgets['lbl_asignatura_seleccionada'] = self.lbl_asignatura_seleccionada

        # Estado
        lbl_estado = Label(frame, text="Estado:", anchor=W)
        lbl_estado.pack(fill=X, pady=(0, 3))

        self.cbx_estado = Combobox(
            frame,
            textvariable=self.var_estado,
            values=["🔵 No cursada", "🟡 Cursando", "🟢 Aprobada", "🔴 Reprobada"],
            state=READONLY,
        )
        self.cbx_estado.pack(fill=X, pady=(0, 10))
        self.map_widgets['cbx_estado'] = self.cbx_estado
        ToolTip(self.cbx_estado, "Selecciona el estado de la asignatura")

        # Nota
        lbl_nota = Label(frame, text="Nota (0-100):", anchor=W)
        lbl_nota.pack(fill=X, pady=(0, 3))

        self.spin_nota = Spinbox(
            frame,
            from_=0,
            to=100,
            increment=0.5,
            textvariable=self.var_nota,
        )
        self.spin_nota.pack(fill=X, pady=(0, 10))
        self.map_widgets['spin_nota'] = self.spin_nota
        ToolTip(self.spin_nota, "Ingresa la nota obtenida (0-100)")

        # Período
        lbl_periodo = Label(frame, text="Período:", anchor=W)
        lbl_periodo.pack(fill=X, pady=(0, 3))

        self.entry_periodo = Entry(frame, textvariable=self.var_periodo)
        self.entry_periodo.pack(fill=X, pady=(0, 10))
        self.map_widgets['entry_periodo'] = self.entry_periodo
        ToolTip(self.entry_periodo, "Ejemplo: 2025-I, 2025-II")

        # Botones
        frame_buttons = Frame(frame, padding=(1, 1), bootstyle="success")
        frame_buttons.pack(fill=X, pady=(10, 0))

        self.btn_aplicar = Button(frame_buttons, text="Aplicar", bootstyle="success")
        self.btn_aplicar.pack(side=LEFT, fill=X, padx=1, pady=1, expand=TRUE)
        self.map_widgets['btn_aplicar'] = self.btn_aplicar

        self.btn_limpiar = Button(frame_buttons, text="Limpiar", bootstyle="secondary")
        self.btn_limpiar.pack(side=LEFT, fill=X, padx=1, pady=1, expand=TRUE)
        self.map_widgets['btn_limpiar'] = self.btn_limpiar

    # ┌────────────────────────────────────────────────────────────┐
    # │ Estadísticas del Estudiante
    # └────────────────────────────────────────────────────────────┘
    def _crear_estadisticas(self, frame: Frame):
        self.lbl_total_asignaturas = Label(
            frame,
            text="Total Asignaturas: -",
            anchor=W,
        )
        self.lbl_total_asignaturas.pack(fill=X, pady=2)
        self.map_widgets['lbl_total_asignaturas'] = self.lbl_total_asignaturas

        self.lbl_aprobadas = Label(
            frame,
            text="🟢 Aprobadas: -",
            anchor=W,
        )
        self.lbl_aprobadas.pack(fill=X, pady=2)
        self.map_widgets['lbl_aprobadas'] = self.lbl_aprobadas

        self.lbl_cursando = Label(
            frame,
            text="🟡 Cursando: -",
            anchor=W,
        )
        self.lbl_cursando.pack(fill=X, pady=2)
        self.map_widgets['lbl_cursando'] = self.lbl_cursando

        self.lbl_reprobadas = Label(
            frame,
            text="🔴 Reprobadas: -",
            anchor=W,
        )
        self.lbl_reprobadas.pack(fill=X, pady=2)
        self.map_widgets['lbl_reprobadas'] = self.lbl_reprobadas

        self.lbl_no_cursadas = Label(
            frame,
            text="🔵 No Cursadas: -",
            anchor=W,
        )
        self.lbl_no_cursadas.pack(fill=X, pady=2)
        self.map_widgets['lbl_no_cursadas'] = self.lbl_no_cursadas

        self.lbl_promedio = Label(
            frame,
            text="📈 Promedio: -",
            font=("Helvetica", 9, "bold"),
            anchor=W,
        )
        self.lbl_promedio.pack(fill=X, pady=(5, 2))
        self.map_widgets['lbl_promedio'] = self.lbl_promedio

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Inferior
    # └────────────────────────────────────────────────────────────┘
    def _frame_inferior(self, frame: Frame):
        self.lbl_estadisticas = Label(frame, text="", bootstyle="secondary", anchor=W)
        self.lbl_estadisticas.pack(side=TOP, fill=X, padx=1, pady=1)
        self.map_widgets['lbl_estadisticas'] = self.lbl_estadisticas
