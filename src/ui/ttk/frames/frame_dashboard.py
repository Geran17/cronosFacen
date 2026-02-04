from ttkbootstrap import (
    Frame,
    Label,
    StringVar,
    Separator,
    Combobox,
    Labelframe,
    Button,
    Progressbar,
    Treeview,
    Scrollbar,
)
from ttkbootstrap.constants import *
from typing import Dict, Any

from ui.ttk.styles.estilos import PADDING_XS, PADDING_SM, PADDING_MD
from ui.ttk.styles.icons import ICON_ESTADISTICAS
from ui.ttk.utils.layout import build_header
from controladores.controlador_dashboard import ControladorDashboard


class FrameDashboard(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        self.var_estudiante = StringVar()
        self.var_carrera = StringVar()

        self.map_vars: Dict[str, Any] = {
            "var_estudiante": self.var_estudiante,
            "var_carrera": self.var_carrera,
        }
        self.map_widgets: Dict[str, Any] = {}

        self._crear_widgets()
        ControladorDashboard(map_widgets=self.map_widgets, map_vars=self.map_vars)

    def _crear_widgets(self):
        frame_superior = Frame(self, padding=(PADDING_XS, PADDING_XS))
        build_header(
            frame_superior,
            f"{ICON_ESTADISTICAS} Dashboard",
            "Resumen de progreso y próximos eventos",
        )
        frame_superior.pack(side=TOP, fill=X, padx=PADDING_XS, pady=PADDING_XS)

        frame_filtros = Frame(self, padding=(PADDING_XS, PADDING_XS))
        self._frame_filtros(frame_filtros)
        frame_filtros.pack(side=TOP, fill=X, padx=PADDING_XS, pady=PADDING_XS)

        frame_resumen = Frame(self, padding=(PADDING_XS, PADDING_XS))
        self._frame_resumen(frame_resumen)
        frame_resumen.pack(side=TOP, fill=X, padx=PADDING_XS, pady=PADDING_XS)

        frame_central = Frame(self, padding=(PADDING_XS, PADDING_XS))
        self._frame_central(frame_central)
        frame_central.pack(side=TOP, fill=BOTH, padx=PADDING_XS, pady=PADDING_XS, expand=TRUE)

    def _frame_filtros(self, frame: Frame):
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(3, weight=1)

        Label(frame, text="Estudiante:", style="FormLabel.TLabel").grid(
            row=0, column=0, sticky=W, padx=PADDING_XS, pady=PADDING_XS
        )
        cbx_est = Combobox(frame, state=READONLY, textvariable=self.var_estudiante)
        cbx_est.grid(row=0, column=1, sticky=EW, padx=PADDING_XS, pady=PADDING_XS)
        self.map_widgets["cbx_estudiante"] = cbx_est

        Label(frame, text="Carrera:", style="FormLabel.TLabel").grid(
            row=0, column=2, sticky=W, padx=PADDING_XS, pady=PADDING_XS
        )
        cbx_carr = Combobox(frame, state=READONLY, textvariable=self.var_carrera)
        cbx_carr.grid(row=0, column=3, sticky=EW, padx=PADDING_XS, pady=PADDING_XS)
        self.map_widgets["cbx_carrera"] = cbx_carr

        btn_ref = Button(frame, text="Refrescar", bootstyle=INFO)
        btn_ref.grid(row=0, column=4, sticky=E, padx=PADDING_XS, pady=PADDING_XS)
        self.map_widgets["btn_refrescar"] = btn_ref

        Separator(frame).grid(row=1, column=0, columnspan=5, sticky=EW, pady=(2, 0))

    def _frame_resumen(self, frame: Frame):
        for col in range(4):
            frame.columnconfigure(col, weight=1)

        def _card(parent, title: str):
            card = Labelframe(parent, text=title, padding=(PADDING_SM, PADDING_SM))
            value = Label(card, text="—", style="Title.TLabel")
            value.pack(anchor=W)
            hint = Label(card, text="", style="Small.TLabel", bootstyle="secondary")
            hint.pack(anchor=W)
            return card, value, hint

        self.card_prog, self.lbl_prog, self.lbl_prog_hint = _card(frame, "Progreso Carrera")
        self.card_asig, self.lbl_asig, self.lbl_asig_hint = _card(frame, "Asignaturas")
        self.card_act, self.lbl_act, self.lbl_act_hint = _card(frame, "Actividades")
        self.card_prox, self.lbl_prox, self.lbl_prox_hint = _card(frame, "Próxima entrega")

        self.map_widgets["lbl_prog"] = self.lbl_prog
        self.map_widgets["lbl_prog_hint"] = self.lbl_prog_hint
        self.map_widgets["lbl_asig"] = self.lbl_asig
        self.map_widgets["lbl_asig_hint"] = self.lbl_asig_hint
        self.map_widgets["lbl_act"] = self.lbl_act
        self.map_widgets["lbl_act_hint"] = self.lbl_act_hint
        self.map_widgets["lbl_prox"] = self.lbl_prox
        self.map_widgets["lbl_prox_hint"] = self.lbl_prox_hint

        self.card_prog.grid(row=0, column=0, sticky=EW, padx=PADDING_XS, pady=PADDING_XS)
        self.card_asig.grid(row=0, column=1, sticky=EW, padx=PADDING_XS, pady=PADDING_XS)
        self.card_act.grid(row=0, column=2, sticky=EW, padx=PADDING_XS, pady=PADDING_XS)
        self.card_prox.grid(row=0, column=3, sticky=EW, padx=PADDING_XS, pady=PADDING_XS)

    def _frame_central(self, frame: Frame):
        frame.columnconfigure(0, weight=2)
        frame.columnconfigure(1, weight=1)

        lf_eventos = Labelframe(frame, text="Próximos 7 días", padding=PADDING_SM)
        lf_eventos.grid(row=0, column=0, sticky=NSEW, padx=PADDING_XS, pady=PADDING_XS)

        columns = ("fecha", "titulo", "dias")
        tree = Treeview(lf_eventos, columns=columns, show="headings", height=10)
        tree.heading("fecha", text="Fecha")
        tree.heading("titulo", text="Actividad")
        tree.heading("dias", text="Días")
        tree.column("fecha", width=90, anchor=CENTER)
        tree.column("titulo", width=260, anchor=W)
        tree.column("dias", width=60, anchor=CENTER)
        tree.pack(side=LEFT, fill=BOTH, expand=TRUE)

        scroll_y = Scrollbar(lf_eventos, orient=VERTICAL, command=tree.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        tree.configure(yscrollcommand=scroll_y.set)
        self.map_widgets["tree_eventos"] = tree

        lf_progreso = Labelframe(frame, text="Progreso por semestre", padding=PADDING_SM)
        lf_progreso.grid(row=0, column=1, sticky=NSEW, padx=PADDING_XS, pady=PADDING_XS)

        cont = Frame(lf_progreso)
        cont.pack(fill=BOTH, expand=TRUE)
        self.map_widgets["frame_progreso"] = cont
