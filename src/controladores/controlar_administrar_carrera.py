from typing import Dict, Any, List, Optional
from tkinter.messagebox import askyesno, showinfo
from ttkbootstrap import Button, Entry, StringVar, Combobox, IntVar, Label
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from modelos.daos.carrera_dao import CarreraDAO
from modelos.services.carrera_service import CarreraService
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class ControlarAdministrarCarrera:

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
        # para almacenar las carreras
        self.lista_carreras: List[CarreraService] = []

        # Índice de la carrera actual en la navegación
        self.indice_actual: int = -1

        # cargar widgets
        self._cargar_widgets()

        # cargar los vars
        self._cargar_vars()
        # cargar los widgets
        self._cargar_widgets()

        # mostrar las estadistica en el panel inferior
        self._actualizar_estadisticas()

        # mostramos las carreras en la tabla
        self._actualizar_tabla_carrera()

        # viculamos los eventos
        self._vincular_eventos()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos Privados
    # └────────────────────────────────────────────────────────────┘
    def _vincular_eventos(self):
        # Vincular el evento de doble clic
        self.tabla_carrera.view.bind("<Double-Button-1>", self._on_tabla_doble_click)
        # Vinculamos el evento nuevo
        self.btn_nuevo.config(command=self._on_nuevo)
        self.btn_aplicar.config(command=self._on_aplicar)
        self.btn_eliminar.config(command=self._on_eliminar_carrera)
        # Vinculamos los botones de desplazamiento
        self.btn_primero.config(command=self._on_primero)
        self.btn_anterior.config(command=self._on_anterior)
        self.btn_siguiente.config(command=self._on_siguiente)
        self.btn_ultimo.config(command=self._on_ultimo)

    def _establecer_carrera(self) -> CarreraService:
        carrera = CarreraService(ruta_db=None)
        # establecemos variables
        id_carrera = self.var_id.get()
        codigo = self.var_codigo.get()
        plan = self.var_plan.get()
        modalidad = self.var_modalidad.get()
        nombre = self.var_nombre.get()
        credito = self.var_credito.get()
        # cargamos los datos a la carrera
        carrera.id_carrera = id_carrera
        carrera.codigo = codigo
        carrera.plan = plan
        carrera.modalidad = modalidad
        carrera.nombre = nombre
        carrera.creditos_totales = credito
        return carrera

    def _cargar_formulario(self, carrera: CarreraService):
        if carrera:
            self.var_id.set(carrera.id_carrera)
            self.var_codigo.set(carrera.codigo)
            self.var_plan.set(carrera.plan)
            self.var_modalidad.set(carrera.modalidad)
            self.var_nombre.set(carrera.nombre)
            self.var_credito.set(carrera.creditos_totales)

    def _limpiar_formulario(self):
        self.var_id.set(0)
        self.var_codigo.set("")
        self.var_plan.set("")
        self.var_modalidad.set("Simi-Presencial")
        self.var_nombre.set("")
        self.var_credito.set(0)

    def _insertar_fila(self, carrera: CarreraService):
        if carrera:

            self.tabla_carrera.insert_row(
                index=END,
                values=(
                    carrera.id_carrera,
                    carrera.codigo,
                    carrera.nombre,
                    carrera.plan,
                    carrera.modalidad,
                    carrera.creditos_totales,
                ),
            )

    def _actualizar_tabla_carrera(self):
        # obtenemos las lista de carreras
        self._obtener_carreras()
        if self.lista_carreras:
            # limpiamos la tabla
            self.tabla_carrera.delete_rows()
            for carrera in self.lista_carreras:
                self._insertar_fila(carrera=carrera)

            # ajustamos las columnas
            self.tabla_carrera.autofit_columns()

    def _obtener_carreras(self):
        if self.lista_carreras:
            self.lista_carreras.clear()

        dao = CarreraDAO(ruta_db=None)
        sql = "SELECT * FROM Carrera"
        params = ()
        lista_aux = dao.ejecutar_consulta(sql=sql, params=params)
        if lista_aux:
            for data in lista_aux:
                carrera = CarreraService(ruta_db=None)
                carrera.set_data(data=data)
                self.lista_carreras.append(carrera)

    def _cargar_vars(self):
        self.var_id: IntVar = self.map_vars['var_id']
        self.var_codigo: StringVar = self.map_vars['var_codigo']
        self.var_nombre: StringVar = self.map_vars['var_nombre']
        self.var_plan: StringVar = self.map_vars['var_plan']
        self.var_modalidad: StringVar = self.map_vars['var_modalidad']
        self.var_credito: IntVar = self.map_vars['var_credito']

    def _cargar_widgets(self):
        self.tabla_carrera: Tableview = self.map_widgets['tabla_carrera']
        self.lbl_estadisticas: Label = self.map_widgets['lbl_estadisticas']
        self.btn_nuevo: Button = self.map_widgets['btn_nuevo']
        self.btn_aplicar: Button = self.map_widgets['btn_aplicar']
        self.btn_eliminar: Button = self.map_widgets['btn_eliminar']
        self.btn_primero: Button = self.map_widgets['btn_primero']
        self.btn_anterior: Button = self.map_widgets['btn_anterior']
        self.btn_siguiente: Button = self.map_widgets['btn_siguiente']
        self.btn_ultimo: Button = self.map_widgets['btn_ultimo']

    def _actualizar_estadisticas(self):
        # actulizamos la lista de carreras
        self._obtener_carreras()
        cant_carreras = 0
        if self.lista_carreras:
            cant_carreras = len(self.lista_carreras)

        msg = f"Carreras: {cant_carreras}"

        self.lbl_estadisticas['text'] = msg

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘

    def _on_tabla_doble_click(self, event):
        """Maneja el doble clic en una fila de la tabla"""
        # Obtener la fila seleccionada
        seleccion = self.tabla_carrera.view.selection()

        if not seleccion:
            return

        # Obtener los valores de la fila
        item = self.tabla_carrera.view.item(seleccion[0])
        valores = item['values']

        # Asignar a las variables
        id_carrera = int(valores[0])
        carrera = CarreraService(ruta_db=None)
        carrera.id_carrera = id_carrera
        if carrera.instanciar():
            self._cargar_formulario(carrera=carrera)

    def _on_nuevo(self):
        self._limpiar_formulario()

    def _on_aplicar(self):
        carrera = self._establecer_carrera()
        if carrera:
            if carrera.id_carrera == 0 or carrera.id_carrera is None:
                # cargamos una nueva carrera a la base de datos
                id_carrera = carrera.insertar()
                if id_carrera != 0:
                    self.var_id.set(id_carrera)
                    logger.info(f"Se creo la carrera: {carrera}")
                    showinfo(
                        parent=self.master,
                        title="Insercion",
                        message="Carrera insertada con exito !!!!",
                    )
                    # recargamos la tabla
                    self._actualizar_tabla_carrera()
            else:
                if carrera.id_carreras != 0:
                    # actualizamos la carrera
                    if carrera.actualizar():
                        showinfo(
                            parent=self.master,
                            title="Actualizacion",
                            message="Carrera actulizada correctamente",
                        )
                        # recargamos la tabla
                        self._actualizar_tabla_carrera()

    def _on_eliminar_carrera(self):
        """Maneja la eliminación de una carrera seleccionada"""
        id_carrera = self.var_id.get()

        # Validar que haya una carrera seleccionada
        if id_carrera == 0 or id_carrera is None:
            showinfo(
                parent=self.master,
                title="Advertencia",
                message="Debe seleccionar una carrera para eliminar",
            )
            return

        # Pedir confirmación al usuario
        nombre_carrera = self.var_nombre.get()
        confirmacion = askyesno(
            parent=self.master,
            title="Confirmación",
            message=f"¿Desea eliminar la carrera '{nombre_carrera}'?",
        )

        if not confirmacion:
            return

        # Eliminar la carrera
        carrera = CarreraService(ruta_db=None)
        carrera.id_carrera = id_carrera

        try:
            if carrera.eliminar():
                logger.info(f"Se eliminó la carrera con ID: {id_carrera}")
                showinfo(
                    parent=self.master,
                    title="Eliminación",
                    message="Carrera eliminada exitosamente",
                )
                # Limpiar formulario y actualizar tabla
                self._limpiar_formulario()
                self._actualizar_tabla_carrera()
            else:
                logger.error(f"Error al eliminar la carrera con ID: {id_carrera}")
                showinfo(
                    parent=self.master,
                    title="Error",
                    message="Error al eliminar la carrera",
                )
        except Exception as e:
            logger.error(f"Excepción al eliminar carrera: {str(e)}")
            showinfo(
                parent=self.master,
                title="Error",
                message=f"Error inesperado: {str(e)}",
            )

    def _on_primero(self):
        """Carga la primera carrera de la lista"""
        if self.lista_carreras:
            self.indice_actual = 0
            self._cargar_formulario(carrera=self.lista_carreras[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay carreras para mostrar",
            )

    def _on_anterior(self):
        """Carga la carrera anterior en la lista"""
        if not self.lista_carreras:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay carreras para mostrar",
            )
            return

        if self.indice_actual > 0:
            self.indice_actual -= 1
            self._cargar_formulario(carrera=self.lista_carreras[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="Ya está en la primera carrera",
            )

    def _on_siguiente(self):
        """Carga la siguiente carrera en la lista"""
        if not self.lista_carreras:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay carreras para mostrar",
            )
            return

        if self.indice_actual < len(self.lista_carreras) - 1:
            self.indice_actual += 1
            self._cargar_formulario(carrera=self.lista_carreras[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="Ya está en la última carrera",
            )

    def _on_ultimo(self):
        """Carga la última carrera de la lista"""
        if self.lista_carreras:
            self.indice_actual = len(self.lista_carreras) - 1
            self._cargar_formulario(carrera=self.lista_carreras[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay carreras para mostrar",
            )
