from typing import Dict, Any, List
from tkinter.messagebox import showinfo, showwarning
from ttkbootstrap import Button, Entry, StringVar, IntVar, DoubleVar, Label, Combobox, Spinbox
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from modelos.services.estudiante_asignatura_service import EstudianteAsignaturaService
from modelos.services.estudiante_service import EstudianteService
from modelos.services.asignatura_service import AsignaturaService
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class ControlarAdministrarEstudianteAsignatura:

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

        # Diccionarios para estudiantes
        self.dict_estudiantes: Dict[int, Dict[str, Any]] = {}  # id -> {label, id_carrera}
        self.dict_estudiantes_inv: Dict[str, int] = {}  # label -> id

        # Diccionarios para asignaturas
        self.dict_asignaturas: Dict[int, Dict[str, Any]] = {}  # id -> {codigo, nombre, creditos}

        # Lista de registros del estudiante actual
        self.lista_registros_estudiante: List[EstudianteAsignaturaService] = []

        # ID del estudiante seleccionado actualmente
        self.id_estudiante_actual: int = 0

        # ID de la carrera del estudiante actual
        self.id_carrera_estudiante: int = 0

        # ID de la asignatura seleccionada en la tabla
        self.id_asignatura_seleccionada: int = 0

        # Estados posibles
        self.estados_display = {
            'no_cursada': '🔵 No cursada',
            'cursando': '🟡 Cursando',
            'aprobada': '🟢 Aprobada',
            'reprobada': '🔴 Reprobada',
        }
        self.estados_display_inv = {v: k for k, v in self.estados_display.items()}

        # cargar widgets
        self._cargar_widgets()

        # cargar los vars
        self._cargar_vars()

        # cargar estudiantes
        self._cargar_estudiantes()

        # cargar asignaturas
        self._cargar_asignaturas()

        # mostrar estadísticas
        self._actualizar_estadisticas()

        # vincular eventos
        self._vincular_eventos()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Métodos Privados
    # └────────────────────────────────────────────────────────────┘
    def _vincular_eventos(self):
        # Botón cargar estudiante
        self.btn_cargar_estudiante.config(command=self._on_cargar_estudiante)

        # Evento de selección en tabla
        self.tabla_asignaturas.view.bind("<<TreeviewSelect>>", self._on_asignatura_seleccionada)

        # Evento de cambio en filtro de estado
        self.cbx_filtro_estado.bind("<<ComboboxSelected>>", self._on_filtro_estado_cambiado)

        # Evento de búsqueda
        self.entry_buscar_asignatura.bind("<KeyRelease>", self._on_buscar_asignatura)

        # Botones del formulario
        self.btn_aplicar.config(command=self._on_aplicar)
        self.btn_limpiar.config(command=self._on_limpiar_formulario)

        # Botón de limpiar filtros
        if 'btn_limpiar_filtros' in self.map_widgets:
            self.btn_limpiar_filtros: Button = self.map_widgets['btn_limpiar_filtros']
            self.btn_limpiar_filtros.config(command=self._on_limpiar_filtros)

    def _cargar_vars(self):
        self.var_id_estudiante: IntVar = self.map_vars['var_id_estudiante']
        self.var_nombre_estudiante: StringVar = self.map_vars['var_nombre_estudiante']
        self.var_id_asignatura_seleccionada: IntVar = self.map_vars[
            'var_id_asignatura_seleccionada'
        ]
        self.var_nombre_asignatura_seleccionada: StringVar = self.map_vars[
            'var_nombre_asignatura_seleccionada'
        ]
        self.var_estado: StringVar = self.map_vars['var_estado']
        self.var_nota: DoubleVar = self.map_vars['var_nota']
        self.var_periodo: StringVar = self.map_vars['var_periodo']
        self.var_filtro_estado: StringVar = self.map_vars['var_filtro_estado']

    def _cargar_widgets(self):
        self.cbx_estudiante: Combobox = self.map_widgets['cbx_estudiante']
        self.btn_cargar_estudiante: Button = self.map_widgets['btn_cargar_estudiante']
        self.entry_buscar_asignatura: Entry = self.map_widgets['entry_buscar_asignatura']
        self.cbx_filtro_estado: Combobox = self.map_widgets['cbx_filtro_estado']
        self.tabla_asignaturas: Tableview = self.map_widgets['tabla_asignaturas']
        self.lbl_asignatura_seleccionada: Label = self.map_widgets['lbl_asignatura_seleccionada']
        self.cbx_estado: Combobox = self.map_widgets['cbx_estado']
        self.spin_nota: Spinbox = self.map_widgets['spin_nota']
        self.entry_periodo: Entry = self.map_widgets['entry_periodo']
        self.btn_aplicar: Button = self.map_widgets['btn_aplicar']
        self.btn_limpiar: Button = self.map_widgets['btn_limpiar']
        self.lbl_total_asignaturas: Label = self.map_widgets['lbl_total_asignaturas']
        self.lbl_aprobadas: Label = self.map_widgets['lbl_aprobadas']
        self.lbl_cursando: Label = self.map_widgets['lbl_cursando']
        self.lbl_reprobadas: Label = self.map_widgets['lbl_reprobadas']
        self.lbl_no_cursadas: Label = self.map_widgets['lbl_no_cursadas']
        self.lbl_promedio: Label = self.map_widgets['lbl_promedio']
        self.lbl_estadisticas: Label = self.map_widgets['lbl_estadisticas']

    def _cargar_estudiantes(self):
        """Carga todos los estudiantes con todas sus carreras (activas e inactivas)."""
        try:
            self.dict_estudiantes.clear()
            self.dict_estudiantes_inv.clear()

            servicio_estudiante = EstudianteService(ruta_db=None)
            lista_aux = servicio_estudiante.obtener_estudiantes_con_carrera()

            if lista_aux:
                labels_estudiantes = []
                for data in lista_aux:
                    id_estudiante = data.get('id_estudiante')
                    nombre = data.get('nombre')
                    correo = data.get('correo', '')
                    id_carrera = data.get('id_carrera')
                    nombre_carrera = data.get('nombre_carrera', 'Sin carrera')
                    es_principal = data.get('es_carrera_principal', 0)
                    estado_carrera = data.get('estado_carrera', 'inactiva')

                    # Formato: "Juan Pérez (juan@mail.com) - Ingeniería ⭐"
                    label = f"{nombre}"
                    if correo:
                        label += f" ({correo})"
                    if nombre_carrera and nombre_carrera != 'Sin carrera':
                        label += f" - {nombre_carrera}"
                        if es_principal:
                            label += " ⭐"  # Marca la carrera principal
                        # Indicar si la carrera está activa o inactiva
                        if estado_carrera == 'activa':
                            label += " ✓"  # Activa
                        else:
                            label += " ✗"  # Inactiva

                    # ✅ Crear clave única: combinación de estudiante + carrera
                    # Esto permite múltiples entradas para el mismo estudiante
                    clave_dict = (
                        f"{id_estudiante}_{id_carrera}" if id_carrera else f"{id_estudiante}_0"
                    )

                    # Guardamos con clave única
                    self.dict_estudiantes[clave_dict] = {
                        'id_estudiante': id_estudiante,
                        'label': label,
                        'id_carrera': id_carrera,
                        'nombre_carrera': nombre_carrera,
                        'estado_carrera': estado_carrera,
                    }
                    self.dict_estudiantes_inv[label] = clave_dict
                    labels_estudiantes.append(label)

                self.cbx_estudiante['values'] = labels_estudiantes
                logger.info(f"Se cargaron {len(labels_estudiantes)} entradas (estudiante-carrera)")
            else:
                logger.warning("No se encontraron estudiantes")
                self.cbx_estudiante['values'] = []

        except Exception as e:
            logger.error(f"Error al cargar estudiantes: {e}", exc_info=True)
            self.cbx_estudiante['values'] = []

    def _cargar_asignaturas(self, id_carrera: int = None):
        """Carga las asignaturas en memoria. Si se proporciona id_carrera, filtra por esa carrera."""
        try:
            self.dict_asignaturas.clear()

            if id_carrera:
                # Cargar solo asignaturas de la carrera del estudiante
                servicio_asignatura = AsignaturaService(ruta_db=None)
                lista_aux = servicio_asignatura.obtener_basico_por_carrera(id_carrera)
            else:
                # Cargar todas las asignaturas
                servicio_asignatura = AsignaturaService(ruta_db=None)
                lista_aux = servicio_asignatura.obtener_basico()

            if lista_aux:
                for data in lista_aux:
                    id_asignatura = data.get('id_asignatura')
                    self.dict_asignaturas[id_asignatura] = {
                        'codigo': data.get('codigo'),
                        'nombre': data.get('nombre'),
                        'creditos': data.get('creditos'),
                        'id_carrera': data.get('id_carrera'),
                    }
                logger.info(
                    f"Se cargaron {len(self.dict_asignaturas)} asignaturas"
                    + (f" de la carrera {id_carrera}" if id_carrera else "")
                )
            else:
                logger.warning("No se encontraron asignaturas")

        except Exception as e:
            logger.error(f"Error al cargar asignaturas: {e}")

    def _cargar_registros_estudiante(self, id_estudiante: int):
        """Carga todos los registros de asignaturas del estudiante."""
        try:
            self.lista_registros_estudiante.clear()

            if id_estudiante == 0:
                return

            servicio = EstudianteAsignaturaService(ruta_db=None)
            lista_aux = servicio.obtener_por_estudiante(id_estudiante)

            if lista_aux:
                for data in lista_aux:
                    registro = EstudianteAsignaturaService(ruta_db=None)
                    registro.set_data(data=data)
                    self.lista_registros_estudiante.append(registro)

                logger.info(f"Se cargaron {len(self.lista_registros_estudiante)} registros")

        except Exception as e:
            logger.error(f"Error al cargar registros del estudiante: {e}")

    def _actualizar_tabla_asignaturas(
        self, filtro_busqueda: str = "", filtro_estado: str = "Todos"
    ):
        """Actualiza la tabla con las asignaturas y sus estados."""
        try:
            # Limpiar tabla
            self.tabla_asignaturas.delete_rows()

            if self.id_estudiante_actual == 0:
                return

            # Crear diccionario de registros por id_asignatura
            dict_registros = {}
            for registro in self.lista_registros_estudiante:
                dict_registros[registro.id_asignatura] = registro

            # Agregar filas a la tabla
            for id_asig, datos in sorted(
                self.dict_asignaturas.items(), key=lambda x: x[1]['codigo']
            ):
                # Obtener registro del estudiante (si existe)
                registro = dict_registros.get(id_asig)

                estado_bd = registro.estado if registro else 'no_cursada'
                nota = registro.nota_final if registro and registro.nota_final else 0.0
                periodo = registro.periodo if registro and registro.periodo else '-'

                # Aplicar filtro de búsqueda
                if filtro_busqueda:
                    texto_busqueda = f"{datos['codigo']} {datos['nombre']}".lower()
                    if filtro_busqueda.lower() not in texto_busqueda:
                        continue

                # Aplicar filtro de estado
                estado_display = self.estados_display.get(estado_bd, '🔵 No cursada')
                if filtro_estado != "Todos":
                    if filtro_estado not in estado_display:
                        continue

                # Formato de nota
                nota_str = f"{nota:.1f}" if nota > 0 else "-"

                self.tabla_asignaturas.insert_row(
                    index=END,
                    values=(
                        datos['codigo'],
                        datos['nombre'],
                        datos['creditos'],
                        estado_display,
                        nota_str,
                        periodo,
                    ),
                )

            self.tabla_asignaturas.autofit_columns()
            self._actualizar_estadisticas_estudiante()

        except Exception as e:
            logger.error(f"Error al actualizar tabla: {e}")

    def _actualizar_estadisticas_estudiante(self):
        """Actualiza las estadísticas del panel derecho."""
        try:
            if self.id_estudiante_actual == 0:
                self.lbl_total_asignaturas['text'] = "Total Asignaturas: -"
                self.lbl_aprobadas['text'] = "🟢 Aprobadas: -"
                self.lbl_cursando['text'] = "🟡 Cursando: -"
                self.lbl_reprobadas['text'] = "🔴 Reprobadas: -"
                self.lbl_no_cursadas['text'] = "🔵 No Cursadas: -"
                self.lbl_promedio['text'] = "📈 Promedio: -"
                return

            # Contar por estado
            total = len(self.dict_asignaturas)
            aprobadas = 0
            cursando = 0
            reprobadas = 0
            no_cursadas = 0
            suma_notas = 0.0
            cant_notas = 0

            # Crear diccionario de registros
            dict_registros = {}
            for registro in self.lista_registros_estudiante:
                dict_registros[registro.id_asignatura] = registro

            for id_asig in self.dict_asignaturas.keys():
                registro = dict_registros.get(id_asig)
                estado = registro.estado if registro else 'no_cursada'

                if estado == 'aprobada':
                    aprobadas += 1
                    if registro.nota_final:
                        suma_notas += registro.nota_final
                        cant_notas += 1
                elif estado == 'cursando':
                    cursando += 1
                elif estado == 'reprobada':
                    reprobadas += 1
                else:
                    no_cursadas += 1

            # Calcular promedio
            promedio = suma_notas / cant_notas if cant_notas > 0 else 0.0

            # Actualizar labels
            self.lbl_total_asignaturas['text'] = f"Total Asignaturas: {total}"
            self.lbl_aprobadas['text'] = f"🟢 Aprobadas: {aprobadas}"
            self.lbl_cursando['text'] = f"🟡 Cursando: {cursando}"
            self.lbl_reprobadas['text'] = f"🔴 Reprobadas: {reprobadas}"
            self.lbl_no_cursadas['text'] = f"🔵 No Cursadas: {no_cursadas}"
            self.lbl_promedio['text'] = f"📈 Promedio: {promedio:.2f}"

        except Exception as e:
            logger.error(f"Error al actualizar estadísticas: {e}")

    def _actualizar_estadisticas(self):
        """Actualiza la barra de estadísticas inferior."""
        try:
            if self.id_estudiante_actual == 0:
                self.lbl_estadisticas['text'] = "Seleccione un estudiante para comenzar"
                return

            info_estudiante = self.dict_estudiantes.get(self.id_estudiante_actual, {})
            estudiante = (
                info_estudiante.get('label', 'Desconocido')
                if isinstance(info_estudiante, dict)
                else "Desconocido"
            )
            total_asignaturas = len(self.dict_asignaturas)
            total_registros = len(self.lista_registros_estudiante)

            msg = f"Estudiante: {estudiante} | Total Asignaturas: {total_asignaturas}"

            if (
                self.id_asignatura_seleccionada > 0
                and self.id_asignatura_seleccionada in self.dict_asignaturas
            ):
                datos = self.dict_asignaturas[self.id_asignatura_seleccionada]
                msg += f" | Editando: {datos['codigo']} - {datos['nombre']}"

            self.lbl_estadisticas['text'] = msg

        except Exception as e:
            logger.error(f"Error al actualizar estadísticas: {e}")

    def _limpiar_formulario(self):
        """Limpia el formulario de actualización."""
        self.var_id_asignatura_seleccionada.set(0)
        self.var_nombre_asignatura_seleccionada.set("[Selecciona una asignatura]")
        self.var_estado.set("")
        self.var_nota.set(0.0)
        self.var_periodo.set("")
        self.id_asignatura_seleccionada = 0

    def _cargar_formulario(self, id_asignatura: int):
        """Carga los datos de una asignatura en el formulario."""
        try:
            if id_asignatura not in self.dict_asignaturas:
                return

            datos_asig = self.dict_asignaturas[id_asignatura]
            label_asig = f"{datos_asig['codigo']} - {datos_asig['nombre']}"

            self.var_id_asignatura_seleccionada.set(id_asignatura)
            self.var_nombre_asignatura_seleccionada.set(label_asig)
            self.id_asignatura_seleccionada = id_asignatura

            # Buscar registro existente
            registro = None
            for reg in self.lista_registros_estudiante:
                if reg.id_asignatura == id_asignatura:
                    registro = reg
                    break

            if registro:
                estado_display = self.estados_display.get(registro.estado, '🔵 No cursada')
                self.var_estado.set(estado_display)
                self.var_nota.set(registro.nota_final if registro.nota_final else 0.0)
                self.var_periodo.set(registro.periodo if registro.periodo else "")
            else:
                self.var_estado.set('🔵 No cursada')
                self.var_nota.set(0.0)
                self.var_periodo.set("")

            self._actualizar_estadisticas()

        except Exception as e:
            logger.error(f"Error al cargar formulario: {e}")

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘

    def _on_cargar_estudiante(self):
        """Carga los datos del estudiante-carrera seleccionado."""
        try:
            label_estudiante = self.var_nombre_estudiante.get()
            if not label_estudiante:
                showwarning(
                    parent=self.master,
                    title="Advertencia",
                    message="Debe seleccionar un estudiante",
                )
                return

            # ✅ Obtener clave única (id_estudiante_id_carrera)
            clave_dict = self.dict_estudiantes_inv.get(label_estudiante, None)
            if not clave_dict:
                return

            # Obtener info del estudiante-carrera
            info_estudiante = self.dict_estudiantes.get(clave_dict)
            if not info_estudiante:
                return

            # ✅ Extraer id_estudiante y id_carrera
            id_estudiante = info_estudiante.get('id_estudiante')
            id_carrera = info_estudiante.get('id_carrera')

            # ✅ VALIDACIÓN: Verificar que tenga carrera
            if not id_carrera:
                nombre_carrera = info_estudiante.get('nombre_carrera', 'Sin carrera')
                showwarning(
                    parent=self.master,
                    title="Sin Carrera Asignada",
                    message=f"El estudiante seleccionado no tiene una carrera asignada.\n\n"
                    f"Por favor, use el módulo 'Estudiante-Carrera' para inscribir "
                    f"al estudiante en una carrera antes de asignar asignaturas.",
                )
                logger.warning(f"Estudiante {id_estudiante} sin carrera")
                return

            self.id_estudiante_actual = id_estudiante
            self.id_carrera_estudiante = id_carrera
            self.var_id_estudiante.set(id_estudiante)

            # Cargar asignaturas de la carrera seleccionada
            self._cargar_asignaturas(id_carrera=id_carrera)

            # Cargar registros del estudiante
            self._cargar_registros_estudiante(id_estudiante)

            # Actualizar tabla
            self._actualizar_tabla_asignaturas()

            # Limpiar formulario
            self._limpiar_formulario()

            # Actualizar estadísticas
            self._actualizar_estadisticas()

            # ✅ Mostrar información de la carrera
            nombre_carrera = info_estudiante.get('nombre_carrera', 'Desconocida')
            logger.info(
                f"Estudiante cargado: {label_estudiante} - Carrera: {nombre_carrera} (ID: {id_carrera})"
            )

        except Exception as e:
            logger.error(f"Error al cargar estudiante: {e}", exc_info=True)

    def _on_asignatura_seleccionada(self, event=None):
        """Maneja la selección de una asignatura en la tabla."""
        try:
            seleccion = self.tabla_asignaturas.view.selection()
            if not seleccion:
                return

            # Obtener valores de la fila
            item = self.tabla_asignaturas.view.item(seleccion[0])
            valores = item['values']
            codigo_asig = valores[0]

            # Buscar ID de la asignatura
            id_asignatura = None
            for id_asig, datos in self.dict_asignaturas.items():
                if datos['codigo'] == codigo_asig:
                    id_asignatura = id_asig
                    break

            if id_asignatura:
                self._cargar_formulario(id_asignatura)

        except Exception as e:
            logger.error(f"Error al seleccionar asignatura: {e}")

    def _on_filtro_estado_cambiado(self, event=None):
        """Maneja el cambio de filtro por estado."""
        try:
            filtro_estado = self.var_filtro_estado.get()
            filtro_busqueda = self.entry_buscar_asignatura.get()
            self._actualizar_tabla_asignaturas(filtro_busqueda, filtro_estado)

        except Exception as e:
            logger.error(f"Error al filtrar por estado: {e}")

    def _on_buscar_asignatura(self, event=None):
        """Maneja la búsqueda de asignaturas."""
        try:
            filtro_busqueda = self.entry_buscar_asignatura.get()
            filtro_estado = self.var_filtro_estado.get()
            self._actualizar_tabla_asignaturas(filtro_busqueda, filtro_estado)

        except Exception as e:
            logger.error(f"Error en búsqueda: {e}")

    def _on_limpiar_formulario(self):
        """Limpia el formulario."""
        self._limpiar_formulario()
        self._actualizar_estadisticas()

    def _on_limpiar_filtros(self):
        """Limpia los filtros de búsqueda y estado."""
        self.entry_buscar_asignatura.delete(0, END)
        self.var_filtro_estado.set("Todos")
        self._actualizar_tabla_asignaturas()

    def _on_aplicar(self):
        """Aplica los cambios del formulario."""
        try:
            if self.id_estudiante_actual == 0:
                showwarning(
                    parent=self.master,
                    title="Advertencia",
                    message="Debe cargar un estudiante primero",
                )
                return

            if self.id_asignatura_seleccionada == 0:
                showwarning(
                    parent=self.master,
                    title="Advertencia",
                    message="Debe seleccionar una asignatura",
                )
                return

            # Obtener datos del formulario
            estado_display = self.var_estado.get()
            estado_bd = self.estados_display_inv.get(estado_display, 'no_cursada')
            nota = self.var_nota.get()
            periodo = self.var_periodo.get().strip()

            logger.info(
                f"Aplicando cambios - Estado display: '{estado_display}' -> Estado BD: '{estado_bd}'"
            )
            logger.info(f"Nota: {nota}, Período: '{periodo}'")

            # Validar nota si el estado es aprobada o reprobada
            if estado_bd in ['aprobada', 'reprobada'] and nota <= 0:
                showwarning(
                    parent=self.master,
                    title="Advertencia",
                    message="Debe ingresar una nota válida",
                )
                return

            # Crear o actualizar registro
            registro = EstudianteAsignaturaService(ruta_db=None)
            registro.id_estudiante = self.id_estudiante_actual
            registro.id_asignatura = self.id_asignatura_seleccionada
            registro.estado = estado_bd
            registro.nota_final = nota if nota > 0 else None
            registro.periodo = periodo if periodo else None

            logger.info(
                f"Registro a guardar: estudiante={registro.id_estudiante}, "
                f"asignatura={registro.id_asignatura}, estado={registro.estado}, "
                f"nota={registro.nota_final}, periodo={registro.periodo}"
            )

            # Verificar si existe el registro
            existe = registro.existe()

            logger.info(f"¿Registro existe? {existe}")

            if existe:
                # Actualizar
                resultado = registro.actualizar()
                logger.info(f"Resultado actualización: {resultado}")
                if resultado:
                    showinfo(
                        parent=self.master,
                        title="Éxito",
                        message="Registro actualizado correctamente",
                    )
                else:
                    showwarning(
                        parent=self.master,
                        title="Error",
                        message="No se pudo actualizar el registro",
                    )
            else:
                # Insertar
                resultado = registro.insertar()
                logger.info(f"Resultado inserción: {resultado}")
                if resultado:
                    showinfo(
                        parent=self.master,
                        title="Éxito",
                        message="Registro creado correctamente",
                    )
                else:
                    showwarning(
                        parent=self.master,
                        title="Error",
                        message="No se pudo crear el registro",
                    )

            # Recargar datos
            self._cargar_registros_estudiante(self.id_estudiante_actual)
            self._actualizar_tabla_asignaturas()
            self._limpiar_formulario()

        except Exception as e:
            logger.error(f"Error al aplicar cambios: {e}", exc_info=True)
            showwarning(
                parent=self.master,
                title="Error",
                message=f"Error inesperado: {str(e)}",
            )
