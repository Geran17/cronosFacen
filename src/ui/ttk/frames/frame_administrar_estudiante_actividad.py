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
)
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs import DatePickerDialog
from typing import Dict, Any
from scripts.logging_config import obtener_logger_modulo
from ui.ttk.styles.icons import ICON_ACTIVIDAD
from controladores.controlar_administrar_estudiante_actividad import (
    ControlarAdministrarEstudianteActividad,
)

logger = obtener_logger_modulo(__name__)


class FrameAdministrarEstudianteActividad(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        self.map_widgets: Dict[str, Any] = {}
        self.map_vars: Dict[str, Any] = {}

        # Variables
        self.var_id_estudiante = IntVar(value=0)
        self.map_vars['var_id_estudiante'] = self.var_id_estudiante

        self.var_nombre_estudiante = StringVar()
        self.map_vars['var_nombre_estudiante'] = self.var_nombre_estudiante

        self.var_id_actividad_seleccionada = IntVar(value=0)
        self.map_vars['var_id_actividad_seleccionada'] = self.var_id_actividad_seleccionada

        self.var_nombre_actividad_seleccionada = StringVar()
        self.map_vars['var_nombre_actividad_seleccionada'] = self.var_nombre_actividad_seleccionada

        self.var_estado = StringVar()
        self.map_vars['var_estado'] = self.var_estado

        self.var_fecha_entrega = StringVar()
        self.map_vars['var_fecha_entrega'] = self.var_fecha_entrega

        self.var_filtro_estado = StringVar(value="Todos")
        self.map_vars['var_filtro_estado'] = self.var_filtro_estado

        self.var_filtro_eje = StringVar(value="Todos")
        self.map_vars['var_filtro_eje'] = self.var_filtro_eje

        self.var_filtro_tipo = StringVar(value="Todos")
        self.map_vars['var_filtro_tipo'] = self.var_filtro_tipo

        # creamos los widgets
        self._crear_widgets()

        # Cargamos el controlador
        ControlarAdministrarEstudianteActividad(
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

        Separator(self, orient=HORIZONTAL).pack(fill=X, pady=5)

        frame_contenido = Frame(self, padding=(5, 5))
        self._frame_contenido(frame=frame_contenido)
        frame_contenido.pack(side=TOP, fill=BOTH, expand=TRUE, padx=1, pady=1)

        frame_inferior = Frame(self, padding=(5, 5))
        self._frame_inferior(frame=frame_inferior)
        frame_inferior.pack(side=BOTTOM, fill=X, padx=1, pady=1)

    def _frame_superior(self, frame: Frame):
        """Frame superior con título e ícono"""
        lbl_icono = Label(frame, text=ICON_ACTIVIDAD, font=("Segoe UI Emoji", 24))
        lbl_icono.pack(side=LEFT, padx=(0, 10))

        frame_texto = Frame(frame)
        frame_texto.pack(side=LEFT, fill=BOTH, expand=TRUE)

        lbl_titulo = Label(
            frame_texto,
            text="Administrar Actividades por Estudiante",
            font=("Segoe UI", 14, "bold"),
        )
        lbl_titulo.pack(anchor=W)

        lbl_subtitulo = Label(
            frame_texto,
            text="Gestiona el estado de entrega de actividades para cada estudiante",
            font=("Segoe UI", 9),
            bootstyle="secondary",
        )
        lbl_subtitulo.pack(anchor=W)

    def _frame_selector_estudiante(self, frame: Frame):
        """Frame para seleccionar estudiante"""
        lf_selector = Labelframe(
            frame,
            text="📚 Seleccionar Estudiante",
            padding=10,
        )
        lf_selector.pack(fill=X, pady=5)

        frame_row = Frame(lf_selector)
        frame_row.pack(fill=X)

        # Label
        lbl_estudiante = Label(frame_row, text="Estudiante:", width=15, anchor=W)
        lbl_estudiante.pack(side=LEFT, padx=(0, 5))

        # Combobox
        self.cbx_estudiante = Combobox(
            frame_row,
            textvariable=self.var_nombre_estudiante,
            state=READONLY,
        )
        self.cbx_estudiante.pack(side=LEFT, fill=X, expand=TRUE, padx=(0, 10))
        self.map_widgets['cbx_estudiante'] = self.cbx_estudiante
        ToolTip(self.cbx_estudiante, "Selecciona un estudiante")

        # Botón cargar
        self.btn_cargar_estudiante = Button(
            frame_row,
            text="Cargar",
            bootstyle="primary",
            width=12,
        )
        self.btn_cargar_estudiante.pack(side=LEFT)
        self.map_widgets['btn_cargar_estudiante'] = self.btn_cargar_estudiante
        ToolTip(self.btn_cargar_estudiante, "Cargar actividades del estudiante")

    def _frame_contenido(self, frame: Frame):
        """Frame principal de contenido con tabla y formulario"""
        # Frame izquierdo: Tabla
        frame_izquierdo = Frame(frame)
        frame_izquierdo.pack(side=LEFT, fill=BOTH, expand=TRUE, padx=(0, 5))

        self._frame_tabla(frame=frame_izquierdo)

        # Frame derecho: Formulario
        frame_derecho = Frame(frame, width=350)
        frame_derecho.pack(side=RIGHT, fill=BOTH, padx=(5, 0))
        frame_derecho.pack_propagate(False)

        self._frame_formulario(frame=frame_derecho)

    def _frame_tabla(self, frame: Frame):
        """Frame con filtros y tabla de actividades"""
        lf_tabla = Labelframe(
            frame,
            text="📋 Actividades del Estudiante",
            padding=10,
        )
        lf_tabla.pack(fill=BOTH, expand=TRUE)

        # Filtros
        frame_filtros = Frame(lf_tabla)
        frame_filtros.pack(fill=X, pady=(0, 10))

        # Búsqueda
        lbl_buscar = Label(frame_filtros, text="Buscar:", anchor=W)
        lbl_buscar.pack(side=LEFT, padx=(0, 5))

        self.entry_buscar_actividad = Entry(frame_filtros, width=30)
        self.entry_buscar_actividad.pack(side=LEFT, padx=(0, 15))
        self.map_widgets['entry_buscar_actividad'] = self.entry_buscar_actividad
        ToolTip(self.entry_buscar_actividad, "Buscar por título o asignatura")

        # Filtro por estado
        lbl_estado = Label(frame_filtros, text="Estado:", anchor=W)
        lbl_estado.pack(side=LEFT, padx=(0, 5))

        self.cbx_filtro_estado = Combobox(
            frame_filtros,
            textvariable=self.var_filtro_estado,
            values=["Todos", "⏳ Pendiente", "🔄 En progreso", "✅ Entregada", "❌ Vencida"],
            state=READONLY,
            width=15,
        )
        self.cbx_filtro_estado.pack(side=LEFT, padx=(0, 15))
        self.map_widgets['cbx_filtro_estado'] = self.cbx_filtro_estado
        ToolTip(self.cbx_filtro_estado, "Filtrar actividades por estado")

        # Filtro por tipo de actividad
        lbl_tipo = Label(frame_filtros, text="Tipo:", anchor=W)
        lbl_tipo.pack(side=LEFT, padx=(0, 5))

        self.cbx_filtro_tipo = Combobox(
            frame_filtros,
            textvariable=self.var_filtro_tipo,
            state=READONLY,
            width=20,
        )
        self.cbx_filtro_tipo.pack(side=LEFT)
        self.map_widgets['cbx_filtro_tipo'] = self.cbx_filtro_tipo
        ToolTip(self.cbx_filtro_tipo, "Filtrar por tipo de actividad")

        # Tabla
        columnas = [
            {"text": "Título", "stretch": True, "width": 200},
            {"text": "Asignatura", "stretch": False, "width": 130},
            {"text": "Tipo", "stretch": False, "width": 50},
            {"text": "F. Inicio", "stretch": False, "width": 80},
            {"text": "F. Fin", "stretch": False, "width": 80},
            {"text": "Días", "stretch": False, "width": 50},
            {"text": "Estado", "stretch": False, "width": 110},
            {"text": "F. Entrega", "stretch": False, "width": 90},
        ]

        self.tabla_actividades = Tableview(
            lf_tabla,
            coldata=columnas,
            searchable=False,
            autofit=True,
            paginated=False,
            height=15,
        )
        self.tabla_actividades.pack(fill=BOTH, expand=TRUE)
        self.map_widgets['tabla_actividades'] = self.tabla_actividades

        # Resumen estadístico
        frame_resumen = Frame(lf_tabla)
        frame_resumen.pack(fill=X, pady=(10, 0))

        self.lbl_total_actividades = Label(
            frame_resumen, text="Total Actividades: 0", bootstyle="info"
        )
        self.lbl_total_actividades.pack(side=LEFT, padx=5)
        self.map_widgets['lbl_total_actividades'] = self.lbl_total_actividades

        self.lbl_pendientes = Label(frame_resumen, text="⏳ Pendientes: 0")
        self.lbl_pendientes.pack(side=LEFT, padx=5)
        self.map_widgets['lbl_pendientes'] = self.lbl_pendientes

        self.lbl_en_progreso = Label(frame_resumen, text="🔄 En progreso: 0")
        self.lbl_en_progreso.pack(side=LEFT, padx=5)
        self.map_widgets['lbl_en_progreso'] = self.lbl_en_progreso

        self.lbl_entregadas = Label(frame_resumen, text="✅ Entregadas: 0")
        self.lbl_entregadas.pack(side=LEFT, padx=5)
        self.map_widgets['lbl_entregadas'] = self.lbl_entregadas

        self.lbl_vencidas = Label(frame_resumen, text="❌ Vencidas: 0")
        self.lbl_vencidas.pack(side=LEFT, padx=5)
        self.map_widgets['lbl_vencidas'] = self.lbl_vencidas

    def _frame_formulario(self, frame: Frame):
        """Frame para actualizar estado y fecha de entrega"""
        lf_form = Labelframe(
            frame,
            text="✏️ Actualizar Estado y Entrega",
            padding=10,
        )
        lf_form.pack(fill=BOTH, expand=TRUE)

        # Actividad seleccionada (readonly)
        lbl_actividad = Label(lf_form, text="Actividad seleccionada:", anchor=W)
        lbl_actividad.pack(fill=X, pady=(0, 3))

        entry_actividad = Entry(
            lf_form,
            textvariable=self.var_nombre_actividad_seleccionada,
            state=READONLY,
        )
        entry_actividad.pack(fill=X, pady=(0, 10))
        self.map_widgets['entry_actividad_seleccionada'] = entry_actividad

        # Estado
        lbl_estado = Label(lf_form, text="Estado:", anchor=W)
        lbl_estado.pack(fill=X, pady=(0, 3))

        self.cbx_estado = Combobox(
            lf_form,
            textvariable=self.var_estado,
            values=["⏳ Pendiente", "🔄 En progreso", "✅ Entregada", "❌ Vencida"],
            state=READONLY,
        )
        self.cbx_estado.pack(fill=X, pady=(0, 10))
        self.map_widgets['cbx_estado'] = self.cbx_estado
        ToolTip(self.cbx_estado, "Selecciona el estado de la actividad")

        # Fecha de entrega
        lbl_fecha = Label(lf_form, text="Fecha de entrega:", anchor=W)
        lbl_fecha.pack(fill=X, pady=(0, 3))

        frame_fecha = Frame(lf_form)
        frame_fecha.pack(fill=X, pady=(0, 10))

        self.entry_fecha_entrega = Entry(
            frame_fecha,
            textvariable=self.var_fecha_entrega,
        )
        self.entry_fecha_entrega.pack(side=LEFT, fill=X, expand=TRUE, padx=(0, 5))
        self.map_widgets['entry_fecha_entrega'] = self.entry_fecha_entrega
        ToolTip(self.entry_fecha_entrega, "Formato: YYYY-MM-DD")

        self.btn_calendario = Button(
            frame_fecha,
            text="📅",
            width=4,
        )
        self.btn_calendario.pack(side=LEFT)
        self.map_widgets['btn_calendario'] = self.btn_calendario
        ToolTip(self.btn_calendario, "Abrir calendario")

        Separator(lf_form, orient=HORIZONTAL).pack(fill=X, pady=10)

        # Botones
        frame_botones = Frame(lf_form)
        frame_botones.pack(fill=X)

        self.btn_aplicar = Button(
            frame_botones,
            text="💾 Aplicar",
            bootstyle="success",
        )
        self.btn_aplicar.pack(side=LEFT, fill=X, expand=TRUE, padx=(0, 5))
        self.map_widgets['btn_aplicar'] = self.btn_aplicar
        ToolTip(self.btn_aplicar, "Guardar cambios")

        self.btn_limpiar = Button(
            frame_botones,
            text="🧹 Limpiar",
            bootstyle="secondary",
        )
        self.btn_limpiar.pack(side=LEFT, fill=X, expand=TRUE)
        self.map_widgets['btn_limpiar'] = self.btn_limpiar
        ToolTip(self.btn_limpiar, "Limpiar formulario")

    def _frame_inferior(self, frame: Frame):
        """Frame inferior con información de estado"""
        self.lbl_estadisticas = Label(
            frame,
            text="Seleccione un estudiante para comenzar",
            bootstyle="secondary",
            anchor=W,
        )
        self.lbl_estadisticas.pack(fill=X)
        self.map_widgets['lbl_estadisticas'] = self.lbl_estadisticas
