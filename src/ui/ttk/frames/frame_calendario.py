from ttkbootstrap import Frame, Label, Separator, Combobox, StringVar, Notebook, Button, Treeview
from ttkbootstrap.constants import *
from ui.ttk.styles.icons import *
from typing import Dict, Any
from controladores.controlador_calendario import ControladorCalendario


class FrameCalendario(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)

        self.map_vars: Dict[str, Any] = {}
        self.map_widgets: Dict[str, Any] = {}

        self.var_carrera = StringVar()
        self.map_vars['var_carrera'] = self.var_carrera

        self.var_tipo_actividad = StringVar()
        self.map_vars['var_tipo_actividad'] = self.var_tipo_actividad

        self.var_estado_actividad = StringVar()
        self.map_vars['var_estado_activdad'] = self.var_estado_actividad

        self.var_asignatura = StringVar()
        self.map_vars['var_asignatura'] = self.var_asignatura

        # cargamos los widgets
        self._crear_widgets()

        # Cargamos el controlador
        self.controlador = ControladorCalendario(
            map_widgets=self.map_widgets, map_vars=self.map_vars
        )

    def _crear_widgets(self):
        # frame superior
        frame_superior = Frame(self, padding=(1, 1))
        self._frame_superior(frame=frame_superior)
        frame_superior.pack(side=TOP, padx=1, pady=1, fill=X)

        # frame central
        frame_central = Frame(self, padding=(1, 1))
        self._frame_central(frame=frame_central)
        frame_central.pack(side=TOP, padx=1, pady=1, fill=BOTH, expand=TRUE)

        frame_inferior = Frame(self, padding=(1, 1))
        self._frame_inferior(frame=frame_inferior)
        frame_inferior.pack(side=TOP, padx=1, pady=1, fill=X)

    def _frame_superior(self, frame: Frame):
        lbl_titulo = Label(
            frame,
            text=f"{ICON_CALENDARIO} Calendario Academico",
            bootstyle=INFO,
            font=("Helvetica", 18, "bold"),
        )
        lbl_titulo.pack(side=TOP, pady=5, padx=10, fill=X)

        lbl_subtitulo = Label(
            frame,
            text="Visualiza eventos y actividades académicas",
            bootstyle=SECONDARY,
            font=("Helvetica", 10),
        )
        lbl_subtitulo.pack(side=TOP, padx=10, pady=5, fill=X)

        Separator(frame).pack(side=TOP, fill=X, padx=1, pady=1)

    def _frame_central(self, frame: Frame):

        frame_filtrar = Frame(frame, padding=(1, 1))
        self._frame_filtrado(frame=frame_filtrar)
        frame_filtrar.pack(side=TOP, fill=X, padx=1, pady=1)

        frame_desplazar = Frame(frame, padding=(1, 1))
        self._frame_desplazar_meses(frame=frame_desplazar)
        frame_desplazar.pack(side=TOP, fill=X, padx=1, pady=1)

        Separator(frame).pack(side=TOP, fill=X, padx=1, pady=1)

        frame_notebook = Frame(frame, padding=(1, 1))
        self._frame_notebook(frame=frame_notebook)
        frame_notebook.pack(side=TOP, fill=BOTH, padx=1, pady=1, expand=TRUE)

        frame_treeview_eventos = Frame(frame, padding=1)
        self._frame_treeview(frame=frame_treeview_eventos)
        frame_treeview_eventos.pack(side=TOP, fill=X, padx=1, pady=1)

    def _frame_inferior(self, frame: Frame):
        # Botón Aplicar Filtros
        btn_aplicar_filtros = Button(frame, text="Aplicar Filtros", bootstyle=SUCCESS, width=15)
        btn_aplicar_filtros.pack(side=LEFT, padx=5, pady=5)
        self.map_widgets['btn_aplicar_filtros'] = btn_aplicar_filtros

        # Botón Refrescar
        btn_refrescar = Button(frame, text="Refrescar", bootstyle=INFO, width=15)
        btn_refrescar.pack(side=LEFT, padx=5, pady=5)
        self.map_widgets['btn_refrescar'] = btn_refrescar

        # Botón Limpiar Filtros
        btn_limpiar_filtros = Button(frame, text="Limpiar Filtros", bootstyle=WARNING, width=15)
        btn_limpiar_filtros.pack(side=LEFT, padx=5, pady=5)
        self.map_widgets['btn_limpiar_filtros'] = btn_limpiar_filtros

        # Separator
        Separator(frame, orient=VERTICAL).pack(side=LEFT, fill=Y, padx=10, pady=5)

        # Botón Exportar CSV
        btn_exportar_csv = Button(frame, text="📋 Exportar CSV", bootstyle=SECONDARY, width=15)
        btn_exportar_csv.pack(side=LEFT, padx=5, pady=5)
        self.map_widgets['btn_exportar_csv'] = btn_exportar_csv

        # Botón Exportar iCalendar
        btn_exportar_ical = Button(frame, text="📅 Exportar iCal", bootstyle=SECONDARY, width=15)
        btn_exportar_ical.pack(side=LEFT, padx=5, pady=5)
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
        lbl_filtro.grid(row=0, column=0, padx=1, pady=1, sticky=W)

        # Carrera
        lbl_carrera = Label(frame, text="Carrera: ")
        lbl_carrera.grid(row=1, column=0, padx=1, pady=1, sticky=W)

        cbx_carrera = Combobox(
            frame,
            state=READONLY,
            textvariable=self.var_carrera,
        )
        cbx_carrera.grid(row=1, column=1, padx=1, pady=1, sticky=EW)
        self.map_widgets['cbx_carrera'] = cbx_carrera

        # Asignatura
        lbl_asignatura = Label(frame, text="Asignatura: ")
        lbl_asignatura.grid(row=1, column=2, padx=1, pady=1, sticky=W)

        cbx_asignatura = Combobox(
            frame,
            state=READONLY,
            textvariable=self.var_asignatura,
        )
        cbx_asignatura.grid(row=1, column=3, padx=1, pady=1, sticky=EW)
        self.map_widgets['cbx_asignatura'] = cbx_asignatura

        # Fila 2: Tipo de Evento y Tipo de Actividad
        # Tipo de Evento
        lbl_tipo_evento = Label(frame, text="Tipo de Evento: ")
        lbl_tipo_evento.grid(row=2, column=0, padx=1, pady=1, sticky=W)

        cbx_tipo_evento = Combobox(
            frame,
            state=READONLY,
            textvariable=self.var_estado_actividad,
        )
        cbx_tipo_evento.grid(row=2, column=1, padx=1, pady=1, sticky=EW)
        self.map_widgets['cbx_tipo_evento'] = cbx_tipo_evento

        # Tipo de Actividad
        lbl_tipo_actividad = Label(frame, text="Tipo de Actividad: ")
        lbl_tipo_actividad.grid(row=2, column=2, padx=1, pady=1, sticky=W)

        cbx_tipo_actividad = Combobox(
            frame,
            state=READONLY,
            textvariable=self.var_tipo_actividad,
        )
        cbx_tipo_actividad.grid(row=2, column=3, padx=1, pady=1, sticky=EW)
        self.map_widgets['cbx_tipo_actividad'] = cbx_tipo_actividad

    def _frame_desplazar_meses(self, frame: Frame):
        """Frame para navegar entre meses."""
        # Botón mes anterior
        btn_anterior = Button(frame, text="◀ Anterior", bootstyle=OUTLINE, width=12)
        btn_anterior.pack(side=LEFT, padx=5, pady=5)
        self.map_widgets['btn_anterior'] = btn_anterior

        # Label con mes y año actual
        self.lbl_mes_año = Label(
            frame,
            text="dd, mm de yyy",
            bootstyle=INFO,
            font=("Helvetica", 12, "bold"),
            anchor=CENTER,
            justify=CENTER,
        )
        self.lbl_mes_año.pack(side=LEFT, padx=20, pady=5, expand=TRUE, fill=BOTH)
        self.map_widgets['lbl_mes_año'] = self.lbl_mes_año

        # Botón mes siguiente
        btn_siguiente = Button(frame, text="Siguiente ▶", bootstyle=OUTLINE, width=12)
        btn_siguiente.pack(side=LEFT, padx=5, pady=5)
        self.map_widgets['btn_siguiente'] = btn_siguiente

        # Botón hoy
        btn_hoy = Button(frame, text="Hoy", bootstyle=SUCCESS, width=10)
        btn_hoy.pack(side=LEFT, padx=5, pady=5)
        self.map_widgets['btn_hoy'] = btn_hoy

    def _frame_notebook(self, frame: Frame):
        note_book = Notebook(frame, bootstyle=PRIMARY)
        note_book.pack(side=TOP, padx=1, pady=1, fill=BOTH, expand=True)

        frame_calendario = Frame(frame, padding=(1, 1))
        note_book.add(frame_calendario, text="Calendario")
        self.map_widgets['frame_calendario'] = frame_calendario

        frame_agenda = Frame(frame, padding=(1, 1))
        note_book.add(frame_agenda, text="Agenda")
        self.map_widgets['frame_agenda'] = frame_agenda

    def _frame_treeview(self, frame: Frame):
        treeview_eventos = Treeview(frame, padding=(1, 1), bootstyle=PRIMARY)
        treeview_eventos.pack(side=TOP, fill=X, padx=5, pady=5)
        self.map_widgets['treeview_eventos'] = treeview_eventos

        # Agregar leyenda debajo del treeview
        frame_leyenda = Frame(frame, padding=(1, 1))
        self._frame_leyenda(frame=frame_leyenda)
        frame_leyenda.pack(side=TOP, fill=X, padx=5, pady=5)

    def _frame_leyenda(self, frame: Frame):
        """Crea la leyenda que explica los tipos de eventos."""
        # Label de título de la leyenda
        lbl_leyenda_titulo = Label(
            frame,
            text="Leyenda:",
            bootstyle=INFO,
            font=("Helvetica", 10, "bold"),
        )
        lbl_leyenda_titulo.pack(side=LEFT, padx=5, pady=5)

        Separator(frame, orient=VERTICAL).pack(side=LEFT, fill=Y, padx=10, pady=5)

        # Actividad - Inicio (SUCCESS)
        lbl_actividad_inicio = Label(
            frame,
            text="● Actividad [INICIO]",
            bootstyle=SUCCESS,
            font=("Helvetica", 9),
        )
        lbl_actividad_inicio.pack(side=LEFT, padx=10, pady=5)

        Separator(frame, orient=VERTICAL).pack(side=LEFT, fill=Y, padx=5, pady=5)

        # Actividad - Fin (WARNING)
        lbl_actividad_fin = Label(
            frame,
            text="● Actividad [FIN]",
            bootstyle=WARNING,
            font=("Helvetica", 9),
        )
        lbl_actividad_fin.pack(side=LEFT, padx=10, pady=5)

        Separator(frame, orient=VERTICAL).pack(side=LEFT, fill=Y, padx=5, pady=5)

        # Evento de Calendario (INFO)
        lbl_evento_calendario = Label(
            frame,
            text="● Evento de Calendario",
            bootstyle=INFO,
            font=("Helvetica", 9),
        )
        lbl_evento_calendario.pack(side=LEFT, padx=10, pady=5)

        Separator(frame, orient=VERTICAL).pack(side=LEFT, fill=Y, padx=10, pady=5)

        # Estadísticas del mes
        lbl_estadisticas_titulo = Label(
            frame,
            text="Estadísticas:",
            bootstyle=PRIMARY,
            font=("Helvetica", 10, "bold"),
        )
        lbl_estadisticas_titulo.pack(side=LEFT, padx=5, pady=5)

        # Frame para las estadísticas
        frame_stats = Frame(frame, padding=(1, 1))
        frame_stats.pack(side=LEFT, padx=10, pady=5, fill=BOTH, expand=True)

        # Label de estadísticas que se actualizará dinámicamente
        self.lbl_stats = Label(
            frame_stats,
            text="Cargando...",
            bootstyle=SECONDARY,
            font=("Helvetica", 9),
        )
        self.lbl_stats.pack(side=LEFT, padx=5, pady=5)

        # Guardar referencia para acceso desde el controlador
        self.map_widgets['lbl_stats'] = self.lbl_stats
