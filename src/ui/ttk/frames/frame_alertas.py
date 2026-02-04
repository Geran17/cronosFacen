from ttkbootstrap import (
    Frame,
    Label,
    StringVar,
    Separator,
    Combobox,
    Treeview,
    Scrollbar,
    Button,
)
from ttkbootstrap.constants import *
from typing import Dict, Any

from ui.ttk.styles.estilos import PADDING_XS, PADDING_SM
from ui.ttk.styles.icons import ICON_ALERTA
from ui.ttk.utils.layout import build_header
from controladores.controlador_alertas_actividades import ControladorAlertasActividades


class FrameAlertas(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        self.var_carrera = StringVar()
        self.var_asignatura = StringVar()
        self.var_tipo_actividad = StringVar()
        self.var_rango = StringVar()

        self.map_vars: Dict[str, Any] = {
            'var_carrera': self.var_carrera,
            'var_asignatura': self.var_asignatura,
            'var_tipo_actividad': self.var_tipo_actividad,
            'var_rango': self.var_rango,
        }

        self.map_widgets: Dict[str, Any] = {}

        self._crear_widgets()
        ControladorAlertasActividades(map_widgets=self.map_widgets, map_vars=self.map_vars)

    def _crear_widgets(self):
        frame_superior = Frame(self, padding=(PADDING_XS, PADDING_XS))
        build_header(
            frame_superior,
            f"{ICON_ALERTA} Alertas de Actividades",
            "Revisa actividades próximas a vencer o vencidas",
        )
        frame_superior.pack(side=TOP, fill=X, padx=PADDING_XS, pady=PADDING_XS)

        frame_central = Frame(self, padding=(PADDING_XS, PADDING_XS))
        self._frame_filtros(frame=frame_central)
        frame_central.pack(side=TOP, fill=X, padx=PADDING_XS, pady=PADDING_XS)

        frame_tabla = Frame(self, padding=(PADDING_XS, PADDING_XS))
        self._frame_tabla(frame=frame_tabla)
        frame_tabla.pack(side=TOP, fill=BOTH, padx=PADDING_XS, pady=PADDING_XS, expand=TRUE)

        frame_inferior = Frame(self, padding=(PADDING_XS, PADDING_XS))
        self._frame_inferior(frame=frame_inferior)
        frame_inferior.pack(side=TOP, fill=X, padx=PADDING_XS, pady=PADDING_XS)

    def _frame_filtros(self, frame: Frame):
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(3, weight=1)

        lbl_filtro = Label(frame, text="Filtros:", bootstyle=INFO)
        lbl_filtro.grid(row=0, column=0, padx=PADDING_XS, pady=PADDING_XS, sticky=W)

        lbl_carrera = Label(frame, text="Carrera:")
        lbl_carrera.grid(row=1, column=0, padx=PADDING_XS, pady=PADDING_XS, sticky=W)
        cbx_carrera = Combobox(frame, state=READONLY, textvariable=self.var_carrera)
        cbx_carrera.grid(row=1, column=1, padx=PADDING_XS, pady=PADDING_XS, sticky=EW)
        self.map_widgets['cbx_carrera'] = cbx_carrera

        lbl_asignatura = Label(frame, text="Asignatura:")
        lbl_asignatura.grid(row=1, column=2, padx=PADDING_XS, pady=PADDING_XS, sticky=W)
        cbx_asignatura = Combobox(frame, state=READONLY, textvariable=self.var_asignatura)
        cbx_asignatura.grid(row=1, column=3, padx=PADDING_XS, pady=PADDING_XS, sticky=EW)
        self.map_widgets['cbx_asignatura'] = cbx_asignatura

        lbl_tipo = Label(frame, text="Tipo Actividad:")
        lbl_tipo.grid(row=2, column=0, padx=PADDING_XS, pady=PADDING_XS, sticky=W)
        cbx_tipo = Combobox(frame, state=READONLY, textvariable=self.var_tipo_actividad)
        cbx_tipo.grid(row=2, column=1, padx=PADDING_XS, pady=PADDING_XS, sticky=EW)
        self.map_widgets['cbx_tipo_actividad'] = cbx_tipo

        lbl_rango = Label(frame, text="Rango:")
        lbl_rango.grid(row=2, column=2, padx=PADDING_XS, pady=PADDING_XS, sticky=W)
        cbx_rango = Combobox(frame, state=READONLY, textvariable=self.var_rango)
        cbx_rango.grid(row=2, column=3, padx=PADDING_XS, pady=PADDING_XS, sticky=EW)
        self.map_widgets['cbx_rango'] = cbx_rango

        Separator(frame).grid(
            row=3, column=0, columnspan=4, sticky=EW, padx=PADDING_XS, pady=PADDING_XS
        )

        btn_aplicar = Button(frame, text="Aplicar Filtros", bootstyle=SUCCESS)
        btn_aplicar.grid(row=4, column=0, padx=PADDING_XS, pady=PADDING_SM, sticky=W)
        self.map_widgets['btn_aplicar'] = btn_aplicar

        btn_refrescar = Button(frame, text="Refrescar", bootstyle=INFO)
        btn_refrescar.grid(row=4, column=1, padx=PADDING_XS, pady=PADDING_SM, sticky=W)
        self.map_widgets['btn_refrescar'] = btn_refrescar

        btn_limpiar = Button(frame, text="Limpiar", bootstyle=WARNING)
        btn_limpiar.grid(row=4, column=2, padx=PADDING_XS, pady=PADDING_SM, sticky=W)
        self.map_widgets['btn_limpiar'] = btn_limpiar

        lbl_stats = Label(frame, text="Total: 0", bootstyle=SECONDARY)
        lbl_stats.grid(
            row=4, column=3, padx=PADDING_XS, pady=PADDING_SM, sticky=E
        )
        self.map_widgets['lbl_stats'] = lbl_stats

    def _frame_tabla(self, frame: Frame):
        columns = (
            "titulo",
            "carrera",
            "asignatura",
            "tipo",
            "fecha_fin",
            "dias",
            "estado",
        )
        tree = Treeview(frame, columns=columns, show="headings", height=12)
        tree.pack(side=LEFT, fill=BOTH, expand=TRUE)

        tree.heading("titulo", text="Título")
        tree.heading("carrera", text="Carrera")
        tree.heading("asignatura", text="Asignatura")
        tree.heading("tipo", text="Tipo")
        tree.heading("fecha_fin", text="Fecha Fin")
        tree.heading("dias", text="Días")
        tree.heading("estado", text="Estado")

        tree.column("titulo", width=220, stretch=True)
        tree.column("carrera", width=160, stretch=True)
        tree.column("asignatura", width=160, stretch=True)
        tree.column("tipo", width=120, stretch=False)
        tree.column("fecha_fin", width=110, stretch=False)
        tree.column("dias", width=70, stretch=False, anchor=CENTER)
        tree.column("estado", width=140, stretch=False)

        scroll_y = Scrollbar(frame, orient=VERTICAL, command=tree.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        tree.configure(yscrollcommand=scroll_y.set)

        self.map_widgets['tree_alertas'] = tree

    def _frame_inferior(self, frame: Frame):
        lbl_hint = Label(
            frame,
            text="Tip: Ajusta el rango para priorizar vencidas o próximas a vencer.",
            bootstyle=SECONDARY,
        )
        lbl_hint.pack(side=LEFT, padx=PADDING_SM, pady=PADDING_SM)
