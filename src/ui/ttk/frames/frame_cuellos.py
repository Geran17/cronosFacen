from ttkbootstrap import Frame, Label, StringVar, Separator, Combobox, Button, Text
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from typing import Dict, Any, List

from ui.ttk.styles.estilos import PADDING_SM, PADDING_XS
from ui.ttk.styles.icons import ICON_ESTADISTICAS, ICON_CUELLOS
from controladores.controlador_cuellos import ControladorCuellos


class FrameCuellos(Frame):
    """Frame para visualizar cuellos de botella estructurales por carrera."""

    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        self.var_carrera = StringVar()
        self.var_top = StringVar(value="10")
        self.map_vars: Dict[str, Any] = {
            'var_carrera': self.var_carrera,
            'var_top': self.var_top,
        }
        self.map_widgets: Dict[str, Any] = {}

        self._crear_widgets()

        # Referencia del frame
        self.map_widgets['frame_cuellos'] = self

        # Controlador
        self.controlador = ControladorCuellos(map_widgets=self.map_widgets, map_vars=self.map_vars)

    def _crear_widgets(self) -> None:
        frame_superior = Frame(self, padding=(PADDING_XS, PADDING_XS))
        self._frame_superior(frame_superior)
        frame_superior.pack(side=TOP, fill=X, padx=PADDING_XS, pady=PADDING_SM)

        frame_central = Frame(self, padding=(PADDING_XS, PADDING_XS))
        self._frame_central(frame_central)
        frame_central.pack(side=TOP, fill=BOTH, padx=PADDING_XS, pady=PADDING_XS, expand=TRUE)

    def _frame_superior(self, frame: Frame) -> None:
        lbl_titulo = Label(
            frame,
            text=f"{ICON_CUELLOS} Cuellos de botella estructurales",
            style="Title.TLabel",
            bootstyle=INFO,
        )
        lbl_titulo.pack(side=TOP, fill=X, padx=1, pady=PADDING_SM)

        lbl_sub = Label(
            frame,
            text="Mide cuántas asignaturas dependen de cada asignatura",
            bootstyle=SECONDARY,
            style="Subtitle.TLabel",
        )
        lbl_sub.pack(side=TOP, fill=X, padx=1, pady=(0, PADDING_SM))

        Separator(frame).pack(side=TOP, fill=X, padx=1, pady=1)

    def _frame_central(self, frame: Frame) -> None:
        frame_filtros = Frame(frame)
        frame_filtros.pack(side=TOP, fill=X, pady=(0, PADDING_SM))

        lbl_carrera = Label(frame_filtros, text="Carrera:", style="FormLabel.TLabel")
        lbl_carrera.pack(side=LEFT, padx=(0, PADDING_XS))

        cbx_carrera = Combobox(frame_filtros, textvariable=self.var_carrera, state=READONLY)
        cbx_carrera.pack(side=LEFT, fill=X, expand=TRUE, padx=(0, PADDING_XS))
        self.map_widgets['cbx_carrera'] = cbx_carrera

        lbl_top = Label(frame_filtros, text="Top:", style="FormLabel.TLabel")
        lbl_top.pack(side=LEFT, padx=(PADDING_SM, PADDING_XS))

        cbx_top = Combobox(
            frame_filtros,
            textvariable=self.var_top,
            state=READONLY,
            values=("5", "10", "15", "20", "50", "100", "Todos"),
            width=8,
        )
        cbx_top.pack(side=LEFT, padx=(0, PADDING_XS))
        self.map_widgets['cbx_top'] = cbx_top

        btn_refrescar = Button(frame_filtros, text="🔄 Refrescar", bootstyle=WARNING)
        btn_refrescar.pack(side=LEFT)
        self.map_widgets['btn_refrescar'] = btn_refrescar

        self.tabla = Tableview(
            frame,
            searchable=True,
            paginated=True,
            coldata=[
                {'text': 'Id', 'stretch': False, 'anchor': 'e'},
                {'text': 'Codigo', 'stretch': False, 'anchor': 'center'},
                {'text': 'Asignatura', 'stretch': True, 'anchor': 'w'},
                {'text': 'Semestre', 'stretch': False, 'anchor': 'center'},
                {'text': 'Bloqueo Directo', 'stretch': False, 'anchor': 'e'},
                {'text': 'Bloqueo Total', 'stretch': False, 'anchor': 'e'},
            ],
            bootstyle="primary",
        )
        self.tabla.pack(side=TOP, fill=BOTH, padx=PADDING_SM, pady=PADDING_SM, expand=TRUE)
        self.map_widgets['tabla_cuellos'] = self.tabla

        Separator(frame).pack(side=TOP, fill=X, padx=PADDING_SM, pady=(0, PADDING_SM))

        self.lbl_detalle = Label(frame, text="Detalle de selección", style="FormLabel.TLabel")
        self.lbl_detalle.pack(side=TOP, anchor=W, padx=PADDING_SM, pady=(0, PADDING_XS))

        frame_detalle = Frame(frame)
        frame_detalle.pack(side=TOP, fill=BOTH, padx=PADDING_SM, pady=(0, PADDING_SM))
        frame_detalle.columnconfigure(0, weight=1)
        frame_detalle.columnconfigure(1, weight=1)

        lbl_directo = Label(
            frame_detalle, text="Asignaturas bloqueadas (directo):", style="Small.TLabel"
        )
        lbl_directo.grid(row=0, column=0, sticky=W, padx=(0, PADDING_SM), pady=(0, 2))

        lbl_total = Label(
            frame_detalle, text="Asignaturas bloqueadas (total):", style="Small.TLabel"
        )
        lbl_total.grid(row=0, column=1, sticky=W, padx=(0, PADDING_SM), pady=(0, 2))

        self.txt_directos = Text(frame_detalle, height=6, wrap=WORD)
        self.txt_directos.grid(row=1, column=0, sticky="nsew", padx=(0, PADDING_SM))
        self.map_widgets['txt_directos'] = self.txt_directos

        self.txt_totales = Text(frame_detalle, height=6, wrap=WORD)
        self.txt_totales.grid(row=1, column=1, sticky="nsew")
        self.map_widgets['txt_totales'] = self.txt_totales

        self._set_text(self.txt_directos, "Selecciona una asignatura para ver el detalle.")
        self._set_text(self.txt_totales, "Selecciona una asignatura para ver el detalle.")

    def mostrar_resultados(self, resultados: List[Dict[str, Any]]) -> None:
        """Carga los resultados en la tabla."""
        self.tabla.delete_rows()
        rows = []
        for item in resultados:
            rows.append(
                (
                    item['id_asignatura'],
                    item['codigo'],
                    item['nombre'],
                    item.get('semestre') or "-",
                    item['bloquea_directo'],
                    item['bloquea_total'],
                )
            )
        self.tabla.insert_rows('end', rows)

    def mostrar_detalle(self, nombre: str, directos: List[str], totales: List[str]) -> None:
        self.lbl_detalle.config(text=f"Detalle de selección: {nombre}")
        self._set_text(self.txt_directos, "\n".join(directos) if directos else "-")
        self._set_text(self.txt_totales, "\n".join(totales) if totales else "-")

    def limpiar_detalle(self) -> None:
        self.lbl_detalle.config(text="Detalle de selección")
        self._set_text(self.txt_directos, "Selecciona una asignatura para ver el detalle.")
        self._set_text(self.txt_totales, "Selecciona una asignatura para ver el detalle.")

    @staticmethod
    def _set_text(widget: Text, value: str) -> None:
        widget.config(state=NORMAL)
        widget.delete("1.0", END)
        widget.insert("1.0", value)
        widget.config(state=DISABLED)
