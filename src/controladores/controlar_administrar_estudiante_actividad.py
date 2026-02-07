from tkinter.messagebox import showinfo, showwarning
from typing import Dict, Any, Optional
from scripts.logging_config import obtener_logger_modulo
from modelos.services.estudiante_actividad_service import EstudianteActividadService
from modelos.services.estudiante_service import EstudianteService
from modelos.services.actividad_service import ActividadService
from modelos.services.estudiante_carrera_service import EstudianteCarreraService
from ttkbootstrap.dialogs import DatePickerDialog
from datetime import datetime

logger = obtener_logger_modulo(__name__)


class ControlarAdministrarEstudianteActividad:
    def __init__(
        self,
        master,
        map_vars: Dict[str, Any],
        map_widgets: Dict[str, Any],
        preselect: Optional[Dict[str, Any]] = None,
    ):
        self.master = master
        self.map_widgets = map_widgets
        self.map_vars = map_vars
        self.preselect = preselect or {}
        self.label_estudiante_actual: str = ""

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
        self.cbx_filtro_asignatura = self.map_widgets.get('cbx_filtro_asignatura')
        self.btn_limpiar_filtros = self.map_widgets.get('btn_limpiar_filtros')
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
        self.var_nota = self.map_vars.get('var_nota')
        self.var_nota_estudiante = self.map_vars.get('var_nota_estudiante')
        self.var_porcentaje = self.map_vars.get('var_porcentaje')
        self.var_filtro_estado = self.map_vars.get('var_filtro_estado')
        self.var_filtro_tipo = self.map_vars.get('var_filtro_tipo')
        self.var_filtro_asignatura = self.map_vars.get('var_filtro_asignatura')

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

        # aplicar preselección si viene desde un contexto externo
        self._aplicar_preseleccion()

    def _aplicar_preseleccion(self):
        try:
            if not self.preselect:
                self._auto_cargar_estudiante()
                return

            id_estudiante = self.preselect.get("id_estudiante")
            id_carrera = self.preselect.get("carrera_id")
            id_actividad = self.preselect.get("actividad_id")

            if not id_estudiante:
                return

            # Buscar label por id_estudiante y opcionalmente id_carrera
            label_objetivo = None
            for clave, info in self.dict_estudiantes.items():
                if info.get("id_estudiante") != id_estudiante:
                    continue
                if id_carrera and info.get("id_carrera") != id_carrera:
                    continue
                label_objetivo = info.get("label")
                break

            # Si no encontró por carrera, toma el primero que coincida
            if not label_objetivo:
                for info in self.dict_estudiantes.values():
                    if info.get("id_estudiante") == id_estudiante:
                        label_objetivo = info.get("label")
                        break

            if not label_objetivo:
                # Fallback: cargar directamente por IDs
                self._cargar_registros_estudiante(id_estudiante)
                self.id_estudiante_actual = id_estudiante
                self.id_carrera_estudiante = id_carrera or 0
                self.var_id_estudiante.set(id_estudiante)
                self.label_estudiante_actual = ""

                if id_carrera:
                    self._cargar_actividades(id_carrera=id_carrera)
                else:
                    self._cargar_actividades()

                self._cargar_filtros_iniciales()
                self._actualizar_tabla_actividades()
                self._limpiar_formulario()
                self._actualizar_estadisticas()

                if id_actividad:
                    self._seleccionar_actividad_por_id(id_actividad)
                return

            self.var_nombre_estudiante.set(label_objetivo)
            self.label_estudiante_actual = label_objetivo
            self._on_cargar_estudiante()

            if id_actividad:
                self._seleccionar_actividad_por_id(id_actividad)
        except Exception as e:
            logger.error(f"Error al aplicar preselección: {e}", exc_info=True)

    def _auto_cargar_estudiante(self):
        try:
            valores = self.cbx_estudiante['values'] if self.cbx_estudiante else []
            if not valores:
                return
            if not self.var_nombre_estudiante.get():
                self.var_nombre_estudiante.set(valores[0])
                self.label_estudiante_actual = valores[0]
            self._on_cargar_estudiante()
        except Exception as e:
            logger.error(f"Error al auto cargar estudiante: {e}", exc_info=True)

    def _seleccionar_actividad_por_id(self, id_actividad: int):
        try:
            datos = self.dict_actividades.get(id_actividad)
            if not datos:
                return

            titulo = datos.get("titulo")
            if not titulo:
                return

            for item_id in self.tabla_actividades.view.get_children():
                item = self.tabla_actividades.view.item(item_id)
                valores = item.get("values") or []
                if valores and valores[0] == titulo:
                    self.tabla_actividades.view.selection_set(item_id)
                    self.tabla_actividades.view.see(item_id)
                    self._cargar_formulario(id_actividad)
                    break
        except Exception as e:
            logger.error(f"Error al seleccionar actividad por ID: {e}", exc_info=True)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Métodos Privados
    # └────────────────────────────────────────────────────────────┘
    def _vincular_eventos(self):
        # Botón cargar estudiante
        self.btn_cargar_estudiante.config(command=self._on_cargar_estudiante)

        # Tabla - doble click
        self.tabla_actividades.view.bind("<Double-Button-1>", self._on_actividad_seleccionada)

        if self.var_nota_estudiante:
            self.var_nota_estudiante.trace_add("write", lambda *_: self._actualizar_porcentaje())
        if self.var_nota:
            self.var_nota.trace_add("write", lambda *_: self._actualizar_porcentaje())

        # Botones del formulario
        self.btn_aplicar.config(command=self._on_aplicar)
        self.btn_limpiar.config(command=self._on_limpiar_formulario)
        self.btn_calendario.config(command=self._on_abrir_calendario)

        # Filtros
        self.cbx_filtro_estado.bind("<<ComboboxSelected>>", self._on_filtrar)
        self.cbx_filtro_tipo.bind("<<ComboboxSelected>>", self._on_filtrar)
        self.cbx_filtro_asignatura.bind("<<ComboboxSelected>>", self._on_filtrar)
        self.entry_buscar_actividad.bind("<KeyRelease>", self._on_buscar_actividad)

        # Botón limpiar filtros
        if self.btn_limpiar_filtros:
            self.btn_limpiar_filtros.config(command=self._on_limpiar_filtros)

    def _cargar_widgets(self):
        """Configura el estado inicial de los widgets."""
        self.var_nombre_actividad_seleccionada.set("[Selecciona una actividad]")

    def _cargar_estudiantes(self):
        """Carga todos los estudiantes con sus carreras activas."""
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

            if id_carrera:
                servicio_actividad = ActividadService(ruta_db=None)
                lista_aux = servicio_actividad.obtener_con_detalle(id_carrera=id_carrera)
            else:
                servicio_actividad = ActividadService(ruta_db=None)
                lista_aux = servicio_actividad.obtener_con_detalle()

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
                        'nota': data.get('nota', 0),
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

            # Asegurar que estén todas las actividades con registro del estudiante
            ids_registros = {r.id_actividad for r in self.lista_registros_estudiante}
            faltantes = [i for i in ids_registros if i not in self.dict_actividades]
            if faltantes:
                servicio_all = ActividadService(ruta_db=None)
                lista_all = servicio_all.obtener_con_detalle()
                for data in lista_all:
                    id_actividad = data.get('id_actividad')
                    if id_actividad in faltantes:
                        self.dict_actividades[id_actividad] = {
                            'titulo': data.get('titulo'),
                            'descripcion': data.get('descripcion'),
                            'fecha_inicio': data.get('fecha_inicio'),
                            'fecha_fin': data.get('fecha_fin'),
                            'id_eje': data.get('id_eje'),
                            'id_tipo_actividad': data.get('id_tipo_actividad'),
                            'nota': data.get('nota', 0),
                            'nombre_eje': data.get('nombre_eje'),
                            'nombre_asignatura': data.get('nombre_asignatura'),
                            'sigla_tipo': data.get('sigla_tipo') or '',
                        }
                logger.info(f"Se añadieron {len(faltantes)} actividades faltantes por registros")

        except Exception as e:
            logger.error(f"Error al cargar actividades: {e}")

    def _cargar_filtros_iniciales(self):
        """Carga los filtros iniciales de tipos de actividad y asignaturas."""
        try:
            # Cargar tipos de actividad desde las actividades cargadas
            tipos_set = set()
            asignaturas_set = set()
            for actividad in self.dict_actividades.values():
                if actividad.get('sigla_tipo'):
                    tipos_set.add(actividad.get('sigla_tipo'))
                if actividad.get('nombre_asignatura'):
                    asignaturas_set.add(actividad.get('nombre_asignatura'))

            tipos = ["Todos"] + sorted(list(tipos_set))
            self.cbx_filtro_tipo.config(values=tipos)
            self.var_filtro_tipo.set("Todos")

            # Configurar filtro de asignaturas
            asignaturas = ["Todos"] + sorted(list(asignaturas_set))
            self.cbx_filtro_asignatura.config(values=asignaturas)
            self.var_filtro_asignatura.set("Todos")

        except Exception as e:
            logger.error(f"Error al cargar filtros iniciales: {e}")

    def _cargar_registros_estudiante(self, id_estudiante: int):
        """Carga los registros de estudiante_actividad para un estudiante."""
        try:
            self.lista_registros_estudiante.clear()

            service = EstudianteActividadService(ruta_db=None)
            lista_aux = service.obtener_por_estudiante(id_estudiante)

            if lista_aux:
                for data in lista_aux:
                    registro = EstudianteActividadService(ruta_db=None)
                    registro.id_estudiante = data.get('id_estudiante')
                    registro.id_actividad = data.get('id_actividad')
                    registro.estado = data.get('estado')
                    registro.fecha_entrega = data.get('fecha_entrega')
                    registro.nota_estudiante = data.get('nota_estudiante')
                    registro.porcentaje = data.get('porcentaje')
                    self.lista_registros_estudiante.append(registro)

                logger.info(f"Se cargaron {len(lista_aux)} registros")
            else:
                logger.info("No hay registros para este estudiante")

        except Exception as e:
            logger.error(f"Error al cargar registros del estudiante: {e}")

    def _cargar_carreras_estudiante(self, id_estudiante: int):
        """Carga las carreras disponibles para un estudiante."""
        try:
            self.dict_carreras_estudiante.clear()
            self.dict_carreras_estudiante_inv.clear()

            servicio_ec = EstudianteCarreraService(ruta_db=None)
            lista_aux = servicio_ec.obtener_carreras_estudiante(id_estudiante)

            if lista_aux:
                carreras_labels = []
                for data in lista_aux:
                    id_carrera = data.get('id_carrera')
                    nombre_carrera = data.get('nombre_carrera') or data.get('nombre')
                    estado = data.get('estado')

                    # Agregar indicador de estado
                    label_carrera = nombre_carrera
                    if estado != 'activa':
                        label_carrera += f" ({estado})"

                    self.dict_carreras_estudiante[id_carrera] = {
                        'nombre': nombre_carrera,
                        'estado': estado,
                    }
                    self.dict_carreras_estudiante_inv[label_carrera] = id_carrera
                    carreras_labels.append(label_carrera)

                self.cbx_carrera.config(values=carreras_labels)
                # Seleccionar la primera carrera por defecto
                if carreras_labels:
                    self.var_carrera_seleccionada.set(carreras_labels[0])
                    self._on_carrera_seleccionada()

                logger.info(f"Se cargaron {len(carreras_labels)} carreras para el estudiante")
            else:
                logger.warning("El estudiante no tiene carreras")
                self.cbx_carrera.config(values=[])
                self.var_carrera_seleccionada.set("")

        except Exception as e:
            logger.error(f"Error al cargar carreras del estudiante: {e}")

    def _actualizar_tabla_actividades(
        self,
        filtro_busqueda: str = "",
        filtro_estado: str = "Todos",
        filtro_tipo: str = "Todos",
        filtro_asignatura: str = "Todos",
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

                # Aplicar filtro de asignatura
                if filtro_asignatura != "Todos":
                    nombre_asignatura = datos.get('nombre_asignatura', '')
                    if nombre_asignatura != filtro_asignatura:
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

                nota_val = datos.get('nota', 0)
                try:
                    nota_fmt = f"{float(nota_val):.2f}"
                except Exception:
                    nota_fmt = "0.00"

                nota_est_fmt = ""
                pct_fmt = ""
                if registro:
                    try:
                        if registro.nota_estudiante is not None:
                            nota_est_fmt = f"{float(registro.nota_estudiante):.2f}"
                    except Exception:
                        nota_est_fmt = ""
                    try:
                        if registro.porcentaje is not None:
                            pct_fmt = f"{float(registro.porcentaje):.2f}"
                        elif nota_est_fmt and nota_fmt not in ("", "0.00"):
                            pct_calc = (float(nota_est_fmt) / float(nota_fmt)) * 100
                            pct_fmt = f"{pct_calc:.2f}"
                    except Exception:
                        pct_fmt = ""

                self.tabla_actividades.insert_row(
                    index="end",
                    values=(
                        id_act,
                        datos['titulo'],
                        nombre_asignatura,
                        sigla_tipo,
                        fecha_inicio or '-',
                        fecha_fin or '-',
                        dias_restantes,
                        estado_display,
                        nota_fmt,
                        nota_est_fmt,
                        pct_fmt,
                        fecha_entrega,
                    ),
                )

            self.tabla_actividades.autofit_columns()
            # Re-ocultar columna ID (Tableview puede reescribir anchos)
            try:
                self.tabla_actividades.view.column("#1", width=0, stretch=False)
            except Exception:
                pass
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

            estudiante = (
                self.var_nombre_estudiante.get()
                or self.label_estudiante_actual
                or "Desconocido"
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

    def _set_status_message(self, mensaje: str):
        try:
            base = self.lbl_estadisticas.cget("text")
            if base:
                self.lbl_estadisticas.config(text=f"{base} | {mensaje}")
            else:
                self.lbl_estadisticas.config(text=mensaje)
        except Exception:
            pass

    def _limpiar_formulario(self):
        """Limpia el formulario de actualización."""
        self.var_id_actividad_seleccionada.set(0)
        self.var_nombre_actividad_seleccionada.set("[Selecciona una actividad]")
        self.var_estado.set("")
        self.var_fecha_entrega.set("")
        self.var_nota.set("0")
        if self.var_nota_estudiante:
            self.var_nota_estudiante.set("")
        if self.var_porcentaje:
            self.var_porcentaje.set("")
        self.id_actividad_seleccionada = 0

    def _cargar_formulario(self, id_actividad: int):
        """Carga los datos de una actividad en el formulario."""
        try:
            if id_actividad not in self.dict_actividades:
                return

            datos_act = self.dict_actividades[id_actividad]
            try:
                act = ActividadService(ruta_db=None)
                act.id_actividad = id_actividad
                if act.instanciar():
                    datos_act['nota'] = act.nota
            except Exception as e:
                logger.error(f"Error al cargar nota de actividad: {e}", exc_info=True)
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
                self.var_fecha_entrega.set(
                    datos_act.get('fecha_fin', "") or registro.fecha_entrega or ""
                )
                if self.var_nota_estudiante is not None:
                    nota_est = registro.nota_estudiante
                    self.var_nota_estudiante.set("" if nota_est is None else f"{float(nota_est):.2f}")
                if self.var_porcentaje is not None:
                    pct = registro.porcentaje
                    self.var_porcentaje.set("" if pct is None else f"{float(pct):.2f}")
            else:
                self.var_estado.set('⏳ Pendiente')
                self.var_fecha_entrega.set(datos_act.get('fecha_fin', "") or "")
                if self.var_nota_estudiante is not None:
                    self.var_nota_estudiante.set("")
                if self.var_porcentaje is not None:
                    self.var_porcentaje.set("")

            try:
                nota_val = float(datos_act.get('nota', 0) or 0)
            except Exception:
                nota_val = 0.0
            self.var_nota.set(f"{nota_val:.2f}")
            self._actualizar_porcentaje()

            self._actualizar_estadisticas()

        except Exception as e:
            logger.error(f"Error al cargar formulario: {e}")

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘

    def _on_cargar_estudiante(self):
        """Carga los datos del estudiante seleccionado."""
        try:
            label_estudiante = self.var_nombre_estudiante.get()
            if not label_estudiante:
                showwarning(
                    parent=self.master,
                    title="Advertencia",
                    message="Debe seleccionar un estudiante",
                )
                return

            # Obtener clave única (id_estudiante_id_carrera)
            clave_dict = self.dict_estudiantes_inv.get(label_estudiante, None)
            if not clave_dict:
                return

            # Obtener info del estudiante
            info_estudiante = self.dict_estudiantes.get(clave_dict)
            if not info_estudiante:
                return

            # Extraer id_estudiante
            id_estudiante = info_estudiante.get('id_estudiante')
            id_carrera = info_estudiante.get('id_carrera')

            self.id_estudiante_actual = id_estudiante
            self.id_carrera_estudiante = id_carrera
            self.var_id_estudiante.set(id_estudiante)
            self.label_estudiante_actual = label_estudiante

            # Cargar registros del estudiante
            self._cargar_registros_estudiante(id_estudiante)

            # Cargar actividades de la carrera (luego de registros para completar faltantes)
            if id_carrera:
                self._cargar_actividades(id_carrera=id_carrera)
            else:
                self._cargar_actividades()

            # Recargar filtros de tipo
            self._cargar_filtros_iniciales()

            # Actualizar tabla
            self._actualizar_tabla_actividades()

            # Limpiar formulario
            self._limpiar_formulario()

            # Actualizar estadísticas
            self._actualizar_estadisticas()

            logger.info(f"Estudiante cargado: {label_estudiante}")

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
            id_actividad = valores[0] if valores else None
            if id_actividad:
                self._cargar_formulario(int(id_actividad))

        except Exception as e:
            logger.error(f"Error al seleccionar actividad: {e}")

    def _on_filtrar(self, event=None):
        """Maneja todos los filtros (estado, tipo, asignatura)."""
        try:
            filtro_busqueda = self.entry_buscar_actividad.get()
            filtro_estado = self.var_filtro_estado.get()
            filtro_tipo = self.var_filtro_tipo.get()
            filtro_asignatura = self.var_filtro_asignatura.get()
            self._actualizar_tabla_actividades(
                filtro_busqueda, filtro_estado, filtro_tipo, filtro_asignatura
            )

        except Exception as e:
            logger.error(f"Error al filtrar: {e}")

    def _on_buscar_actividad(self, event=None):
        """Maneja la búsqueda de actividades."""
        try:
            filtro_busqueda = self.entry_buscar_actividad.get()
            filtro_estado = self.var_filtro_estado.get()
            filtro_tipo = self.var_filtro_tipo.get()
            filtro_asignatura = self.var_filtro_asignatura.get()
            self._actualizar_tabla_actividades(
                filtro_busqueda, filtro_estado, filtro_tipo, filtro_asignatura
            )

        except Exception as e:
            logger.error(f"Error en búsqueda: {e}")

    def _on_limpiar_filtros(self):
        """Limpia todos los filtros."""
        self.entry_buscar_actividad.delete(0, "end")
        self.var_filtro_estado.set("Todos")
        self.var_filtro_tipo.set("Todos")
        self.var_filtro_asignatura.set("Todos")
        self._actualizar_tabla_actividades()

    def _on_limpiar_formulario(self):
        """Limpia el formulario."""
        self._limpiar_formulario()
        self._actualizar_estadisticas()

    def _on_abrir_calendario(self):
        """Abre el diálogo de calendario para seleccionar fecha."""
        try:
            dialog = DatePickerDialog(parent=self.master)
            fecha = getattr(dialog, "date_selected", None)
            if fecha:
                fecha_str = fecha.strftime('%Y-%m-%d')
                self.var_fecha_entrega.set(fecha_str)
                logger.info(f"Fecha seleccionada: {fecha_str}")

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
            nota_str = self.var_nota.get().strip() if self.var_nota else ""
            if nota_str == "":
                nota_str = "0"
            try:
                nota_val = float(nota_str)
            except ValueError:
                showwarning(
                    parent=self.master,
                    title="Advertencia",
                    message="Nota inválida. Use un número.",
                )
                return

            nota_estudiante_val = None
            if self.var_nota_estudiante is not None:
                nota_est_str = self.var_nota_estudiante.get().strip()
                if nota_est_str != "":
                    try:
                        nota_estudiante_val = float(nota_est_str)
                    except ValueError:
                        showwarning(
                            parent=self.master,
                            title="Advertencia",
                            message="Nota de estudiante inválida. Use un número.",
                        )
                        return

            porcentaje_val = None
            if self.var_porcentaje is not None:
                pct_str = self.var_porcentaje.get().strip()
                if pct_str != "":
                    try:
                        porcentaje_val = float(pct_str)
                    except ValueError:
                        showwarning(
                            parent=self.master,
                            title="Advertencia",
                            message="Porcentaje inválido. Use un número.",
                        )
                        return
            if porcentaje_val is None:
                try:
                    if nota_estudiante_val is not None and nota_val > 0:
                        porcentaje_val = (nota_estudiante_val / nota_val) * 100
                except Exception:
                    porcentaje_val = None

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
            registro.nota_estudiante = nota_estudiante_val
            registro.porcentaje = porcentaje_val

            # Verificar si existe el registro
            existe = registro.existe()

            if existe:
                resultado = registro.actualizar()
            else:
                resultado = registro.insertar()

            if not resultado:
                showwarning(
                    parent=self.master,
                    title="Error",
                    message="No se pudo guardar el registro",
                )

            # Actualizar nota de la actividad (opcional) antes de limpiar formulario
            if nota_str != "":
                try:
                    act = ActividadService(ruta_db=None)
                    act.id_actividad = self.id_actividad_seleccionada
                    if act.instanciar():
                        act.nota = nota_val
                        act.actualizar()
                        self.dict_actividades[self.id_actividad_seleccionada]['nota'] = nota_val
                        self.var_nota.set(f"{nota_val:.2f}")
                except Exception as e:
                    logger.error(f"Error al actualizar nota de actividad: {e}", exc_info=True)

            # Recargar datos
            self._cargar_registros_estudiante(self.id_estudiante_actual)
            self._actualizar_tabla_actividades(
                self.entry_buscar_actividad.get(),
                self.var_filtro_estado.get(),
                self.var_filtro_tipo.get(),
                self.var_filtro_asignatura.get(),
            )
            self._limpiar_formulario()
            if resultado:
                self._set_status_message("Cambios guardados")

        except Exception as e:
            logger.error(f"Error al aplicar cambios: {e}", exc_info=True)
            showwarning(
                parent=self.master,
                title="Error",
                message=f"Error inesperado: {str(e)}",
            )

    def _actualizar_porcentaje(self):
        if not self.var_porcentaje:
            return
        try:
            nota_act = float(self.var_nota.get()) if self.var_nota and self.var_nota.get().strip() != "" else 0.0
        except Exception:
            nota_act = 0.0
        try:
            nota_est = (
                float(self.var_nota_estudiante.get())
                if self.var_nota_estudiante and self.var_nota_estudiante.get().strip() != ""
                else None
            )
        except Exception:
            nota_est = None

        if nota_act > 0 and nota_est is not None:
            pct = (nota_est / nota_act) * 100
            self.var_porcentaje.set(f"{pct:.2f}")
