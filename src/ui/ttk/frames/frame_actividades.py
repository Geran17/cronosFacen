from ttkbootstrap import Frame, Label, StringVar, Separator, Combobox, Labelframe, Button
from typing import Dict, Any
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.scrolled import ScrolledFrame
from ui.ttk.styles.estilos import PADDING_SM, PADDING_MD
from ui.ttk.styles.icons import *
from controladores.controlador_actividades import ControlarActividades


class FrameActividades(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        # Vars
        self.var_estudiante = StringVar()
        self.var_carrera = StringVar()
        self.var_asignatura = StringVar()
        self.var_tipo_actividad = StringVar()

        self.map_vars: Dict[str, Any] = {
            'var_estudiante': self.var_estudiante,
            'var_carrera': self.var_carrera,
            'var_asignatura': self.var_asignatura,
            'var_tipo_actividad': self.var_tipo_actividad,
        }

        self.map_widgets: Dict[str, Any] = {}

        # creamos los widgets
        self._crear_widgets()

        # Conectamos con el controlador
        ControlarActividades(map_widgets=self.map_widgets, map_vars=self.map_vars)

    def _crear_widgets(self):
        frame_superior = Frame(self, padding=(PADDING_SM, PADDING_SM))
        self._frame_superior(frame=frame_superior)
        frame_superior.pack(side=TOP, fill=X, padx=PADDING_SM, pady=PADDING_MD)

        frame_central = Frame(self, padding=(PADDING_SM, PADDING_SM))
        self._frame_central(frame=frame_central)
        frame_central.pack(side=TOP, fill=BOTH, padx=PADDING_SM, pady=PADDING_SM, expand=TRUE)

        frame_inferior = Frame(self, padding=(PADDING_SM, PADDING_SM))
        self._frame_inferior(frame=frame_inferior)
        frame_inferior.pack(side=TOP, fill=X, padx=PADDING_SM, pady=PADDING_SM)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Frames Principales
    # └────────────────────────────────────────────────────────────┘

    def _frame_superior(self, frame: Frame):
        frame_titulo = Frame(frame, padding=(PADDING_SM, PADDING_SM))
        frame_titulo.pack(side=LEFT, padx=1, pady=1, fill=X)
        lbl_titulo = Label(
            frame_titulo,
            text=f"{ICON_ACTIVIDAD} Actividades del Estudiante",
            bootstyle=INFO,
            style="Title.TLabel",
        )
        lbl_titulo.pack(side=TOP, fill=X, padx=1, pady=PADDING_MD)

        lbl_subtitulo = Label(
            frame_titulo,
            text="Visualiza actividades academicas del estudiante",
            bootstyle=SECONDARY,
            style="Subtitle.TLabel",
        )
        lbl_subtitulo.pack(side=TOP, fill=X, padx=1, pady=PADDING_SM)

        lbl_tip = Label(
            frame_titulo,
            text="Tip: clic derecho sobre una actividad para cambiar su estado",
            bootstyle="secondary",
            style="Small.TLabel",
        )
        lbl_tip.pack(side=TOP, fill=X, padx=1, pady=(0, PADDING_SM))

        label_frame_datos = Labelframe(
            frame, padding=(1, 1), text="📈 Estadisticas", style="Stats.TLabelframe"
        )
        label_frame_datos.pack(side=LEFT, padx=1, pady=1, fill=X, expand=TRUE)
        self.map_widgets['label_frame_datos'] = label_frame_datos

    def _frame_central(self, frame: Frame):
        frame_filtrado = Labelframe(frame, text="Filtros", padding=(PADDING_SM, PADDING_SM))
        self._frame_filtrado(frame=frame_filtrado)
        frame_filtrado.pack(
            side=TOP,
            fill=X,
            padx=1,
            pady=1,
            ipadx=PADDING_SM,
            ipady=PADDING_SM,
        )

        scrolled_frame = ScrolledFrame(frame)
        scrolled_frame.pack(side=TOP, fill=BOTH, padx=PADDING_SM, pady=PADDING_SM, expand=TRUE)
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

        lbl_estudiante = Label(frame, text="Estudiante:", style="FormLabel.TLabel")
        lbl_estudiante.grid(row=0, column=0, padx=PADDING_SM, pady=PADDING_SM, sticky=EW)

        cbx_estudiantes = Combobox(frame, textvariable=self.var_estudiante, state=READONLY)
        cbx_estudiantes.grid(row=1, column=0, padx=PADDING_SM, pady=PADDING_SM, sticky=EW)
        self.map_widgets['cbx_estudiantes'] = cbx_estudiantes
        ToolTip(
            cbx_estudiantes,
            text="Seleccione un estudiante de la lista, para poder visualizar las carreras que esta cursando",
        )

        lbl_carreras = Label(frame, text="Carreras:", style="FormLabel.TLabel")
        lbl_carreras.grid(row=0, column=1, padx=PADDING_SM, pady=PADDING_SM, sticky=EW)

        cbx_carreras = Combobox(frame, state=READONLY, textvariable=self.var_carrera)
        cbx_carreras.grid(row=1, column=1, padx=PADDING_SM, pady=PADDING_SM, sticky=EW)
        self.map_widgets['cbx_carreras'] = cbx_carreras
        ToolTip(
            cbx_carreras,
            text="Seleccione un carrera de la lista, para poder visualizar las asignaturas que esta cursando",
        )

        lbl_asignaturas = Label(frame, text="Asignaturas:", style="FormLabel.TLabel")
        lbl_asignaturas.grid(row=2, column=0, padx=PADDING_SM, pady=PADDING_SM, sticky=EW)

        cbx_asignaturas = Combobox(frame, state=READONLY, textvariable=self.var_asignatura)
        cbx_asignaturas.grid(row=3, column=0, padx=PADDING_SM, pady=PADDING_SM, sticky=EW)
        self.map_widgets['cbx_asignaturas'] = cbx_asignaturas
        ToolTip(
            cbx_asignaturas,
            text="Seleccione una asignatura para visualizar las actividades de la misma",
        )

        lbl_tipo_actividad = Label(
            frame, text="Tipo de Actividades:", style="FormLabel.TLabel"
        )
        lbl_tipo_actividad.grid(row=2, column=1, padx=PADDING_SM, pady=PADDING_SM, sticky=EW)

        cbx_tipo_actividades = Combobox(frame, state=READONLY, textvariable=self.var_tipo_actividad)
        cbx_tipo_actividades.grid(row=3, column=1, padx=PADDING_SM, pady=PADDING_SM, sticky=EW)
        self.map_widgets['cbx_tipo_actividades'] = cbx_tipo_actividades
        ToolTip(
            cbx_tipo_actividades,
            text="Seleccione un tipo de actividad para filtrar las actividades del estudiante",
        )
