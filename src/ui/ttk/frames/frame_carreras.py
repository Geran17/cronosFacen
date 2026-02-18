from ttkbootstrap import (
    Frame,
    Label,
    StringVar,
    Separator,
    Combobox,
    Button,
    Treeview,
)
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.tooltip import ToolTip
from typing import Dict, Any
from ui.ttk.styles.estilos import PADDING_SM, PADDING_MD, PADDING_XS
from ui.ttk.styles.icons import *
from controladores.controlador_carreras import ControladorCarreras


class FrameCarreras(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        # Variables
        self.var_carrera = StringVar()
        self.var_estudiante = StringVar()
        self.var_vista = StringVar(value="Lista")

        self.map_vars: Dict[str, Any] = {
            'var_carrera': self.var_carrera,
            'var_estudiante': self.var_estudiante,
            'var_vista': self.var_vista,
        }

        self.map_widgets: Dict[str, Any] = {}
        self._asignaturas_cache: Dict[int, list] = {}

        # Crear widgets
        self._crear_widgets()

        # Agregar referencia a este frame en el mapa
        self.map_widgets['frame_carreras'] = self

        # Conectar con el controlador
        self.controlador = ControladorCarreras(map_widgets=self.map_widgets, map_vars=self.map_vars)

        # Cargar asignaturas cuando se selecciona una carrera (al iniciar, cargará automáticamente)
        self.controlador._on_change_carrera()

    def _crear_widgets(self):
        """Crea la estructura principal de widgets"""
        frame_superior = Frame(self, padding=(PADDING_XS, PADDING_XS))
        self._frame_superior(frame=frame_superior)
        frame_superior.pack(side=TOP, fill=X, padx=PADDING_XS, pady=PADDING_SM)

        frame_central = Frame(self, padding=(PADDING_XS, PADDING_XS))
        self._frame_central(frame=frame_central)
        frame_central.pack(side=TOP, fill=BOTH, padx=PADDING_XS, pady=PADDING_XS, expand=TRUE)

        frame_inferior = Frame(self, padding=(PADDING_XS, PADDING_XS))
        self._frame_inferior(frame=frame_inferior)
        frame_inferior.pack(side=TOP, fill=X, padx=PADDING_XS, pady=PADDING_XS)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frames Principales
    # └────────────────────────────────────────────────────────────┘

    def _frame_superior(self, frame: Frame):
        """Frame superior con título y subtítulo"""
        frame_titulo = Frame(frame, padding=(PADDING_XS, PADDING_XS))
        frame_titulo.pack(side=TOP, padx=1, pady=1, fill=X)

        lbl_titulo = Label(
            frame_titulo,
            text="🎓 Carreras",
            style="Title.TLabel",
            bootstyle=INFO,
        )
        lbl_titulo.pack(side=TOP, fill=X, padx=1, pady=PADDING_MD)

        lbl_subtitulo = Label(
            frame_titulo,
            text="Gestiona y visualiza las carreras académicas",
            bootstyle=SECONDARY,
            style="Subtitle.TLabel",
        )
        lbl_subtitulo.pack(side=TOP, fill=X, padx=1, pady=PADDING_SM)

        Separator(frame).pack(side=TOP, fill=X, padx=1, pady=1)

    def _frame_central(self, frame: Frame):
        """Frame central con filtros y contenido principal"""
        frame_filtrado_wrap = Frame(frame, padding=(PADDING_XS, PADDING_XS))
        frame_filtrado_wrap.pack(
            side=TOP,
            fill=X,
            padx=1,
            pady=1,
            ipadx=PADDING_XS,
            ipady=PADDING_XS,
        )
        Label(
            frame_filtrado_wrap,
            text="Filtros",
            style="FormLabel.TLabel",
            bootstyle="info",
        ).pack(side=TOP, anchor=W, padx=PADDING_XS, pady=(0, PADDING_XS))
        Separator(frame_filtrado_wrap).pack(side=TOP, fill=X, pady=(0, PADDING_XS))

        frame_filtrado = Frame(frame_filtrado_wrap)
        frame_filtrado.pack(side=TOP, fill=X)
        self._frame_filtrado(frame=frame_filtrado)

        Separator(frame).pack(side=TOP, fill=X, padx=1, pady=1)

        scrolled_frame = ScrolledFrame(frame, padding=(PADDING_XS, PADDING_XS))
        scrolled_frame.pack(side=TOP, fill=BOTH, padx=PADDING_XS, pady=PADDING_XS, expand=TRUE)
        self.map_widgets['scrolled_frame'] = scrolled_frame

    def _frame_inferior(self, frame: Frame):
        """Frame inferior con botón de refrescar"""
        btn_refrescar = Button(frame, text="🔄 Refrescar", bootstyle=WARNING)
        btn_refrescar.pack(side=LEFT, padx=PADDING_XS, pady=PADDING_XS)
        self.map_widgets['btn_refrescar'] = btn_refrescar

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frames Funcionales
    # └────────────────────────────────────────────────────────────┘

    def _frame_filtrado(self, frame: Frame):
        """Frame para filtros de estudiantes y carreras"""
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)

        # Label y Combobox para Estudiantes
        lbl_estudiante = Label(frame, text="Estudiante:", style="FormLabel.TLabel")
        lbl_estudiante.grid(row=0, column=0, padx=PADDING_XS, pady=PADDING_XS, sticky=W)

        cbx_estudiante = Combobox(frame, textvariable=self.var_estudiante, state=READONLY)
        cbx_estudiante.grid(row=1, column=0, padx=PADDING_XS, pady=PADDING_XS, sticky=EW)
        self.map_widgets['cbx_estudiante'] = cbx_estudiante
        ToolTip(
            cbx_estudiante,
            text="Seleccione un estudiante para ver sus carreras asociadas",
        )

        # Label y Combobox para Carreras
        lbl_carrera = Label(frame, text="Carrera:", style="FormLabel.TLabel")
        lbl_carrera.grid(row=0, column=1, padx=PADDING_XS, pady=PADDING_XS, sticky=W)

        cbx_carrera = Combobox(frame, textvariable=self.var_carrera, state=READONLY)
        cbx_carrera.grid(row=1, column=1, padx=PADDING_XS, pady=PADDING_XS, sticky=EW)
        self.map_widgets['cbx_carrera'] = cbx_carrera
        ToolTip(
            cbx_carrera,
            text="Muestra la carrera asociada al estudiante seleccionado",
        )

        # Label y Combobox para tipo de vista
        lbl_vista = Label(frame, text="Vista:", style="FormLabel.TLabel")
        lbl_vista.grid(row=0, column=2, padx=PADDING_XS, pady=PADDING_XS, sticky=W)

        cbx_vista = Combobox(
            frame,
            textvariable=self.var_vista,
            state=READONLY,
            values=("Lista", "Cuadricula"),
        )
        cbx_vista.grid(row=1, column=2, padx=PADDING_XS, pady=PADDING_XS, sticky=EW)
        self.map_widgets['cbx_vista'] = cbx_vista
        cbx_vista.bind('<<ComboboxSelected>>', self._on_change_vista)
        ToolTip(
            cbx_vista,
            text="Cambiar entre vista en lista o cuadricula para las asignaturas",
        )

    # ┌────────────────────────────────────────────────────────────┐
    # │ Métodos para Crear Tarjetas
    # └────────────────────────────────────────────────────────────┘

    def _build_text_progress_bar(self, pct: float, width: int = 30) -> str:
        """Construye una barra textual tipo ███░░░."""
        if width <= 0:
            return ""
        clamped = max(0.0, min(100.0, float(pct)))
        filled = int((clamped / 100.0) * width + 0.5)
        if clamped > 0:
            filled = max(1, filled)
        filled = min(width, filled)
        return f"{'█' * filled}{'░' * (width - filled)}"

    def _format_text_progress(self, pct: float) -> str:
        clamped = max(0.0, min(100.0, float(pct)))
        check = " ✔" if clamped >= 100.0 else ""
        return f"[{self._build_text_progress_bar(clamped)}] {clamped:.0f}%{check}"

    def _progress_bootstyle(self, pct: float) -> str:
        value = max(0.0, min(100.0, float(pct)))
        if value >= 100.0:
            return "success"
        if value >= 70.0:
            return "info"
        if value >= 40.0:
            return "warning"
        return "danger"

    def _obtener_modo_vista(self) -> str:
        """Retorna el modo de vista normalizado: 'list' o 'grid'."""
        return "list" if self.var_vista.get() == "Lista" else "grid"

    def _on_change_vista(self, _event=None) -> None:
        """Re-renderiza asignaturas con el modo seleccionado."""
        if self._asignaturas_cache:
            self._render_asignaturas(self._asignaturas_cache)

    def crear_semestre_con_asignaturas(
        self,
        numero_semestre: int,
        porcentaje: float,
        asignaturas: list,
        modo_vista: str = "",
    ):
        """Crea una sección con semestre (arriba) y asignaturas debajo.

        Args:
            numero_semestre (int): Número del semestre
            porcentaje (float): Porcentaje de progreso
            asignaturas (list): Lista de diccionarios con datos de asignaturas
            modo_vista (str): 'list' o 'grid'
        """
        try:
            scrolled_frame = self.map_widgets.get('scrolled_frame')
            if not scrolled_frame:
                return
            vista = modo_vista or self._obtener_modo_vista()

            # Frame contenedor para la sección del semestre
            section_frame = Frame(scrolled_frame)
            section_frame.pack(fill=BOTH, padx=PADDING_XS, pady=PADDING_SM, expand=TRUE)

            # -------- ARRIBA: TARJETA DE SEMESTRE --------
            self._crear_tarjeta_semestre_header(section_frame, numero_semestre, porcentaje)

            # -------- ABAJO: ASIGNATURAS --------
            self._crear_asignaturas_container(section_frame, asignaturas, vista)

        except Exception as e:
            from scripts.logging_config import obtener_logger_modulo

            logger = obtener_logger_modulo(__name__)
            logger.error(f"Error al crear semestre con asignaturas: {e}", exc_info=True)

    def _crear_tarjeta_semestre_header(
        self, parent: Frame, numero_semestre: int, porcentaje: float
    ):
        """Crea la tarjeta de semestre como encabezado.

        Args:
            parent (Frame): Frame padre
            numero_semestre (int): Número del semestre
            porcentaje (float): Porcentaje de progreso
        """
        # Frame de la tarjeta de semestre
        card_frame = Frame(parent)
        card_frame.pack(fill=X, pady=4)

        # Contenedor del encabezado
        sem_box = Frame(card_frame, padding=6)
        sem_box.pack(fill=X, expand=FALSE)

        Label(
            sem_box,
            text=f"📚 Semestre {numero_semestre}",
            style="FormLabel.TLabel",
            bootstyle="info",
        ).pack(side=TOP, anchor=W, pady=(0, 3))
        Separator(sem_box).pack(side=TOP, fill=X, pady=(0, 3))

        # Frame interno para contenido
        content = Frame(sem_box)
        content.pack(fill=X)

        # Número de semestre (grande)
        lbl_numero = Label(
            content,
            text=f"Semestre {numero_semestre}",
            style="Section.TLabel",
            bootstyle="info",
        )
        lbl_numero.pack(side=LEFT, padx=10, pady=4)

        # Porcentaje con barra de progreso
        progress_frame = Frame(content)
        progress_frame.pack(side=LEFT, fill=BOTH, expand=TRUE, padx=10, pady=4)

        # Label de porcentaje
        lbl_porcentaje = Label(
            progress_frame,
            text=f"Progreso: {self._format_text_progress(porcentaje)}",
            bootstyle=self._progress_bootstyle(porcentaje),
            font=("DejaVu Sans Mono", 9),
        )
        lbl_porcentaje.pack(side=TOP, pady=1)

    def _crear_asignaturas_container(self, parent: Frame, asignaturas: list, modo_vista: str):
        """Crea el contenedor con las tarjetas de asignaturas en lista o grilla.

        Args:
            parent (Frame): Frame padre
            asignaturas (list): Lista de diccionarios con datos de asignaturas
            modo_vista (str): 'list' o 'grid'
        """
        # Frame contenedor para asignaturas
        asig_container = Frame(parent)
        asig_container.pack(fill=BOTH, expand=TRUE, padx=2, pady=4)

        if modo_vista == "list":
            for asignatura in asignaturas:
                self._crear_tarjeta_asignatura(
                    asig_container,
                    asignatura,
                    modo_vista="list",
                )
            return

        # Frame para la grilla
        grid_frame = Frame(asig_container)
        grid_frame.pack(fill=BOTH, expand=TRUE, padx=2, pady=2)

        # Configurar columnas (5 asignaturas por fila)
        num_columnas = 6
        for col in range(num_columnas):
            grid_frame.columnconfigure(col, weight=1)

        # Crear tarjetas en grilla
        for idx, asignatura in enumerate(asignaturas):
            row = idx // num_columnas
            col = idx % num_columnas
            self._crear_tarjeta_asignatura(
                grid_frame,
                asignatura,
                row=row,
                col=col,
                modo_vista="grid",
            )

    def _crear_tarjeta_asignatura(
        self,
        parent: Frame,
        asignatura: Dict[str, Any],
        row: int = 0,
        col: int = 0,
        modo_vista: str = "grid",
    ):
        """Crea una tarjeta individual de asignatura.

        Args:
            parent (Frame): Frame padre
            asignatura (Dict): Diccionario con los datos de la asignatura
            row (int): Fila en la grilla
            col (int): Columna en la grilla
            modo_vista (str): 'list' o 'grid'
        """
        try:
            nombre = asignatura.get('nombre', 'Sin nombre')
            ejes_tematicos = asignatura.get('ejes_tematicos', 0)
            actividades = asignatura.get('actividades', 0)
            nota = asignatura.get('nota', 0.0)
            prerequisitos = asignatura.get('prerequisitos', '-')
            estado = asignatura.get('estado', 'pendiente')
            progreso_actividades = asignatura.get('progreso_actividades', 0.0)
            progreso_prerequisitos = asignatura.get('progreso_prerequisitos', 0.0)
            prerequisitos_completados = asignatura.get('prerequisitos_completados', 0)
            prerequisitos_totales = asignatura.get('prerequisitos_totales', 0)

            # Log para debug de Probabilidad y Estadística
            if 'Probabilidad' in nombre:
                from scripts.logging_config import obtener_logger_modulo

                logger_debug = obtener_logger_modulo(__name__)
                logger_debug.info(
                    f"FRAME: {nombre} - Prereq Total: {prerequisitos_totales}, "
                    f"Completados: {prerequisitos_completados}, Progreso: {progreso_prerequisitos:.0f}%"
                )

            # Determinar icono de estado
            icon_estado = {
                'completada': '✓',
                'aprobada': '✓',
                'cursando': '◐',
                'activa': '◐',
                'pendiente': '○',
                'disponible': '📅',
            }.get(estado, '?')

            color_estado = {
                'completada': 'success',
                'aprobada': 'success',
                'cursando': 'info',
                'activa': 'info',
                'pendiente': 'warning',
                'disponible': 'secondary',
            }.get(estado, 'secondary')

            # Frame de la tarjeta
            card_frame = Frame(parent, padding=5)
            if modo_vista == "list":
                card_frame.pack(fill=X, padx=3, pady=3)
            else:
                card_frame.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)

            Label(
                card_frame,
                text=f"📖 {nombre}",
                style="FormLabel.TLabel",
                bootstyle=color_estado,
            ).pack(side=TOP, anchor=W, pady=(0, 2))
            Separator(card_frame).pack(side=TOP, fill=X, pady=(0, 2))

            # Fila 1: Estado y nota
            header_frame = Frame(card_frame)
            header_frame.pack(fill=X, pady=2)

            lbl_estado = Label(
                header_frame,
                text=f"{icon_estado} {estado.title()}",
                style="Small.TLabel",
                bootstyle=color_estado,
            )
            lbl_estado.pack(side=LEFT, padx=2)

            lbl_nota = Label(
                header_frame,
                text=f"📊 Nota: {nota:.1f}",
                style="Small.TLabel",
                bootstyle="info",
            )
            lbl_nota.pack(side=RIGHT, padx=2)

            # Fila 2: Ejes temáticos y actividades
            content_frame = Frame(card_frame)
            content_frame.pack(fill=X, pady=1)

            lbl_ejes = Label(
                content_frame,
                text=f"🎯 Ejes: {ejes_tematicos}",
                style="Small.TLabel",
                bootstyle="secondary",
            )
            lbl_ejes.pack(side=LEFT, padx=2)

            lbl_actividades = Label(
                content_frame,
                text=f"✔️ Actividades: {actividades}",
                style="Small.TLabel",
                bootstyle="secondary",
            )
            lbl_actividades.pack(side=LEFT, padx=2)

            # Fila 3: Barra de progreso de actividades
            progress_frame = Frame(card_frame)
            progress_frame.pack(fill=X, pady=2, padx=2)

            lbl_progress_title = Label(
                progress_frame,
                text=f"Actividades: {self._format_text_progress(progreso_actividades)}",
                bootstyle=self._progress_bootstyle(progreso_actividades),
                font=("DejaVu Sans Mono", 8),
            )
            lbl_progress_title.pack(side=TOP, pady=0)

            # Fila 4: Barra de progreso de prerequisitos (si existen)
            if prerequisitos_totales > 0:
                prereq_progress_frame = Frame(card_frame)
                prereq_progress_frame.pack(fill=X, pady=2, padx=2)

                lbl_prereq_progress_title = Label(
                    prereq_progress_frame,
                    text=(
                        f"Prereq: {self._format_text_progress(progreso_prerequisitos)} "
                        f"({prerequisitos_completados}/{prerequisitos_totales})"
                    ),
                    bootstyle=self._progress_bootstyle(progreso_prerequisitos),
                    font=("DejaVu Sans Mono", 8),
                )
                lbl_prereq_progress_title.pack(side=TOP, pady=0)

            # Fila 5: Prerrequisitos (si existen)
            prerequisitos = prerequisitos if prerequisitos else '-'
            if prerequisitos and prerequisitos != '-' and progreso_prerequisitos < 100:
                prereq_frame = Frame(card_frame)
                prereq_frame.pack(fill=X, pady=1)

                lbl_prereq_title = Label(
                    prereq_frame,
                    text="📋 Requerimientos:",
                    style="Small.TLabel",
                    bootstyle="secondary",
                )
                lbl_prereq_title.pack(side=LEFT, padx=2)

                lbl_prereq = Label(
                    prereq_frame,
                    text=prerequisitos,
                    style="Small.TLabel",
                    bootstyle="secondary",
                    wraplength=520 if modo_vista == "list" else 140,
                    justify=LEFT,
                )
                lbl_prereq.pack(side=LEFT, padx=2, fill=X, expand=TRUE)

        except Exception as e:
            from scripts.logging_config import obtener_logger_modulo

            logger = obtener_logger_modulo(__name__)
            logger.error(f"Error al crear tarjeta de asignatura: {e}", exc_info=True)

    def crear_tarjeta_semestre(self, numero_semestre: int, porcentaje: float):
        """Crea una tarjeta visual para mostrar información de un semestre.

        Args:
            numero_semestre (int): Número del semestre (1, 2, 3, etc.)
            porcentaje (float): Porcentaje de progreso (0-100)
        """
        try:
            scrolled_frame = self.map_widgets.get('scrolled_frame')
            if not scrolled_frame:
                return

            # Frame principal de la tarjeta
            card_frame = Frame(scrolled_frame, padding=10)
            card_frame.pack(fill=X, padx=5, pady=5)

            Label(
                card_frame,
                text="📚 Semestre",
                style="FormLabel.TLabel",
                bootstyle="info",
            ).pack(side=TOP, anchor=W, pady=(0, 3))
            Separator(card_frame).pack(side=TOP, fill=X, pady=(0, 6))

            # Frame para contenido
            content_frame = Frame(card_frame)
            content_frame.pack(fill=BOTH, expand=TRUE)

            # Número de semestre
            lbl_numero = Label(
                content_frame,
                text=str(numero_semestre),
                style="Display.TLabel",
                bootstyle="info",
            )
            lbl_numero.pack(pady=10)

            # Porcentaje con barra de progreso
            progress_frame = Frame(content_frame)
            progress_frame.pack(fill=X, padx=10, pady=10)

            # Label de porcentaje
            lbl_porcentaje = Label(
                progress_frame,
                text=f"Progreso: {self._format_text_progress(porcentaje)}",
                bootstyle=self._progress_bootstyle(porcentaje),
                font=("DejaVu Sans Mono", 9),
            )
            lbl_porcentaje.pack(side=TOP, pady=5)

        except Exception as e:
            from scripts.logging_config import obtener_logger_modulo

            logger = obtener_logger_modulo(__name__)
            logger.error(f"Error al crear tarjeta de semestre: {e}", exc_info=True)

    def _crear_tarjetas_prueba(self):
        """Crea tarjetas de prueba para visualizar el diseño."""
        try:
            # Semestre 1
            asignaturas_s1 = [
                {
                    'nombre': 'Matemática I',
                    'ejes_tematicos': 3,
                    'actividades': 12,
                    'nota': 95.5,
                    'prerequisitos': '-',
                    'estado': 'completada',
                    'progreso_actividades': 100.0,
                },
                {
                    'nombre': 'Programación I',
                    'ejes_tematicos': 4,
                    'actividades': 15,
                    'nota': 88.0,
                    'prerequisitos': '-',
                    'estado': 'completada',
                    'progreso_actividades': 100.0,
                },
                {
                    'nombre': 'Física I',
                    'ejes_tematicos': 3,
                    'actividades': 10,
                    'nota': 92.3,
                    'prerequisitos': '-',
                    'estado': 'completada',
                    'progreso_actividades': 100.0,
                },
            ]
            self.crear_semestre_con_asignaturas(
                numero_semestre=1, porcentaje=100.0, asignaturas=asignaturas_s1
            )

            # Semestre 2
            asignaturas_s2 = [
                {
                    'nombre': 'Matemática II',
                    'ejes_tematicos': 3,
                    'actividades': 12,
                    'nota': 85.5,
                    'prerequisitos': 'Matemática I',
                    'estado': 'completada',
                    'progreso_actividades': 100.0,
                },
                {
                    'nombre': 'Programación II',
                    'ejes_tematicos': 4,
                    'actividades': 14,
                    'nota': 78.0,
                    'prerequisitos': 'Programación I',
                    'estado': 'completada',
                    'progreso_actividades': 100.0,
                },
                {
                    'nombre': 'Estructuras de Datos',
                    'ejes_tematicos': 4,
                    'actividades': 16,
                    'nota': 82.5,
                    'prerequisitos': 'Programación I',
                    'estado': 'completada',
                    'progreso_actividades': 100.0,
                },
            ]
            self.crear_semestre_con_asignaturas(
                numero_semestre=2, porcentaje=85.5, asignaturas=asignaturas_s2
            )

            # Semestre 3
            asignaturas_s3 = [
                {
                    'nombre': 'Análisis Matemático',
                    'ejes_tematicos': 3,
                    'actividades': 11,
                    'nota': 68.0,
                    'prerequisitos': 'Matemática II',
                    'estado': 'activa',
                    'progreso_actividades': 72.7,
                },
                {
                    'nombre': 'Bases de Datos',
                    'ejes_tematicos': 3,
                    'actividades': 13,
                    'nota': 72.5,
                    'prerequisitos': 'Programación II',
                    'estado': 'activa',
                    'progreso_actividades': 61.5,
                },
            ]
            self.crear_semestre_con_asignaturas(
                numero_semestre=3, porcentaje=65.0, asignaturas=asignaturas_s3
            )

            # Semestre 4
            asignaturas_s4 = [
                {
                    'nombre': 'Sistemas Operativos',
                    'ejes_tematicos': 3,
                    'actividades': 10,
                    'nota': 0.0,
                    'prerequisitos': 'Programación II',
                    'estado': 'pendiente',
                    'progreso_actividades': 0.0,
                },
                {
                    'nombre': 'Algoritmos Avanzados',
                    'ejes_tematicos': 4,
                    'actividades': 12,
                    'nota': 0.0,
                    'prerequisitos': 'Estructuras de Datos, Análisis Matemático',
                    'estado': 'pendiente',
                    'progreso_actividades': 0.0,
                },
            ]
            self.crear_semestre_con_asignaturas(
                numero_semestre=4, porcentaje=45.3, asignaturas=asignaturas_s4
            )

        except Exception as e:
            from scripts.logging_config import obtener_logger_modulo

            logger = obtener_logger_modulo(__name__)
            logger.error(f"Error al crear tarjetas de prueba: {e}", exc_info=True)

    def limpiar_asignaturas(self) -> None:
        """Limpia el scrolled_frame eliminando todos los widgets."""
        try:
            scrolled_frame = self.map_widgets.get('scrolled_frame')
            if scrolled_frame:
                for widget in scrolled_frame.winfo_children():
                    widget.destroy()
            from scripts.logging_config import obtener_logger_modulo

            logger = obtener_logger_modulo(__name__)
            logger.debug("Área de asignaturas limpiada")
        except Exception as e:
            from scripts.logging_config import obtener_logger_modulo

            logger = obtener_logger_modulo(__name__)
            logger.error(f"Error al limpiar asignaturas: {e}", exc_info=True)

    def mostrar_asignaturas_reales(self, asignaturas_por_semestre: Dict[int, list]) -> None:
        """Muestra las asignaturas reales agrupadas por semestre.

        Args:
            asignaturas_por_semestre (Dict[int, list]): Diccionario {semestre: [asignaturas]}
        """
        self._asignaturas_cache = asignaturas_por_semestre
        self._render_asignaturas(asignaturas_por_semestre)

    def _render_asignaturas(self, asignaturas_por_semestre: Dict[int, list]) -> None:
        """Renderiza asignaturas usando el modo de vista actual."""
        try:
            # Limpiar el área
            self.limpiar_asignaturas()
            modo_vista = self._obtener_modo_vista()

            # Mostrar asignaturas por semestre
            for semestre in sorted(asignaturas_por_semestre.keys()):
                asignaturas = asignaturas_por_semestre[semestre]

                # Calcular progreso promedio del semestre
                if asignaturas:
                    progresos = [float(a.get('progreso_actividades', 0)) for a in asignaturas]
                    progreso_semestre = sum(progresos) / len(progresos) if progresos else 0.0

                    # Convertir asignaturas a formato esperado
                    asignaturas_formateadas = []
                    for asig in asignaturas:
                        nota_final = asig.get('nota_final', 0)
                        if nota_final is None:
                            nota_final = 0.0
                        else:
                            nota_final = float(nota_final)

                        # Procesar prerequisitos: garantizar que no sea None
                        prereq = asig.get('prerequisitos', '-')
                        if prereq is None or prereq == '':
                            prereq = '-'

                        asig_formateada = {
                            'nombre': asig.get('nombre_asignatura', ''),
                            'ejes_tematicos': int(asig.get('cantidad_ejes_tematicos', 0)),
                            'actividades': int(asig.get('cantidad_actividades', 0)),
                            'nota': nota_final,
                            'prerequisitos': prereq,
                            'estado': asig.get('estado', 'pendiente'),
                            'progreso_actividades': float(asig.get('progreso_actividades', 0)),
                            'prerequisitos_completados': int(
                                asig.get('prerequisitos_completados', 0)
                            ),
                            'prerequisitos_totales': int(asig.get('prerequisitos_totales', 0)),
                            'progreso_prerequisitos': float(
                                asig.get('progreso_prerequisitos', 0.0)
                            ),
                        }
                        asignaturas_formateadas.append(asig_formateada)
                else:
                    # Semestre sin asignaturas
                    asignaturas_formateadas = []
                    progreso_semestre = 0.0

                # Crear tarjetas del semestre con asignaturas
                self.crear_semestre_con_asignaturas(
                    numero_semestre=semestre,
                    porcentaje=progreso_semestre,
                    asignaturas=asignaturas_formateadas,
                    modo_vista=modo_vista,
                )

            from scripts.logging_config import obtener_logger_modulo

            logger = obtener_logger_modulo(__name__)
            logger.info(f"Asignaturas reales mostradas: {len(asignaturas_por_semestre)} semestres")

        except Exception as e:
            from scripts.logging_config import obtener_logger_modulo

            logger = obtener_logger_modulo(__name__)
            logger.error(f"Error al mostrar asignaturas reales: {e}", exc_info=True)
