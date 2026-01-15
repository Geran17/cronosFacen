from ttkbootstrap import Frame, Label, StringVar, Separator, Combobox, Labelframe, Button
from typing import Dict, Any
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.scrolled import ScrolledFrame
from ui.ttk.styles.icons import *
from controladores.controlador_actividades import ControlarActividades


class FrameActividades(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        self.map_vars: Dict[Any, str] = {}
        self.map_widgets: Dict[Any, str] = {}

        # Vars
        self.var_estudiante = StringVar()
        self.map_vars['var_estudiante'] = self.var_estudiante

        self.var_carrera = StringVar()
        self.map_vars['var_carrera'] = self.var_carrera

        self.var_asignatura = StringVar()
        self.map_vars['var_asignatura'] = self.var_asignatura

        self.var_tipo_actividad = StringVar()
        self.map_vars['var_tipo_actividad'] = self.var_tipo_actividad

        # creamos los widgets
        self._crear_widgets()

        # Conectamos con el controlador
        ControlarActividades(map_widgets=self.map_widgets, map_vars=self.map_vars)

    def _crear_widgets(self):
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
        frame_titulo = Frame(frame, padding=(1, 1))
        frame_titulo.pack(side=LEFT, padx=1, pady=1, fill=X)
        lbl_titulo = Label(
            frame_titulo,
            text=f"{ICON_ACTIVIDAD} Acitividades del Estudiante",
            font=("Helvetica", 18, 'bold'),
            bootstyle=INFO,
        )
        lbl_titulo.pack(side=TOP, fill=X, padx=1, pady=10)

        lbl_subtitulo = Label(
            frame_titulo,
            text="Visualiza actividades academicas del estudiante",
            bootstyle=SECONDARY,
            font=("Helvetica", 9),
        )
        lbl_subtitulo.pack(side=TOP, fill=X, padx=1, pady=1)

        label_frame_datos = Labelframe(frame, padding=(1, 1), text="📈 Estadisticas")
        label_frame_datos.pack(side=LEFT, padx=1, pady=1, fill=X, expand=TRUE)
        self.map_widgets['label_frame_datos'] = label_frame_datos

    def _frame_central(self, frame: Frame):
        frame_filtrado = Labelframe(frame, text="Filtros", padding=(1, 1))
        self._frame_filtrado(frame=frame_filtrado)
        frame_filtrado.pack(side=TOP, fill=X, padx=1, pady=1, ipadx=5, ipady=5)

        scrolled_frame = ScrolledFrame(frame)
        scrolled_frame.pack(side=TOP, fill=BOTH, padx=1, pady=1, expand=TRUE)
        self.map_widgets['scrolled_frame'] = scrolled_frame

    def _frame_inferior(self, frame: Frame):
        """Frame inferior con botones de acción"""
        pass

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frames Funcionales
    # └────────────────────────────────────────────────────────────┘

    def _frame_filtrado(self, frame: Frame):
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        lbl_estudiante = Label(frame, text="Estudiante: ")
        lbl_estudiante.grid(row=0, column=0, padx=2, pady=2, sticky=EW)

        cbx_estudiantes = Combobox(frame, textvariable=self.var_estudiante, state=READONLY)
        cbx_estudiantes.grid(row=1, column=0, padx=2, pady=2, sticky=EW)
        self.map_widgets['cbx_estudiantes'] = cbx_estudiantes
        ToolTip(
            cbx_estudiantes,
            text="Seleccione un estudiante de la lista, para poder visualizar las carreras que esta cursando",
        )

        lbl_carreras = Label(frame, text="Carreras: ")
        lbl_carreras.grid(row=0, column=1, padx=2, pady=2, sticky=EW)

        cbx_carreras = Combobox(frame, state=READONLY, textvariable=self.var_carrera)
        cbx_carreras.grid(row=1, column=1, padx=2, pady=2, sticky=EW)
        self.map_widgets['cbx_carreras'] = cbx_carreras
        ToolTip(
            cbx_carreras,
            text="Seleccione un carrera de la lista, para poder visualizar las asignaturas que esta cursando",
        )

        lbl_asignaturas = Label(frame, text="Asignaturas: ")
        lbl_asignaturas.grid(row=2, column=0, padx=2, pady=2, sticky=EW)

        cbx_asignaturas = Combobox(frame, state=READONLY, textvariable=self.var_asignatura)
        cbx_asignaturas.grid(row=3, column=0, padx=2, pady=2, sticky=EW)
        self.map_widgets['cbx_asignaturas'] = cbx_asignaturas
        ToolTip(
            cbx_asignaturas,
            text="Seleccione una asignatura para visualizar las actividades de la misma",
        )

        lbl_tipo_actividad = Label(frame, text="Tipo de Actividades: ")
        lbl_tipo_actividad.grid(row=2, column=1, padx=2, pady=2, sticky=EW)

        cbx_tipo_actividades = Combobox(frame, state=READONLY, textvariable=self.var_tipo_actividad)
        cbx_tipo_actividades.grid(row=3, column=1, padx=2, pady=2, sticky=EW)
        self.map_widgets['cbx_tipo_actividades'] = cbx_tipo_actividades
        ToolTip(
            cbx_tipo_actividades,
            text="Seleccione un tipo de actividad para filtrar las actividades del estudiante",
        )
