from typing import Dict, Any, List
from datetime import datetime
from tkinter.messagebox import showinfo, showwarning, askyesno
from ttkbootstrap import Button, Entry, StringVar, IntVar, Label, Combobox, Text
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from modelos.services.estudiante_carrera_service import EstudianteCarreraService
from modelos.dtos.estudiante_carrera_dto import EstudianteCarreraDTO
from modelos.daos.estudiante_dao import EstudianteDAO
from modelos.daos.carrera_dao import CarreraDAO
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class ControlarAdministrarEstudianteCarrera:

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

        # Servicio principal
        self.ec_service = EstudianteCarreraService()

        # Diccionarios para estudiantes
        self.dict_estudiantes: Dict[int, str] = {}  # id -> "Nombre - Correo"
        self.dict_estudiantes_inv: Dict[str, int] = {}  # "Nombre - Correo" -> id

        # Diccionarios para carreras
        self.dict_carreras: Dict[int, str] = {}  # id -> "Nombre - Plan"
        self.dict_carreras_inv: Dict[str, int] = {}  # "Nombre - Plan" -> id

        # ID del estudiante seleccionado actualmente
        self.id_estudiante_actual: int = 0

        # Lista de inscripciones del estudiante actual
        self.lista_inscripciones: List[Dict[str, Any]] = []

        # cargar widgets
        self._cargar_widgets()

        # cargar los vars
        self._cargar_vars()

        # cargar estudiantes
        self._cargar_estudiantes()

        # cargar carreras
        self._cargar_carreras()

        # mostrar estadísticas
        self._actualizar_estadisticas()

        # vincular eventos
        self._vincular_eventos()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Métodos Privados
    # └────────────────────────────────────────────────────────────┘
    def _vincular_eventos(self):
        # Combobox de estudiante
        self.cbx_estudiante.bind("<<ComboboxSelected>>", self._on_estudiante_seleccionado)

        # Botón refrescar
        self.btn_refrescar_estudiante.config(command=self._on_refrescar_estudiante)

        # Filtro de estado
        self.cbx_filtro_estado.bind("<<ComboboxSelected>>", self._on_filtro_cambiado)

        # Evento de selección en tabla
        self.tabla_carreras.view.bind("<Double-Button-1>", self._on_tabla_doble_click)

        # Botones del formulario
        self.btn_nuevo.config(command=self._on_nuevo)
        self.btn_aplicar.config(command=self._on_aplicar)
        self.btn_eliminar.config(command=self._on_eliminar)
        self.btn_cambiar_estado.config(command=self._on_cambiar_estado)
        self.btn_completar.config(command=self._on_completar)

    def _cargar_vars(self):
        self.var_id_estudiante: IntVar = self.map_vars['var_id_estudiante']
        self.var_nombre_estudiante: StringVar = self.map_vars['var_nombre_estudiante']
        self.var_id_carrera: IntVar = self.map_vars['var_id_carrera']
        self.var_nombre_carrera: StringVar = self.map_vars['var_nombre_carrera']
        self.var_estado: StringVar = self.map_vars['var_estado']
        self.var_fecha_inscripcion: StringVar = self.map_vars['var_fecha_inscripcion']
        self.var_fecha_inicio: StringVar = self.map_vars['var_fecha_inicio']
        self.var_fecha_fin: StringVar = self.map_vars['var_fecha_fin']
        self.var_es_principal: IntVar = self.map_vars['var_es_principal']
        self.var_periodo_ingreso: StringVar = self.map_vars['var_periodo_ingreso']
        self.var_filtro_estado: StringVar = self.map_vars['var_filtro_estado']

    def _cargar_widgets(self):
        self.cbx_estudiante: Combobox = self.map_widgets['cbx_estudiante']
        self.btn_refrescar_estudiante: Button = self.map_widgets['btn_refrescar_estudiante']
        self.cbx_filtro_estado: Combobox = self.map_widgets['cbx_filtro_estado']
        self.tabla_carreras: Tableview = self.map_widgets['tabla_carreras']
        self.entry_id_estudiante: Entry = self.map_widgets['entry_id_estudiante']
        self.cbx_carrera: Combobox = self.map_widgets['cbx_carrera']
        self.cbx_estado: Combobox = self.map_widgets['cbx_estado']
        self.entry_fecha_inscripcion: Entry = self.map_widgets['entry_fecha_inscripcion']
        self.entry_fecha_inicio: Entry = self.map_widgets['entry_fecha_inicio']
        self.entry_fecha_fin: Entry = self.map_widgets['entry_fecha_fin']
        self.chk_es_principal: Button = self.map_widgets['chk_es_principal']
        self.entry_periodo: Entry = self.map_widgets['entry_periodo']
        self.text_observaciones: Text = self.map_widgets['text_observaciones']
        self.btn_nuevo: Button = self.map_widgets['btn_nuevo']
        self.btn_aplicar: Button = self.map_widgets['btn_aplicar']
        self.btn_eliminar: Button = self.map_widgets['btn_eliminar']
        self.btn_cambiar_estado: Button = self.map_widgets['btn_cambiar_estado']
        self.btn_completar: Button = self.map_widgets['btn_completar']
        self.lbl_estadisticas: Label = self.map_widgets['lbl_estadisticas']

    def _cargar_estudiantes(self):
        """Carga la lista de estudiantes en el combobox"""
        try:
            self.dict_estudiantes.clear()
            self.dict_estudiantes_inv.clear()

            dao = EstudianteDAO()
            sql = "SELECT id_estudiante, nombre, correo FROM estudiante ORDER BY nombre"
            estudiantes = dao.ejecutar_consulta(sql, ())

            if estudiantes:
                lista_labels = []
                for est in estudiantes:
                    id_est = est['id_estudiante']
                    nombre = est['nombre']
                    correo = est['correo']
                    label = f"{nombre} - {correo}"

                    self.dict_estudiantes[id_est] = label
                    self.dict_estudiantes_inv[label] = id_est
                    lista_labels.append(label)

                self.cbx_estudiante['values'] = lista_labels
                logger.info(f"Cargados {len(lista_labels)} estudiantes")
            else:
                self.cbx_estudiante['values'] = []
                logger.warning("No se encontraron estudiantes")

        except Exception as e:
            logger.error(f"Error al cargar estudiantes: {e}", exc_info=True)
            self.cbx_estudiante['values'] = []

    def _cargar_carreras(self):
        """Carga la lista de carreras en el combobox"""
        try:
            self.dict_carreras.clear()
            self.dict_carreras_inv.clear()

            dao = CarreraDAO()
            sql = "SELECT id_carrera, nombre, plan FROM carrera ORDER BY nombre"
            carreras = dao.ejecutar_consulta(sql, ())

            if carreras:
                lista_labels = []
                for carr in carreras:
                    id_carr = carr['id_carrera']
                    nombre = carr['nombre']
                    plan = carr['plan']
                    label = f"{nombre} - {plan}"

                    self.dict_carreras[id_carr] = label
                    self.dict_carreras_inv[label] = id_carr
                    lista_labels.append(label)

                self.cbx_carrera['values'] = lista_labels
                logger.info(f"Cargadas {len(lista_labels)} carreras")
            else:
                self.cbx_carrera['values'] = []
                logger.warning("No se encontraron carreras")

        except Exception as e:
            logger.error(f"Error al cargar carreras: {e}", exc_info=True)
            self.cbx_carrera['values'] = []

    def _actualizar_tabla_carreras(self):
        """Actualiza la tabla con las carreras del estudiante actual"""
        if self.id_estudiante_actual <= 0:
            return

        try:
            # Verificar que la tabla existe
            if not self.tabla_carreras.winfo_exists():
                return

            # Obtener filtro
            filtro_estado = self.var_filtro_estado.get()

            # Obtener carreras
            if filtro_estado == "Todos":
                carreras = self.ec_service.obtener_carreras_estudiante(self.id_estudiante_actual)
            else:
                carreras = self.ec_service.obtener_carreras_estudiante(
                    self.id_estudiante_actual, estado=filtro_estado
                )

            self.lista_inscripciones = carreras

            # Limpiar tabla
            self.tabla_carreras.delete_rows()

            # Llenar tabla
            for inscripcion in carreras:
                id_estudiante = inscripcion['id_estudiante']
                id_carrera = inscripcion['id_carrera']
                nombre_carrera = inscripcion['nombre_carrera']
                estado = inscripcion['estado']
                es_principal = "⭐" if inscripcion.get('es_carrera_principal') == 1 else "☆"
                fecha_inscripcion = inscripcion.get('fecha_inscripcion', '')
                periodo = inscripcion.get('periodo_ingreso', '')

                self.tabla_carreras.insert_row(
                    index=END,
                    values=(
                        id_estudiante,
                        id_carrera,
                        nombre_carrera,
                        estado,
                        es_principal,
                        fecha_inscripcion,
                        periodo,
                    ),
                )

            self.tabla_carreras.autofit_columns()
            logger.info(f"Tabla actualizada con {len(carreras)} inscripciones")

        except Exception as e:
            logger.error(f"Error al actualizar tabla: {e}", exc_info=True)

    def _actualizar_estadisticas(self):
        """Actualiza el label de estadísticas"""
        try:
            # Verificar que el widget existe
            if not self.lbl_estadisticas.winfo_exists():
                return

            if self.id_estudiante_actual <= 0:
                self.lbl_estadisticas['text'] = "Seleccione un estudiante para comenzar"
                return

            nombre = self.var_nombre_estudiante.get()
            carreras = self.ec_service.obtener_carreras_estudiante(self.id_estudiante_actual)

            total = len(carreras)
            activas = len([c for c in carreras if c['estado'] == 'activa'])
            completadas = len([c for c in carreras if c['estado'] == 'completada'])

            msg = f"Estudiante: {nombre.split(' - ')[0]} | Total carreras: {total} | "
            msg += f"Activas: {activas} | Completadas: {completadas}"

            self.lbl_estadisticas['text'] = msg

        except Exception as e:
            logger.error(f"Error al actualizar estadísticas: {e}", exc_info=True)
            # No intentar actualizar el label si ya fue destruido
            try:
                if self.lbl_estadisticas.winfo_exists():
                    self.lbl_estadisticas['text'] = "Error al cargar estadísticas"
            except:
                pass

    def _limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.var_id_carrera.set(0)
        self.var_nombre_carrera.set("")
        self.var_estado.set('activa')
        self.var_fecha_inscripcion.set("")
        self.var_fecha_inicio.set("")
        self.var_fecha_fin.set("")
        self.var_es_principal.set(1)
        self.var_periodo_ingreso.set("")
        self.text_observaciones.delete("1.0", END)

        # Actualizar botón de principal
        self.chk_es_principal.config(text="⭐ Es Carrera Principal", bootstyle="warning")

    def _cargar_formulario(self, inscripcion: Dict[str, Any]):
        """Carga los datos de una inscripción en el formulario"""
        try:
            # Carrera
            id_carrera = inscripcion['id_carrera']
            self.var_id_carrera.set(id_carrera)
            label_carrera = self.dict_carreras.get(id_carrera, "")
            self.var_nombre_carrera.set(label_carrera)

            # Datos de inscripción
            self.var_estado.set(inscripcion['estado'])
            self.var_fecha_inscripcion.set(inscripcion.get('fecha_inscripcion', ''))
            self.var_fecha_inicio.set(inscripcion.get('fecha_inicio', '') or '')
            self.var_fecha_fin.set(inscripcion.get('fecha_fin', '') or '')

            es_principal = inscripcion.get('es_carrera_principal', 0)
            self.var_es_principal.set(es_principal)

            # Actualizar botón
            if es_principal == 1:
                self.chk_es_principal.config(text="⭐ Es Carrera Principal", bootstyle="warning")
            else:
                self.chk_es_principal.config(text="☆ No es Principal", bootstyle="warning-outline")

            self.var_periodo_ingreso.set(inscripcion.get('periodo_ingreso', '') or '')

            # Observaciones
            self.text_observaciones.delete("1.0", END)
            obs = inscripcion.get('observaciones', '')
            if obs:
                self.text_observaciones.insert("1.0", obs)

            logger.info(
                f"Formulario cargado con inscripción: Est {inscripcion['id_estudiante']} - Car {id_carrera}"
            )

        except Exception as e:
            logger.error(f"Error al cargar formulario: {e}", exc_info=True)

    def _obtener_dto_desde_formulario(self) -> EstudianteCarreraDTO:
        """Crea un DTO con los datos del formulario"""
        dto = EstudianteCarreraDTO()

        dto.id_estudiante = self.var_id_estudiante.get()

        # Obtener id de carrera desde el combobox
        label_carrera = self.var_nombre_carrera.get()
        dto.id_carrera = self.dict_carreras_inv.get(label_carrera, 0)

        dto.estado = self.var_estado.get()
        dto.fecha_inscripcion = self.var_fecha_inscripcion.get() or None
        dto.fecha_inicio = self.var_fecha_inicio.get() or None
        dto.fecha_fin = self.var_fecha_fin.get() or None
        dto.es_carrera_principal = self.var_es_principal.get()
        dto.periodo_ingreso = self.var_periodo_ingreso.get() or None

        # Observaciones
        obs = self.text_observaciones.get("1.0", END).strip()
        dto.observaciones = obs if obs else None

        return dto

    # ┌────────────────────────────────────────────────────────────┐
    # │ Event Handlers
    # └────────────────────────────────────────────────────────────┘
    def _on_estudiante_seleccionado(self, event=None):
        """Evento cuando se selecciona un estudiante"""
        try:
            label_estudiante = self.var_nombre_estudiante.get()
            id_estudiante = self.dict_estudiantes_inv.get(label_estudiante, 0)

            if id_estudiante > 0:
                self.id_estudiante_actual = id_estudiante
                self.var_id_estudiante.set(id_estudiante)

                # Actualizar tabla y estadísticas
                self._actualizar_tabla_carreras()
                self._actualizar_estadisticas()

                # Limpiar formulario
                self._limpiar_formulario()

                logger.info(f"Estudiante seleccionado: {id_estudiante}")

        except Exception as e:
            logger.error(f"Error al seleccionar estudiante: {e}", exc_info=True)

    def _on_refrescar_estudiante(self):
        """Refresca la lista de estudiantes"""
        self._cargar_estudiantes()
        showinfo("Actualizado", "Lista de estudiantes actualizada")

    def _on_filtro_cambiado(self, event=None):
        """Evento cuando cambia el filtro de estado"""
        self._actualizar_tabla_carreras()

    def _on_tabla_doble_click(self, event=None):
        """Evento de doble click en la tabla"""
        try:
            # Obtener fila seleccionada
            selected = self.tabla_carreras.view.selection()
            if not selected:
                return

            item = self.tabla_carreras.view.item(selected[0])
            values = item['values']

            if not values or len(values) < 7:
                return

            id_estudiante = int(values[0])
            id_carrera = int(values[1])

            # Buscar la inscripción en la lista
            inscripcion = None
            for insc in self.lista_inscripciones:
                if insc['id_estudiante'] == id_estudiante and insc['id_carrera'] == id_carrera:
                    inscripcion = insc
                    break

            if inscripcion:
                self._cargar_formulario(inscripcion)
            else:
                logger.warning(f"No se encontró inscripción: Est {id_estudiante}, Car {id_carrera}")

        except Exception as e:
            logger.error(f"Error en doble click: {e}", exc_info=True)

    def _on_nuevo(self):
        """Limpia el formulario para crear nueva inscripción"""
        self._limpiar_formulario()

        # Establecer fecha actual por defecto
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        self.var_fecha_inscripcion.set(fecha_actual)

        logger.info("Formulario limpiado para nueva inscripción")

    def _on_aplicar(self):
        """Guarda o actualiza una inscripción"""
        if self.id_estudiante_actual <= 0:
            showwarning("Advertencia", "Debe seleccionar un estudiante primero")
            return

        try:
            dto = self._obtener_dto_desde_formulario()

            # Validaciones básicas
            if dto.id_carrera <= 0:
                showwarning("Advertencia", "Debe seleccionar una carrera")
                return

            if not dto.fecha_inscripcion:
                showwarning("Advertencia", "La fecha de inscripción es obligatoria")
                return

            # Verificar si existe
            existe = self.ec_service.dao.existe(dto)

            if existe:
                # Actualizar
                if self.ec_service.actualizar_inscripcion(dto):
                    showinfo("Éxito", "Inscripción actualizada correctamente")
                    self._actualizar_tabla_carreras()
                    self._actualizar_estadisticas()
                    self._limpiar_formulario()
                else:
                    showwarning("Error", "No se pudo actualizar la inscripción")
            else:
                # Insertar
                if self.ec_service.inscribir_estudiante(dto):
                    showinfo("Éxito", "Estudiante inscrito en carrera correctamente")
                    self._actualizar_tabla_carreras()
                    self._actualizar_estadisticas()
                    self._limpiar_formulario()
                else:
                    showwarning("Error", "No se pudo inscribir al estudiante")

        except Exception as e:
            logger.error(f"Error al aplicar: {e}", exc_info=True)
            showwarning("Error", f"Error al guardar:\n{str(e)}")

    def _on_eliminar(self):
        """Elimina una inscripción"""
        if self.id_estudiante_actual <= 0:
            showwarning("Advertencia", "Debe seleccionar un estudiante")
            return

        try:
            label_carrera = self.var_nombre_carrera.get()
            id_carrera = self.dict_carreras_inv.get(label_carrera, 0)

            if id_carrera <= 0:
                showwarning("Advertencia", "Debe seleccionar una carrera de la tabla")
                return

            # Confirmar
            nombre_est = self.var_nombre_estudiante.get().split(' - ')[0]
            nombre_car = label_carrera.split(' - ')[0]

            if not askyesno(
                "Confirmar", f"¿Eliminar inscripción de '{nombre_est}' en '{nombre_car}'?"
            ):
                return

            dto = EstudianteCarreraDTO(
                id_estudiante=self.id_estudiante_actual, id_carrera=id_carrera
            )

            if self.ec_service.eliminar_inscripcion(dto):
                showinfo("Éxito", "Inscripción eliminada correctamente")
                self._actualizar_tabla_carreras()
                self._actualizar_estadisticas()
                self._limpiar_formulario()
            else:
                showwarning("Error", "No se pudo eliminar la inscripción")

        except Exception as e:
            logger.error(f"Error al eliminar: {e}", exc_info=True)
            showwarning("Error", f"Error al eliminar:\n{str(e)}")

    def _on_cambiar_estado(self):
        """Cambia el estado de una inscripción"""
        if self.id_estudiante_actual <= 0:
            showwarning("Advertencia", "Debe seleccionar un estudiante")
            return

        try:
            label_carrera = self.var_nombre_carrera.get()
            id_carrera = self.dict_carreras_inv.get(label_carrera, 0)

            if id_carrera <= 0:
                showwarning("Advertencia", "Debe seleccionar una carrera de la tabla")
                return

            nuevo_estado = self.var_estado.get()

            if self.ec_service.cambiar_estado(self.id_estudiante_actual, id_carrera, nuevo_estado):
                showinfo("Éxito", f"Estado cambiado a '{nuevo_estado}'")
                self._actualizar_tabla_carreras()
                self._actualizar_estadisticas()
            else:
                showwarning("Error", "No se pudo cambiar el estado")

        except Exception as e:
            logger.error(f"Error al cambiar estado: {e}", exc_info=True)
            showwarning("Error", f"Error:\n{str(e)}")

    def _on_completar(self):
        """Marca una carrera como completada"""
        if self.id_estudiante_actual <= 0:
            showwarning("Advertencia", "Debe seleccionar un estudiante")
            return

        try:
            label_carrera = self.var_nombre_carrera.get()
            id_carrera = self.dict_carreras_inv.get(label_carrera, 0)

            if id_carrera <= 0:
                showwarning("Advertencia", "Debe seleccionar una carrera de la tabla")
                return

            # Fecha de fin
            fecha_fin = self.var_fecha_fin.get()
            if not fecha_fin:
                fecha_fin = datetime.now().strftime('%Y-%m-%d')
                if not askyesno("Confirmar", f"¿Marcar como completada con fecha {fecha_fin}?"):
                    return

            if self.ec_service.completar_carrera(self.id_estudiante_actual, id_carrera, fecha_fin):
                showinfo("Éxito", "Carrera marcada como completada")
                self._actualizar_tabla_carreras()
                self._actualizar_estadisticas()
                self._limpiar_formulario()
            else:
                showwarning("Error", "No se pudo completar la carrera")

        except Exception as e:
            logger.error(f"Error al completar: {e}", exc_info=True)
            showwarning("Error", f"Error:\n{str(e)}")
