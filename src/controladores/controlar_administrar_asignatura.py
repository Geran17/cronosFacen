from typing import Dict, Any, List, Optional
from tkinter.messagebox import askyesno, showinfo
from ttkbootstrap import Button, Entry, StringVar, Combobox, IntVar, Label
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from modelos.daos.asignatura_dao import AsignaturaDAO
from modelos.daos.carrera_dao import CarreraDAO
from modelos.services.asignatura_service import AsignaturaService
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class ControlarAdministrarAsignatura:

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
        # para almacenar las asignaturas
        self.lista_asignaturas: List[AsignaturaService] = []

        # Índice de la asignatura actual en la navegación
        self.indice_actual: int = -1

        # Diccionarios para carreras: id_carrera -> nombre_carrera y viceversa
        self.dict_carreras: Dict[int, str] = {}  # {1: "Ingeniería - 2024"}
        self.dict_carreras_inv: Dict[str, int] = {}  # {"Ingeniería - 2024": 1}

        # cargar widgets
        self._cargar_widgets()

        # cargar los vars
        self._cargar_vars()

        # cargar las carreras en el combobox
        self._cargar_carreras()

        # mostrar las estadistica en el panel inferior
        self._actualizar_estadisticas()

        # mostramos las asignaturas en la tabla
        self._actualizar_tabla_asignatura()

        # viculamos los eventos
        self._vincular_eventos()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos Privados
    # └────────────────────────────────────────────────────────────┘
    def _vincular_eventos(self):
        # Vincular el evento de doble clic
        self.tabla_asignatura.view.bind("<Double-Button-1>", self._on_tabla_doble_click)
        # Vinculamos el evento nuevo
        self.btn_nuevo.config(command=self._on_nuevo)
        self.btn_aplicar.config(command=self._on_aplicar)
        self.btn_eliminar.config(command=self._on_eliminar_asignatura)
        # Vinculamos los botones de desplazamiento
        self.btn_primero.config(command=self._on_primero)
        self.btn_anterior.config(command=self._on_anterior)
        self.btn_siguiente.config(command=self._on_siguiente)
        self.btn_ultimo.config(command=self._on_ultimo)
        # Vinculamos el evento de selección en el combobox de carrera
        self.cbx_carrera.bind("<<ComboboxSelected>>", self._on_carrera_seleccionada)

    def _establecer_asignatura(self) -> AsignaturaService:
        asignatura = AsignaturaService(ruta_db=None)
        # establecemos variables
        id_asignatura = self.var_id.get()
        codigo = self.var_codigo.get()
        nombre = self.var_nombre.get()
        creditos = self.var_creditos.get()
        horas_semanales = self.var_horas_semanales.get()
        tipo = self.var_tipo.get()
        semestre = self.var_semestre.get()
        label_carrera = self.var_carrera.get()
        # Convertir nombre de carrera a id_carrera
        id_carrera = self.dict_carreras_inv.get(label_carrera, 0)
        # cargamos los datos a la asignatura
        asignatura.id_asignatura = id_asignatura
        asignatura.codigo = codigo
        asignatura.nombre = nombre
        asignatura.creditos = creditos
        asignatura.horas_semanales = horas_semanales
        asignatura.tipo = tipo
        asignatura.semestre = semestre
        asignatura.id_carrera = id_carrera
        return asignatura

    def _cargar_formulario(self, asignatura: AsignaturaService):
        if asignatura:
            self.var_id.set(asignatura.id_asignatura)
            self.var_codigo.set(asignatura.codigo)
            self.var_nombre.set(asignatura.nombre)
            self.var_creditos.set(asignatura.creditos)
            self.var_horas_semanales.set(asignatura.horas_semanales)
            self.var_tipo.set(asignatura.tipo)
            self.var_semestre.set(asignatura.semestre if asignatura.semestre else 0)
            # Convertir id_carrera a label de carrera
            label_carrera = self.dict_carreras.get(asignatura.id_carrera, "")
            self.var_carrera.set(label_carrera)
            # Actualizar estadísticas de la asignatura seleccionada
            self._actualizar_estadisticas_asignatura(asignatura.id_asignatura)

    def _limpiar_formulario(self):
        self.var_id.set(0)
        self.var_codigo.set("")
        self.var_nombre.set("")
        self.var_creditos.set(0)
        self.var_horas_semanales.set(0)
        self.var_tipo.set("")
        self.var_semestre.set(0)
        self.var_carrera.set("")

    def _insertar_fila(self, asignatura: AsignaturaService):
        if asignatura:
            # Convertir id_carrera a nombre - plan para mostrar en tabla
            label_carrera = self.dict_carreras.get(asignatura.id_carrera, "N/A")

            self.tabla_asignatura.insert_row(
                index=END,
                values=(
                    asignatura.id_asignatura,
                    asignatura.codigo,
                    asignatura.nombre,
                    asignatura.creditos,
                    asignatura.horas_semanales,
                    asignatura.tipo,
                    asignatura.semestre if asignatura.semestre else "",
                    label_carrera,
                ),
            )

    def _actualizar_tabla_asignatura(self):
        # obtenemos la lista de asignaturas
        self._obtener_asignaturas()
        if self.lista_asignaturas:
            # limpiamos la tabla
            self.tabla_asignatura.delete_rows()
            for asignatura in self.lista_asignaturas:
                self._insertar_fila(asignatura=asignatura)

            # ajustamos las columnas
            self.tabla_asignatura.autofit_columns()

    def _obtener_asignaturas(self):
        if self.lista_asignaturas:
            self.lista_asignaturas.clear()

        dao = AsignaturaDAO(ruta_db=None)
        sql = "SELECT * FROM Asignatura"
        params = ()
        lista_aux = dao.ejecutar_consulta(sql=sql, params=params)
        if lista_aux:
            for data in lista_aux:
                asignatura = AsignaturaService(ruta_db=None)
                asignatura.set_data(data=data)
                self.lista_asignaturas.append(asignatura)

    def _cargar_vars(self):
        self.var_id: IntVar = self.map_vars['var_id']
        self.var_codigo: StringVar = self.map_vars['var_codigo']
        self.var_nombre: StringVar = self.map_vars['var_nombre']
        self.var_creditos: IntVar = self.map_vars['var_creditos']
        self.var_horas_semanales: IntVar = self.map_vars['var_horas_semanales']
        self.var_tipo: StringVar = self.map_vars['var_tipo']
        self.var_semestre: IntVar = self.map_vars['var_semestre']
        self.var_carrera: StringVar = self.map_vars['var_carrera']

    def _cargar_widgets(self):
        self.tabla_asignatura: Tableview = self.map_widgets['tabla_asignatura']
        self.lbl_estadisticas: Label = self.map_widgets['lbl_estadisticas']
        self.btn_nuevo: Button = self.map_widgets['btn_nuevo']
        self.btn_aplicar: Button = self.map_widgets['btn_aplicar']
        self.btn_eliminar: Button = self.map_widgets['btn_eliminar']
        self.btn_primero: Button = self.map_widgets['btn_primero']
        self.btn_anterior: Button = self.map_widgets['btn_anterior']
        self.btn_siguiente: Button = self.map_widgets['btn_siguiente']
        self.btn_ultimo: Button = self.map_widgets['btn_ultimo']
        self.cbx_carrera: Combobox = self.map_widgets['cbx_carrera']
        self.cbx_tipo: Combobox = self.map_widgets['cbx_tipo']
        self.entry_semestre: Entry = self.map_widgets['entry_semestre']

    def _actualizar_estadisticas(self):
        # actualizamos la lista de asignaturas
        self._obtener_asignaturas()
        cant_asignaturas = 0
        if self.lista_asignaturas:
            cant_asignaturas = len(self.lista_asignaturas)

        msg = f"Asignaturas: {cant_asignaturas}"

        self.lbl_estadisticas['text'] = msg

    def _cargar_carreras(self):
        """
        Carga la lista de carreras desde la BD y las agrega al combobox.
        Muestra: "Nombre - Plan" para mayor claridad.
        Mantiene dos diccionarios sincronizados para conversión id <-> label.
        """
        try:
            # Limpiar diccionarios previos
            self.dict_carreras.clear()
            self.dict_carreras_inv.clear()

            # Obtener carreras de la BD con nombre y plan
            dao = CarreraDAO(ruta_db=None)
            sql = "SELECT id_carrera, nombre, plan FROM Carrera ORDER BY nombre"
            params = ()
            lista_aux = dao.ejecutar_consulta(sql=sql, params=params)

            if lista_aux:
                # Construir diccionarios y lista de nombres para el combobox
                nombres_carreras = []
                for data in lista_aux:
                    id_carrera = data.get('id_carrera')
                    nombre_carrera = data.get('nombre')
                    plan_carrera = data.get('plan')
                    # Construir label en formato "Nombre - Plan"
                    label_carrera = f"{nombre_carrera} - {plan_carrera}"
                    # Agregar a diccionarios bidireccionales
                    self.dict_carreras[id_carrera] = label_carrera
                    self.dict_carreras_inv[label_carrera] = id_carrera
                    nombres_carreras.append(label_carrera)

                # Cargar labels en el combobox
                self.cbx_carrera['values'] = nombres_carreras
                logger.info(f"Se cargaron {len(nombres_carreras)} carreras en el combobox")
            else:
                logger.warning("No se encontraron carreras en la BD")
                self.cbx_carrera['values'] = []

        except Exception as e:
            logger.error(f"Error al cargar carreras: {e}")
            self.cbx_carrera['values'] = []

    def _actualizar_estadisticas_asignatura(self, id_asignatura: int):
        """
        Actualiza las estadísticas mostrando la información
        de la asignatura seleccionada.

        Args:
            id_asignatura (int): ID de la asignatura seleccionada
        """
        try:
            if id_asignatura <= 0:
                self.lbl_estadisticas['text'] = "Asignaturas: 0"
                return

            # Obtener nombre y código de la asignatura
            nombre_asignatura = self.var_nombre.get()
            codigo_asignatura = self.var_codigo.get()

            # Actualizar la etiqueta con las estadísticas
            msg = f"Asignatura: {codigo_asignatura} - {nombre_asignatura}"
            self.lbl_estadisticas['text'] = msg

            logger.info(f"Estadísticas actualizadas para asignatura {id_asignatura}")

        except Exception as e:
            logger.error(f"Error al actualizar estadísticas de asignatura: {e}")
            self.lbl_estadisticas['text'] = "Error al cargar estadísticas"

    def _on_carrera_seleccionada(self, event=None):
        """
        Evento disparado cuando el usuario selecciona una carrera en el combobox.
        Solo para propósitos de logging o validación adicional si es necesario.
        """
        label_carrera = self.var_carrera.get()
        id_carrera = self.dict_carreras_inv.get(label_carrera)
        logger.debug(f"Carrera seleccionada: {label_carrera} (ID: {id_carrera})")

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘

    def _on_tabla_doble_click(self, event):
        """Maneja el doble clic en una fila de la tabla"""
        # Obtener la fila seleccionada
        seleccion = self.tabla_asignatura.view.selection()

        if not seleccion:
            return

        # Obtener los valores de la fila
        item = self.tabla_asignatura.view.item(seleccion[0])
        valores = item['values']

        # Asignar a las variables
        id_asignatura = int(valores[0])
        asignatura = AsignaturaService(ruta_db=None)
        asignatura.id_asignatura = id_asignatura
        if asignatura.instanciar():
            self._cargar_formulario(asignatura=asignatura)

    def _on_nuevo(self):
        self._limpiar_formulario()

    def _on_aplicar(self):
        asignatura = self._establecer_asignatura()
        if asignatura:
            if asignatura.id_asignatura == 0 or asignatura.id_asignatura is None:
                # cargamos una nueva asignatura a la base de datos
                id_asignatura = asignatura.insertar()
                if id_asignatura != 0:
                    self.var_id.set(id_asignatura)
                    logger.info(f"Se creo la asignatura: {asignatura}")
                    showinfo(
                        parent=self.master,
                        title="Inserción",
                        message="Asignatura insertada con éxito!",
                    )
                    # recargamos la tabla
                    self._actualizar_tabla_asignatura()
            else:
                # actualizamos la asignatura
                if asignatura.actualizar():
                    showinfo(
                        parent=self.master,
                        title="Actualización",
                        message="Asignatura actualizada correctamente",
                    )
                    # recargamos la tabla
                    self._actualizar_tabla_asignatura()

    def _on_eliminar_asignatura(self):
        """Maneja la eliminación de una asignatura seleccionada"""
        id_asignatura = self.var_id.get()

        # Validar que haya una asignatura seleccionada
        if id_asignatura == 0 or id_asignatura is None:
            showinfo(
                parent=self.master,
                title="Advertencia",
                message="Debe seleccionar una asignatura para eliminar",
            )
            return

        # Pedir confirmación al usuario
        nombre_asignatura = self.var_nombre.get()
        confirmacion = askyesno(
            parent=self.master,
            title="Confirmación",
            message=f"¿Desea eliminar la asignatura '{nombre_asignatura}'?",
        )

        if not confirmacion:
            return

        # Eliminar la asignatura
        asignatura = AsignaturaService(ruta_db=None)
        asignatura.id_asignatura = id_asignatura

        try:
            if asignatura.eliminar():
                logger.info(f"Se eliminó la asignatura con ID: {id_asignatura}")
                showinfo(
                    parent=self.master,
                    title="Eliminación",
                    message="Asignatura eliminada exitosamente",
                )
                # Limpiar formulario y actualizar tabla
                self._limpiar_formulario()
                self._actualizar_tabla_asignatura()
            else:
                logger.error(f"Error al eliminar la asignatura con ID: {id_asignatura}")
                showinfo(
                    parent=self.master,
                    title="Error",
                    message="Error al eliminar la asignatura",
                )
        except Exception as e:
            logger.error(f"Excepción al eliminar asignatura: {str(e)}")
            showinfo(
                parent=self.master,
                title="Error",
                message=f"Error inesperado: {str(e)}",
            )

    def _on_primero(self):
        """Carga la primera asignatura de la lista"""
        if self.lista_asignaturas:
            self.indice_actual = 0
            self._cargar_formulario(asignatura=self.lista_asignaturas[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay asignaturas para mostrar",
            )

    def _on_anterior(self):
        """Carga la asignatura anterior en la lista"""
        if not self.lista_asignaturas:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay asignaturas para mostrar",
            )
            return

        if self.indice_actual > 0:
            self.indice_actual -= 1
            self._cargar_formulario(asignatura=self.lista_asignaturas[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="Ya está en la primera asignatura",
            )

    def _on_siguiente(self):
        """Carga la siguiente asignatura en la lista"""
        if not self.lista_asignaturas:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay asignaturas para mostrar",
            )
            return

        if self.indice_actual < len(self.lista_asignaturas) - 1:
            self.indice_actual += 1
            self._cargar_formulario(asignatura=self.lista_asignaturas[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="Ya está en la última asignatura",
            )

    def _on_ultimo(self):
        """Carga la última asignatura de la lista"""
        if self.lista_asignaturas:
            self.indice_actual = len(self.lista_asignaturas) - 1
            self._cargar_formulario(asignatura=self.lista_asignaturas[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay asignaturas para mostrar",
            )
