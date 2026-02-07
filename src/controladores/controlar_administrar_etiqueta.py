from typing import Dict, Any, List
from tkinter.messagebox import askyesno, showinfo
from ttkbootstrap import Button, StringVar, IntVar, Label, Entry
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview

from modelos.services.etiqueta_service import EtiquetaService
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class ControlarAdministrarEtiqueta:

    def __init__(
        self,
        master=None,
        map_widgets: Dict[str, Any] = None,
        map_vars: Dict[str, Any] = None,
    ):
        self.master = master
        self.map_widgets = map_widgets
        self.map_vars = map_vars

        self.lista_etiquetas: List[EtiquetaService] = []
        self.indice_actual: int = -1

        self._cargar_widgets()
        self._cargar_vars()
        self._actualizar_estadisticas()
        self._actualizar_tabla_etiquetas()
        self._vincular_eventos()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Métodos Privados
    # └────────────────────────────────────────────────────────────┘
    def _vincular_eventos(self):
        self.tabla_etiquetas.view.bind("<Double-Button-1>", self._on_tabla_doble_click)
        self.btn_nuevo.config(command=self._on_nuevo)
        self.btn_aplicar.config(command=self._on_aplicar)
        self.btn_eliminar.config(command=self._on_eliminar_etiqueta)
        self.btn_primero.config(command=self._on_primero)
        self.btn_anterior.config(command=self._on_anterior)
        self.btn_siguiente.config(command=self._on_siguiente)
        self.btn_ultimo.config(command=self._on_ultimo)

    def _establecer_etiqueta(self) -> EtiquetaService:
        etiqueta = EtiquetaService(ruta_db=None)
        etiqueta.id_etiqueta = self.var_id_etiqueta.get()
        etiqueta.nombre = self.var_nombre.get()
        return etiqueta

    def _cargar_formulario(self, etiqueta: EtiquetaService):
        if etiqueta:
            self.var_id_etiqueta.set(etiqueta.id_etiqueta)
            self.var_nombre.set(etiqueta.nombre)
            self._actualizar_estadisticas_etiqueta(etiqueta.id_etiqueta)

    def _limpiar_formulario(self):
        self.var_id_etiqueta.set(0)
        self.var_nombre.set("")

    def _insertar_fila(self, etiqueta: EtiquetaService):
        if etiqueta:
            self.tabla_etiquetas.insert_row(
                index=END,
                values=(
                    etiqueta.id_etiqueta,
                    etiqueta.nombre,
                ),
            )

    def _actualizar_tabla_etiquetas(self):
        self._obtener_etiquetas()
        if self.lista_etiquetas:
            self.tabla_etiquetas.delete_rows()
            for etiqueta in self.lista_etiquetas:
                self._insertar_fila(etiqueta=etiqueta)
            self.tabla_etiquetas.autofit_columns()

    def _obtener_etiquetas(self):
        if self.lista_etiquetas:
            self.lista_etiquetas.clear()

        servicio = EtiquetaService(ruta_db=None)
        lista_aux = servicio.obtener_todas()
        for data in lista_aux:
            etiqueta = EtiquetaService(ruta_db=None)
            etiqueta.set_data(data=data)
            self.lista_etiquetas.append(etiqueta)

    def _cargar_vars(self):
        self.var_id_etiqueta: IntVar = self.map_vars['var_id_etiqueta']
        self.var_nombre: StringVar = self.map_vars['var_nombre']

    def _cargar_widgets(self):
        self.tabla_etiquetas: Tableview = self.map_widgets['tabla_etiquetas']
        self.lbl_estadisticas: Label = self.map_widgets['lbl_estadisticas']
        self.btn_nuevo: Button = self.map_widgets['btn_nuevo']
        self.btn_aplicar: Button = self.map_widgets['btn_aplicar']
        self.btn_eliminar: Button = self.map_widgets['btn_eliminar']
        self.btn_primero: Button = self.map_widgets['btn_primero']
        self.btn_anterior: Button = self.map_widgets['btn_anterior']
        self.btn_siguiente: Button = self.map_widgets['btn_siguiente']
        self.btn_ultimo: Button = self.map_widgets['btn_ultimo']
        self.entry_nombre: Entry = self.map_widgets['entry_nombre']

    def _actualizar_estadisticas(self):
        self._obtener_etiquetas()
        cant_etiquetas = len(self.lista_etiquetas) if self.lista_etiquetas else 0
        self.lbl_estadisticas['text'] = f"Etiquetas: {cant_etiquetas}"

    def _actualizar_estadisticas_etiqueta(self, id_etiqueta: int):
        try:
            if id_etiqueta <= 0:
                self.lbl_estadisticas['text'] = "Etiquetas: 0"
                return
            nombre = self.var_nombre.get()
            self.lbl_estadisticas['text'] = f"Etiqueta: {nombre}"
        except Exception as e:
            logger.error(f"Error al actualizar estadísticas de etiqueta: {e}")
            self.lbl_estadisticas['text'] = "Error al cargar estadísticas"

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘
    def _on_tabla_doble_click(self, _event):
        seleccion = self.tabla_etiquetas.view.selection()
        if not seleccion:
            return
        item = self.tabla_etiquetas.view.item(seleccion[0])
        valores = item['values']
        id_etiqueta = int(valores[0])
        etiqueta = EtiquetaService(ruta_db=None)
        etiqueta.id_etiqueta = id_etiqueta
        if etiqueta.instanciar():
            self._cargar_formulario(etiqueta=etiqueta)

    def _on_nuevo(self):
        self._limpiar_formulario()

    def _on_aplicar(self):
        etiqueta = self._establecer_etiqueta()
        if etiqueta:
            if etiqueta.id_etiqueta == 0 or etiqueta.id_etiqueta is None:
                id_etiqueta = etiqueta.insertar()
                if id_etiqueta != 0:
                    self.var_id_etiqueta.set(id_etiqueta)
                    showinfo(parent=self.master, title="Inserción", message="Etiqueta insertada con éxito!")
                    self._actualizar_tabla_etiquetas()
            else:
                if etiqueta.actualizar():
                    showinfo(parent=self.master, title="Actualización", message="Etiqueta actualizada correctamente")
                    self._actualizar_tabla_etiquetas()

    def _on_eliminar_etiqueta(self):
        id_etiqueta = self.var_id_etiqueta.get()
        if id_etiqueta == 0 or id_etiqueta is None:
            showinfo(parent=self.master, title="Advertencia", message="Debe seleccionar una etiqueta para eliminar")
            return

        nombre = self.var_nombre.get()
        confirmacion = askyesno(
            parent=self.master,
            title="Confirmación",
            message=f"¿Desea eliminar la etiqueta '{nombre}'?",
        )

        if not confirmacion:
            return

        etiqueta = EtiquetaService(ruta_db=None)
        etiqueta.id_etiqueta = id_etiqueta
        try:
            if etiqueta.eliminar():
                showinfo(parent=self.master, title="Eliminación", message="Etiqueta eliminada exitosamente")
                self._limpiar_formulario()
                self._actualizar_tabla_etiquetas()
            else:
                showinfo(parent=self.master, title="Error", message="Error al eliminar la etiqueta")
        except Exception as e:
            logger.error(f"Excepción al eliminar etiqueta: {str(e)}")
            showinfo(parent=self.master, title="Error", message=f"Error inesperado: {str(e)}")

    def _on_primero(self):
        if self.lista_etiquetas:
            self.indice_actual = 0
            self._cargar_formulario(etiqueta=self.lista_etiquetas[self.indice_actual])
        else:
            showinfo(parent=self.master, title="Información", message="No hay etiquetas para mostrar")

    def _on_anterior(self):
        if not self.lista_etiquetas:
            showinfo(parent=self.master, title="Información", message="No hay etiquetas para mostrar")
            return
        if self.indice_actual > 0:
            self.indice_actual -= 1
            self._cargar_formulario(etiqueta=self.lista_etiquetas[self.indice_actual])
        else:
            showinfo(parent=self.master, title="Información", message="Ya está en la primera etiqueta")

    def _on_siguiente(self):
        if not self.lista_etiquetas:
            showinfo(parent=self.master, title="Información", message="No hay etiquetas para mostrar")
            return
        if self.indice_actual < len(self.lista_etiquetas) - 1:
            self.indice_actual += 1
            self._cargar_formulario(etiqueta=self.lista_etiquetas[self.indice_actual])
        else:
            showinfo(parent=self.master, title="Información", message="Ya está en la última etiqueta")

    def _on_ultimo(self):
        if self.lista_etiquetas:
            self.indice_actual = len(self.lista_etiquetas) - 1
            self._cargar_formulario(etiqueta=self.lista_etiquetas[self.indice_actual])
        else:
            showinfo(parent=self.master, title="Información", message="No hay etiquetas para mostrar")
