from ttkbootstrap import (
    Frame,
    Label,
    Separator,
    Combobox,
    StringVar,
    Button,
    Labelframe,
)
from ttkbootstrap.constants import *
from ui.ttk.styles.estilos import PADDING_XS, PADDING_SM, PADDING_MD
from ui.ttk.styles.icons import *
from typing import Dict, Any
from controladores.controlador_calendario import ControladorCalendario


class FrameCalendario(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)

        self.var_carrera = StringVar()
        self.var_tipo_actividad = StringVar()
        self.var_estado_actividad = StringVar()
        self.var_asignatura = StringVar()

        self.map_vars: Dict[str, Any] = {
            'var_carrera': self.var_carrera,
            'var_tipo_actividad': self.var_tipo_actividad,
            'var_estado_actividad': self.var_estado_actividad,
            'var_asignatura': self.var_asignatura,
        }

        self.map_widgets: Dict[str, Any] = {}

        # cargamos los widgets
        self._crear_widgets()

        # Cargamos el controlador
        self.controlador = ControladorCalendario(
            map_widgets=self.map_widgets, map_vars=self.map_vars
        )

    def _crear_widgets(self):
        # frame superior
        frame_superior = Frame(self, padding=(PADDING_XS, PADDING_XS))
        self._frame_superior(frame=frame_superior)
        frame_superior.pack(side=TOP, padx=PADDING_XS, pady=PADDING_XS, fill=X)

        # frame central
        frame_central = Frame(self, padding=(PADDING_XS, PADDING_XS))
        self._frame_central(frame=frame_central)
        frame_central.pack(
            side=TOP, padx=PADDING_XS, pady=PADDING_XS, fill=BOTH, expand=TRUE
        )

        frame_inferior = Frame(self, padding=(PADDING_XS, PADDING_XS))
        self._frame_inferior(frame=frame_inferior)
        frame_inferior.pack(side=TOP, padx=PADDING_XS, pady=PADDING_XS, fill=X)

    def _frame_superior(self, frame: Frame):
        lbl_titulo = Label(
            frame,
            text=f"{ICON_CALENDARIO} Calendario Académico",
            bootstyle=INFO,
            style="Title.TLabel",
        )
        lbl_titulo.pack(side=TOP, pady=PADDING_SM, padx=PADDING_MD, fill=X)

        lbl_subtitulo = Label(
            frame,
            text="Visualiza eventos y actividades académicas",
            bootstyle=SECONDARY,
            style="Subtitle.TLabel",
        )
        lbl_subtitulo.pack(side=TOP, padx=PADDING_MD, pady=PADDING_SM, fill=X)

        Separator(frame).pack(side=TOP, fill=X, padx=PADDING_XS, pady=PADDING_XS)

    def _frame_central(self, frame: Frame):

        frame_filtrar = Frame(frame, padding=(PADDING_XS, PADDING_XS))
        self._frame_filtrado(frame=frame_filtrar)
        frame_filtrar.pack(side=TOP, fill=X, padx=PADDING_XS, pady=PADDING_XS)

        frame_desplazar = Frame(frame, padding=(PADDING_XS, PADDING_XS))
        self._frame_desplazar_meses(frame=frame_desplazar)
        frame_desplazar.pack(side=TOP, fill=X, padx=PADDING_XS, pady=PADDING_XS)

        Separator(frame).pack(side=TOP, fill=X, padx=PADDING_XS, pady=PADDING_XS)

        frame_notebook = Frame(frame, padding=(PADDING_XS, PADDING_XS))
        self._frame_notebook(frame=frame_notebook)
        frame_notebook.pack(
            side=TOP, fill=BOTH, padx=PADDING_XS, pady=PADDING_XS, expand=TRUE
        )

        frame_info = Frame(frame, padding=PADDING_XS)
        self._frame_info(frame=frame_info)
        frame_info.pack(side=TOP, fill=X, padx=PADDING_XS, pady=PADDING_XS)

    def _frame_inferior(self, frame: Frame):
        # Botón Aplicar Filtros
        btn_aplicar_filtros = Button(frame, text="Aplicar Filtros", bootstyle=SUCCESS)
        btn_aplicar_filtros.pack(side=LEFT, padx=PADDING_SM, pady=PADDING_SM)
        self.map_widgets['btn_aplicar_filtros'] = btn_aplicar_filtros

        # Botón Refrescar
        btn_refrescar = Button(frame, text="Refrescar", bootstyle=INFO)
        btn_refrescar.pack(side=LEFT, padx=PADDING_SM, pady=PADDING_SM)
        self.map_widgets['btn_refrescar'] = btn_refrescar

        # Botón Limpiar Filtros
        btn_limpiar_filtros = Button(frame, text="Limpiar Filtros", bootstyle=WARNING)
        btn_limpiar_filtros.pack(side=LEFT, padx=PADDING_SM, pady=PADDING_SM)
        self.map_widgets['btn_limpiar_filtros'] = btn_limpiar_filtros

        # Separator
        Separator(frame, orient=VERTICAL).pack(
            side=LEFT, fill=Y, padx=PADDING_MD, pady=PADDING_SM
        )

        # Botón Exportar CSV
        btn_exportar_csv = Button(frame, text="📋 Exportar CSV", bootstyle=SECONDARY)
        btn_exportar_csv.pack(side=LEFT, padx=PADDING_SM, pady=PADDING_SM)
        self.map_widgets['btn_exportar_csv'] = btn_exportar_csv

        # Botón Exportar iCalendar
        btn_exportar_ical = Button(frame, text="📅 Exportar iCal", bootstyle=SECONDARY)
        btn_exportar_ical.pack(side=LEFT, padx=PADDING_SM, pady=PADDING_SM)
        self.map_widgets['btn_exportar_ical'] = btn_exportar_ical

    def _frame_filtrado(self, frame: Frame):
        # Configurar columnas para que sean redimensionables
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(3, weight=1)

        # Configurar filas para mejor distribución
        frame.rowconfigure(0, weight=0)
        frame.rowconfigure(1, weight=0)
        frame.rowconfigure(2, weight=0)

        # Label Filtro
        lbl_filtro = Label(frame, text="Filtrar por:", bootstyle=INFO)
        lbl_filtro.grid(row=0, column=0, padx=PADDING_XS, pady=PADDING_XS, sticky=W)

        # Carrera
        lbl_carrera = Label(frame, text="Carrera: ")
        lbl_carrera.grid(row=1, column=0, padx=PADDING_XS, pady=PADDING_XS, sticky=W)

        cbx_carrera = Combobox(
            frame,
            state=READONLY,
            textvariable=self.var_carrera)
        cbx_carrera.grid(row=1, column=1, padx=PADDING_XS, pady=PADDING_XS, sticky=EW)
        self.map_widgets['cbx_carrera'] = cbx_carrera

        # Asignatura
        lbl_asignatura = Label(frame, text="Asignatura: ")
        lbl_asignatura.grid(row=1, column=2, padx=PADDING_XS, pady=PADDING_XS, sticky=W)

        cbx_asignatura = Combobox(
            frame,
            state=READONLY,
            textvariable=self.var_asignatura)
        cbx_asignatura.grid(row=1, column=3, padx=PADDING_XS, pady=PADDING_XS, sticky=EW)
        self.map_widgets['cbx_asignatura'] = cbx_asignatura

        # Fila 2: Tipo de Evento y Tipo de Actividad
        # Tipo de Evento
        lbl_tipo_evento = Label(frame, text="Tipo de Evento: ")
        lbl_tipo_evento.grid(row=2, column=0, padx=PADDING_XS, pady=PADDING_XS, sticky=W)

        cbx_tipo_evento = Combobox(
            frame,
            state=READONLY,
            textvariable=self.var_estado_actividad)
        cbx_tipo_evento.grid(row=2, column=1, padx=PADDING_XS, pady=PADDING_XS, sticky=EW)
        self.map_widgets['cbx_tipo_evento'] = cbx_tipo_evento

        # Tipo de Actividad
        lbl_tipo_actividad = Label(frame, text="Tipo de Actividad: ")
        lbl_tipo_actividad.grid(row=2, column=2, padx=PADDING_XS, pady=PADDING_XS, sticky=W)

        cbx_tipo_actividad = Combobox(
            frame,
            state=READONLY,
            textvariable=self.var_tipo_actividad)
        cbx_tipo_actividad.grid(
            row=2, column=3, padx=PADDING_XS, pady=PADDING_XS, sticky=EW
        )
        self.map_widgets['cbx_tipo_actividad'] = cbx_tipo_actividad

    def _frame_desplazar_meses(self, frame: Frame):
        """Frame para navegar entre meses."""
        # Botón mes anterior
        btn_anterior = Button(frame, text="◀ Anterior", bootstyle=OUTLINE)
        btn_anterior.pack(side=LEFT, padx=PADDING_SM, pady=PADDING_SM)
        self.map_widgets['btn_anterior'] = btn_anterior

        # Label con mes y año actual
        self.lbl_mes_año = Label(
            frame,
            text="dd, mm de yyy",
            bootstyle=INFO,
            style="Section.TLabel",
            anchor=CENTER,
            justify=CENTER,
        )
        self.lbl_mes_año.pack(
            side=LEFT, padx=PADDING_MD, pady=PADDING_SM, expand=TRUE, fill=BOTH
        )
        self.map_widgets['lbl_mes_año'] = self.lbl_mes_año

        # Botón mes siguiente
        btn_siguiente = Button(frame, text="Siguiente ▶", bootstyle=OUTLINE)
        btn_siguiente.pack(side=LEFT, padx=PADDING_SM, pady=PADDING_SM)
        self.map_widgets['btn_siguiente'] = btn_siguiente

        # Botón hoy
        btn_hoy = Button(frame, text="Hoy", bootstyle=SUCCESS)
        btn_hoy.pack(side=LEFT, padx=PADDING_SM, pady=PADDING_SM)
        self.map_widgets['btn_hoy'] = btn_hoy

    def _frame_notebook(self, frame: Frame):
        # Vista doble: Calendario + Agenda lado a lado
        split = Frame(frame, padding=(PADDING_XS, PADDING_XS))
        split.pack(side=TOP, padx=PADDING_XS, pady=PADDING_XS, fill=BOTH, expand=True)
        split.columnconfigure(0, weight=3)
        split.columnconfigure(1, weight=2)
        split.rowconfigure(0, weight=1)

        frame_calendario = Labelframe(
            split, text="Calendario", padding=(PADDING_XS, PADDING_XS)
        )
        frame_calendario.grid(row=0, column=0, sticky=NSEW, padx=(0, PADDING_XS), pady=0)
        self.map_widgets['frame_calendario'] = frame_calendario

        frame_agenda = Labelframe(split, text="Agenda", padding=(PADDING_XS, PADDING_XS))
        frame_agenda.grid(row=0, column=1, sticky=NSEW, padx=(PADDING_XS, 0), pady=0)
        self.map_widgets['frame_agenda'] = frame_agenda

    def _frame_info(self, frame: Frame):
        self._frame_leyenda(frame=frame)

    def _frame_leyenda(self, frame: Frame):
        """Crea la leyenda que explica los tipos de eventos."""
        frame_row1 = Frame(frame)
        frame_row1.pack(side=TOP, fill=X)

        frame_row2 = Frame(frame)
        frame_row2.pack(side=TOP, fill=X)

        # Row 1: Indicadores
        lbl_leyenda_titulo = Label(
            frame_row1,
            text="Indicadores",
            bootstyle=INFO,
            style="Section.TLabel",
        )
        lbl_leyenda_titulo.pack(side=LEFT, padx=PADDING_SM, pady=(PADDING_XS, PADDING_SM))

        Separator(frame_row1, orient=VERTICAL).pack(
            side=LEFT, fill=Y, padx=PADDING_MD, pady=PADDING_SM
        )

        lbl_actividad_inicio = Label(
            frame_row1,
            text="● Actividad (inicio)",
            bootstyle=SUCCESS,
            style="Small.TLabel",
        )
        lbl_actividad_inicio.pack(side=LEFT, padx=PADDING_MD, pady=PADDING_SM)

        Separator(frame_row1, orient=VERTICAL).pack(
            side=LEFT, fill=Y, padx=PADDING_SM, pady=PADDING_SM
        )

        lbl_actividad_fin = Label(
            frame_row1,
            text="● Actividad (fin)",
            bootstyle=WARNING,
            style="Small.TLabel",
        )
        lbl_actividad_fin.pack(side=LEFT, padx=PADDING_MD, pady=PADDING_SM)

        Separator(frame_row1, orient=VERTICAL).pack(
            side=LEFT, fill=Y, padx=PADDING_SM, pady=PADDING_SM
        )

        lbl_evento_calendario = Label(
            frame_row1,
            text="● Evento",
            bootstyle=INFO,
            style="Small.TLabel",
        )
        lbl_evento_calendario.pack(side=LEFT, padx=PADDING_MD, pady=PADDING_SM)

        # Row 2: Estadísticas
        lbl_estadisticas_titulo = Label(
            frame_row2,
            text="Resumen",
            bootstyle=PRIMARY,
            style="Section.TLabel",
        )
        lbl_estadisticas_titulo.pack(side=LEFT, padx=PADDING_SM, pady=PADDING_SM)

        frame_stats = Frame(frame_row2, padding=(PADDING_XS, PADDING_XS))
        frame_stats.pack(
            side=LEFT, padx=PADDING_MD, pady=PADDING_SM, fill=BOTH, expand=True
        )

        # Label de estadísticas que se actualizará dinámicamente
        self.lbl_stats = Label(
            frame_stats,
            text="Cargando...",
            bootstyle=SECONDARY,
            style="Small.TLabel",
        )
        self.lbl_stats.pack(side=LEFT, padx=PADDING_SM, pady=PADDING_SM)

        # Guardar referencia para acceso desde el controlador
        self.map_widgets['lbl_stats'] = self.lbl_stats
