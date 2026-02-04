from typing import Dict, Any, List, Optional
from tkinter.messagebox import askyesno, showinfo, showwarning
from ttkbootstrap import Button, Entry, StringVar, IntVar, Label
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from modelos.services.estudiante_service import EstudianteService
from modelos.services.estudiante_carrera_service import EstudianteCarreraService
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class ControlarAdministrarEstudiante:

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
        # para almacenar los estudiantes
        self.lista_estudiantes: List[EstudianteService] = []

        # Índice del estudiante actual en la navegación
        self.indice_actual: int = -1

        # Servicio para gestionar carreras
        self.ec_service = EstudianteCarreraService()

        # cargar widgets
        self._cargar_widgets()

        # cargar los vars
        self._cargar_vars()

        # mostrar las estadistica en el panel inferior
        self._actualizar_estadisticas()

        # mostramos los estudiantes en la tabla
        self._actualizar_tabla_estudiante()

        # viculamos los eventos
        self._vincular_eventos()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos Privados
    # └────────────────────────────────────────────────────────────┘
    def _vincular_eventos(self):
        # Vincular el evento de doble clic
        self.tabla_estudiante.view.bind("<Double-Button-1>", self._on_tabla_doble_click)
        # Vinculamos el evento nuevo
        self.btn_nuevo.config(command=self._on_nuevo)
        self.btn_aplicar.config(command=self._on_aplicar)
        self.btn_eliminar.config(command=self._on_eliminar_estudiante)
        # Vinculamos los botones de desplazamiento
        self.btn_primero.config(command=self._on_primero)
        self.btn_anterior.config(command=self._on_anterior)
        self.btn_siguiente.config(command=self._on_siguiente)
        self.btn_ultimo.config(command=self._on_ultimo)
        # Vincular botón de gestionar carreras
        self.btn_gestionar_carreras.config(command=self._on_gestionar_carreras)

    def _establecer_estudiante(self) -> EstudianteService:
        estudiante = EstudianteService(ruta_db=None)
        # establecemos variables
        id_estudiante = self.var_id.get()
        nombre = self.var_nombre.get()
        correo = self.var_correo.get()
        # cargamos los datos al estudiante
        estudiante.id_estudiante = id_estudiante
        estudiante.nombre = nombre
        estudiante.correo = correo
        return estudiante

    def _cargar_formulario(self, estudiante: EstudianteService):
        if estudiante:
            self.var_id.set(estudiante.id_estudiante)
            self.var_nombre.set(estudiante.nombre)
            self.var_correo.set(estudiante.correo)
            # Actualizar información de carreras
            self._actualizar_info_carreras(estudiante.id_estudiante)
            # Actualizar estadísticas del estudiante seleccionado
            self._actualizar_estadisticas_estudiante(estudiante.id_estudiante)
            # Habilitar botón de gestionar carreras
            self.btn_gestionar_carreras.config(state=NORMAL)

    def _limpiar_formulario(self):
        self.var_id.set(0)
        self.var_nombre.set("")
        self.var_correo.set("")
        self.lbl_info_carreras.config(text="Seleccione un estudiante para ver sus carreras")
        self.btn_gestionar_carreras.config(state=DISABLED)

    def _insertar_fila(self, estudiante: EstudianteService):
        if estudiante:
            # Obtener carreras activas del estudiante
            carreras_activas = self.ec_service.obtener_carreras_estudiante(
                estudiante.id_estudiante, estado='activa'
            )

            # Formatear nombres de carreras
            if carreras_activas:
                nombres_carreras = [c['nombre_carrera'] for c in carreras_activas]
                carreras_texto = ", ".join(nombres_carreras)
            else:
                carreras_texto = "Sin carrera asignada"

            self.tabla_estudiante.insert_row(
                index=END,
                values=(
                    estudiante.id_estudiante,
                    estudiante.nombre,
                    estudiante.correo,
                    carreras_texto,
                ),
            )

    def _actualizar_tabla_estudiante(self):
        # obtenemos la lista de estudiantes
        self._obtener_estudiantes()
        if self.lista_estudiantes:
            # limpiamos la tabla
            self.tabla_estudiante.delete_rows()
            for estudiante in self.lista_estudiantes:
                self._insertar_fila(estudiante=estudiante)

            # ajustamos las columnas
            self.tabla_estudiante.autofit_columns()

    def _obtener_estudiantes(self):
        if self.lista_estudiantes:
            self.lista_estudiantes.clear()

        servicio = EstudianteService(ruta_db=None)
        self.lista_estudiantes.extend(servicio.obtener_todos())

    def _cargar_vars(self):
        self.var_id: IntVar = self.map_vars['var_id']
        self.var_nombre: StringVar = self.map_vars['var_nombre']
        self.var_correo: StringVar = self.map_vars['var_correo']

    def _cargar_widgets(self):
        self.tabla_estudiante: Tableview = self.map_widgets['tabla_estudiante']
        self.lbl_estadisticas: Label = self.map_widgets['lbl_estadisticas']
        self.lbl_info_carreras: Label = self.map_widgets['lbl_info_carreras']
        self.btn_nuevo: Button = self.map_widgets['btn_nuevo']
        self.btn_aplicar: Button = self.map_widgets['btn_aplicar']
        self.btn_eliminar: Button = self.map_widgets['btn_eliminar']
        self.btn_primero: Button = self.map_widgets['btn_primero']
        self.btn_anterior: Button = self.map_widgets['btn_anterior']
        self.btn_siguiente: Button = self.map_widgets['btn_siguiente']
        self.btn_ultimo: Button = self.map_widgets['btn_ultimo']
        self.btn_gestionar_carreras: Button = self.map_widgets['btn_gestionar_carreras']

    def _actualizar_estadisticas(self):
        # actualizamos la lista de estudiantes
        self._obtener_estudiantes()
        cant_estudiantes = 0
        if self.lista_estudiantes:
            cant_estudiantes = len(self.lista_estudiantes)

        msg = f"Estudiantes: {cant_estudiantes}"

        self.lbl_estadisticas['text'] = msg

    def _actualizar_info_carreras(self, id_estudiante: int):
        """
        Actualiza la información de carreras del estudiante seleccionado.

        Args:
            id_estudiante (int): ID del estudiante
        """
        try:
            carreras = self.ec_service.obtener_carreras_estudiante(id_estudiante)

            if not carreras:
                self.lbl_info_carreras.config(text="⚠️ Sin carreras asignadas")
                return

            # Separar carreras activas e inactivas
            activas = [c for c in carreras if c['estado'] == 'activa']
            otras = [c for c in carreras if c['estado'] != 'activa']

            # Encontrar carrera principal
            principal = None
            for c in activas:
                if c.get('es_carrera_principal') == 1:
                    principal = c
                    break

            # Construir mensaje
            if principal:
                msg = f"📚 Principal: {principal['nombre_carrera']}"
                if len(activas) > 1:
                    msg += f" (+{len(activas)-1} más)"
            elif activas:
                msg = f"📚 Carreras activas: {len(activas)}"
            else:
                msg = f"ℹ️ {len(otras)} carrera(s) inactiva(s)"

            self.lbl_info_carreras.config(text=msg)

        except Exception as e:
            logger.error(f"Error al actualizar info de carreras: {e}")
            self.lbl_info_carreras.config(text="⚠️ Error al cargar carreras")

    def _on_gestionar_carreras(self):
        """
        Abre un diálogo para gestionar las carreras del estudiante seleccionado.
        """
        id_estudiante = self.var_id.get()
        nombre_estudiante = self.var_nombre.get()

        if id_estudiante <= 0:
            showwarning("Advertencia", "Debe seleccionar un estudiante primero")
            return

        try:
            # TODO: Implementar diálogo de gestión de carreras
            # Por ahora, mostrar información básica
            carreras = self.ec_service.obtener_carreras_estudiante(id_estudiante)

            if not carreras:
                msg = f"El estudiante '{nombre_estudiante}' no tiene carreras asignadas.\n\n"
                msg += "Use el módulo de Estudiante-Carrera para asignar carreras."
                showinfo("Sin Carreras", msg)
            else:
                msg = f"Carreras de '{nombre_estudiante}':\n\n"
                for c in carreras:
                    principal = "⭐" if c.get('es_carrera_principal') == 1 else "  "
                    msg += f"{principal} {c['nombre_carrera']} - {c['estado']}\n"
                msg += "\n💡 Use el módulo de Estudiante-Carrera para modificar."
                showinfo("Carreras del Estudiante", msg)

        except Exception as e:
            logger.error(f"Error al gestionar carreras: {e}", exc_info=True)
            showwarning("Error", f"No se pudieron cargar las carreras:\n{str(e)}")

    def _actualizar_estadisticas_estudiante(self, id_estudiante: int):
        """
        Actualiza las estadísticas mostrando la información
        del estudiante seleccionado.

        Args:
            id_estudiante (int): ID del estudiante seleccionado
        """
        try:
            if id_estudiante <= 0:
                self.lbl_estadisticas['text'] = "Estudiantes: 0"
                return

            # Obtener nombre y correo del estudiante
            nombre_estudiante = self.var_nombre.get()
            correo_estudiante = self.var_correo.get()

            # Actualizar la etiqueta con las estadísticas
            msg = f"Estudiante: {nombre_estudiante} | Email: {correo_estudiante}"
            self.lbl_estadisticas['text'] = msg

            logger.info(f"Estadísticas actualizadas para estudiante {id_estudiante}")

        except Exception as e:
            logger.error(f"Error al actualizar estadísticas de estudiante: {e}")
            self.lbl_estadisticas['text'] = "Error al cargar estadísticas"

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘

    def _on_tabla_doble_click(self, event):
        """Maneja el doble clic en una fila de la tabla"""
        # Obtener la fila seleccionada
        seleccion = self.tabla_estudiante.view.selection()

        if not seleccion:
            return

        # Obtener los valores de la fila
        item = self.tabla_estudiante.view.item(seleccion[0])
        valores = item['values']

        # Asignar a las variables
        id_estudiante = int(valores[0])
        estudiante = EstudianteService(ruta_db=None)
        estudiante.id_estudiante = id_estudiante
        if estudiante.instanciar():
            self._cargar_formulario(estudiante=estudiante)

    def _on_nuevo(self):
        self._limpiar_formulario()

    def _on_aplicar(self):
        estudiante = self._establecer_estudiante()
        if estudiante:
            if estudiante.id_estudiante == 0 or estudiante.id_estudiante is None:
                # cargamos un nuevo estudiante a la base de datos
                id_estudiante = estudiante.insertar()
                if id_estudiante != 0:
                    self.var_id.set(id_estudiante)
                    logger.info(f"Se creo el estudiante: {estudiante}")
                    showinfo(
                        parent=self.master,
                        title="Inserción",
                        message="Estudiante insertado con éxito!",
                    )
                    # recargamos la tabla
                    self._actualizar_tabla_estudiante()
            else:
                # actualizamos el estudiante
                if estudiante.actualizar():
                    showinfo(
                        parent=self.master,
                        title="Actualización",
                        message="Estudiante actualizado correctamente",
                    )
                    # recargamos la tabla
                    self._actualizar_tabla_estudiante()

    def _on_eliminar_estudiante(self):
        """Maneja la eliminación de un estudiante seleccionado"""
        id_estudiante = self.var_id.get()

        # Validar que haya un estudiante seleccionado
        if id_estudiante == 0 or id_estudiante is None:
            showinfo(
                parent=self.master,
                title="Advertencia",
                message="Debe seleccionar un estudiante para eliminar",
            )
            return

        # Pedir confirmación al usuario
        nombre_estudiante = self.var_nombre.get()
        confirmacion = askyesno(
            parent=self.master,
            title="Confirmación",
            message=f"¿Desea eliminar al estudiante '{nombre_estudiante}'?",
        )

        if not confirmacion:
            return

        # Eliminar el estudiante
        estudiante = EstudianteService(ruta_db=None)
        estudiante.id_estudiante = id_estudiante

        try:
            if estudiante.eliminar():
                logger.info(f"Se eliminó el estudiante con ID: {id_estudiante}")
                showinfo(
                    parent=self.master,
                    title="Eliminación",
                    message="Estudiante eliminado exitosamente",
                )
                # Limpiar formulario y actualizar tabla
                self._limpiar_formulario()
                self._actualizar_tabla_estudiante()
            else:
                logger.error(f"Error al eliminar el estudiante con ID: {id_estudiante}")
                showinfo(
                    parent=self.master,
                    title="Error",
                    message="Error al eliminar el estudiante",
                )
        except Exception as e:
            logger.error(f"Excepción al eliminar estudiante: {str(e)}")
            showinfo(
                parent=self.master,
                title="Error",
                message=f"Error inesperado: {str(e)}",
            )

    def _on_primero(self):
        """Carga el primer estudiante de la lista"""
        if self.lista_estudiantes:
            self.indice_actual = 0
            self._cargar_formulario(estudiante=self.lista_estudiantes[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay estudiantes para mostrar",
            )

    def _on_anterior(self):
        """Carga el estudiante anterior en la lista"""
        if not self.lista_estudiantes:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay estudiantes para mostrar",
            )
            return

        if self.indice_actual > 0:
            self.indice_actual -= 1
            self._cargar_formulario(estudiante=self.lista_estudiantes[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="Ya está en el primer estudiante",
            )

    def _on_siguiente(self):
        """Carga el siguiente estudiante en la lista"""
        if not self.lista_estudiantes:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay estudiantes para mostrar",
            )
            return

        if self.indice_actual < len(self.lista_estudiantes) - 1:
            self.indice_actual += 1
            self._cargar_formulario(estudiante=self.lista_estudiantes[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="Ya está en el último estudiante",
            )

    def _on_ultimo(self):
        """Carga el último estudiante de la lista"""
        if self.lista_estudiantes:
            self.indice_actual = len(self.lista_estudiantes) - 1
            self._cargar_formulario(estudiante=self.lista_estudiantes[self.indice_actual])
        else:
            showinfo(
                parent=self.master,
                title="Información",
                message="No hay estudiantes para mostrar",
            )
