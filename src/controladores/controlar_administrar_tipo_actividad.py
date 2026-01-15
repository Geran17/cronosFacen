from typing import Dict, Any, List, Optional
from tkinter.messagebox import askyesno, showinfo
from ttkbootstrap import Button, StringVar, IntVar, Label, Text, Combobox
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from modelos.daos.tipo_actividad_dao import TipoActividadDAO
from modelos.services.tipo_actividad_service import TipoActividadService
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class ControlarAdministrarTipoActividad:

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
        # para almacenar los tipos de actividad
        self.lista_tipos_actividad: List[TipoActividadService] = []

        # Índice del tipo de actividad actual en la navegación
        self.indice_actual: int = -1

        # cargar widgets
        self._cargar_widgets()

        # cargar los vars
        self._cargar_vars()

        # mostrar las estadistica en el panel inferior
        self._actualizar_estadisticas()

        # mostramos los tipos de actividad en la tabla
        self._actualizar_tabla_tipo_actividad()

        # viculamos los eventos
        self._vincular_eventos()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos Privados
    # └────────────────────────────────────────────────────────────┘
    def _vincular_eventos(self):
        # Vincular el evento de doble clic
        self.tabla_tipo_actividad.view.bind("<Double-Button-1>", self._on_tabla_doble_click)
        # Vinculamos el evento nuevo
        self.btn_nuevo.config(command=self._on_nuevo)
        self.btn_aplicar.config(command=self._on_aplicar)
        self.btn_eliminar.config(command=self._on_eliminar_tipo_actividad)
        # Vinculamos los botones de desplazamiento
        self.btn_primero.config(command=self._on_primero)
        self.btn_anterior.config(command=self._on_anterior)
        self.btn_siguiente.config(command=self._on_siguiente)
        self.btn_ultimo.config(command=self._on_ultimo)

    def _establecer_tipo_actividad(self) -> TipoActividadService:
        tipo_actividad = TipoActividadService(ruta_db=None)
        # establecemos variables
        id_tipo_actividad = self.var_id_tipo_actividad.get()
        nombre = self.var_nombre.get()
        siglas = self.var_siglas.get()
        descripcion = self.text_descripcion.get("1.0", END).strip()

        # Extraer el número de prioridad del combobox (ej: "2 - Alta" -> 2)
        prioridad_texto = self.var_prioridad.get()
        try:
            prioridad = int(prioridad_texto.split(" - ")[0])
        except (ValueError, IndexError):
            prioridad = 0

        # cargamos los datos al tipo de actividad
        tipo_actividad.id_tipo_actividad = id_tipo_actividad
        tipo_actividad.nombre = nombre
        tipo_actividad.siglas = siglas
        tipo_actividad.descripcion = descripcion
        tipo_actividad.prioridad = prioridad
        return tipo_actividad

    def _cargar_formulario(self, tipo_actividad: TipoActividadService):
        if tipo_actividad:
            self.var_id_tipo_actividad.set(tipo_actividad.id_tipo_actividad)
            self.var_nombre.set(tipo_actividad.nombre)
            self.var_siglas.set(tipo_actividad.siglas)
            # Cargar descripción en el widget Text
            self.text_descripcion.delete("1.0", END)
            if tipo_actividad.descripcion:
                self.text_descripcion.insert("1.0", tipo_actividad.descripcion)
            # Cargar prioridad - convertir número a formato "X - Nombre"
            if tipo_actividad.prioridad is not None:
                opciones_prioridad = {0: "0 - Baja", 1: "1 - Media", 2: "2 - Alta"}
                valor_prioridad = opciones_prioridad.get(tipo_actividad.prioridad, "0 - Baja")
                self.var_prioridad.set(valor_prioridad)
            else:
                self.var_prioridad.set("0 - Baja")
            # Actualizar estadísticas del tipo de actividad seleccionado
            self._actualizar_estadisticas_tipo_actividad(tipo_actividad.id_tipo_actividad)

    def _limpiar_formulario(self):
        self.var_id_tipo_actividad.set(0)
        self.var_nombre.set("")
        self.var_siglas.set("")
        self.text_descripcion.delete("1.0", END)
        self.var_prioridad.set("0 - Baja")

    def _insertar_fila(self, tipo_actividad: TipoActividadService):
        if tipo_actividad:
            # Truncar descripción si es muy larga para la tabla
            descripcion_corta = tipo_actividad.descripcion or ""
            if len(descripcion_corta) > 50:
                descripcion_corta = descripcion_corta[:47] + "..."

            self.tabla_tipo_actividad.insert_row(
                index=END,
                values=(
                    tipo_actividad.id_tipo_actividad,
                    tipo_actividad.nombre,
                    tipo_actividad.siglas,
                    descripcion_corta,
                ),
            )

    def _actualizar_tabla_tipo_actividad(self):
        # obtenemos la lista de tipos de actividad
        self._obtener_tipos_actividad()
        if self.lista_tipos_actividad:
            # limpiamos la tabla
            self.tabla_tipo_actividad.delete_rows()
            for tipo_actividad in self.lista_tipos_actividad:
                self._insertar_fila(tipo_actividad=tipo_actividad)

            # ajustamos las columnas
            self.tabla_tipo_actividad.autofit_columns()

    def _obtener_tipos_actividad(self):
        if self.lista_tipos_actividad:
            self.lista_tipos_actividad.clear()

        dao = TipoActividadDAO(ruta_db=None)
        sql = "SELECT * FROM tipo_actividad ORDER BY nombre"
        params = ()
        lista_aux = dao.ejecutar_consulta(sql=sql, params=params)
        if lista_aux:
            for data in lista_aux:
                tipo_actividad = TipoActividadService(ruta_db=None)
                tipo_actividad.set_data(data=data)
                self.lista_tipos_actividad.append(tipo_actividad)

    def _cargar_vars(self):
        self.var_id_tipo_actividad: IntVar = self.map_vars['var_id_tipo_actividad']
        self.var_nombre: StringVar = self.map_vars['var_nombre']
        self.var_siglas: StringVar = self.map_vars['var_siglas']
        self.var_descripcion: StringVar = self.map_vars['var_descripcion']
        self.var_prioridad: StringVar = self.map_vars['var_prioridad']

    def _cargar_widgets(self):
        self.tabla_tipo_actividad: Tableview = self.map_widgets['tabla_tipo_actividad']
        self.lbl_estadisticas: Label = self.map_widgets['lbl_estadisticas']
        self.btn_nuevo: Button = self.map_widgets['btn_nuevo']
        self.btn_aplicar: Button = self.map_widgets['btn_aplicar']
        self.btn_eliminar: Button = self.map_widgets['btn_eliminar']
        self.btn_primero: Button = self.map_widgets['btn_primero']
        self.btn_anterior: Button = self.map_widgets['btn_anterior']
        self.btn_siguiente: Button = self.map_widgets['btn_siguiente']
        self.btn_ultimo: Button = self.map_widgets['btn_ultimo']
        self.text_descripcion: Text = self.map_widgets['text_descripcion']
        self.cbx_prioridad: Combobox = self.map_widgets['cbx_prioridad']

    def _actualizar_estadisticas(self):
        # actualizamos la lista de tipos de actividad
        self._obtener_tipos_actividad()
        cant_tipos_actividad = 0
        if self.lista_tipos_actividad:
            cant_tipos_actividad = len(self.lista_tipos_actividad)

        msg = f"Tipos de Actividad: {cant_tipos_actividad}"

        self.lbl_estadisticas['text'] = msg

    def _actualizar_estadisticas_tipo_actividad(self, id_tipo_actividad: int):
        """
        Actualiza las estadísticas mostrando la información
        del tipo de actividad seleccionado.

        Args:
            id_tipo_actividad (int): ID del tipo de actividad seleccionado
        """
        try:
            if id_tipo_actividad <= 0:
                self.lbl_estadisticas['text'] = "Tipos de Actividad: 0"
                return

            # Obtener nombre y siglas del tipo de actividad
            nombre_tipo = self.var_nombre.get()
            siglas_tipo = self.var_siglas.get()

            # Actualizar la etiqueta con las estadísticas
            msg = f"Tipo de Actividad: {nombre_tipo} | Siglas: {siglas_tipo}"
            self.lbl_estadisticas['text'] = msg

            logger.info(f"Estadísticas actualizadas para tipo de actividad {id_tipo_actividad}")

        except Exception as e:
            logger.error(f"Error al actualizar estadísticas de tipo de actividad: {e}")
            self.lbl_estadisticas['text'] = "Error al cargar estadísticas"

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘

    def _on_tabla_doble_click(self, event):
        """Maneja el doble clic en una fila de la tabla"""
        # Obtener la fila seleccionada
        seleccion = self.tabla_tipo_actividad.view.selection()

        if not seleccion:
            return

        # Obtener los valores de la fila
        item = self.tabla_tipo_actividad.view.item(seleccion[0])
        valores = item['values']

        # Asignar a las variables
        id_tipo_actividad = int(valores[0])
        tipo_actividad = TipoActividadService(ruta_db=None)
        tipo_actividad.id_tipo_actividad = id_tipo_actividad
        if tipo_actividad.instanciar():
            self._cargar_formulario(tipo_actividad=tipo_actividad)

    def _on_nuevo(self):
        self._limpiar_formulario()

    def _on_aplicar(self):
        tipo_actividad = self._establecer_tipo_actividad()
        if tipo_actividad:
            if tipo_actividad.id_tipo_actividad == 0 or tipo_actividad.id_tipo_actividad is None:
                # cargamos un nuevo tipo de actividad a la base de datos
                id_tipo_actividad = tipo_actividad.insertar()
                if id_tipo_actividad != 0:
                    self.var_id_tipo_actividad.set(id_tipo_actividad)
                    logger.info(f"Se creó el tipo de actividad: {tipo_actividad}")
                    showinfo(
                        parent=self.master,
                        title="Inserción",
                        message="Tipo de Actividad insertado con éxito!",
                    )
                    # recargamos la tabla
                    self._actualizar_tabla_tipo_actividad()
            else:
                # actualizamos el tipo de actividad
                if tipo_actividad.actualizar():
                    showinfo(
                        parent=self.master,
                        title="Actualización",
                        message="Tipo de Actividad actualizado correctamente",
                    )
                    # recargamos la tabla
                    self._actualizar_tabla_tipo_actividad()

    def _on_eliminar_tipo_actividad(self):
        """Maneja la eliminación de un tipo de actividad seleccionado"""
        id_tipo_actividad = self.var_id_tipo_actividad.get()

        # Validar que haya un tipo de actividad seleccionado
        if id_tipo_actividad == 0 or id_tipo_actividad is None:
            showinfo(
                parent=self.master,
                title="Advertencia",
                message="Debe seleccionar un tipo de actividad para eliminar",
            )
            return

        # Pedir confirmación al usuario
        nombre_tipo = self.var_nombre.get()
        confirmacion = askyesno(
            parent=self.master,
            title="Confirmación",
            message=f"¿Desea eliminar el tipo de actividad '{nombre_tipo}'?",
        )

        if not confirmacion:
            return

        # Eliminar el tipo de actividad
        tipo_actividad = TipoActividadService(ruta_db=None)
        tipo_actividad.id_tipo_actividad = id_tipo_actividad

        try:
            if tipo_actividad.eliminar():
                logger.info(f"Se eliminó el tipo de actividad con ID: {id_tipo_actividad}")
                showinfo(
                    parent=self.master,
                    title="Eliminación",
                    message="Tipo de Actividad eliminado exitosamente",
                )
                # Limpiar formulario y actualizar tabla
                self._limpiar_formulario()
                self._actualizar_tabla_tipo_actividad()
            else:
                logger.error(f"Error al eliminar el tipo de actividad con ID: {id_tipo_actividad}")
                showinfo(
                    parent=self.master,
                    title="Error",
                    message="Error al eliminar el tipo de actividad",
                )
        except Exception as e:
            logger.error(f"Excepción al eliminar tipo de actividad: {str(e)}")
            showinfo(
                parent=self.master,
                title="Error",
                message=f"Error inesperado: {str(e)}",
            )

    def _on_primero(self):
        """Carga el primer tipo de actividad de la lista"""
        if self.lista_tipos_actividad:
            self.indice_actual = 0
            self._cargar_formulario(tipo_actividad=self.lista_tipos_actividad[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay tipos de actividad para mostrar",
            )

    def _on_anterior(self):
        """Carga el tipo de actividad anterior en la lista"""
        if not self.lista_tipos_actividad:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay tipos de actividad para mostrar",
            )
            return

        if self.indice_actual > 0:
            self.indice_actual -= 1
            self._cargar_formulario(tipo_actividad=self.lista_tipos_actividad[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="Ya está en el primer tipo de actividad",
            )

    def _on_siguiente(self):
        """Carga el siguiente tipo de actividad en la lista"""
        if not self.lista_tipos_actividad:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay tipos de actividad para mostrar",
            )
            return

        if self.indice_actual < len(self.lista_tipos_actividad) - 1:
            self.indice_actual += 1
            self._cargar_formulario(tipo_actividad=self.lista_tipos_actividad[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="Ya está en el último tipo de actividad",
            )

    def _on_ultimo(self):
        """Carga el último tipo de actividad de la lista"""
        if self.lista_tipos_actividad:
            self.indice_actual = len(self.lista_tipos_actividad) - 1
            self._cargar_formulario(tipo_actividad=self.lista_tipos_actividad[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay tipos de actividad para mostrar",
            )
