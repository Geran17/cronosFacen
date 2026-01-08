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

        # cargamos los widgets
        self._crear_widgets()

        # Cargamos el controlador
        ControladorCalendario(map_widgets=self.map_widgets, map_vars=self.map_vars)

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
        self._frame_treeview(frame=frame)
        frame_treeview_eventos.pack(side=TOP, fill=X, padx=1, pady=1)

    def _frame_inferior(self, frame: Frame):
        pass

    def _frame_filtrado(self, frame: Frame):
        # Label Filtro
        lbl_filtro = Label(frame, text="Filtrar por: ", bootstyle=INFO)
        lbl_filtro.pack(side=LEFT, fill=X, padx=1, pady=1, ipadx=10)

        # Carrera
        lbl_carrera = Label(frame, text="Carrera: ")
        lbl_carrera.pack(side=LEFT, padx=1, pady=1, fill=X)

        cbx_carrera = Combobox(
            frame,
            state=READONLY,
            textvariable=self.var_carrera,
        )
        cbx_carrera.pack(side=LEFT, padx=1, pady=1, fill=X, expand=TRUE)
        self.map_widgets['cbx_carrera'] = cbx_carrera

        # Tipo Actividad
        lbl_tipo_actividad = Label(frame, text="Tipo: ")
        lbl_tipo_actividad.pack(side=LEFT, padx=1, pady=1, fill=X)

        cbx_tipo_actividad = Combobox(
            frame,
            state=READONLY,
            textvariable=self.var_tipo_actividad,
        )
        cbx_tipo_actividad.pack(side=LEFT, padx=1, pady=1, fill=X, expand=TRUE)
        self.map_widgets['cbx_tipo_actividad'] = cbx_tipo_actividad

        # Estado Actividad
        lbl_estado_actividad = Label(frame, text="Estado: ")
        lbl_estado_actividad.pack(side=LEFT, padx=1, pady=1, fill=X)

        cbx_estado_actividad = Combobox(
            frame, state=READONLY, textvariable=self.var_estado_actividad
        )
        cbx_estado_actividad.pack(side=LEFT, padx=1, pady=1, fill=X, expand=TRUE)
        self.map_widgets['cbx_estado_actividad'] = cbx_estado_actividad

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
