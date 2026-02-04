from ttkbootstrap import (
    Frame,
    Label,
    Button,
    Separator,
    Entry,
    Combobox,
    Labelframe,
    StringVar,
    IntVar,
    Text,
    Scrollbar,
)
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs import Messagebox
from typing import Dict, Any
from ui.ttk.styles.estilos import PADDING_MD, PADDING_SM
from scripts.logging_config import obtener_logger_modulo
from ui.ttk.utils.layout import build_header
from controladores.controlar_administrar_estudiante_carrera import (
    ControlarAdministrarEstudianteCarrera,
)

logger = obtener_logger_modulo(__name__)


class FrameAdministrarEstudianteCarrera(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        self.map_widgets: Dict[str, Any] = {}
        self.map_vars: Dict[str, Any] = {}

        # Variables para Estudiante
        self.var_id_estudiante = IntVar(value=0)
        self.map_vars['var_id_estudiante'] = self.var_id_estudiante

        self.var_nombre_estudiante = StringVar()
        self.map_vars['var_nombre_estudiante'] = self.var_nombre_estudiante

        # Variables para Carrera
        self.var_id_carrera = IntVar(value=0)
        self.map_vars['var_id_carrera'] = self.var_id_carrera

        self.var_nombre_carrera = StringVar()
        self.map_vars['var_nombre_carrera'] = self.var_nombre_carrera

        # Variables de inscripción
        self.var_estado = StringVar(value='activa')
        self.map_vars['var_estado'] = self.var_estado

        self.var_fecha_inscripcion = StringVar()
        self.map_vars['var_fecha_inscripcion'] = self.var_fecha_inscripcion

        self.var_fecha_inicio = StringVar()
        self.map_vars['var_fecha_inicio'] = self.var_fecha_inicio

        self.var_fecha_fin = StringVar()
        self.map_vars['var_fecha_fin'] = self.var_fecha_fin

        self.var_es_principal = IntVar(value=1)
        self.map_vars['var_es_principal'] = self.var_es_principal

        self.var_periodo_ingreso = StringVar()
        self.map_vars['var_periodo_ingreso'] = self.var_periodo_ingreso

        # Variables de filtro
        self.var_filtro_estado = StringVar(value="Todos")
        self.map_vars['var_filtro_estado'] = self.var_filtro_estado

        # creamos los widgets
        self._crear_widgets()

        # Cargamos el controlador
        ControlarAdministrarEstudianteCarrera(
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

        frame_selector = Frame(self, padding=(5, 5))
        self._frame_selector_estudiante(frame=frame_selector)
        frame_selector.pack(side=TOP, fill=X, padx=PADDING_SM, pady=PADDING_SM)

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
            titulo="🎓 Administrador de Inscripciones Estudiante-Carrera",
            subtitulo="Gestión de inscripciones y estados de carrera",
        )

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Selector de Estudiante
    # └────────────────────────────────────────────────────────────┘
    def _frame_selector_estudiante(self, frame: Frame):
        # Frame contenedor
        frame_contenedor = Labelframe(
            frame,
            text="👤 Selección de Estudiante",
            padding=10,
            bootstyle="primary",
        )
        frame_contenedor.pack(fill=X, padx=PADDING_SM, pady=PADDING_SM)

        # Layout horizontal
        frame_contenedor.columnconfigure(1, weight=1)

        # Label
        Label(
            frame_contenedor,
            text="Estudiante:",
            style="FormLabel.TLabel",
        ).grid(row=0, column=0, sticky=W, padx=(5, 10))

        # Combobox de estudiantes
        self.cbx_estudiante = Combobox(
            frame_contenedor,
            textvariable=self.var_nombre_estudiante,
            state=READONLY,
            bootstyle="primary",
        )
        self.cbx_estudiante.grid(row=0, column=1, sticky=EW, padx=PADDING_SM)
        self.map_widgets['cbx_estudiante'] = self.cbx_estudiante
        ToolTip(self.cbx_estudiante, text="Seleccione un estudiante para ver sus carreras")

        # Botón de refrescar
        self.btn_refrescar_estudiante = Button(
            frame_contenedor,
            text="🔄",
            bootstyle="info-outline")
        self.btn_refrescar_estudiante.grid(row=0, column=2, padx=PADDING_SM)
        self.map_widgets['btn_refrescar_estudiante'] = self.btn_refrescar_estudiante
        ToolTip(self.btn_refrescar_estudiante, text="Refrescar lista de estudiantes")

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Central
    # └────────────────────────────────────────────────────────────┘
    def _frame_central(self, frame: Frame):
        # Configurar columnas: tabla izquierda (60%) y formulario derecho (40%)
        frame.columnconfigure(0, weight=6, minsize=400)
        frame.columnconfigure(1, weight=4, minsize=300)
        frame.rowconfigure(0, weight=1)

        # Panel Izquierdo: Tabla de Carreras
        frame_izquierdo = Labelframe(
            frame,
            text="📚 Carreras del Estudiante",
            padding=10,
            bootstyle="primary",
        )
        frame_izquierdo.grid(row=0, column=0, sticky=NSEW, padx=(0, 5))
        self._frame_tabla(frame_izquierdo)

        # Panel Derecho: Formulario
        frame_derecho = Labelframe(
            frame,
            text="📝 Detalles de la Inscripción",
            padding=10,
            bootstyle="info",
        )
        frame_derecho.grid(row=0, column=1, sticky=NSEW, padx=(5, 0))
        self._frame_formulario(frame_derecho)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Tabla
    # └────────────────────────────────────────────────────────────┘
    def _frame_tabla(self, frame: Frame):
        # Frame superior con filtros y búsqueda
        frame_controles = Frame(frame)
        frame_controles.pack(fill=X, pady=(0, PADDING_MD))
        frame_controles.columnconfigure(1, weight=1)

        # Filtro por estado
        Label(frame_controles, text="Filtrar:", style="Small.TLabel").grid(
            row=0, column=0, sticky=W, padx=PADDING_SM, pady=PADDING_SM
        )

        self.cbx_filtro_estado = Combobox(
            frame_controles,
            textvariable=self.var_filtro_estado,
            values=["Todos", "activa", "inactiva", "suspendida", "completada", "abandonada"],
            state=READONLY,
            bootstyle="secondary",
        )
        self.cbx_filtro_estado.grid(row=0, column=1, sticky=EW, padx=PADDING_SM, pady=PADDING_SM)
        self.map_widgets['cbx_filtro_estado'] = self.cbx_filtro_estado

        lbl_info = Label(
            frame_controles,
            text="💡 Doble clic para editar",
            bootstyle="secondary",
            style="Hint.TLabel",
        )
        lbl_info.grid(row=1, column=0, columnspan=2, sticky=E, padx=PADDING_SM)

        # Tabla
        self.tabla_carreras = Tableview(
            frame,
            searchable=TRUE,
            paginated=TRUE,
            coldata=[
                {'text': 'ID Est.', 'stretch': False, 'width': 60, 'anchor': 'e'},
                {'text': 'ID Car.', 'stretch': False, 'width': 60, 'anchor': 'e'},
                {'text': 'Carrera', 'stretch': True, 'anchor': 'w'},
                {'text': 'Estado', 'stretch': False, 'width': 100, 'anchor': 'center'},
                {'text': 'Principal', 'stretch': False, 'width': 80, 'anchor': 'center'},
                {'text': 'F. Inscripción', 'stretch': False, 'width': 100, 'anchor': 'center'},
                {'text': 'Periodo', 'stretch': False, 'width': 80, 'anchor': 'center'},
            ],
            bootstyle="primary",
        )
        self.tabla_carreras.pack(side=TOP, fill=BOTH, padx=PADDING_SM, pady=PADDING_SM, expand=TRUE)
        self.map_widgets['tabla_carreras'] = self.tabla_carreras

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Formulario
    # └────────────────────────────────────────────────────────────┘
    def _frame_formulario(self, frame: Frame):
        # Frame para scroll si es necesario
        frame_campos = Frame(frame)
        frame_campos.pack(fill=BOTH, expand=True, pady=(0, 10))
        frame_campos.columnconfigure(0, weight=1)

        row = 0

        # ID Estudiante (readonly)
        Label(
            frame_campos,
            text="ID Estudiante:",
            anchor=W,
            style="Small.TLabel",
        ).grid(column=0, row=row, sticky=W, padx=PADDING_SM, pady=(5, 2))
        row += 1

        self.entry_id_estudiante = Entry(
            frame_campos,
            textvariable=self.var_id_estudiante,
            state=READONLY,
            justify=RIGHT,
            bootstyle="secondary",
        )
        self.entry_id_estudiante.grid(column=0, row=row, padx=PADDING_SM, pady=(0, 8), sticky=EW)
        self.map_widgets['entry_id_estudiante'] = self.entry_id_estudiante
        row += 1

        # Selección de Carrera
        Label(
            frame_campos,
            text="🎓 Carrera:",
            anchor=W,
            style="FormLabel.TLabel",
        ).grid(column=0, row=row, sticky=W, padx=PADDING_SM, pady=(5, 2))
        row += 1

        self.cbx_carrera = Combobox(
            frame_campos,
            textvariable=self.var_nombre_carrera,
            state=READONLY,
            bootstyle="info",
        )
        self.cbx_carrera.grid(column=0, row=row, padx=PADDING_SM, pady=(0, 8), sticky=EW)
        self.map_widgets['cbx_carrera'] = self.cbx_carrera
        ToolTip(self.cbx_carrera, text="Seleccione la carrera a inscribir")
        row += 1

        # Estado
        Label(
            frame_campos,
            text="📊 Estado:",
            anchor=W,
            style="FormLabel.TLabel",
        ).grid(column=0, row=row, sticky=W, padx=PADDING_SM, pady=(5, 2))
        row += 1

        self.cbx_estado = Combobox(
            frame_campos,
            textvariable=self.var_estado,
            values=['activa', 'inactiva', 'suspendida', 'completada', 'abandonada'],
            state=READONLY,
            bootstyle="info",
        )
        self.cbx_estado.grid(column=0, row=row, padx=PADDING_SM, pady=(0, 8), sticky=EW)
        self.map_widgets['cbx_estado'] = self.cbx_estado
        row += 1

        # Fecha de Inscripción
        Label(
            frame_campos,
            text="📅 Fecha Inscripción:",
            anchor=W,
            style="FormLabel.TLabel",
        ).grid(column=0, row=row, sticky=W, padx=PADDING_SM, pady=(5, 2))
        row += 1

        self.entry_fecha_inscripcion = Entry(
            frame_campos,
            textvariable=self.var_fecha_inscripcion,
            bootstyle="info",
        )
        self.entry_fecha_inscripcion.grid(column=0, row=row, padx=PADDING_SM, pady=(0, 8), sticky=EW)
        self.map_widgets['entry_fecha_inscripcion'] = self.entry_fecha_inscripcion
        ToolTip(self.entry_fecha_inscripcion, text="Formato: YYYY-MM-DD")
        row += 1

        # Fecha de Inicio (Opcional)
        Label(
            frame_campos,
            text="📅 Fecha Inicio (opcional):",
            anchor=W,
            style="Small.TLabel",
        ).grid(column=0, row=row, sticky=W, padx=PADDING_SM, pady=(5, 2))
        row += 1

        self.entry_fecha_inicio = Entry(
            frame_campos,
            textvariable=self.var_fecha_inicio,
            bootstyle="secondary",
        )
        self.entry_fecha_inicio.grid(column=0, row=row, padx=PADDING_SM, pady=(0, 8), sticky=EW)
        self.map_widgets['entry_fecha_inicio'] = self.entry_fecha_inicio
        ToolTip(self.entry_fecha_inicio, text="Formato: YYYY-MM-DD (opcional)")
        row += 1

        # Fecha de Fin (Opcional)
        Label(
            frame_campos,
            text="📅 Fecha Fin (opcional):",
            anchor=W,
            style="Small.TLabel",
        ).grid(column=0, row=row, sticky=W, padx=PADDING_SM, pady=(5, 2))
        row += 1

        self.entry_fecha_fin = Entry(
            frame_campos,
            textvariable=self.var_fecha_fin,
            bootstyle="secondary",
        )
        self.entry_fecha_fin.grid(column=0, row=row, padx=PADDING_SM, pady=(0, 8), sticky=EW)
        self.map_widgets['entry_fecha_fin'] = self.entry_fecha_fin
        ToolTip(self.entry_fecha_fin, text="Formato: YYYY-MM-DD (opcional)")
        row += 1

        # Es Carrera Principal
        frame_principal = Frame(frame_campos)
        frame_principal.grid(column=0, row=row, padx=PADDING_SM, pady=(5, 8), sticky=EW)
        row += 1

        self.chk_es_principal = Button(
            frame_principal,
            text="⭐ Es Carrera Principal",
            bootstyle="warning-outline",
            command=self._toggle_principal)
        self.chk_es_principal.pack(fill=X)
        self.map_widgets['chk_es_principal'] = self.chk_es_principal
        ToolTip(
            self.chk_es_principal,
            text="Marcar como carrera principal del estudiante (solo una puede ser principal)",
        )

        # Periodo de Ingreso
        Label(
            frame_campos,
            text="📆 Periodo Ingreso:",
            anchor=W,
            style="FormLabel.TLabel",
        ).grid(column=0, row=row, sticky=W, padx=PADDING_SM, pady=(5, 2))
        row += 1

        self.entry_periodo = Entry(
            frame_campos,
            textvariable=self.var_periodo_ingreso,
            bootstyle="info",
        )
        self.entry_periodo.grid(column=0, row=row, padx=PADDING_SM, pady=(0, 8), sticky=EW)
        self.map_widgets['entry_periodo'] = self.entry_periodo
        ToolTip(self.entry_periodo, text="Ej: 2024-1, 2024-2")
        row += 1

        # Observaciones
        Label(
            frame_campos,
            text="📝 Observaciones:",
            anchor=W,
            style="Small.TLabel",
        ).grid(column=0, row=row, sticky=W, padx=PADDING_SM, pady=(5, 2))
        row += 1

        frame_text = Frame(frame_campos)
        frame_text.grid(column=0, row=row, padx=PADDING_SM, pady=(0, 8), sticky=EW)
        row += 1

        self.text_observaciones = Text(
            frame_text,
            height=3,
            wrap=WORD,
        )
        self.text_observaciones.pack(side=LEFT, fill=BOTH, expand=True)
        self.map_widgets['text_observaciones'] = self.text_observaciones

        scrollbar = Scrollbar(frame_text, command=self.text_observaciones.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.text_observaciones.config(yscrollcommand=scrollbar.set)

        # Separador
        Separator(frame_campos, bootstyle="secondary").grid(
            column=0, row=row, sticky=EW, padx=PADDING_SM, pady=PADDING_MD
        )
        row += 1

        # Botones de acción
        frame_acciones = Frame(frame_campos)
        frame_acciones.grid(column=0, row=row, sticky=EW, padx=PADDING_SM, pady=(0, 5))
        row += 1

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

        # Botones adicionales
        frame_extras = Frame(frame_campos)
        frame_extras.grid(column=0, row=row, sticky=EW, padx=PADDING_SM, pady=(5, 0))
        row += 1

        self.btn_cambiar_estado = Button(
            frame_extras,
            text="🔄 Cambiar Estado",
            bootstyle="warning-outline")
        self.btn_cambiar_estado.pack(side=LEFT, padx=2, fill=X, expand=True)
        self.map_widgets['btn_cambiar_estado'] = self.btn_cambiar_estado

        self.btn_completar = Button(
            frame_extras,
            text="🎓 Completar",
            bootstyle="success")
        self.btn_completar.pack(side=LEFT, padx=2, fill=X, expand=True)
        self.map_widgets['btn_completar'] = self.btn_completar

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frame Inferior
    # └────────────────────────────────────────────────────────────┘
    def _frame_inferior(self, frame: Frame):
        self.lbl_estadisticas = Label(frame, text="", bootstyle="secondary", anchor=W, style="Small.TLabel")
        self.lbl_estadisticas.pack(side=TOP, fill=X, padx=PADDING_SM, pady=PADDING_SM)
        self.map_widgets['lbl_estadisticas'] = self.lbl_estadisticas

    # ┌────────────────────────────────────────────────────────────┐
    # │ Métodos auxiliares
    # └────────────────────────────────────────────────────────────┘
    def _toggle_principal(self):
        """Toggle del estado de carrera principal"""
        nuevo_valor = 0 if self.var_es_principal.get() == 1 else 1
        self.var_es_principal.set(nuevo_valor)
        
        # Actualizar apariencia del botón
        if nuevo_valor == 1:
            self.chk_es_principal.config(
                text="⭐ Es Carrera Principal",
                bootstyle="warning"
            )
        else:
            self.chk_es_principal.config(
                text="☆ No es Principal",
                bootstyle="warning-outline"
            )
