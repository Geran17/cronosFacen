from typing import Dict, Any, List, Optional
from tkinter.messagebox import askyesno, showinfo
from ttkbootstrap import Button, Entry, StringVar, IntVar, Label, Combobox, Checkbutton
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from modelos.daos.calendario_evento_dao import CalendarioEventoDAO
from modelos.services.calendario_evento_service import CalendarioEventoService
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class ControlarAdministrarCalendario:

    def __init__(
        self,
        master=None,
        map_widgets: Dict[str, Any] = None,
        map_vars: Dict[str, Any] = None,
    ):
        # Variables y Widgets del Frame
        self.master = master
        self.map_widgets = map_widgets
        self.map_vars = map_vars

        # Creamos una lista vacia
        # para almacenar los eventos
        self.lista_eventos: List[CalendarioEventoService] = []

        # Índice del evento actual en la navegación
        self.indice_actual: int = -1

        # cargar widgets
        self._cargar_widgets()

        # cargar los vars
        self._cargar_vars()

        # mostrar las estadistica en el panel inferior
        self._actualizar_estadisticas()

        # mostramos los eventos en la tabla
        self._actualizar_tabla_evento()

        # viculamos los eventos
        self._vincular_eventos()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos Privados
    # └────────────────────────────────────────────────────────────┘
    def _vincular_eventos(self):
        # Vincular el evento de doble clic
        self.tabla_evento.view.bind("<Double-Button-1>", self._on_tabla_doble_click)
        # Vinculamos el evento nuevo
        self.btn_nuevo.config(command=self._on_nuevo)
        self.btn_aplicar.config(command=self._on_aplicar)
        self.btn_eliminar.config(command=self._on_eliminar_evento)
        # Vinculamos los botones de desplazamiento
        self.btn_primero.config(command=self._on_primero)
        self.btn_anterior.config(command=self._on_anterior)
        self.btn_siguiente.config(command=self._on_siguiente)
        self.btn_ultimo.config(command=self._on_ultimo)

    def _establecer_evento(self) -> CalendarioEventoService:
        evento = CalendarioEventoService(ruta_db=None)
        # establecemos variables
        id_evento = self.var_id_evento.get()
        titulo = self.var_titulo.get()
        tipo = self.var_tipo.get()
        fecha_inicio = self.var_fecha_inicio.get()
        fecha_fin = self.var_fecha_fin.get()
        afecta_actividades = self.var_afecta_actividades.get()
        # cargamos los datos al evento
        evento.id_evento = id_evento
        evento.titulo = titulo
        evento.tipo = tipo
        evento.fecha_inicio = fecha_inicio
        evento.fecha_fin = fecha_fin
        evento.afecta_actividades = afecta_actividades
        return evento

    def _cargar_formulario(self, evento: CalendarioEventoService):
        if evento:
            self.var_id_evento.set(evento.id_evento)
            self.var_titulo.set(evento.titulo)
            self.var_tipo.set(evento.tipo or "")
            self.var_fecha_inicio.set(evento.fecha_inicio or "")
            self.var_fecha_fin.set(evento.fecha_fin or "")
            self.var_afecta_actividades.set(evento.afecta_actividades or 0)
            # Actualizar estadísticas del evento seleccionado
            self._actualizar_estadisticas_evento(evento.id_evento)

    def _limpiar_formulario(self):
        self.var_id_evento.set(0)
        self.var_titulo.set("")
        self.var_tipo.set("")
        self.var_fecha_inicio.set("")
        self.var_fecha_fin.set("")
        self.var_afecta_actividades.set(0)

    def _insertar_fila(self, evento: CalendarioEventoService):
        if evento:
            # Mostrar Sí/No para afecta_actividades
            afecta_texto = "Sí" if evento.afecta_actividades == 1 else "No"

            self.tabla_evento.insert_row(
                index=END,
                values=(
                    evento.id_evento,
                    evento.titulo,
                    evento.tipo or "",
                    evento.fecha_inicio or "",
                    evento.fecha_fin or "",
                    afecta_texto,
                ),
            )

    def _actualizar_tabla_evento(self):
        # obtenemos la lista de eventos
        self._obtener_eventos()
        if self.lista_eventos:
            # limpiamos la tabla
            self.tabla_evento.delete_rows()
            for evento in self.lista_eventos:
                self._insertar_fila(evento=evento)

            # ajustamos las columnas
            self.tabla_evento.autofit_columns()

    def _obtener_eventos(self):
        if self.lista_eventos:
            self.lista_eventos.clear()

        dao = CalendarioEventoDAO(ruta_db=None)
        sql = "SELECT * FROM calendario_evento ORDER BY fecha_inicio DESC"
        params = ()
        lista_aux = dao.ejecutar_consulta(sql=sql, params=params)
        if lista_aux:
            for data in lista_aux:
                evento = CalendarioEventoService(ruta_db=None)
                evento.set_data(data=data)
                self.lista_eventos.append(evento)

    def _cargar_vars(self):
        self.var_id_evento: IntVar = self.map_vars['var_id_evento']
        self.var_titulo: StringVar = self.map_vars['var_titulo']
        self.var_tipo: StringVar = self.map_vars['var_tipo']
        self.var_fecha_inicio: StringVar = self.map_vars['var_fecha_inicio']
        self.var_fecha_fin: StringVar = self.map_vars['var_fecha_fin']
        self.var_afecta_actividades: IntVar = self.map_vars['var_afecta_actividades']

    def _cargar_widgets(self):
        self.tabla_evento: Tableview = self.map_widgets['tabla_evento']
        self.lbl_estadisticas: Label = self.map_widgets['lbl_estadisticas']
        self.btn_nuevo: Button = self.map_widgets['btn_nuevo']
        self.btn_aplicar: Button = self.map_widgets['btn_aplicar']
        self.btn_eliminar: Button = self.map_widgets['btn_eliminar']
        self.btn_primero: Button = self.map_widgets['btn_primero']
        self.btn_anterior: Button = self.map_widgets['btn_anterior']
        self.btn_siguiente: Button = self.map_widgets['btn_siguiente']
        self.btn_ultimo: Button = self.map_widgets['btn_ultimo']
        self.cbx_tipo: Combobox = self.map_widgets['cbx_tipo']
        self.chk_afecta_actividades: Checkbutton = self.map_widgets['chk_afecta_actividades']

    def _actualizar_estadisticas(self):
        # actualizamos la lista de eventos
        self._obtener_eventos()
        cant_eventos = 0
        if self.lista_eventos:
            cant_eventos = len(self.lista_eventos)

        msg = f"Eventos del Calendario: {cant_eventos}"

        self.lbl_estadisticas['text'] = msg

    def _actualizar_estadisticas_evento(self, id_evento: int):
        """
        Actualiza las estadísticas mostrando la información
        del evento seleccionado.

        Args:
            id_evento (int): ID del evento seleccionado
        """
        try:
            if id_evento <= 0:
                self.lbl_estadisticas['text'] = "Eventos del Calendario: 0"
                return

            # Obtener título del evento
            titulo_evento = self.var_titulo.get()
            tipo_evento = self.var_tipo.get()

            # Actualizar la etiqueta con las estadísticas
            msg = f"Evento: {titulo_evento} | Tipo: {tipo_evento}"
            self.lbl_estadisticas['text'] = msg

            logger.info(f"Estadísticas actualizadas para evento {id_evento}")

        except Exception as e:
            logger.error(f"Error al actualizar estadísticas de evento: {e}")
            self.lbl_estadisticas['text'] = "Error al cargar estadísticas"

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘

    def _on_tabla_doble_click(self, event):
        """Maneja el doble clic en una fila de la tabla"""
        # Obtener la fila seleccionada
        seleccion = self.tabla_evento.view.selection()

        if not seleccion:
            return

        # Obtener los valores de la fila
        item = self.tabla_evento.view.item(seleccion[0])
        valores = item['values']

        # Asignar a las variables
        id_evento = int(valores[0])
        evento = CalendarioEventoService(ruta_db=None)
        evento.id_evento = id_evento
        if evento.instanciar():
            self._cargar_formulario(evento=evento)

    def _on_nuevo(self):
        self._limpiar_formulario()

    def _on_aplicar(self):
        evento = self._establecer_evento()
        if evento:
            if evento.id_evento == 0 or evento.id_evento is None:
                # cargamos un nuevo evento a la base de datos
                id_evento = evento.insertar()
                if id_evento != 0:
                    self.var_id_evento.set(id_evento)
                    logger.info(f"Se creó el evento: {evento}")
                    showinfo(
                        parent=self.master,
                        title="Inserción",
                        message="Evento del calendario insertado con éxito!",
                    )
                    # recargamos la tabla
                    self._actualizar_tabla_evento()
            else:
                # actualizamos el evento
                if evento.actualizar():
                    showinfo(
                        parent=self.master,
                        title="Actualización",
                        message="Evento del calendario actualizado correctamente",
                    )
                    # recargamos la tabla
                    self._actualizar_tabla_evento()

    def _on_eliminar_evento(self):
        """Maneja la eliminación de un evento seleccionado"""
        id_evento = self.var_id_evento.get()

        # Validar que haya un evento seleccionado
        if id_evento == 0 or id_evento is None:
            showinfo(
                parent=self.master,
                title="Advertencia",
                message="Debe seleccionar un evento para eliminar",
            )
            return

        # Pedir confirmación al usuario
        titulo_evento = self.var_titulo.get()
        confirmacion = askyesno(
            parent=self.master,
            title="Confirmación",
            message=f"¿Desea eliminar el evento '{titulo_evento}'?",
        )

        if not confirmacion:
            return

        # Eliminar el evento
        evento = CalendarioEventoService(ruta_db=None)
        evento.id_evento = id_evento

        try:
            if evento.eliminar():
                logger.info(f"Se eliminó el evento con ID: {id_evento}")
                showinfo(
                    parent=self.master,
                    title="Eliminación",
                    message="Evento del calendario eliminado exitosamente",
                )
                # Limpiar formulario y actualizar tabla
                self._limpiar_formulario()
                self._actualizar_tabla_evento()
            else:
                logger.error(f"Error al eliminar el evento con ID: {id_evento}")
                showinfo(
                    parent=self.master,
                    title="Error",
                    message="Error al eliminar el evento",
                )
        except Exception as e:
            logger.error(f"Excepción al eliminar evento: {str(e)}")
            showinfo(
                parent=self.master,
                title="Error",
                message=f"Error inesperado: {str(e)}",
            )

    def _on_primero(self):
        """Carga el primer evento de la lista"""
        if self.lista_eventos:
            self.indice_actual = 0
            self._cargar_formulario(evento=self.lista_eventos[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay eventos para mostrar",
            )

    def _on_anterior(self):
        """Carga el evento anterior en la lista"""
        if not self.lista_eventos:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay eventos para mostrar",
            )
            return

        if self.indice_actual > 0:
            self.indice_actual -= 1
            self._cargar_formulario(evento=self.lista_eventos[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="Ya está en el primer evento",
            )

    def _on_siguiente(self):
        """Carga el siguiente evento en la lista"""
        if not self.lista_eventos:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay eventos para mostrar",
            )
            return

        if self.indice_actual < len(self.lista_eventos) - 1:
            self.indice_actual += 1
            self._cargar_formulario(evento=self.lista_eventos[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="Ya está en el último evento",
            )

    def _on_ultimo(self):
        """Carga el último evento de la lista"""
        if self.lista_eventos:
            self.indice_actual = len(self.lista_eventos) - 1
            self._cargar_formulario(evento=self.lista_eventos[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay eventos para mostrar",
            )
