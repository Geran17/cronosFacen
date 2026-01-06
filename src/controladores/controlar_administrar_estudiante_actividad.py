from tkinter.messagebox import showinfo, showwarning
from typing import Dict, Any
from scripts.logging_config import obtener_logger_modulo
from modelos.daos.estudiante_dao import EstudianteDAO
from modelos.daos.actividad_dao import ActividadDAO
from modelos.services.estudiante_actividad_service import EstudianteActividadService
from ttkbootstrap.dialogs import DatePickerDialog
from datetime import datetime

logger = obtener_logger_modulo(__name__)


class ControlarAdministrarEstudianteActividad:
    def __init__(self, master, map_vars: Dict[str, Any], map_widgets: Dict[str, Any]):
        self.master = master
        self.map_widgets = map_widgets
        self.map_vars = map_vars

        # Diccionarios para estudiantes
        self.dict_estudiantes: Dict[str, Dict[str, Any]] = (
            {}
        )  # clave_unica -> {id_estudiante, label, id_carrera}
        self.dict_estudiantes_inv: Dict[str, str] = {}  # label -> clave_unica

        # Diccionarios para actividades
        self.dict_actividades: Dict[int, Dict[str, Any]] = {}  # id -> {titulo, ...}

        # Diccionario para asignaturas (para mostrar nombre)
        self.dict_asignaturas: Dict[int, str] = {}  # id -> nombre

        # Lista de registros del estudiante actual
        self.lista_registros_estudiante = []

        # ID del estudiante seleccionado actualmente
        self.id_estudiante_actual: int = 0

        # ID de la carrera del estudiante actual
        self.id_carrera_estudiante: int = 0

        # ID de la actividad seleccionada en la tabla
        self.id_actividad_seleccionada: int = 0

        # Estados posibles
        self.estados_display = {
            'pendiente': '⏳ Pendiente',
            'en_progreso': '🔄 En progreso',
            'entregada': '✅ Entregada',
            'vencida': '❌ Vencida',
        }
        self.estados_display_inv = {v: k for k, v in self.estados_display.items()}

        # Obtener widgets
        self.cbx_estudiante = self.map_widgets.get('cbx_estudiante')
        self.btn_cargar_estudiante = self.map_widgets.get('btn_cargar_estudiante')
        self.tabla_actividades = self.map_widgets.get('tabla_actividades')
        self.cbx_estado = self.map_widgets.get('cbx_estado')
        self.entry_fecha_entrega = self.map_widgets.get('entry_fecha_entrega')
        self.btn_calendario = self.map_widgets.get('btn_calendario')
        self.btn_aplicar = self.map_widgets.get('btn_aplicar')
        self.btn_limpiar = self.map_widgets.get('btn_limpiar')
        self.entry_buscar_actividad = self.map_widgets.get('entry_buscar_actividad')
        self.cbx_filtro_estado = self.map_widgets.get('cbx_filtro_estado')
        self.cbx_filtro_tipo = self.map_widgets.get('cbx_filtro_tipo')
        self.lbl_estadisticas = self.map_widgets.get('lbl_estadisticas')
        self.lbl_total_actividades = self.map_widgets.get('lbl_total_actividades')
        self.lbl_pendientes = self.map_widgets.get('lbl_pendientes')
        self.lbl_en_progreso = self.map_widgets.get('lbl_en_progreso')
        self.lbl_entregadas = self.map_widgets.get('lbl_entregadas')
        self.lbl_vencidas = self.map_widgets.get('lbl_vencidas')

        # Obtener variables
        self.var_id_estudiante = self.map_vars.get('var_id_estudiante')
        self.var_nombre_estudiante = self.map_vars.get('var_nombre_estudiante')
        self.var_id_actividad_seleccionada = self.map_vars.get('var_id_actividad_seleccionada')
        self.var_nombre_actividad_seleccionada = self.map_vars.get(
            'var_nombre_actividad_seleccionada'
        )
        self.var_estado = self.map_vars.get('var_estado')
        self.var_fecha_entrega = self.map_vars.get('var_fecha_entrega')
        self.var_filtro_estado = self.map_vars.get('var_filtro_estado')
        self.var_filtro_tipo = self.map_vars.get('var_filtro_tipo')

        # cargar los widgets
        self._cargar_widgets()

        # cargar estudiantes
        self._cargar_estudiantes()

        # cargar actividades
        self._cargar_actividades()

        # cargar filtros
        self._cargar_filtros_iniciales()

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

        # Tabla - doble click
        self.tabla_actividades.view.bind("<Double-Button-1>", self._on_actividad_seleccionada)

        # Botones del formulario
        self.btn_aplicar.config(command=self._on_aplicar)
        self.btn_limpiar.config(command=self._on_limpiar_formulario)
        self.btn_calendario.config(command=self._on_abrir_calendario)

        # Filtros
        self.cbx_filtro_estado.bind("<<ComboboxSelected>>", self._on_filtrar)
        self.cbx_filtro_tipo.bind("<<ComboboxSelected>>", self._on_filtrar)
        self.entry_buscar_actividad.bind("<KeyRelease>", self._on_buscar_actividad)

    def _cargar_widgets(self):
        """Configura el estado inicial de los widgets."""
        self.var_nombre_actividad_seleccionada.set("[Selecciona una actividad]")

    def _cargar_estudiantes(self):
        """Carga todos los estudiantes con sus carreras activas."""
        try:
            self.dict_estudiantes.clear()
            self.dict_estudiantes_inv.clear()

            dao = EstudianteDAO(ruta_db=None)

            # ✅ CONSULTA: Une con estudiante_carrera para obtener todas las carreras activas
            sql = """
            SELECT 
                e.id_estudiante, 
                e.nombre, 
                e.correo,
                ec.id_carrera,
                c.nombre as nombre_carrera,
                ec.es_carrera_principal
            FROM estudiante e
            LEFT JOIN estudiante_carrera ec 
                ON e.id_estudiante = ec.id_estudiante 
                AND ec.estado = 'activa'
            LEFT JOIN carrera c 
                ON ec.id_carrera = c.id_carrera
            ORDER BY e.nombre, ec.es_carrera_principal DESC, c.nombre
            """
            params = ()
            lista_aux = dao.ejecutar_consulta(sql=sql, params=params)

            if lista_aux:
                labels_estudiantes = []
                for data in lista_aux:
                    id_estudiante = data.get('id_estudiante')
                    nombre = data.get('nombre')
                    correo = data.get('correo', '')
                    id_carrera = data.get('id_carrera')
                    nombre_carrera = data.get('nombre_carrera', 'Sin carrera')
                    es_principal = data.get('es_carrera_principal', 0)

                    # Formato: "Juan Pérez (juan@mail.com) - Ingeniería ⭐"
                    label = f"{nombre}"
                    if correo:
                        label += f" ({correo})"
                    if nombre_carrera and nombre_carrera != 'Sin carrera':
                        label += f" - {nombre_carrera}"
                        if es_principal:
                            label += " ⭐"

                    # ✅ Crear clave única: combinación de estudiante + carrera
                    clave_dict = (
                        f"{id_estudiante}_{id_carrera}" if id_carrera else f"{id_estudiante}_0"
                    )

                    # Guardamos con clave única
                    self.dict_estudiantes[clave_dict] = {
                        'id_estudiante': id_estudiante,
                        'label': label,
                        'id_carrera': id_carrera,
                        'nombre_carrera': nombre_carrera,
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

    def _cargar_actividades(self, id_carrera: int = None):
        """Carga las actividades en memoria. Si se proporciona id_carrera, filtra por esa carrera."""
        try:
            self.dict_actividades.clear()

            dao = ActividadDAO(ruta_db=None)

            if id_carrera:
                # Cargar solo actividades de la carrera del estudiante
                # Relación: actividad -> eje_tematico -> asignatura -> carrera
                sql = """SELECT a.id_actividad, a.titulo, a.descripcion, 
                                a.fecha_inicio, a.fecha_fin, a.id_eje, a.id_tipo_actividad,
                                e.nombre as nombre_eje, asig.nombre as nombre_asignatura,
                                ta.siglas as sigla_tipo
                         FROM actividad a
                         INNER JOIN eje_tematico e ON a.id_eje = e.id_eje
                         INNER JOIN asignatura asig ON e.id_asignatura = asig.id_asignatura
                         LEFT JOIN tipo_actividad ta ON a.id_tipo_actividad = ta.id_tipo_actividad
                         WHERE asig.id_carrera = ?
                         ORDER BY a.fecha_fin DESC, a.titulo"""
                params = (id_carrera,)
            else:
                # Cargar todas las actividades
                sql = """SELECT a.id_actividad, a.titulo, a.descripcion, 
                                a.fecha_inicio, a.fecha_fin, a.id_eje, a.id_tipo_actividad,
                                e.nombre as nombre_eje, asig.nombre as nombre_asignatura,
                                ta.siglas as sigla_tipo
                         FROM actividad a
                         INNER JOIN eje_tematico e ON a.id_eje = e.id_eje
                         INNER JOIN asignatura asig ON e.id_asignatura = asig.id_asignatura
                         LEFT JOIN tipo_actividad ta ON a.id_tipo_actividad = ta.id_tipo_actividad
                         ORDER BY a.fecha_fin DESC, a.titulo"""
                params = ()

            lista_aux = dao.ejecutar_consulta(sql=sql, params=params)

            if lista_aux:
                for data in lista_aux:
                    id_actividad = data.get('id_actividad')
                    self.dict_actividades[id_actividad] = {
                        'titulo': data.get('titulo'),
                        'descripcion': data.get('descripcion'),
                        'fecha_inicio': data.get('fecha_inicio'),
                        'fecha_fin': data.get('fecha_fin'),
                        'id_eje': data.get('id_eje'),
                        'id_tipo_actividad': data.get('id_tipo_actividad'),
                        'nombre_eje': data.get('nombre_eje'),
                        'nombre_asignatura': data.get('nombre_asignatura'),
                        'sigla_tipo': data.get('sigla_tipo') or '',
                    }
                logger.info(
                    f"Se cargaron {len(self.dict_actividades)} actividades"
                    + (f" de la carrera {id_carrera}" if id_carrera else "")
                )
            else:
                logger.warning("No se encontraron actividades")

        except Exception as e:
            logger.error(f"Error al cargar actividades: {e}")

    def _cargar_filtros_iniciales(self):
        """Carga los filtros iniciales de tipos de actividad."""
        try:
            # Cargar tipos de actividad desde las actividades cargadas
            tipos_set = set()
            for actividad in self.dict_actividades.values():
                if actividad.get('sigla_tipo'):
                    tipos_set.add(actividad.get('sigla_tipo'))

            tipos = ["Todos"] + sorted(list(tipos_set))
            self.cbx_filtro_tipo.config(values=tipos)
            self.var_filtro_tipo.set("Todos")

        except Exception as e:
            logger.error(f"Error al cargar filtros iniciales: {e}")

    def _cargar_registros_estudiante(self, id_estudiante: int):
        """Carga los registros de estudiante_actividad para un estudiante."""
        try:
            self.lista_registros_estudiante.clear()

            service = EstudianteActividadService(ruta_db=None)
            service.id_estudiante = id_estudiante

            # Obtener todos los registros del estudiante
            dao = service.dao
            sql = """SELECT id_estudiante, id_actividad, estado, fecha_entrega 
                     FROM estudiante_actividad 
                     WHERE id_estudiante = ?"""
            params = (id_estudiante,)
            lista_aux = dao.ejecutar_consulta(sql=sql, params=params)

            if lista_aux:
                for data in lista_aux:
                    registro = EstudianteActividadService(ruta_db=None)
                    registro.id_estudiante = data.get('id_estudiante')
                    registro.id_actividad = data.get('id_actividad')
                    registro.estado = data.get('estado')
                    registro.fecha_entrega = data.get('fecha_entrega')
                    self.lista_registros_estudiante.append(registro)

                logger.info(f"Se cargaron {len(lista_aux)} registros")
            else:
                logger.info("No hay registros para este estudiante")

        except Exception as e:
            logger.error(f"Error al cargar registros del estudiante: {e}")

    def _actualizar_tabla_actividades(
        self,
        filtro_busqueda: str = "",
        filtro_estado: str = "Todos",
        filtro_tipo: str = "Todos",
    ):
        """Actualiza la tabla con las actividades y sus estados."""
        try:
            # Limpiar tabla
            self.tabla_actividades.delete_rows()

            if self.id_estudiante_actual == 0:
                return

            # Crear diccionario de registros por id_actividad
            dict_registros = {}
            for registro in self.lista_registros_estudiante:
                dict_registros[registro.id_actividad] = registro

            # Contadores para estadísticas
            total = 0
            pendientes = 0
            en_progreso = 0
            entregadas = 0
            vencidas = 0

            # Fecha actual para calcular días
            fecha_actual = datetime.now().date()

            # Agregar filas a la tabla
            for id_act, datos in sorted(
                self.dict_actividades.items(),
                key=lambda x: (x[1]['fecha_fin'] or '9999-99-99', x[1]['titulo']),
            ):
                # Obtener registro del estudiante (si existe)
                registro = dict_registros.get(id_act)

                estado_bd = registro.estado if registro else 'pendiente'
                fecha_entrega = (
                    registro.fecha_entrega if registro and registro.fecha_entrega else '-'
                )

                # Aplicar filtro de búsqueda
                if filtro_busqueda:
                    texto_busqueda = (
                        f"{datos['titulo']} {datos.get('nombre_asignatura', '')}".lower()
                    )
                    if filtro_busqueda.lower() not in texto_busqueda:
                        continue

                # Aplicar filtro de estado
                estado_display = self.estados_display.get(estado_bd, '⏳ Pendiente')
                if filtro_estado != "Todos":
                    if filtro_estado not in estado_display:
                        continue

                # Aplicar filtro de tipo de actividad
                if filtro_tipo != "Todos":
                    if datos.get('sigla_tipo') != filtro_tipo:
                        continue

                # Contadores
                total += 1
                if estado_bd == 'pendiente':
                    pendientes += 1
                elif estado_bd == 'en_progreso':
                    en_progreso += 1
                elif estado_bd == 'entregada':
                    entregadas += 1
                elif estado_bd == 'vencida':
                    vencidas += 1

                # Obtener información adicional
                nombre_asignatura = datos.get('nombre_asignatura', '-')
                sigla_tipo = datos.get('sigla_tipo', '-')
                fecha_inicio = datos.get('fecha_inicio', '-')
                fecha_fin = datos.get('fecha_fin', '-')

                # Calcular días restantes
                dias_restantes = '-'
                if fecha_fin and fecha_fin != '-':
                    try:
                        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
                        dias_dif = (fecha_fin_dt - fecha_actual).days
                        if dias_dif < 0:
                            dias_restantes = f"{abs(dias_dif)} ⏰"  # Vencido
                        else:
                            dias_restantes = str(dias_dif)
                    except:
                        dias_restantes = '-'

                self.tabla_actividades.insert_row(
                    index="end",
                    values=(
                        datos['titulo'],
                        nombre_asignatura,
                        sigla_tipo,
                        fecha_inicio or '-',
                        fecha_fin or '-',
                        dias_restantes,
                        estado_display,
                        fecha_entrega,
                    ),
                )

            self.tabla_actividades.autofit_columns()
            self.tabla_actividades.load_table_data()

            # Actualizar estadísticas
            self.lbl_total_actividades['text'] = f"Total Actividades: {total}"
            self.lbl_pendientes['text'] = f"⏳ Pendientes: {pendientes}"
            self.lbl_en_progreso['text'] = f"🔄 En progreso: {en_progreso}"
            self.lbl_entregadas['text'] = f"✅ Entregadas: {entregadas}"
            self.lbl_vencidas['text'] = f"❌ Vencidas: {vencidas}"

        except Exception as e:
            logger.error(f"Error al actualizar tabla: {e}")

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
            total_actividades = len(self.dict_actividades)

            msg = f"Estudiante: {estudiante} | Total Actividades: {total_actividades}"

            if (
                self.id_actividad_seleccionada > 0
                and self.id_actividad_seleccionada in self.dict_actividades
            ):
                datos = self.dict_actividades[self.id_actividad_seleccionada]
                msg += f" | Editando: {datos['titulo']}"

            self.lbl_estadisticas['text'] = msg

        except Exception as e:
            logger.error(f"Error al actualizar estadísticas: {e}")

    def _limpiar_formulario(self):
        """Limpia el formulario de actualización."""
        self.var_id_actividad_seleccionada.set(0)
        self.var_nombre_actividad_seleccionada.set("[Selecciona una actividad]")
        self.var_estado.set("")
        self.var_fecha_entrega.set("")
        self.id_actividad_seleccionada = 0

    def _cargar_formulario(self, id_actividad: int):
        """Carga los datos de una actividad en el formulario."""
        try:
            if id_actividad not in self.dict_actividades:
                return

            datos_act = self.dict_actividades[id_actividad]
            label_act = f"{datos_act['titulo']}"

            self.var_id_actividad_seleccionada.set(id_actividad)
            self.var_nombre_actividad_seleccionada.set(label_act)
            self.id_actividad_seleccionada = id_actividad

            # Buscar registro existente
            registro = None
            for reg in self.lista_registros_estudiante:
                if reg.id_actividad == id_actividad:
                    registro = reg
                    break

            if registro:
                estado_display = self.estados_display.get(registro.estado, '⏳ Pendiente')
                self.var_estado.set(estado_display)
                self.var_fecha_entrega.set(registro.fecha_entrega if registro.fecha_entrega else "")
            else:
                self.var_estado.set('⏳ Pendiente')
                self.var_fecha_entrega.set("")

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
                    f"al estudiante en una carrera antes de asignar actividades.",
                )
                logger.warning(f"Estudiante {id_estudiante} sin carrera")
                return

            self.id_estudiante_actual = id_estudiante
            self.id_carrera_estudiante = id_carrera
            self.var_id_estudiante.set(id_estudiante)

            # Cargar actividades de la carrera seleccionada
            self._cargar_actividades(id_carrera=id_carrera)

            # Recargar filtros de tipo basados en las nuevas actividades
            self._cargar_filtros_iniciales()

            # Cargar registros del estudiante
            self._cargar_registros_estudiante(id_estudiante)

            # Actualizar tabla
            self._actualizar_tabla_actividades()

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

    def _on_actividad_seleccionada(self, event=None):
        """Maneja la selección de una actividad en la tabla."""
        try:
            seleccion = self.tabla_actividades.view.selection()
            if not seleccion:
                return

            # Obtener valores de la fila
            item = self.tabla_actividades.view.item(seleccion[0])
            valores = item['values']
            titulo_act = valores[0]  # Primera columna es el título

            # Buscar ID de la actividad por título
            id_actividad = None
            for id_act, datos in self.dict_actividades.items():
                if datos['titulo'] == titulo_act:
                    id_actividad = id_act
                    break

            if id_actividad:
                self._cargar_formulario(id_actividad)

        except Exception as e:
            logger.error(f"Error al seleccionar actividad: {e}")

    def _on_filtrar(self, event=None):
        """Maneja todos los filtros (estado, tipo)."""
        try:
            filtro_busqueda = self.entry_buscar_actividad.get()
            filtro_estado = self.var_filtro_estado.get()
            filtro_tipo = self.var_filtro_tipo.get()
            self._actualizar_tabla_actividades(filtro_busqueda, filtro_estado, filtro_tipo)

        except Exception as e:
            logger.error(f"Error al filtrar: {e}")

    def _on_buscar_actividad(self, event=None):
        """Maneja la búsqueda de actividades."""
        try:
            filtro_busqueda = self.entry_buscar_actividad.get()
            filtro_estado = self.var_filtro_estado.get()
            filtro_tipo = self.var_filtro_tipo.get()
            self._actualizar_tabla_actividades(filtro_busqueda, filtro_estado, filtro_tipo)

        except Exception as e:
            logger.error(f"Error en búsqueda: {e}")

    def _on_limpiar_formulario(self):
        """Limpia el formulario."""
        self._limpiar_formulario()
        self._actualizar_estadisticas()

    def _on_abrir_calendario(self):
        """Abre el diálogo de calendario para seleccionar fecha."""
        try:
            result = DatePickerDialog(parent=self.master).show()

            if result:
                fecha = result.strftime('%Y-%m-%d')
                self.var_fecha_entrega.set(fecha)
                logger.info(f"Fecha seleccionada: {fecha}")

        except Exception as e:
            logger.error(f"Error al abrir calendario: {e}")

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

            if self.id_actividad_seleccionada == 0:
                showwarning(
                    parent=self.master,
                    title="Advertencia",
                    message="Debe seleccionar una actividad",
                )
                return

            # Obtener datos del formulario
            estado_display = self.var_estado.get()
            estado_bd = self.estados_display_inv.get(estado_display, 'pendiente')
            fecha_entrega = self.var_fecha_entrega.get().strip()

            # Validar fecha si está presente
            if fecha_entrega:
                try:
                    datetime.strptime(fecha_entrega, "%Y-%m-%d")
                except ValueError:
                    showwarning(
                        parent=self.master,
                        title="Advertencia",
                        message="Formato de fecha inválido. Use YYYY-MM-DD",
                    )
                    return

            # Crear o actualizar registro
            registro = EstudianteActividadService(ruta_db=None)
            registro.id_estudiante = self.id_estudiante_actual
            registro.id_actividad = self.id_actividad_seleccionada
            registro.estado = estado_bd
            registro.fecha_entrega = fecha_entrega if fecha_entrega else None

            # Verificar si existe el registro
            existe = registro.existe()

            if existe:
                # Actualizar
                resultado = registro.actualizar()
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
            self._actualizar_tabla_actividades()
            self._limpiar_formulario()

        except Exception as e:
            logger.error(f"Error al aplicar cambios: {e}", exc_info=True)
            showwarning(
                parent=self.master,
                title="Error",
                message=f"Error inesperado: {str(e)}",
            )
