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
    Style,
    Panedwindow,
)
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs import DatePickerDialog
from typing import Dict, Any
from scripts.logging_config import obtener_logger_modulo
from ui.ttk.styles.icons import ICON_ACTIVIDAD
from ui.ttk.styles.estilos import PADDING_MD, PADDING_SM, FONT_SMALL
from controladores.controlar_administrar_estudiante_actividad import (
    ControlarAdministrarEstudianteActividad,
)

logger = obtener_logger_modulo(__name__)


class FrameAdministrarEstudianteActividad(Frame):
    def __init__(self, master=None, preselect=None, **kwargs):
        super().__init__(master=master, **kwargs)

        self.preselect = preselect or {}

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

        self.var_nota = StringVar(value="0")
        self.map_vars['var_nota'] = self.var_nota

        self.var_filtro_estado = StringVar(value="Todos")
        self.map_vars['var_filtro_estado'] = self.var_filtro_estado

        self.var_filtro_eje = StringVar(value="Todos")
        self.map_vars['var_filtro_eje'] = self.var_filtro_eje

        self.var_filtro_tipo = StringVar(value="Todos")
        self.map_vars['var_filtro_tipo'] = self.var_filtro_tipo

        self.var_filtro_asignatura = StringVar(value="Todos")
        self.map_vars['var_filtro_asignatura'] = self.var_filtro_asignatura

        # creamos los widgets
        self._crear_widgets()

        # Cargamos el controlador
        ControlarAdministrarEstudianteActividad(
            master=self,
            map_vars=self.map_vars,
            map_widgets=self.map_widgets,
            preselect=self.preselect,
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

        Separator(self, orient=HORIZONTAL).pack(fill=X, pady=PADDING_SM)

        frame_contenido = Frame(self, padding=(5, 5))
        self._frame_contenido(frame=frame_contenido)
        frame_contenido.pack(side=TOP, fill=BOTH, expand=TRUE, padx=PADDING_SM, pady=PADDING_SM)

        frame_inferior = Frame(self, padding=(5, 5))
        self._frame_inferior(frame=frame_inferior)
        frame_inferior.pack(side=BOTTOM, fill=X, padx=PADDING_SM, pady=PADDING_SM)

    def _frame_superior(self, frame: Frame):
        """Frame superior con título e ícono"""
        lbl_icono = Label(frame, text=ICON_ACTIVIDAD, font=("Segoe UI Emoji", 24))
        lbl_icono.pack(side=LEFT, padx=(0, 10))

        frame_texto = Frame(frame)
        frame_texto.pack(side=LEFT, fill=BOTH, expand=TRUE)

        lbl_titulo = Label(
            frame_texto,
            text="Administrar Actividades por Estudiante",
            style="Title.TLabel",
        )
        lbl_titulo.pack(anchor=W)

        lbl_subtitulo = Label(
            frame_texto,
            text="Gestiona el estado de entrega de actividades para cada estudiante",
            style="Subtitle.TLabel",
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
        lf_selector.pack(fill=X, pady=PADDING_SM)

        frame_row = Frame(lf_selector)
        frame_row.pack(fill=X)
        frame_row.columnconfigure(1, weight=1)

        # Label
        lbl_estudiante = Label(frame_row, text="Estudiante:", anchor=W)
        lbl_estudiante.grid(row=0, column=0, sticky=W, padx=PADDING_SM, pady=PADDING_SM)

        # Combobox
        self.cbx_estudiante = Combobox(
            frame_row,
            textvariable=self.var_nombre_estudiante,
            state=READONLY,
        )
        self.cbx_estudiante.grid(row=0, column=1, sticky=EW, padx=PADDING_SM, pady=PADDING_SM)
        self.map_widgets['cbx_estudiante'] = self.cbx_estudiante
        ToolTip(self.cbx_estudiante, "Selecciona un estudiante")

        # Botón cargar
        self.btn_cargar_estudiante = Button(
            frame_row,
            text="Cargar",
            bootstyle="primary")
        self.btn_cargar_estudiante.grid(
            row=0, column=2, sticky=E, padx=PADDING_SM, pady=PADDING_SM
        )
        self.map_widgets['btn_cargar_estudiante'] = self.btn_cargar_estudiante
        ToolTip(self.btn_cargar_estudiante, "Cargar actividades del estudiante")

    def _frame_contenido(self, frame: Frame):
        """Frame principal de contenido con tabla y formulario"""
        # Separador ajustable entre tabla y formulario
        paned = Panedwindow(frame, orient=HORIZONTAL)
        paned.pack(fill=BOTH, expand=TRUE)

        frame_izquierdo = Frame(paned)
        self._frame_tabla(frame=frame_izquierdo)
        paned.add(frame_izquierdo, weight=3)

        frame_derecho = Frame(paned, width=360)
        frame_derecho.pack_propagate(False)
        self._frame_formulario(frame=frame_derecho)
        paned.add(frame_derecho, weight=1)

    def _frame_tabla(self, frame: Frame):
        """Frame con filtros y tabla de actividades"""
        lf_tabla = Labelframe(
            frame,
            text="📋 Actividades del Estudiante",
            padding=8,
        )
        lf_tabla.pack(fill=BOTH, expand=TRUE)

        # Filtros
        frame_filtros = Frame(lf_tabla)
        frame_filtros.pack(fill=X, pady=(0, PADDING_SM))
        frame_filtros.columnconfigure(1, weight=2)
        frame_filtros.columnconfigure(3, weight=1)
        frame_filtros.columnconfigure(5, weight=1)

        # Búsqueda
        lbl_buscar = Label(
            frame_filtros,
            text="🔎 Buscar por título:",
            anchor=W,
            style="FormLabel.TLabel",
        )
        lbl_buscar.grid(row=0, column=0, sticky=W, padx=PADDING_SM, pady=(PADDING_SM, 2))

        self.entry_buscar_actividad = Entry(frame_filtros)
        self.entry_buscar_actividad.grid(
            row=0, column=1, columnspan=3, sticky=EW, padx=PADDING_SM, pady=(PADDING_SM, 2)
        )
        self.map_widgets['entry_buscar_actividad'] = self.entry_buscar_actividad
        ToolTip(self.entry_buscar_actividad, "Busca por título de la actividad en tiempo real")

        # Botón para limpiar filtros
        self.btn_limpiar_filtros = Button(
            frame_filtros,
            text="🔄 Limpiar",
            bootstyle="secondary-outline")
        self.btn_limpiar_filtros.grid(row=0, column=4, sticky=E, padx=PADDING_SM, pady=(PADDING_SM, 2))
        self.map_widgets['btn_limpiar_filtros'] = self.btn_limpiar_filtros
        ToolTip(self.btn_limpiar_filtros, "Limpiar todos los filtros")

        # Filtro por asignatura
        lbl_asignatura = Label(
            frame_filtros,
            text="Asignatura:",
            anchor=W,
            style="FormLabel.TLabel",
        )
        lbl_asignatura.grid(row=1, column=0, sticky=W, padx=PADDING_SM, pady=(2, PADDING_SM))

        self.cbx_filtro_asignatura = Combobox(
            frame_filtros,
            textvariable=self.var_filtro_asignatura,
            state=READONLY,
        )
        self.cbx_filtro_asignatura.grid(
            row=1, column=1, sticky=EW, padx=PADDING_SM, pady=(2, PADDING_SM)
        )
        self.map_widgets['cbx_filtro_asignatura'] = self.cbx_filtro_asignatura
        ToolTip(self.cbx_filtro_asignatura, "Filtrar actividades por asignatura")

        # Filtro por estado
        lbl_estado = Label(
            frame_filtros,
            text="Estado:",
            anchor=W,
            style="FormLabel.TLabel",
        )
        lbl_estado.grid(row=1, column=2, sticky=W, padx=PADDING_SM, pady=(2, PADDING_SM))

        self.cbx_filtro_estado = Combobox(
            frame_filtros,
            textvariable=self.var_filtro_estado,
            values=["Todos", "⏳ Pendiente", "🔄 En progreso", "✅ Entregada", "❌ Vencida"],
            state=READONLY,
        )
        self.cbx_filtro_estado.grid(
            row=1, column=3, sticky=EW, padx=PADDING_SM, pady=(2, PADDING_SM)
        )
        self.map_widgets['cbx_filtro_estado'] = self.cbx_filtro_estado
        ToolTip(self.cbx_filtro_estado, "Filtrar actividades por estado")

        # Filtro por tipo de actividad
        lbl_tipo = Label(
            frame_filtros,
            text="Tipo:",
            anchor=W,
            style="FormLabel.TLabel",
        )
        lbl_tipo.grid(row=1, column=4, sticky=W, padx=PADDING_SM, pady=(2, PADDING_SM))

        self.cbx_filtro_tipo = Combobox(
            frame_filtros,
            textvariable=self.var_filtro_tipo,
            state=READONLY,
        )
        self.cbx_filtro_tipo.grid(
            row=1, column=5, sticky=EW, padx=PADDING_SM, pady=(2, PADDING_SM)
        )
        self.map_widgets['cbx_filtro_tipo'] = self.cbx_filtro_tipo
        ToolTip(self.cbx_filtro_tipo, "Filtrar por tipo de actividad")

        # Tabla
        columnas = [
            {"text": "ID", "stretch": False, "anchor": "center", "width": 0},
            {"text": "Título", "stretch": True, "anchor": "w", "minwidth": 200},
            {"text": "Asignatura", "stretch": False, "anchor": "w", "width": 130},
            {"text": "Tipo", "stretch": False, "anchor": "center", "width": 70},
            {"text": "F. Inicio", "stretch": False, "anchor": "center", "width": 90},
            {"text": "F. Fin", "stretch": False, "anchor": "center", "width": 90},
            {"text": "Días", "stretch": False, "anchor": "center", "width": 50},
            {"text": "Estado", "stretch": False, "anchor": "center", "width": 110},
            {"text": "Nota", "stretch": False, "anchor": "center", "width": 70},
            {"text": "F. Entrega", "stretch": False, "anchor": "center", "width": 100},
        ]

        self.tabla_actividades = Tableview(
            lf_tabla,
            coldata=columnas,
            searchable=False,
            autofit=True,
            paginated=False,
            height=15,
        )
        style = Style()
        style.configure("Actividad.Treeview", rowheight=24, font=FONT_SMALL)
        self.tabla_actividades.view.configure(style="Actividad.Treeview")
        # Ocultar columna ID (solo para lógica interna)
        try:
            self.tabla_actividades.view.column("#1", width=0, stretch=False)
        except Exception:
            pass
        self.tabla_actividades.pack(fill=BOTH, expand=TRUE)
        self.map_widgets['tabla_actividades'] = self.tabla_actividades

        # Resumen estadístico
        frame_resumen = Frame(lf_tabla)
        frame_resumen.pack(fill=X, pady=(8, 0))
        frame_resumen.columnconfigure(0, weight=1)
        frame_resumen.columnconfigure(1, weight=1)
        frame_resumen.columnconfigure(2, weight=1)
        frame_resumen.columnconfigure(3, weight=1)
        frame_resumen.columnconfigure(4, weight=1)

        self.lbl_total_actividades = Label(
            frame_resumen, text="Total: 0", bootstyle="info"
        )
        self.lbl_total_actividades.grid(row=0, column=0, sticky=W, padx=PADDING_SM)
        self.map_widgets['lbl_total_actividades'] = self.lbl_total_actividades

        self.lbl_pendientes = Label(frame_resumen, text="⏳ Pend: 0")
        self.lbl_pendientes.grid(row=0, column=1, sticky=W, padx=PADDING_SM)
        self.map_widgets['lbl_pendientes'] = self.lbl_pendientes

        self.lbl_en_progreso = Label(frame_resumen, text="🔄 Prog: 0")
        self.lbl_en_progreso.grid(row=0, column=2, sticky=W, padx=PADDING_SM)
        self.map_widgets['lbl_en_progreso'] = self.lbl_en_progreso

        self.lbl_entregadas = Label(frame_resumen, text="✅ Ent: 0")
        self.lbl_entregadas.grid(row=0, column=3, sticky=W, padx=PADDING_SM)
        self.map_widgets['lbl_entregadas'] = self.lbl_entregadas

        self.lbl_vencidas = Label(frame_resumen, text="❌ Venc: 0")
        self.lbl_vencidas.grid(row=0, column=4, sticky=W, padx=PADDING_SM)
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
            bootstyle="info-outline",
        )
        self.btn_calendario.pack(side=LEFT)
        self.map_widgets['btn_calendario'] = self.btn_calendario
        ToolTip(self.btn_calendario, "Abrir calendario")

        # Nota (opcional)
        lbl_nota = Label(lf_form, text="Nota (opcional):", anchor=W)
        lbl_nota.pack(fill=X, pady=(0, 3))

        entry_nota = Entry(
            lf_form,
            textvariable=self.var_nota,
        )
        entry_nota.pack(fill=X, pady=(0, 10))
        self.map_widgets['entry_nota'] = entry_nota
        ToolTip(entry_nota, "Ingrese la nota obtenida (0 por defecto)")

        Separator(lf_form, orient=HORIZONTAL).pack(fill=X, pady=PADDING_MD)

        # Botones
        frame_botones = Frame(lf_form)
        frame_botones.pack(fill=X)

        self.btn_aplicar = Button(
            frame_botones,
            text="💾 Aplicar",
            bootstyle="success")
        self.btn_aplicar.pack(side=LEFT, fill=X, expand=TRUE, padx=(0, 5))
        self.map_widgets['btn_aplicar'] = self.btn_aplicar
        ToolTip(self.btn_aplicar, "Guardar cambios")

        self.btn_limpiar = Button(
            frame_botones,
            text="🧹 Limpiar",
            bootstyle="secondary-outline",
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
            style="Small.TLabel",
        )
        self.lbl_estadisticas.pack(fill=X, padx=PADDING_SM, pady=PADDING_SM)
        self.map_widgets['lbl_estadisticas'] = self.lbl_estadisticas
