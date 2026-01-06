from typing import Dict, Any, List, Optional
from tkinter.messagebox import askyesno, showinfo
from ttkbootstrap import Button, Entry, StringVar, Combobox, IntVar, Label
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from modelos.daos.eje_tematico_dao import EjeTematicoDAO
from modelos.daos.asignatura_dao import AsignaturaDAO
from modelos.services.eje_tematico_service import EjeTematicoService
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class ControlarAdministrarEjeTematico:

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
        # para almacenar los ejes temáticos
        self.lista_ejes_tematicos: List[EjeTematicoService] = []

        # Índice del eje temático actual en la navegación
        self.indice_actual: int = -1

        # Diccionarios para asignaturas: id_asignatura -> nombre_asignatura y viceversa
        self.dict_asignaturas: Dict[int, str] = {}  # {1: "Matemática I - MAT101"}
        self.dict_asignaturas_inv: Dict[str, int] = {}  # {"Matemática I - MAT101": 1}

        # cargar widgets
        self._cargar_widgets()

        # cargar los vars
        self._cargar_vars()

        # cargar las asignaturas en el combobox
        self._cargar_asignaturas()

        # mostrar las estadistica en el panel inferior
        self._actualizar_estadisticas()

        # mostramos los ejes temáticos en la tabla
        self._actualizar_tabla_eje_tematico()

        # viculamos los eventos
        self._vincular_eventos()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos Privados
    # └────────────────────────────────────────────────────────────┘
    def _vincular_eventos(self):
        # Vincular el evento de doble clic
        self.tabla_eje_tematico.view.bind("<Double-Button-1>", self._on_tabla_doble_click)
        # Vinculamos el evento nuevo
        self.btn_nuevo.config(command=self._on_nuevo)
        self.btn_aplicar.config(command=self._on_aplicar)
        self.btn_eliminar.config(command=self._on_eliminar_eje_tematico)
        # Vinculamos los botones de desplazamiento
        self.btn_primero.config(command=self._on_primero)
        self.btn_anterior.config(command=self._on_anterior)
        self.btn_siguiente.config(command=self._on_siguiente)
        self.btn_ultimo.config(command=self._on_ultimo)
        # Vinculamos el evento de selección en el combobox de asignatura
        self.cbx_asignatura.bind("<<ComboboxSelected>>", self._on_asignatura_seleccionada)

    def _establecer_eje_tematico(self) -> EjeTematicoService:
        eje_tematico = EjeTematicoService(ruta_db=None)
        # establecemos variables
        id_eje = self.var_id_eje.get()
        nombre = self.var_nombre.get()
        orden = self.var_orden.get()
        label_asignatura = self.var_nombre_asignatura.get()
        # Convertir nombre de asignatura a id_asignatura
        id_asignatura = self.dict_asignaturas_inv.get(label_asignatura, 0)
        # cargamos los datos al eje temático
        eje_tematico.id_eje = id_eje
        eje_tematico.nombre = nombre
        eje_tematico.orden = orden
        eje_tematico.id_asignatura = id_asignatura
        return eje_tematico

    def _cargar_formulario(self, eje_tematico: EjeTematicoService):
        if eje_tematico:
            self.var_id_eje.set(eje_tematico.id_eje)
            self.var_nombre.set(eje_tematico.nombre)
            self.var_orden.set(eje_tematico.orden)
            self.var_id_asignatura.set(eje_tematico.id_asignatura)
            # Convertir id_asignatura a label de asignatura
            label_asignatura = self.dict_asignaturas.get(eje_tematico.id_asignatura, "")
            self.var_nombre_asignatura.set(label_asignatura)
            # Actualizar estadísticas del eje temático seleccionado
            self._actualizar_estadisticas_eje_tematico(eje_tematico.id_eje)

    def _limpiar_formulario(self):
        self.var_id_eje.set(0)
        self.var_nombre.set("")
        self.var_orden.set(0)
        self.var_id_asignatura.set(0)
        self.var_nombre_asignatura.set("")

    def _insertar_fila(self, eje_tematico: EjeTematicoService):
        if eje_tematico:
            # Convertir id_asignatura a label para mostrar en tabla
            label_asignatura = self.dict_asignaturas.get(eje_tematico.id_asignatura, "N/A")

            self.tabla_eje_tematico.insert_row(
                index=END,
                values=(
                    eje_tematico.id_eje,
                    eje_tematico.nombre,
                    eje_tematico.orden,
                    eje_tematico.id_asignatura,
                    label_asignatura,
                ),
            )

    def _actualizar_tabla_eje_tematico(self):
        # obtenemos la lista de ejes temáticos
        self._obtener_ejes_tematicos()
        if self.lista_ejes_tematicos:
            # limpiamos la tabla
            self.tabla_eje_tematico.delete_rows()
            for eje_tematico in self.lista_ejes_tematicos:
                self._insertar_fila(eje_tematico=eje_tematico)

            # ajustamos las columnas
            self.tabla_eje_tematico.autofit_columns()

    def _obtener_ejes_tematicos(self):
        if self.lista_ejes_tematicos:
            self.lista_ejes_tematicos.clear()

        dao = EjeTematicoDAO(ruta_db=None)
        sql = "SELECT * FROM eje_tematico ORDER BY id_asignatura, orden"
        params = ()
        lista_aux = dao.ejecutar_consulta(sql=sql, params=params)
        if lista_aux:
            for data in lista_aux:
                eje_tematico = EjeTematicoService(ruta_db=None)
                eje_tematico.set_data(data=data)
                self.lista_ejes_tematicos.append(eje_tematico)

    def _cargar_vars(self):
        self.var_id_eje: IntVar = self.map_vars['var_id_eje']
        self.var_nombre: StringVar = self.map_vars['var_nombre']
        self.var_orden: IntVar = self.map_vars['var_orden']
        self.var_id_asignatura: IntVar = self.map_vars['var_id_asignatura']
        self.var_nombre_asignatura: StringVar = self.map_vars['var_nombre_asignatura']

    def _cargar_widgets(self):
        self.tabla_eje_tematico: Tableview = self.map_widgets['tabla_eje_tematico']
        self.lbl_estadisticas: Label = self.map_widgets['lbl_estadisticas']
        self.btn_nuevo: Button = self.map_widgets['btn_nuevo']
        self.btn_aplicar: Button = self.map_widgets['btn_aplicar']
        self.btn_eliminar: Button = self.map_widgets['btn_eliminar']
        self.btn_primero: Button = self.map_widgets['btn_primero']
        self.btn_anterior: Button = self.map_widgets['btn_anterior']
        self.btn_siguiente: Button = self.map_widgets['btn_siguiente']
        self.btn_ultimo: Button = self.map_widgets['btn_ultimo']
        self.cbx_asignatura: Combobox = self.map_widgets['cbx_asignatura']

    def _actualizar_estadisticas(self):
        # actualizamos la lista de ejes temáticos
        self._obtener_ejes_tematicos()
        cant_ejes_tematicos = 0
        if self.lista_ejes_tematicos:
            cant_ejes_tematicos = len(self.lista_ejes_tematicos)

        msg = f"Ejes Temáticos: {cant_ejes_tematicos}"

        self.lbl_estadisticas['text'] = msg

    def _cargar_asignaturas(self):
        """
        Carga la lista de asignaturas desde la BD y las agrega al combobox.
        Muestra: "Nombre - Código" para mayor claridad.
        Mantiene dos diccionarios sincronizados para conversión id <-> label.
        """
        try:
            # Limpiar diccionarios previos
            self.dict_asignaturas.clear()
            self.dict_asignaturas_inv.clear()

            # Obtener asignaturas de la BD con nombre y código
            dao = AsignaturaDAO(ruta_db=None)
            sql = "SELECT id_asignatura, nombre, codigo FROM Asignatura ORDER BY nombre"
            params = ()
            lista_aux = dao.ejecutar_consulta(sql=sql, params=params)

            if lista_aux:
                # Construir diccionarios y lista de nombres para el combobox
                nombres_asignaturas = []
                for data in lista_aux:
                    id_asignatura = data.get('id_asignatura')
                    nombre_asignatura = data.get('nombre')
                    codigo_asignatura = data.get('codigo')
                    # Construir label en formato "Nombre - Código"
                    label_asignatura = f"{nombre_asignatura} - {codigo_asignatura}"
                    # Agregar a diccionarios bidireccionales
                    self.dict_asignaturas[id_asignatura] = label_asignatura
                    self.dict_asignaturas_inv[label_asignatura] = id_asignatura
                    nombres_asignaturas.append(label_asignatura)

                # Cargar labels en el combobox
                self.cbx_asignatura['values'] = nombres_asignaturas
                logger.info(f"Se cargaron {len(nombres_asignaturas)} asignaturas en el combobox")
            else:
                logger.warning("No se encontraron asignaturas en la BD")
                self.cbx_asignatura['values'] = []

        except Exception as e:
            logger.error(f"Error al cargar asignaturas: {e}")
            self.cbx_asignatura['values'] = []

    def _actualizar_estadisticas_eje_tematico(self, id_eje: int):
        """
        Actualiza las estadísticas mostrando la información
        del eje temático seleccionado.

        Args:
            id_eje (int): ID del eje temático seleccionado
        """
        try:
            if id_eje <= 0:
                self.lbl_estadisticas['text'] = "Ejes Temáticos: 0"
                return

            # Obtener nombre del eje temático
            nombre_eje = self.var_nombre.get()
            orden_eje = self.var_orden.get()

            # Actualizar la etiqueta con las estadísticas
            msg = f"Eje Temático: {nombre_eje} | Orden: {orden_eje}"
            self.lbl_estadisticas['text'] = msg

            logger.info(f"Estadísticas actualizadas para eje temático {id_eje}")

        except Exception as e:
            logger.error(f"Error al actualizar estadísticas de eje temático: {e}")
            self.lbl_estadisticas['text'] = "Error al cargar estadísticas"

    def _on_asignatura_seleccionada(self, event=None):
        """
        Evento disparado cuando el usuario selecciona una asignatura en el combobox.
        Solo para propósitos de logging o validación adicional si es necesario.
        """
        label_asignatura = self.var_nombre_asignatura.get()
        id_asignatura = self.dict_asignaturas_inv.get(label_asignatura)
        logger.debug(f"Asignatura seleccionada: {label_asignatura} (ID: {id_asignatura})")

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘

    def _on_tabla_doble_click(self, event):
        """Maneja el doble clic en una fila de la tabla"""
        # Obtener la fila seleccionada
        seleccion = self.tabla_eje_tematico.view.selection()

        if not seleccion:
            return

        # Obtener los valores de la fila
        item = self.tabla_eje_tematico.view.item(seleccion[0])
        valores = item['values']

        # Asignar a las variables
        id_eje = int(valores[0])
        eje_tematico = EjeTematicoService(ruta_db=None)
        eje_tematico.id_eje = id_eje
        if eje_tematico.instanciar():
            self._cargar_formulario(eje_tematico=eje_tematico)

    def _on_nuevo(self):
        self._limpiar_formulario()

    def _on_aplicar(self):
        eje_tematico = self._establecer_eje_tematico()
        if eje_tematico:
            if eje_tematico.id_eje == 0 or eje_tematico.id_eje is None:
                # cargamos un nuevo eje temático a la base de datos
                id_eje = eje_tematico.insertar()
                if id_eje != 0:
                    self.var_id_eje.set(id_eje)
                    logger.info(f"Se creó el eje temático: {eje_tematico}")
                    showinfo(
                        parent=self.master,
                        title="Inserción",
                        message="Eje Temático insertado con éxito!",
                    )
                    # recargamos la tabla
                    self._actualizar_tabla_eje_tematico()
            else:
                # actualizamos el eje temático
                if eje_tematico.actualizar():
                    showinfo(
                        parent=self.master,
                        title="Actualización",
                        message="Eje Temático actualizado correctamente",
                    )
                    # recargamos la tabla
                    self._actualizar_tabla_eje_tematico()

    def _on_eliminar_eje_tematico(self):
        """Maneja la eliminación de un eje temático seleccionado"""
        id_eje = self.var_id_eje.get()

        # Validar que haya un eje temático seleccionado
        if id_eje == 0 or id_eje is None:
            showinfo(
                parent=self.master,
                title="Advertencia",
                message="Debe seleccionar un eje temático para eliminar",
            )
            return

        # Pedir confirmación al usuario
        nombre_eje = self.var_nombre.get()
        confirmacion = askyesno(
            parent=self.master,
            title="Confirmación",
            message=f"¿Desea eliminar el eje temático '{nombre_eje}'?",
        )

        if not confirmacion:
            return

        # Eliminar el eje temático
        eje_tematico = EjeTematicoService(ruta_db=None)
        eje_tematico.id_eje = id_eje

        try:
            if eje_tematico.eliminar():
                logger.info(f"Se eliminó el eje temático con ID: {id_eje}")
                showinfo(
                    parent=self.master,
                    title="Eliminación",
                    message="Eje Temático eliminado exitosamente",
                )
                # Limpiar formulario y actualizar tabla
                self._limpiar_formulario()
                self._actualizar_tabla_eje_tematico()
            else:
                logger.error(f"Error al eliminar el eje temático con ID: {id_eje}")
                showinfo(
                    parent=self.master,
                    title="Error",
                    message="Error al eliminar el eje temático",
                )
        except Exception as e:
            logger.error(f"Excepción al eliminar eje temático: {str(e)}")
            showinfo(
                parent=self.master,
                title="Error",
                message=f"Error inesperado: {str(e)}",
            )

    def _on_primero(self):
        """Carga el primer eje temático de la lista"""
        if self.lista_ejes_tematicos:
            self.indice_actual = 0
            self._cargar_formulario(eje_tematico=self.lista_ejes_tematicos[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay ejes temáticos para mostrar",
            )

    def _on_anterior(self):
        """Carga el eje temático anterior en la lista"""
        if not self.lista_ejes_tematicos:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay ejes temáticos para mostrar",
            )
            return

        if self.indice_actual > 0:
            self.indice_actual -= 1
            self._cargar_formulario(eje_tematico=self.lista_ejes_tematicos[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="Ya está en el primer eje temático",
            )

    def _on_siguiente(self):
        """Carga el siguiente eje temático en la lista"""
        if not self.lista_ejes_tematicos:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay ejes temáticos para mostrar",
            )
            return

        if self.indice_actual < len(self.lista_ejes_tematicos) - 1:
            self.indice_actual += 1
            self._cargar_formulario(eje_tematico=self.lista_ejes_tematicos[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="Ya está en el último eje temático",
            )

    def _on_ultimo(self):
        """Carga el último eje temático de la lista"""
        if self.lista_ejes_tematicos:
            self.indice_actual = len(self.lista_ejes_tematicos) - 1
            self._cargar_formulario(eje_tematico=self.lista_ejes_tematicos[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay ejes temáticos para mostrar",
            )
