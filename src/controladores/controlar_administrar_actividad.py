from typing import Dict, Any, List, Optional
from tkinter.messagebox import askyesno, showinfo
from ttkbootstrap import Button, Entry, StringVar, IntVar, Label, Text, Combobox
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from modelos.daos.actividad_dao import ActividadDAO
from modelos.daos.eje_tematico_dao import EjeTematicoDAO
from modelos.daos.tipo_actividad_dao import TipoActividadDAO
from modelos.services.actividad_service import ActividadService
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class ControlarAdministrarActividad:

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
        # para almacenar las actividades
        self.lista_actividades: List[ActividadService] = []

        # Índice de la actividad actual en la navegación
        self.indice_actual: int = -1

        # Diccionarios para ejes temáticos: id_eje -> nombre_eje y viceversa
        self.dict_ejes: Dict[int, str] = {}
        self.dict_ejes_inv: Dict[str, int] = {}

        # Diccionarios para tipos de actividad: id_tipo -> nombre_tipo y viceversa
        self.dict_tipos: Dict[int, str] = {}
        self.dict_tipos_inv: Dict[str, int] = {}
        self.dict_tipos_siglas: Dict[int, str] = {}  # id_tipo -> siglas

        # Diccionarios para carreras: id_carrera -> nombre_carrera y viceversa
        self.dict_carreras: Dict[int, str] = {}
        self.dict_carreras_inv: Dict[str, int] = {}

        # cargar widgets
        self._cargar_widgets()

        # cargar los vars
        self._cargar_vars()

        # cargar los ejes temáticos en el combobox
        self._cargar_ejes_tematicos()

        # cargar los tipos de actividad en el combobox
        self._cargar_tipos_actividad()

        # cargar las carreras en el combobox
        self._cargar_carreras()

        # mostrar las estadistica en el panel inferior
        self._actualizar_estadisticas()

        # mostramos las actividades en la tabla
        self._actualizar_tabla_actividad()

        # viculamos los eventos
        self._vincular_eventos()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos Privados
    # └────────────────────────────────────────────────────────────┘
    def _vincular_eventos(self):
        # Vincular el evento de doble clic
        self.tabla_actividad.view.bind("<Double-Button-1>", self._on_tabla_doble_click)
        # Vinculamos el evento nuevo
        self.btn_nuevo.config(command=self._on_nuevo)
        self.btn_aplicar.config(command=self._on_aplicar)
        self.btn_eliminar.config(command=self._on_eliminar_actividad)
        # Vinculamos los botones de desplazamiento
        self.btn_primero.config(command=self._on_primero)
        self.btn_anterior.config(command=self._on_anterior)
        self.btn_siguiente.config(command=self._on_siguiente)
        self.btn_ultimo.config(command=self._on_ultimo)
        # Vinculamos eventos de selección en comboboxes
        self.cbx_eje.bind("<<ComboboxSelected>>", self._on_eje_seleccionado)
        self.cbx_tipo_actividad.bind("<<ComboboxSelected>>", self._on_tipo_seleccionado)
        self.cbx_carrera_filtro.bind("<<ComboboxSelected>>", self._on_carrera_filtro_seleccionada)

    def _establecer_actividad(self) -> ActividadService:
        actividad = ActividadService(ruta_db=None)
        # establecemos variables
        id_actividad = self.var_id_actividad.get()
        titulo = self.var_titulo.get()
        fecha_inicio = self.var_fecha_inicio.get()
        fecha_fin = self.var_fecha_fin.get()
        descripcion = self.text_descripcion.get("1.0", END).strip()
        label_eje = self.var_nombre_eje.get()
        label_tipo = self.var_nombre_tipo_actividad.get()
        # Convertir nombres a ids
        id_eje = self.dict_ejes_inv.get(label_eje, 0)
        id_tipo_actividad = self.dict_tipos_inv.get(label_tipo, 0)
        # cargamos los datos a la actividad
        actividad.id_actividad = id_actividad
        actividad.titulo = titulo
        actividad.descripcion = descripcion
        actividad.fecha_inicio = fecha_inicio
        actividad.fecha_fin = fecha_fin
        actividad.id_eje = id_eje
        actividad.id_tipo_actividad = id_tipo_actividad
        return actividad

    def _cargar_formulario(self, actividad: ActividadService):
        if actividad:
            self.var_id_actividad.set(actividad.id_actividad)
            self.var_titulo.set(actividad.titulo)
            self.var_fecha_inicio.set(actividad.fecha_inicio or "")
            self.var_fecha_fin.set(actividad.fecha_fin or "")
            self.var_id_eje.set(actividad.id_eje)
            self.var_id_tipo_actividad.set(actividad.id_tipo_actividad)
            # Cargar descripción en el widget Text
            self.text_descripcion.delete("1.0", END)
            if actividad.descripcion:
                self.text_descripcion.insert("1.0", actividad.descripcion)
            # Convertir ids a labels
            label_eje = self.dict_ejes.get(actividad.id_eje, "")
            self.var_nombre_eje.set(label_eje)
            label_tipo = self.dict_tipos.get(actividad.id_tipo_actividad, "")
            self.var_nombre_tipo_actividad.set(label_tipo)
            # Actualizar estadísticas de la actividad seleccionada
            self._actualizar_estadisticas_actividad(actividad.id_actividad)

    def _limpiar_formulario(self):
        self.var_id_actividad.set(0)
        self.var_titulo.set("")
        self.var_fecha_inicio.set("")
        self.var_fecha_fin.set("")
        self.var_id_eje.set(0)
        self.var_id_tipo_actividad.set(0)
        self.var_nombre_eje.set("")
        self.var_nombre_tipo_actividad.set("")
        self.text_descripcion.delete("1.0", END)

    def _insertar_fila(self, actividad: ActividadService):
        if actividad:
            # Convertir ids a labels para mostrar en tabla
            label_eje = self.dict_ejes.get(actividad.id_eje, "N/A")
            # Usar siglas en lugar del nombre completo para tipo
            siglas_tipo = self.dict_tipos_siglas.get(actividad.id_tipo_actividad, "N/A")

            # Obtener nombre de carrera desde eje -> asignatura -> carrera
            nombre_carrera = self._obtener_nombre_carrera(actividad.id_eje)

            self.tabla_actividad.insert_row(
                index=END,
                values=(
                    actividad.id_actividad,
                    actividad.titulo,
                    nombre_carrera,
                    actividad.fecha_inicio or "",
                    actividad.fecha_fin or "",
                    label_eje,
                    siglas_tipo,
                ),
            )

    def _obtener_nombre_carrera(self, id_eje: int) -> str:
        """
        Obtiene el nombre de la carrera a partir del ID del eje temático.
        Eje -> Asignatura -> Carrera
        """
        try:
            from modelos.daos.eje_tematico_dao import EjeTematicoDAO
            from modelos.daos.asignatura_dao import AsignaturaDAO
            from modelos.daos.carrera_dao import CarreraDAO

            # Obtener asignatura del eje
            dao_eje = EjeTematicoDAO(ruta_db=None)
            eje = dao_eje.obtener_por_id(id_eje)
            if not eje:
                return "N/A"

            id_asignatura = eje.id_asignatura

            # Obtener carrera de la asignatura
            dao_asig = AsignaturaDAO(ruta_db=None)
            asignatura = dao_asig.obtener_por_id(id_asignatura)
            if not asignatura:
                return "N/A"

            id_carrera = asignatura.id_carrera

            # Obtener nombre de la carrera
            dao_carrera = CarreraDAO(ruta_db=None)
            carrera = dao_carrera.obtener_por_id(id_carrera)
            if not carrera:
                return "N/A"

            return carrera.nombre

        except Exception as e:
            logger.error(f"Error al obtener nombre de carrera: {e}")
            return "N/A"

    def _actualizar_tabla_actividad(self):
        # obtenemos la lista de actividades
        self._obtener_actividades()
        if self.lista_actividades:
            # limpiamos la tabla
            self.tabla_actividad.delete_rows()
            for actividad in self.lista_actividades:
                self._insertar_fila(actividad=actividad)

            # ajustamos las columnas
            self.tabla_actividad.autofit_columns()

    def _obtener_actividades(self):
        """
        Obtiene las actividades de la BD, aplicando filtro de carrera si está seleccionado.
        """
        if self.lista_actividades:
            self.lista_actividades.clear()

        dao = ActividadDAO(ruta_db=None)

        # Obtener ID de carrera del filtro
        id_carrera_filtro = self.map_vars.get('var_id_carrera_filtro', IntVar(value=0)).get()

        # Construir consulta SQL según filtro
        if id_carrera_filtro and id_carrera_filtro > 0:
            # Filtrar por carrera específica
            sql = """
            SELECT a.* 
            FROM actividad a
            INNER JOIN eje_tematico et ON a.id_eje = et.id_eje
            INNER JOIN asignatura asig ON et.id_asignatura = asig.id_asignatura
            WHERE asig.id_carrera = ?
            ORDER BY a.fecha_inicio DESC
            """
            params = (id_carrera_filtro,)
        else:
            # Sin filtro: todas las actividades
            sql = "SELECT * FROM actividad ORDER BY fecha_inicio DESC"
            params = ()

        lista_aux = dao.ejecutar_consulta(sql=sql, params=params)
        if lista_aux:
            for data in lista_aux:
                actividad = ActividadService(ruta_db=None)
                actividad.set_data(data=data)
                self.lista_actividades.append(actividad)

    def _cargar_vars(self):
        self.var_id_actividad: IntVar = self.map_vars['var_id_actividad']
        self.var_titulo: StringVar = self.map_vars['var_titulo']
        self.var_descripcion: StringVar = self.map_vars['var_descripcion']
        self.var_fecha_inicio: StringVar = self.map_vars['var_fecha_inicio']
        self.var_fecha_fin: StringVar = self.map_vars['var_fecha_fin']
        self.var_id_eje: IntVar = self.map_vars['var_id_eje']
        self.var_nombre_eje: StringVar = self.map_vars['var_nombre_eje']
        self.var_id_tipo_actividad: IntVar = self.map_vars['var_id_tipo_actividad']
        self.var_nombre_tipo_actividad: StringVar = self.map_vars['var_nombre_tipo_actividad']
        self.var_id_carrera_filtro: IntVar = self.map_vars['var_id_carrera_filtro']
        self.var_nombre_carrera_filtro: StringVar = self.map_vars['var_nombre_carrera_filtro']

    def _cargar_widgets(self):
        self.tabla_actividad: Tableview = self.map_widgets['tabla_actividad']
        self.lbl_estadisticas: Label = self.map_widgets['lbl_estadisticas']
        self.btn_nuevo: Button = self.map_widgets['btn_nuevo']
        self.btn_aplicar: Button = self.map_widgets['btn_aplicar']
        self.btn_eliminar: Button = self.map_widgets['btn_eliminar']
        self.btn_primero: Button = self.map_widgets['btn_primero']
        self.btn_anterior: Button = self.map_widgets['btn_anterior']
        self.btn_siguiente: Button = self.map_widgets['btn_siguiente']
        self.btn_ultimo: Button = self.map_widgets['btn_ultimo']
        self.text_descripcion: Text = self.map_widgets['text_descripcion']
        self.cbx_eje: Combobox = self.map_widgets['cbx_eje']
        self.cbx_tipo_actividad: Combobox = self.map_widgets['cbx_tipo_actividad']
        self.cbx_carrera_filtro: Combobox = self.map_widgets['cbx_carrera_filtro']

    def _actualizar_estadisticas(self):
        # actualizamos la lista de actividades
        self._obtener_actividades()
        cant_actividades = 0
        if self.lista_actividades:
            cant_actividades = len(self.lista_actividades)

        msg = f"Actividades: {cant_actividades}"

        self.lbl_estadisticas['text'] = msg

    def _cargar_ejes_tematicos(self):
        """
        Carga la lista de ejes temáticos desde la BD y los agrega al combobox.
        Mantiene dos diccionarios sincronizados para conversión id <-> label.
        """
        try:
            # Limpiar diccionarios previos
            self.dict_ejes.clear()
            self.dict_ejes_inv.clear()

            # Obtener ejes temáticos de la BD
            dao = EjeTematicoDAO(ruta_db=None)
            sql = "SELECT id_eje, nombre FROM eje_tematico ORDER BY orden, nombre"
            params = ()
            lista_aux = dao.ejecutar_consulta(sql=sql, params=params)

            if lista_aux:
                # Construir diccionarios y lista de nombres para el combobox
                nombres_ejes = []
                for data in lista_aux:
                    id_eje = data.get('id_eje')
                    nombre_eje = data.get('nombre')
                    # Agregar a diccionarios bidireccionales
                    self.dict_ejes[id_eje] = nombre_eje
                    self.dict_ejes_inv[nombre_eje] = id_eje
                    nombres_ejes.append(nombre_eje)

                # Cargar labels en el combobox
                self.cbx_eje['values'] = nombres_ejes
                logger.info(f"Se cargaron {len(nombres_ejes)} ejes temáticos en el combobox")
            else:
                logger.warning("No se encontraron ejes temáticos en la BD")
                self.cbx_eje['values'] = []

        except Exception as e:
            logger.error(f"Error al cargar ejes temáticos: {e}")
            self.cbx_eje['values'] = []

    def _cargar_tipos_actividad(self):
        """
        Carga la lista de tipos de actividad desde la BD y los agrega al combobox.
        Mantiene dos diccionarios sincronizados para conversión id <-> label.
        Combobox muestra formato: "Nombre - SIGLAS"
        """
        try:
            # Limpiar diccionarios previos
            self.dict_tipos.clear()
            self.dict_tipos_inv.clear()

            # Obtener tipos de actividad de la BD
            dao = TipoActividadDAO(ruta_db=None)
            sql = "SELECT id_tipo_actividad, nombre, siglas FROM tipo_actividad ORDER BY nombre"
            params = ()
            lista_aux = dao.ejecutar_consulta(sql=sql, params=params)

            if lista_aux:
                # Construir diccionarios y lista de labels para el combobox
                labels_tipos = []
                # Diccionario adicional para mapear id -> siglas
                self.dict_tipos_siglas = {}

                for data in lista_aux:
                    id_tipo = data.get('id_tipo_actividad')
                    nombre_tipo = data.get('nombre')
                    siglas_tipo = data.get('siglas')
                    # Crear label con formato: "Nombre - SIGLAS"
                    label_tipo = f"{nombre_tipo} - {siglas_tipo}"
                    # Agregar a diccionarios bidireccionales (label completo para combobox)
                    self.dict_tipos[id_tipo] = label_tipo
                    self.dict_tipos_inv[label_tipo] = id_tipo
                    # Mapear id -> siglas para la tabla
                    self.dict_tipos_siglas[id_tipo] = siglas_tipo
                    labels_tipos.append(label_tipo)

                # Cargar labels en el combobox
                self.cbx_tipo_actividad['values'] = labels_tipos
                logger.info(f"Se cargaron {len(labels_tipos)} tipos de actividad en el combobox")
            else:
                logger.warning("No se encontraron tipos de actividad en la BD")
                self.cbx_tipo_actividad['values'] = []

        except Exception as e:
            logger.error(f"Error al cargar tipos de actividad: {e}")
            self.cbx_tipo_actividad['values'] = []

    def _cargar_carreras(self):
        """
        Carga la lista de carreras desde la BD y las agrega al combobox filtro.
        Incluye opción "Todas las carreras" para mostrar sin filtrar.
        """
        try:
            from modelos.daos.carrera_dao import CarreraDAO

            # Limpiar diccionarios previos
            self.dict_carreras.clear()
            self.dict_carreras_inv.clear()

            # Obtener carreras de la BD
            dao = CarreraDAO(ruta_db=None)
            sql = "SELECT id_carrera, nombre FROM carrera ORDER BY nombre"
            params = ()
            lista_aux = dao.ejecutar_consulta(sql=sql, params=params)

            if lista_aux:
                # Construir diccionarios y lista de labels
                labels_carreras = ["📚 Todas las carreras"]
                self.dict_carreras[0] = "📚 Todas las carreras"
                self.dict_carreras_inv["📚 Todas las carreras"] = 0

                for data in lista_aux:
                    id_carrera = data.get('id_carrera')
                    nombre_carrera = data.get('nombre')
                    label_carrera = f"🎓 {nombre_carrera}"

                    # Agregar a diccionarios
                    self.dict_carreras[id_carrera] = label_carrera
                    self.dict_carreras_inv[label_carrera] = id_carrera
                    labels_carreras.append(label_carrera)

                # Actualizar combobox
                self.cbx_carrera_filtro['values'] = labels_carreras
                # Seleccionar "Todas" por defecto
                self.map_vars['var_nombre_carrera_filtro'].set("📚 Todas las carreras")
                self.map_vars['var_id_carrera_filtro'].set(0)

                logger.info(f"Se cargaron {len(lista_aux)} carreras para filtro")
            else:
                logger.warning("No se encontraron carreras")
                self.cbx_carrera_filtro['values'] = ["📚 Todas las carreras"]
                self.map_vars['var_nombre_carrera_filtro'].set("📚 Todas las carreras")

        except Exception as e:
            logger.error(f"Error al cargar carreras: {e}")
            self.cbx_carrera_filtro['values'] = ["📚 Todas las carreras"]
            self.map_vars['var_nombre_carrera_filtro'].set("📚 Todas las carreras")

    def _actualizar_estadisticas_actividad(self, id_actividad: int):
        """
        Actualiza las estadísticas mostrando la información
        de la actividad seleccionada.

        Args:
            id_actividad (int): ID de la actividad seleccionada
        """
        try:
            if id_actividad <= 0:
                self.lbl_estadisticas['text'] = "Actividades: 0"
                return

            # Obtener título de la actividad
            titulo_actividad = self.var_titulo.get()
            fecha_inicio = self.var_fecha_inicio.get()

            # Actualizar la etiqueta con las estadísticas
            msg = f"Actividad: {titulo_actividad} | Inicio: {fecha_inicio}"
            self.lbl_estadisticas['text'] = msg

            logger.info(f"Estadísticas actualizadas para actividad {id_actividad}")

        except Exception as e:
            logger.error(f"Error al actualizar estadísticas de actividad: {e}")
            self.lbl_estadisticas['text'] = "Error al cargar estadísticas"

    def _on_eje_seleccionado(self, event=None):
        """
        Evento disparado cuando el usuario selecciona un eje temático en el combobox.
        """
        label_eje = self.var_nombre_eje.get()
        id_eje = self.dict_ejes_inv.get(label_eje)
        logger.debug(f"Eje temático seleccionado: {label_eje} (ID: {id_eje})")

    def _on_tipo_seleccionado(self, event=None):
        """
        Evento disparado cuando el usuario selecciona un tipo de actividad en el combobox.
        """
        label_tipo = self.var_nombre_tipo_actividad.get()
        id_tipo = self.dict_tipos_inv.get(label_tipo)
        logger.debug(f"Tipo de actividad seleccionado: {label_tipo} (ID: {id_tipo})")

    def _on_carrera_filtro_seleccionada(self, event=None):
        """
        Evento disparado cuando el usuario selecciona una carrera en el filtro.
        Actualiza la tabla para mostrar solo actividades de esa carrera.
        """
        label_carrera = self.map_vars['var_nombre_carrera_filtro'].get()
        id_carrera = self.dict_carreras_inv.get(label_carrera, 0)
        self.map_vars['var_id_carrera_filtro'].set(id_carrera)

        logger.info(f"Filtro de carrera seleccionado: {label_carrera} (ID: {id_carrera})")

        # Actualizar tabla con el filtro aplicado
        self._actualizar_tabla_actividad()
        self._actualizar_estadisticas()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘

    def _on_tabla_doble_click(self, event):
        """Maneja el doble clic en una fila de la tabla"""
        # Obtener la fila seleccionada
        seleccion = self.tabla_actividad.view.selection()

        if not seleccion:
            return

        # Obtener los valores de la fila
        item = self.tabla_actividad.view.item(seleccion[0])
        valores = item['values']

        # Asignar a las variables
        id_actividad = int(valores[0])
        actividad = ActividadService(ruta_db=None)
        actividad.id_actividad = id_actividad
        if actividad.instanciar():
            self._cargar_formulario(actividad=actividad)

    def _on_nuevo(self):
        self._limpiar_formulario()

    def _on_aplicar(self):
        actividad = self._establecer_actividad()
        if actividad:
            if actividad.id_actividad == 0 or actividad.id_actividad is None:
                # cargamos una nueva actividad a la base de datos
                id_actividad = actividad.insertar()
                if id_actividad != 0:
                    self.var_id_actividad.set(id_actividad)
                    logger.info(f"Se creó la actividad: {actividad}")
                    showinfo(
                        parent=self.master,
                        title="Inserción",
                        message="Actividad insertada con éxito!",
                    )
                    # recargamos la tabla
                    self._actualizar_tabla_actividad()
            else:
                # actualizamos la actividad
                if actividad.actualizar():
                    showinfo(
                        parent=self.master,
                        title="Actualización",
                        message="Actividad actualizada correctamente",
                    )
                    # recargamos la tabla
                    self._actualizar_tabla_actividad()

    def _on_eliminar_actividad(self):
        """Maneja la eliminación de una actividad seleccionada"""
        id_actividad = self.var_id_actividad.get()

        # Validar que haya una actividad seleccionada
        if id_actividad == 0 or id_actividad is None:
            showinfo(
                parent=self.master,
                title="Advertencia",
                message="Debe seleccionar una actividad para eliminar",
            )
            return

        # Pedir confirmación al usuario
        titulo_actividad = self.var_titulo.get()
        confirmacion = askyesno(
            parent=self.master,
            title="Confirmación",
            message=f"¿Desea eliminar la actividad '{titulo_actividad}'?",
        )

        if not confirmacion:
            return

        # Eliminar la actividad
        actividad = ActividadService(ruta_db=None)
        actividad.id_actividad = id_actividad

        try:
            if actividad.eliminar():
                logger.info(f"Se eliminó la actividad con ID: {id_actividad}")
                showinfo(
                    parent=self.master,
                    title="Eliminación",
                    message="Actividad eliminada exitosamente",
                )
                # Limpiar formulario y actualizar tabla
                self._limpiar_formulario()
                self._actualizar_tabla_actividad()
            else:
                logger.error(f"Error al eliminar la actividad con ID: {id_actividad}")
                showinfo(
                    parent=self.master,
                    title="Error",
                    message="Error al eliminar la actividad",
                )
        except Exception as e:
            logger.error(f"Excepción al eliminar actividad: {str(e)}")
            showinfo(
                parent=self.master,
                title="Error",
                message=f"Error inesperado: {str(e)}",
            )

    def _on_primero(self):
        """Carga la primera actividad de la lista"""
        if self.lista_actividades:
            self.indice_actual = 0
            self._cargar_formulario(actividad=self.lista_actividades[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay actividades para mostrar",
            )

    def _on_anterior(self):
        """Carga la actividad anterior en la lista"""
        if not self.lista_actividades:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay actividades para mostrar",
            )
            return

        if self.indice_actual > 0:
            self.indice_actual -= 1
            self._cargar_formulario(actividad=self.lista_actividades[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="Ya está en la primera actividad",
            )

    def _on_siguiente(self):
        """Carga la siguiente actividad en la lista"""
        if not self.lista_actividades:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay actividades para mostrar",
            )
            return

        if self.indice_actual < len(self.lista_actividades) - 1:
            self.indice_actual += 1
            self._cargar_formulario(actividad=self.lista_actividades[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="Ya está en la última actividad",
            )

    def _on_ultimo(self):
        """Carga la última actividad de la lista"""
        if self.lista_actividades:
            self.indice_actual = len(self.lista_actividades) - 1
            self._cargar_formulario(actividad=self.lista_actividades[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay actividades para mostrar",
            )
