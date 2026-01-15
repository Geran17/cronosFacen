from typing import Dict, Any, List, Optional
from tkinter.messagebox import askyesno, showinfo
from ttkbootstrap import Button, Entry, StringVar, Combobox, IntVar, Label
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from modelos.daos.eje_tematico_dao import EjeTematicoDAO
from modelos.daos.asignatura_dao import AsignaturaDAO
from modelos.daos.carrera_dao import CarreraDAO
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

        # Diccionarios para carreras: id_carrera -> nombre_carrera y viceversa
        self.dict_carreras: Dict[int, str] = {}  # {1: "Ingeniería"}
        self.dict_carreras_inv: Dict[str, int] = {}  # {"Ingeniería": 1}

        # Diccionarios para asignaturas filtradas por carrera: id_carrera -> lista de asignaturas
        self.dict_asignaturas_por_carrera: Dict[int, List[tuple]] = (
            {}
        )  # {1: [(id, nombre - codigo), ...]}

        # Variables de filtro actual
        self.id_carrera_filtro_actual: int = 0
        self.id_asignatura_filtro_actual: int = 0

        # cargar widgets
        self._cargar_widgets()

        # cargar los vars
        self._cargar_vars()

        # cargar las asignaturas en el combobox
        self._cargar_asignaturas()

        # cargar las carreras en el combobox de filtro
        self._cargar_carreras()

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
        # Vinculamos los eventos de filtros
        self.cbx_carrera_filtro.bind("<<ComboboxSelected>>", self._on_carrera_filtro_seleccionada)
        self.cbx_asignatura_filtro.bind(
            "<<ComboboxSelected>>", self._on_asignatura_filtro_seleccionada
        )
        self.btn_limpiar_filtros.config(command=self._on_limpiar_filtros)

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
        # Decidir si usar filtrados o todos
        if self.id_carrera_filtro_actual > 0 or self.id_asignatura_filtro_actual > 0:
            self._obtener_ejes_tematicos_filtrados()
        else:
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

    def _obtener_ejes_tematicos_filtrados(self):
        """
        Obtiene los ejes temáticos aplicando los filtros de carrera y asignatura.
        """
        if self.lista_ejes_tematicos:
            self.lista_ejes_tematicos.clear()

        dao = EjeTematicoDAO(ruta_db=None)

        # Construir la consulta con filtros
        sql = """
            SELECT DISTINCT et.* 
            FROM eje_tematico et
            INNER JOIN asignatura a ON et.id_asignatura = a.id_asignatura
        """
        params = []

        # Agregar filtro de carrera si está seleccionada
        if self.id_carrera_filtro_actual > 0:
            sql += " WHERE a.id_carrera = ?"
            params.append(self.id_carrera_filtro_actual)

            # Agregar filtro de asignatura si está seleccionada
            if self.id_asignatura_filtro_actual > 0:
                sql += " AND et.id_asignatura = ?"
                params.append(self.id_asignatura_filtro_actual)
        else:
            # Solo filtro de asignatura (sin carrera)
            if self.id_asignatura_filtro_actual > 0:
                sql += " WHERE et.id_asignatura = ?"
                params.append(self.id_asignatura_filtro_actual)

        sql += " ORDER BY a.id_carrera, et.id_asignatura, et.orden"

        lista_aux = dao.ejecutar_consulta(sql=sql, params=tuple(params))
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
        self.var_id_carrera_filtro: IntVar = self.map_vars['var_id_carrera_filtro']
        self.var_nombre_carrera_filtro: StringVar = self.map_vars['var_nombre_carrera_filtro']
        self.var_id_asignatura_filtro: IntVar = self.map_vars['var_id_asignatura_filtro']
        self.var_nombre_asignatura_filtro: StringVar = self.map_vars['var_nombre_asignatura_filtro']

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
        self.cbx_carrera_filtro: Combobox = self.map_widgets['cbx_carrera_filtro']
        self.cbx_asignatura_filtro: Combobox = self.map_widgets['cbx_asignatura_filtro']
        self.btn_limpiar_filtros: Button = self.map_widgets['btn_limpiar_filtros']

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

    def _cargar_carreras(self):
        """
        Carga la lista de carreras desde la BD y las agrega al combobox de filtro.
        Mantiene dos diccionarios sincronizados para conversión id <-> nombre.
        """
        try:
            # Limpiar diccionarios previos
            self.dict_carreras.clear()
            self.dict_carreras_inv.clear()

            # Obtener carreras de la BD
            dao = CarreraDAO(ruta_db=None)
            sql = "SELECT id_carrera, nombre FROM carrera ORDER BY nombre"
            params = ()
            lista_aux = dao.ejecutar_consulta(sql=sql, params=params)

            if lista_aux:
                nombres_carreras = []
                for data in lista_aux:
                    id_carrera = data.get('id_carrera')
                    nombre_carrera = data.get('nombre')
                    # Agregar a diccionarios bidireccionales
                    self.dict_carreras[id_carrera] = nombre_carrera
                    self.dict_carreras_inv[nombre_carrera] = id_carrera
                    nombres_carreras.append(nombre_carrera)

                # Cargar nombres en el combobox
                self.cbx_carrera_filtro['values'] = nombres_carreras
                logger.info(f"Se cargaron {len(nombres_carreras)} carreras en el filtro")
            else:
                logger.warning("No se encontraron carreras en la BD")
                self.cbx_carrera_filtro['values'] = []

        except Exception as e:
            logger.error(f"Error al cargar carreras: {e}")
            self.cbx_carrera_filtro['values'] = []

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

    def _on_carrera_filtro_seleccionada(self, event=None):
        """
        Evento disparado cuando el usuario selecciona una carrera en el filtro.
        Actualiza las asignaturas disponibles según la carrera seleccionada.
        También actualiza el combobox de asignaturas en el formulario.
        """
        nombre_carrera = self.var_nombre_carrera_filtro.get()
        self.id_carrera_filtro_actual = self.dict_carreras_inv.get(nombre_carrera, 0)

        logger.debug(
            f"Carrera filtro seleccionada: {nombre_carrera} (ID: {self.id_carrera_filtro_actual})"
        )

        # Limpiar filtro de asignatura
        self.var_nombre_asignatura_filtro.set("")
        self.id_asignatura_filtro_actual = 0

        # Cargar asignaturas de la carrera seleccionada en el filtro
        self._cargar_asignaturas_filtro_por_carrera(self.id_carrera_filtro_actual)

        # Actualizar también el combobox de asignaturas en el formulario
        self._cargar_asignaturas_formulario_por_carrera(self.id_carrera_filtro_actual)

        # Actualizar tabla con el filtro
        self._actualizar_tabla_eje_tematico()

    def _on_asignatura_filtro_seleccionada(self, event=None):
        """
        Evento disparado cuando el usuario selecciona una asignatura en el filtro.
        """
        nombre_asignatura = self.var_nombre_asignatura_filtro.get()

        # Buscar el ID de la asignatura en el diccionario general
        self.id_asignatura_filtro_actual = self.dict_asignaturas_inv.get(nombre_asignatura, 0)

        logger.debug(
            f"Asignatura filtro seleccionada: {nombre_asignatura} (ID: {self.id_asignatura_filtro_actual})"
        )

        # Actualizar tabla con los filtros aplicados
        self._actualizar_tabla_eje_tematico()

    def _on_limpiar_filtros(self):
        """
        Evento disparado al hacer clic en el botón de limpiar filtros.
        Resetea todos los filtros y muestra todos los ejes temáticos.
        También restaura todas las asignaturas en el formulario.
        """
        self.var_nombre_carrera_filtro.set("")
        self.var_nombre_asignatura_filtro.set("")
        self.id_carrera_filtro_actual = 0
        self.id_asignatura_filtro_actual = 0

        # Restaurar todas las asignaturas en el combobox de filtro
        self._cargar_asignaturas_filtro()

        # Restaurar todas las asignaturas en el combobox del formulario
        self._cargar_asignaturas()

        # Actualizar tabla
        self._actualizar_tabla_eje_tematico()

        logger.info("Filtros limpiados, mostrando todos los ejes temáticos")

    def _cargar_asignaturas_filtro(self):
        """
        Carga todas las asignaturas en el combobox de filtro.
        """
        try:
            nombres_asignaturas = []
            for label_asignatura in sorted(self.dict_asignaturas_inv.keys()):
                nombres_asignaturas.append(label_asignatura)

            self.cbx_asignatura_filtro['values'] = nombres_asignaturas
            logger.info(f"Se cargaron {len(nombres_asignaturas)} asignaturas en filtro")

        except Exception as e:
            logger.error(f"Error al cargar asignaturas en filtro: {e}")
            self.cbx_asignatura_filtro['values'] = []

    def _cargar_asignaturas_filtro_por_carrera(self, id_carrera: int):
        """
        Carga las asignaturas que pertenecen a una carrera específica en el combobox de filtro.

        Args:
            id_carrera (int): ID de la carrera a filtrar
        """
        try:
            if id_carrera <= 0:
                self.cbx_asignatura_filtro['values'] = []
                return

            # Obtener asignaturas de la carrera
            dao = AsignaturaDAO(ruta_db=None)
            sql = "SELECT id_asignatura, nombre, codigo FROM asignatura WHERE id_carrera = ? ORDER BY nombre"
            params = (id_carrera,)
            lista_aux = dao.ejecutar_consulta(sql=sql, params=params)

            nombres_asignaturas = []
            if lista_aux:
                for data in lista_aux:
                    id_asignatura = data.get('id_asignatura')
                    nombre_asignatura = data.get('nombre')
                    codigo_asignatura = data.get('codigo')
                    label_asignatura = f"{nombre_asignatura} - {codigo_asignatura}"
                    nombres_asignaturas.append(label_asignatura)

            self.cbx_asignatura_filtro['values'] = nombres_asignaturas
            logger.info(
                f"Se cargaron {len(nombres_asignaturas)} asignaturas de la carrera {id_carrera}"
            )

        except Exception as e:
            logger.error(f"Error al cargar asignaturas por carrera: {e}")
            self.cbx_asignatura_filtro['values'] = []

    def _cargar_asignaturas_formulario_por_carrera(self, id_carrera: int):
        """
        Carga las asignaturas que pertenecen a una carrera específica en el combobox del formulario.
        Esto facilita la inserción de nuevos ejes temáticos mostrando solo las asignaturas relevantes.

        Args:
            id_carrera (int): ID de la carrera a filtrar
        """
        try:
            if id_carrera <= 0:
                # Si no hay carrera seleccionada, mostrar todas
                self._cargar_asignaturas()
                return

            # Obtener asignaturas de la carrera
            dao = AsignaturaDAO(ruta_db=None)
            sql = "SELECT id_asignatura, nombre, codigo FROM asignatura WHERE id_carrera = ? ORDER BY nombre"
            params = (id_carrera,)
            lista_aux = dao.ejecutar_consulta(sql=sql, params=params)

            # Limpiar diccionarios y reconstruir solo con asignaturas de esta carrera
            self.dict_asignaturas.clear()
            self.dict_asignaturas_inv.clear()

            nombres_asignaturas = []
            if lista_aux:
                for data in lista_aux:
                    id_asignatura = data.get('id_asignatura')
                    nombre_asignatura = data.get('nombre')
                    codigo_asignatura = data.get('codigo')
                    label_asignatura = f"{nombre_asignatura} - {codigo_asignatura}"

                    # Reconstruir diccionarios
                    self.dict_asignaturas[id_asignatura] = label_asignatura
                    self.dict_asignaturas_inv[label_asignatura] = id_asignatura
                    nombres_asignaturas.append(label_asignatura)

            self.cbx_asignatura['values'] = nombres_asignaturas
            logger.info(
                f"Se cargaron {len(nombres_asignaturas)} asignaturas de la carrera {id_carrera} en el formulario"
            )

        except Exception as e:
            logger.error(f"Error al cargar asignaturas en el formulario por carrera: {e}")
            self._cargar_asignaturas()

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
