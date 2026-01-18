from ttkbootstrap import (
    Frame,
    Label,
    StringVar,
    Separator,
    Combobox,
    Labelframe,
    Button,
    Treeview,
    Progressbar,
)
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.tooltip import ToolTip
from typing import Dict, Any
from ui.ttk.styles.icons import *
from controladores.controlador_carreras import ControladorCarreras


class FrameCarreras(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        self.map_vars: Dict[str, Any] = {}
        self.map_widgets: Dict[str, Any] = {}

        # Variables
        self.var_carrera = StringVar()
        self.map_vars['var_carrera'] = self.var_carrera

        self.var_estudiante = StringVar()
        self.map_vars['var_estudiante'] = self.var_estudiante

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
        frame_superior = Frame(self, padding=(1, 1))
        self._frame_superior(frame=frame_superior)
        frame_superior.pack(side=TOP, fill=X, padx=5, pady=10)

        frame_central = Frame(self, padding=(1, 1))
        self._frame_central(frame=frame_central)
        frame_central.pack(side=TOP, fill=BOTH, padx=5, pady=5, expand=TRUE)

        frame_inferior = Frame(self, padding=(1, 1))
        self._frame_inferior(frame=frame_inferior)
        frame_inferior.pack(side=TOP, fill=X, padx=5, pady=5)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frames Principales
    # └────────────────────────────────────────────────────────────┘

    def _frame_superior(self, frame: Frame):
        """Frame superior con título y subtítulo"""
        frame_titulo = Frame(frame, padding=(1, 1))
        frame_titulo.pack(side=TOP, padx=1, pady=1, fill=X)

        lbl_titulo = Label(
            frame_titulo,
            text="🎓 Carreras",
            font=("Helvetica", 18, "bold"),
            bootstyle=INFO,
        )
        lbl_titulo.pack(side=TOP, fill=X, padx=1, pady=10)

        lbl_subtitulo = Label(
            frame_titulo,
            text="Gestiona y visualiza las carreras académicas",
            bootstyle=SECONDARY,
            font=("Helvetica", 9),
        )
        lbl_subtitulo.pack(side=TOP, fill=X, padx=1, pady=1)

        Separator(frame).pack(side=TOP, fill=X, padx=1, pady=1)

    def _frame_central(self, frame: Frame):
        """Frame central con filtros y contenido principal"""
        frame_filtrado = Labelframe(frame, text="Filtros", padding=(1, 1))
        self._frame_filtrado(frame=frame_filtrado)
        frame_filtrado.pack(side=TOP, fill=X, padx=1, pady=1, ipadx=5, ipady=5)

        Separator(frame).pack(side=TOP, fill=X, padx=1, pady=1)

        scrolled_frame = ScrolledFrame(frame, padding=(1, 1))
        scrolled_frame.pack(side=TOP, fill=BOTH, padx=1, pady=1, expand=TRUE)
        self.map_widgets['scrolled_frame'] = scrolled_frame

    def _frame_inferior(self, frame: Frame):
        """Frame inferior con botón de refrescar"""
        btn_refrescar = Button(frame, text="🔄 Refrescar", bootstyle=WARNING, width=20)
        btn_refrescar.pack(side=LEFT, padx=5, pady=5)
        self.map_widgets['btn_refrescar'] = btn_refrescar

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frames Funcionales
    # └────────────────────────────────────────────────────────────┘

    def _frame_filtrado(self, frame: Frame):
        """Frame para filtros de estudiantes y carreras"""
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        # Label y Combobox para Estudiantes
        lbl_estudiante = Label(frame, text="Estudiante: ")
        lbl_estudiante.grid(row=0, column=0, padx=2, pady=2, sticky=W)

        cbx_estudiante = Combobox(frame, textvariable=self.var_estudiante, state=READONLY, width=30)
        cbx_estudiante.grid(row=1, column=0, padx=2, pady=2, sticky=EW)
        self.map_widgets['cbx_estudiante'] = cbx_estudiante
        ToolTip(
            cbx_estudiante,
            text="Seleccione un estudiante para ver sus carreras asociadas",
        )

        # Label y Combobox para Carreras
        lbl_carrera = Label(frame, text="Carrera: ")
        lbl_carrera.grid(row=0, column=1, padx=2, pady=2, sticky=W)

        cbx_carrera = Combobox(frame, textvariable=self.var_carrera, state=READONLY, width=30)
        cbx_carrera.grid(row=1, column=1, padx=2, pady=2, sticky=EW)
        self.map_widgets['cbx_carrera'] = cbx_carrera
        ToolTip(
            cbx_carrera,
            text="Muestra la carrera asociada al estudiante seleccionado",
        )

    # ┌────────────────────────────────────────────────────────────┐
    # │ Métodos para Crear Tarjetas
    # └────────────────────────────────────────────────────────────┘

    def crear_semestre_con_asignaturas(
        self, numero_semestre: int, porcentaje: float, asignaturas: list
    ):
        """Crea una sección con semestre (arriba) y asignaturas en grilla (abajo).

        Args:
            numero_semestre (int): Número del semestre
            porcentaje (float): Porcentaje de progreso
            asignaturas (list): Lista de diccionarios con datos de asignaturas
        """
        try:
            scrolled_frame = self.map_widgets.get('scrolled_frame')
            if not scrolled_frame:
                return

            # Frame contenedor para la sección del semestre
            section_frame = Frame(scrolled_frame)
            section_frame.pack(fill=BOTH, padx=10, pady=15, expand=TRUE)

            # -------- ARRIBA: TARJETA DE SEMESTRE --------
            self._crear_tarjeta_semestre_header(section_frame, numero_semestre, porcentaje)

            # -------- ABAJO: ASIGNATURAS EN GRILLA --------
            self._crear_asignaturas_container(section_frame, asignaturas)

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
        card_frame.pack(fill=X, pady=10)

        # Contenedor con estilo
        sem_box = Labelframe(
            card_frame,
            text=f"📚 Semestre {numero_semestre}",
            padding=10,
            bootstyle="info",
        )
        sem_box.pack(fill=X, expand=FALSE)

        # Frame interno para contenido
        content = Frame(sem_box)
        content.pack(fill=X)

        # Número de semestre (grande)
        lbl_numero = Label(
            content,
            text=f"Semestre {numero_semestre}",
            font=("Helvetica", 14, "bold"),
            bootstyle="info",
        )
        lbl_numero.pack(side=LEFT, padx=20, pady=10)

        # Porcentaje con barra de progreso
        progress_frame = Frame(content)
        progress_frame.pack(side=LEFT, fill=BOTH, expand=TRUE, padx=20, pady=10)

        # Label de porcentaje
        lbl_porcentaje = Label(
            progress_frame,
            text=f"Progreso: {porcentaje:.1f}%",
            font=("Helvetica", 10, "bold"),
            bootstyle="info",
        )
        lbl_porcentaje.pack(side=TOP, pady=3)

        # Barra de progreso
        progress_bar = Progressbar(
            progress_frame,
            value=porcentaje,
            maximum=100,
            length=300,
            bootstyle="info",
        )
        progress_bar.pack(side=TOP, fill=X)

    def _crear_asignaturas_container(self, parent: Frame, asignaturas: list):
        """Crea el contenedor con las tarjetas de asignaturas en grilla.

        Args:
            parent (Frame): Frame padre
            asignaturas (list): Lista de diccionarios con datos de asignaturas
        """
        # Frame contenedor para asignaturas
        asig_container = Frame(parent)
        asig_container.pack(fill=BOTH, expand=TRUE, padx=5, pady=10)

        # Label de encabezado (opcional, ya que el semestre lo indica)
        # lbl_asignaturas = Label(
        #     asig_container,
        #     text="📚 Asignaturas",
        #     font=("Helvetica", 12, "bold"),
        #     bootstyle="info",
        # )
        # lbl_asignaturas.pack(pady=5)

        # Frame para la grilla
        grid_frame = Frame(asig_container)
        grid_frame.pack(fill=BOTH, expand=TRUE, padx=5, pady=5)

        # Configurar columnas (5 asignaturas por fila)
        num_columnas = 5
        for col in range(num_columnas):
            grid_frame.columnconfigure(col, weight=1)

        # Crear tarjetas en grilla
        for idx, asignatura in enumerate(asignaturas):
            row = idx // num_columnas
            col = idx % num_columnas
            self._crear_tarjeta_asignatura(grid_frame, asignatura, row, col)

    def _crear_tarjeta_asignatura(
        self, parent: Frame, asignatura: Dict[str, Any], row: int = 0, col: int = 0
    ):
        """Crea una tarjeta individual de asignatura en grilla.

        Args:
            parent (Frame): Frame padre
            asignatura (Dict): Diccionario con los datos de la asignatura
            row (int): Fila en la grilla
            col (int): Columna en la grilla
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

            # Frame de la tarjeta (usar grid)
            card_frame = Labelframe(
                parent,
                text=f"📖 {nombre}",
                padding=8,
                bootstyle=color_estado,
            )
            card_frame.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

            # Fila 1: Estado y nota
            header_frame = Frame(card_frame)
            header_frame.pack(fill=X, pady=2)

            lbl_estado = Label(
                header_frame,
                text=f"{icon_estado} {estado.title()}",
                font=("Helvetica", 8, "bold"),
                bootstyle=color_estado,
            )
            lbl_estado.pack(side=LEFT, padx=2)

            lbl_nota = Label(
                header_frame,
                text=f"📊 Nota: {nota:.1f}",
                font=("Helvetica", 8, "bold"),
                bootstyle="info",
            )
            lbl_nota.pack(side=RIGHT, padx=2)

            # Fila 2: Ejes temáticos y actividades
            content_frame = Frame(card_frame)
            content_frame.pack(fill=X, pady=2)

            lbl_ejes = Label(
                content_frame,
                text=f"🎯 Ejes: {ejes_tematicos}",
                font=("Helvetica", 8),
                bootstyle="secondary",
            )
            lbl_ejes.pack(side=LEFT, padx=2)

            lbl_actividades = Label(
                content_frame,
                text=f"✔️ Actividades: {actividades}",
                font=("Helvetica", 8),
                bootstyle="secondary",
            )
            lbl_actividades.pack(side=LEFT, padx=2)

            # Fila 3: Barra de progreso de actividades
            progress_frame = Frame(card_frame)
            progress_frame.pack(fill=X, pady=3, padx=2)

            lbl_progress_title = Label(
                progress_frame,
                text=f"Actividades: {progreso_actividades:.0f}%",
                font=("Helvetica", 7, "bold"),
                bootstyle="secondary",
            )
            lbl_progress_title.pack(side=TOP, pady=1)

            progress_bar = Progressbar(
                progress_frame,
                value=progreso_actividades,
                maximum=100,
                bootstyle=color_estado,
            )
            progress_bar.pack(side=TOP, fill=X)

            # Fila 4: Barra de progreso de prerequisitos (si existen)
            if prerequisitos_totales > 0:
                prereq_progress_frame = Frame(card_frame)
                prereq_progress_frame.pack(fill=X, pady=3, padx=2)

                lbl_prereq_progress_title = Label(
                    prereq_progress_frame,
                    text=f"Prerequisitos: {progreso_prerequisitos:.0f}% ({prerequisitos_completados}/{prerequisitos_totales})",
                    font=("Helvetica", 7, "bold"),
                    bootstyle="secondary",
                )
                lbl_prereq_progress_title.pack(side=TOP, pady=1)

                prereq_progress_bar = Progressbar(
                    prereq_progress_frame,
                    value=progreso_prerequisitos,
                    maximum=100,
                    bootstyle="warning" if progreso_prerequisitos < 100 else "success",
                )
                prereq_progress_bar.pack(side=TOP, fill=X)

            # Fila 5: Prerrequisitos (si existen)
            prerequisitos = prerequisitos if prerequisitos else '-'
            if prerequisitos and prerequisitos != '-':
                prereq_frame = Frame(card_frame)
                prereq_frame.pack(fill=X, pady=2)

                lbl_prereq_title = Label(
                    prereq_frame,
                    text="📋 Requerimientos:",
                    font=("Helvetica", 7, "bold"),
                    bootstyle="secondary",
                )
                lbl_prereq_title.pack(side=LEFT, padx=2)

                lbl_prereq = Label(
                    prereq_frame,
                    text=prerequisitos,
                    font=("Helvetica", 7),
                    bootstyle="secondary",
                    wraplength=180,
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
            card_frame = Labelframe(
                scrolled_frame,
                text="📚 Semestre",
                padding=10,
                bootstyle="info",
            )
            card_frame.pack(fill=X, padx=5, pady=5)

            # Frame para contenido
            content_frame = Frame(card_frame)
            content_frame.pack(fill=BOTH, expand=TRUE)

            # Número de semestre
            lbl_numero = Label(
                content_frame,
                text=str(numero_semestre),
                font=("Helvetica", 32, "bold"),
                bootstyle="info",
            )
            lbl_numero.pack(pady=10)

            # Porcentaje con barra de progreso
            progress_frame = Frame(content_frame)
            progress_frame.pack(fill=X, padx=10, pady=10)

            # Label de porcentaje
            lbl_porcentaje = Label(
                progress_frame,
                text=f"Progreso: {porcentaje:.1f}%",
                font=("Helvetica", 10, "bold"),
                bootstyle="info",
            )
            lbl_porcentaje.pack(side=TOP, pady=5)

            # Barra de progreso
            progress_bar = Progressbar(
                progress_frame,
                value=porcentaje,
                maximum=100,
                length=200,
                bootstyle="info",
            )
            progress_bar.pack(side=TOP, fill=X)

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
        try:
            # Limpiar el área
            self.limpiar_asignaturas()

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
                )

            from scripts.logging_config import obtener_logger_modulo

            logger = obtener_logger_modulo(__name__)
            logger.info(f"Asignaturas reales mostradas: {len(asignaturas_por_semestre)} semestres")

        except Exception as e:
            from scripts.logging_config import obtener_logger_modulo

            logger = obtener_logger_modulo(__name__)
            logger.error(f"Error al mostrar asignaturas reales: {e}", exc_info=True)
