from ttkbootstrap import Combobox, StringVar, Frame, Label, Labelframe, Button
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.constants import *
from typing import Dict, Any, List, Optional
from tkinter.messagebox import showwarning
from tkinter import Menu
from datetime import datetime
from modelos.services.estudiante_service import EstudianteService
from modelos.services.estudiante_carrera_service import EstudianteCarreraService
from modelos.services.asignatura_service import AsignaturaService
from modelos.services.actividad_service import ActividadService
from modelos.services.tipo_actividad_service import TipoActividadService
from modelos.services.estudiante_carrera_service import EstudianteCarreraService
from modelos.services.estudiante_asignatura_service import EstudianteAsignaturaService
from modelos.services.carrera_service import CarreraService
from modelos.services.estudiante_actividad_service import EstudianteActividadService
from scripts.logging_config import obtener_logger_modulo
from ui.ttk.dialogos.dialogo_estado_actividad import DialogoEstadoActividad
from ui.ttk.dialogos.dialogo_administrar_estudiante_actividad import (
    DialogoAdministrarEstudianteActividad,
)

logger = obtener_logger_modulo(__name__)


class ControlarActividades:
    def __init__(self, map_vars: Dict[str, Any], map_widgets: Dict[str, Any]):
        self.map_vars: Dict[str, Any] = map_vars
        self.map_widgets: Dict[str, Any] = map_widgets

        # Diccionarios para estudiantes
        self.dict_estudiantes: Dict[int, str] = {}  # id -> "Nombre - Correo"
        self.dict_estudiantes_inv: Dict[str, int] = {}  # "Nombre - Correo" -> id

        # Diccionarios para carreras
        self.dict_carreras: Dict[int, str] = {}  # id -> "Nombre - Plan"
        self.dict_carreras_inv: Dict[str, int] = {}  # "Nombre - Plan" -> id

        # Diccionarios para asignaturas
        self.dict_asignaturas: Dict[int, str] = {}  # id -> "Codigo - Nombre"
        self.dict_asignaturas_inv: Dict[str, int] = {}  # "Codigo - Nombre" -> id

        # Diccionarios para tipos de actividad
        self.dict_tipos_actividad: Dict[int, str] = {}  # id -> "Nombre"
        self.dict_tipos_actividad_inv: Dict[str, int] = {}  # "Nombre" -> id

        # Lista de las actividades detalladas
        self.lista_actividades_detalladas: List[Dict[str, Any]] = []

        # IDs actuales
        self.id_estudiante_actual: int = 0
        self.id_carrera_actual: int = 0
        self.id_asignatura_actual: int = 0
        self.id_tipo_actividad_actual: int = 0

        # Vista actual de estadísticas
        self.vista_actual: str = "resumen"  # resumen, desempeño, timeline, comparativa

        # Cargar datos iniciales
        self._cargar_vars()
        self._cargar_widgets()
        self._cargar_estudiantes()
        self._cargar_tipos_actividad()
        # vinculamos los eventos a los widgets
        self._vincular_eventos()
        # Crear botones de estadísticas
        self._crear_botones_estadisticas()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Métodos de Carga
    # └────────────────────────────────────────────────────────────┘

    def _cargar_vars(self) -> None:
        """Carga las variables StringVar desde el diccionario de variables.

        Las variables se utilizan para mantener sincronizados los valores
        seleccionados en los comboboxes con el controlador.

        Raises:
            Exception: Si no se encuentran las variables requeridas.
        """
        try:
            self.var_estudiante: StringVar = self.map_vars.get('var_estudiante')
            self.var_carrera: StringVar = self.map_vars.get('var_carrera')
            self.var_asignatura: StringVar = self.map_vars.get('var_asignatura')
            self.var_tipo_actividad: StringVar = self.map_vars.get('var_tipo_actividad')
            logger.info("Variables cargadas correctamente")
        except Exception as e:
            logger.error(f"Error al cargar variables: {e}")
            showwarning("Error", f"Error al cargar variables: {e}")

    def _cargar_widgets(self) -> None:
        """Carga los widgets combobox desde el diccionario de widgets.

        Los widgets se utilizan para mostrar las opciones de selección
        al usuario (estudiantes, carreras, asignaturas, tipos de actividad).

        Raises:
            Exception: Si no se encuentran los widgets requeridos.
        """
        try:
            self.cbx_estudiantes: Combobox = self.map_widgets.get('cbx_estudiantes')
            self.cbx_carreras: Combobox = self.map_widgets.get('cbx_carreras')
            self.cbx_asignaturas: Combobox = self.map_widgets.get('cbx_asignaturas')
            self.cbx_tipo_actividades: Combobox = self.map_widgets.get('cbx_tipo_actividades')
            self.scrolled_frame: ScrolledFrame = self.map_widgets.get('scrolled_frame')
            self.label_frame_datos: Labelframe = self.map_widgets.get('label_frame_datos')
            logger.info("Widgets cargados correctamente")
        except Exception as e:
            logger.error(f"Error al cargar widgets: {e}")
            showwarning("Error", f"Error al cargar widgets: {e}")

    def _filtrar_actividades_detalladas(self):
        """Filtra las actividades detalladas basado en los filtros seleccionados.

        Niveles de filtrado:
        1. Solo estudiante: Muestra todas sus actividades
        2. Estudiante + Carrera: Muestra actividades de esa carrera
        3. Estudiante + Carrera + Asignatura: Muestra actividades de esa asignatura
        4. Estudiante + Carrera + Asignatura + Tipo: Muestra actividades filtradas por tipo
        """
        try:
            # Limpiar la lista
            self.lista_actividades_detalladas.clear()

            # Obtener valores seleccionados
            nombre_estudiante = self.var_estudiante.get()
            nombre_carrera = self.var_carrera.get()
            nombre_asignatura = self.var_asignatura.get()
            nombre_tipo_actividad = self.var_tipo_actividad.get()

            # Validar que haya estudiante seleccionado
            if not nombre_estudiante:
                logger.warning("No hay estudiante seleccionado")
                return

            # Obtener ID del estudiante
            id_estudiante = self.dict_estudiantes_inv.get(nombre_estudiante, 0)
            if id_estudiante == 0:
                logger.warning(f"Estudiante no encontrado: {nombre_estudiante}")
                return

            id_carrera = None
            id_asignatura = None
            id_tipo_actividad = None

            if nombre_carrera and nombre_carrera != "Todos":
                id_carrera = self.dict_carreras_inv.get(nombre_carrera, 0) or None

            if nombre_asignatura and nombre_asignatura != "Todos":
                id_asignatura = self.dict_asignaturas_inv.get(nombre_asignatura, 0) or None

            if nombre_tipo_actividad and nombre_tipo_actividad != "Todos":
                id_tipo_actividad = self.dict_tipos_actividad_inv.get(nombre_tipo_actividad, 0) or None

            servicio_actividad = ActividadService(ruta_db=None)
            resultado = servicio_actividad.obtener_detalladas_filtradas(
                id_estudiante=id_estudiante,
                id_carrera=id_carrera,
                id_asignatura=id_asignatura,
                id_tipo_actividad=id_tipo_actividad,
            )

            if resultado:
                self.lista_actividades_detalladas = resultado
                logger.info(
                    f"Se cargaron {len(resultado)} actividades filtradas "
                    f"(Estudiante: {nombre_estudiante}, Carrera: {nombre_carrera}, "
                    f"Asignatura: {nombre_asignatura}, Tipo: {nombre_tipo_actividad})"
                )
            else:
                logger.warning("No se encontraron actividades con los filtros especificados")

        except Exception as e:
            logger.error(f"Error al filtrar actividades: {e}", exc_info=True)

    def _mostrar_actividades_filtradas(self):
        """Muestra las actividades filtradas en el scrolled_frame.

        Crea una tarjeta (card) para cada actividad con:
        - Título de la actividad
        - Asignatura
        - Tipo de actividad
        - Fechas (inicio y fin)
        - Días de duración
        - Estado del estudiante
        - Fecha de entrega
        """
        try:
            # Limpiar el scrolled_frame
            for widget in self.scrolled_frame.winfo_children():
                widget.destroy()

            if not self.lista_actividades_detalladas:
                # Mostrar mensaje vacío
                label_vacio = Label(
                    self.scrolled_frame,
                    text="📭 No hay actividades que mostrar con los filtros seleccionados",
                    font=("Helvetica", 12),
                    bootstyle="secondary",
                    padding=20,
                )
                label_vacio.pack(fill=BOTH, expand=TRUE)
                return

            # Crear tarjetas para cada actividad
            for actividad in self.lista_actividades_detalladas:
                self._crear_tarjeta_actividad(actividad)

            logger.info(f"Se mostraron {len(self.lista_actividades_detalladas)} actividades")

        except Exception as e:
            logger.error(f"Error al mostrar actividades filtradas: {e}", exc_info=True)

    def _crear_tarjeta_actividad(self, actividad: Dict[str, Any]):
        """Crea una tarjeta visual compacta para una actividad.

        Args:
            actividad: Diccionario con los datos de la actividad
        """
        try:
            titulo = actividad.get('titulo', 'Sin título')
            tipo_nombre = actividad.get('actividad_nombre', 'Sin tipo')
            prioridad = actividad.get('prioridad', 0)
            icon_prioridad = self._obtener_icono_prioridad(prioridad)

            # Frame principal de la tarjeta con Labelframe - padding reducido
            card_frame = Labelframe(
                self.scrolled_frame,
                text=f"📌 {titulo}",
                padding=5,
                bootstyle="info",
            )
            card_frame.pack(fill=X, padx=3, pady=2)


            # Línea 1: Tipo + Descripción resumida en una sola línea
            header_frame = Frame(card_frame)
            header_frame.pack(fill=X, pady=1)

            label_tipo = Label(
                header_frame,
                text=f"{icon_prioridad} {tipo_nombre}",
                font=("Helvetica", 8, "bold"),
                bootstyle="info",
            )
            label_tipo.pack(side=LEFT, padx=2)

            # Descripción compacta
            descripcion = actividad.get('descripcion', '-')
            if descripcion and descripcion != '-':
                # Limitar descripción a 60 caracteres
                desc_corta = (descripcion[:60] + '...') if len(descripcion) > 60 else descripcion
                label_descripcion = Label(
                    header_frame,
                    text=f"📝 {desc_corta}",
                    font=("Helvetica", 8),
                    bootstyle="secondary",
                    justify=LEFT,
                )
                label_descripcion.pack(side=LEFT, padx=2, fill=X, expand=True)

            # Línea 2: Fechas y asignatura en una línea
            info_frame = Frame(card_frame)
            info_frame.pack(fill=X, pady=1)

            fecha_inicio = actividad.get('fecha_inicio', '-')
            fecha_fin = actividad.get('fecha_fin', '-')
            dias_duracion = actividad.get('dias_duracion', '-')
            asignatura = actividad.get('nombre_asignatura', '-')[:20]  # Limitar nombre
            eje = actividad.get('eje_nombre', '-')[:15]  # Limitar eje

            info_text = (
                f"📅 {fecha_inicio}→{fecha_fin} | ⏱️ {dias_duracion}d | 📚 {asignatura} | 🎯 {eje}"
            )
            label_info = Label(
                info_frame,
                text=info_text,
                font=("Helvetica", 8),
            )
            label_info.pack(fill=X)

            # Línea 3: Estado y entrega
            estado = actividad.get('actividad_estado', 'pendiente')
            fecha_entrega = actividad.get('fecha_entrega', '-')
            dias_desde_fin = actividad.get('dias_desde_fin', 0)

            # Determinar color según estado
            estado_color = self._obtener_color_estado(estado)
            estado_display = self._obtener_display_estado(estado)

            # Información adicional de entrega
            if dias_desde_fin < 0:
                dias_info = f"Faltan {abs(dias_desde_fin)}d"
            else:
                dias_info = f"Hace {dias_desde_fin}d"

            estado_frame = Frame(card_frame)
            estado_frame.pack(fill=X, pady=1)

            label_estado = Label(
                estado_frame,
                text=f"{estado_display}",
                font=("Helvetica", 8, "bold"),
                bootstyle=estado_color,
                padding=2,
            )
            label_estado.pack(side=LEFT, padx=2)

            label_entrega = Label(
                estado_frame,
                text=f"📮 {fecha_entrega} | {dias_info}",
                font=("Helvetica", 8),
            )
            label_entrega.pack(side=LEFT, padx=5)

            menu = self._crear_menu_contextual(card_frame, actividad)
            self._vincular_menu_contextual(card_frame, menu)
            self._vincular_hover(card_frame)

        except Exception as e:
            logger.error(f"Error al crear tarjeta de actividad: {e}", exc_info=True)

    def _vincular_hover(self, widget):
        def _enter(_event):
            try:
                widget.configure(bootstyle="primary")
            except Exception:
                pass

        def _leave(_event):
            try:
                widget.configure(bootstyle="info")
            except Exception:
                pass

        widget.bind("<Enter>", _enter)
        widget.bind("<Leave>", _leave)

    def _crear_menu_contextual(self, parent, actividad: Dict[str, Any]) -> Menu:
        menu = Menu(parent, tearoff=0)
        estado_actual = actividad.get("actividad_estado", "pendiente")
        menu.add_command(
            label=f"Estado actual: {estado_actual}",
            state="disabled",
        )
        menu.add_separator()
        menu.add_command(
            label="Cambiar estado…", command=lambda: self._abrir_dialogo_estado(actividad)
        )
        menu.add_separator()
        menu.add_command(
            label="Marcar como Pendiente",
            command=lambda: self._actualizar_estado_actividad(actividad, "pendiente"),
        )
        menu.add_command(
            label="Marcar como En progreso",
            command=lambda: self._actualizar_estado_actividad(actividad, "en_progreso"),
        )
        menu.add_command(
            label="Marcar como Entregada",
            command=lambda: self._actualizar_estado_actividad(actividad, "entregada"),
        )
        menu.add_command(
            label="Marcar como Vencida",
            command=lambda: self._actualizar_estado_actividad(actividad, "vencida"),
        )
        menu.add_separator()
        menu.add_command(
            label="Abrir administrador completo",
            command=lambda act=actividad: self._abrir_admin_estudiante_actividad(act),
        )
        return menu

    def _vincular_menu_contextual(self, widget, menu: Menu):
        def _show_menu(event):
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()

        def _bind_recursively(w):
            w.bind("<Button-3>", _show_menu)
            for child in w.winfo_children():
                _bind_recursively(child)

        _bind_recursively(widget)

    def _abrir_dialogo_estado(self, actividad: Dict[str, Any]):
        try:
            DialogoEstadoActividad(
                parent=self.scrolled_frame.winfo_toplevel(),
                actividad=actividad,
                on_save=self._actualizar_estado_actividad,
            )
        except Exception as e:
            logger.error(f"Error al abrir diálogo de estado: {e}", exc_info=True)

    def _abrir_admin_estudiante_actividad(self, actividad: Dict[str, Any]):
        try:
            preselect = {
                "id_estudiante": actividad.get("id_estudiante"),
                "actividad_id": actividad.get("actividad_id"),
                "carrera_id": actividad.get("carrera_id"),
            }
            DialogoAdministrarEstudianteActividad(
                parent=self.scrolled_frame.winfo_toplevel(),
                preselect=preselect,
            )
        except Exception as e:
            logger.error(
                f"Error al abrir administrador de estudiante-actividad: {e}", exc_info=True
            )

    def _actualizar_estado_actividad(
        self, actividad: Dict[str, Any], nuevo_estado: str, fecha_entrega: Optional[str] = None
    ):
        try:
            id_estudiante = actividad.get('id_estudiante')
            id_actividad = actividad.get('actividad_id')
            if not id_estudiante or not id_actividad:
                logger.warning("Actividad sin IDs válidos para actualizar estado")
                return

            if nuevo_estado == "entregada" and not fecha_entrega:
                fecha_entrega = datetime.now().date().isoformat()

            servicio = EstudianteActividadService(
                ruta_db=None,
                id_estudiante=id_estudiante,
                id_actividad=id_actividad,
                estado=nuevo_estado,
                fecha_entrega=fecha_entrega,
            )
            if servicio.actualizar():
                logger.info(
                    f"Estado actualizado: estudiante={id_estudiante}, actividad={id_actividad}, "
                    f"estado={nuevo_estado}"
                )
                self._filtrar_actividades_detalladas()
                self._mostrar_actividades_filtradas()
        except Exception as e:
            logger.error(f"Error al actualizar estado de actividad: {e}", exc_info=True)

    @staticmethod
    def _obtener_color_estado(estado: str) -> str:
        """Obtiene el color de bootstrap según el estado.

        Args:
            estado: Estado de la actividad

        Returns:
            str: Color de bootstrap (success, warning, danger, info)
        """
        colores = {
            'pendiente': 'secondary',
            'en_progreso': 'info',
            'entregada': 'success',
            'vencida': 'danger',
        }
        return colores.get(estado, 'secondary')

    @staticmethod
    def _obtener_display_estado(estado: str) -> str:
        """Obtiene el texto mostrable del estado.

        Args:
            estado: Estado de la actividad

        Returns:
            str: Texto con emoji
        """
        estados = {
            'pendiente': '⏳ Pendiente',
            'en_progreso': '🔄 En progreso',
            'entregada': '✅ Entregada',
            'vencida': '❌ Vencida',
        }
        return estados.get(estado, '⏳ Pendiente')

    def _cargar_estudiantes(self) -> None:
        """Carga todos los estudiantes de la base de datos.

        Obtiene la lista de estudiantes y la muestra en el combobox.
        También actualiza los diccionarios de mapeo de IDs.

        El formato mostrado es: "Nombre - Correo"
        """
        try:
            estudiante_service = EstudianteService(ruta_db=None)
            lista_estudiantes = estudiante_service.obtener_id_nombre_correo()

            # Limpiar diccionarios
            self.dict_estudiantes.clear()
            self.dict_estudiantes_inv.clear()
            lista = []

            if lista_estudiantes:
                for dato in lista_estudiantes:
                    id_estudiante = dato['id_estudiante']
                    nombre = dato['nombre']
                    correo = dato['correo']

                    label = f"{nombre} - {correo}"
                    lista.append(label)

                    # Mapeo bidireccional
                    self.dict_estudiantes[id_estudiante] = label
                    self.dict_estudiantes_inv[label] = id_estudiante

                logger.info(f"Se cargaron {len(lista)} estudiantes")
            else:
                logger.warning("No se encontraron estudiantes")

            # Actualizar combobox
            self.cbx_estudiantes.config(values=lista)
            if lista:
                self.cbx_estudiantes.current(0)

        except Exception as e:
            logger.error(f"Error al cargar estudiantes: {e}", exc_info=True)
            self.cbx_estudiantes.config(values=[])

    def _cargar_carreras(self, nombre_estudiante: str) -> None:
        """Carga las carreras del estudiante seleccionado.

        Args:
            nombre_estudiante (str): Nombre del estudiante en formato "Nombre - Correo"

        El formato mostrado es: "✓ Nombre Carrera (estado)"
        Ej: "✓ Ingeniería en Sistemas (activa)"
             "✗ Administración (inactiva)"

        Nota: Siempre incluye la opción "Todos" como primera opción.
        """
        try:
            # Limpiar diccionarios
            self.dict_carreras.clear()
            self.dict_carreras_inv.clear()
            lista_aux = ["Todos"]

            if not nombre_estudiante:
                self.cbx_carreras.config(values=lista_aux)
                self.cbx_carreras.current(0)
                return

            # Obtener ID del estudiante
            id_estudiante = self.dict_estudiantes_inv.get(nombre_estudiante, 0)
            if id_estudiante == 0:
                logger.warning(f"Estudiante no encontrado: {nombre_estudiante}")
                self.cbx_carreras.config(values=lista_aux)
                self.cbx_carreras.current(0)
                return

            # Consultar carreras del estudiante
            servicio_ec = EstudianteCarreraService(ruta_db=None)
            consulta = servicio_ec.obtener_carreras_estudiante(id_estudiante)

            if consulta:
                for dato in consulta:
                    id_carrera = dato['id_carrera']
                    nombre_carrera = dato.get('nombre_carrera') or dato.get('nombre')
                    estado = dato['estado']

                    # Obtener ícono del estado
                    icon_estado = self._obtener_icono_estado_carrera(estado)

                    # Formato: "✓ Nombre Carrera (estado)"
                    label = f"{icon_estado} {nombre_carrera} ({estado})"
                    lista_aux.append(label)

                    # Mapeo bidireccional
                    self.dict_carreras[id_carrera] = label
                    self.dict_carreras_inv[label] = id_carrera

                logger.info(f"Se cargaron {len(lista_aux) - 1} carreras")
            else:
                logger.warning(f"No se encontraron carreras para: {nombre_estudiante}")

            # Actualizar combobox
            self.cbx_carreras.config(values=lista_aux)
            self.cbx_carreras.current(0)

        except Exception as e:
            logger.error(f"Error al cargar carreras: {e}", exc_info=True)
            self.cbx_carreras.config(values=["Todos"])
            self.cbx_carreras.current(0)

    @staticmethod
    def _obtener_icono_estado_asignatura(estado: str) -> str:
        """Obtiene el ícono correspondiente al estado de una asignatura.

        Args:
            estado (str): Estado de la asignatura (no_cursada, cursando, aprobada, reprobada)

        Returns:
            str: Ícono emoji correspondiente al estado
                 🔵 No cursada
                 🟡 Cursando
                 🟢 Aprobada
                 🔴 Reprobada
        """
        estados_icon = {
            'no_cursada': '🔵',
            'cursando': '🟡',
            'aprobada': '🟢',
            'reprobada': '🔴',
        }
        return estados_icon.get(estado, '🔵')

    @staticmethod
    def _obtener_icono_prioridad(prioridad: int) -> str:
        """Obtiene el ícono correspondiente al nivel de prioridad.

        Args:
            prioridad (int): Nivel de prioridad (0: baja, 1: media, 2: alta)

        Returns:
            str: Ícono emoji correspondiente al nivel
                 🟢 Baja (0)
                 🟡 Media (1)
                 🔴 Alta (2)
        """
        iconos_prioridad = {
            0: '🟢',  # Baja
            1: '🟡',  # Media
            2: '🔴',  # Alta
        }
        return iconos_prioridad.get(prioridad, '🟢')

    @staticmethod
    def _obtener_nombre_prioridad(prioridad: int) -> str:
        """Obtiene el nombre del nivel de prioridad.

        Args:
            prioridad (int): Nivel de prioridad (0: baja, 1: media, 2: alta)

        Returns:
            str: Nombre del nivel (Baja, Media, Alta)
        """
        nombres_prioridad = {
            0: 'Baja',
            1: 'Media',
            2: 'Alta',
        }
        return nombres_prioridad.get(prioridad, 'Desconocida')

    @staticmethod
    def _obtener_icono_estado_carrera(estado: str) -> str:
        """Obtiene el ícono correspondiente al estado de una carrera.

        Args:
            estado (str): Estado de la carrera (activa, inactiva)

        Returns:
            str: Ícono emoji correspondiente al estado
                 ✓ Activa
                 ✗ Inactiva
        """
        estados_icon = {
            'activa': '✓',
            'inactiva': '✗',
        }
        return estados_icon.get(estado, '✗')

    def _cargar_asignaturas(self, nombre_carrera: str) -> None:
        """Carga las asignaturas basadas en la carrera seleccionada usando vw_estudiante_asignatura_carrera.

        Args:
            nombre_carrera (str): Nombre de la carrera en formato "Nombre (estado)"

        Si se selecciona "Todos", carga todas las asignaturas de todas las carreras.
        Si se selecciona una carrera específica, carga solo sus asignaturas.

        El formato mostrado es: "🔵 Nombre Asignatura (Carrera)"
        Ejemplo: "🟢 Cálculo I (Ingeniería en Sistemas)"
        """
        try:
            # Limpiar diccionarios
            self.dict_asignaturas.clear()
            self.dict_asignaturas_inv.clear()
            lista_aux = []

            if not nombre_carrera:
                self.cbx_asignaturas.config(values=lista_aux)
                return

            if nombre_carrera == "Todos":
                asignatura_service = AsignaturaService(ruta_db=None)
                consulta = asignatura_service.obtener_estudiante_asignatura_carrera()
            else:
                # Obtener id_carrera del nombre
                id_carrera = self.dict_carreras_inv.get(nombre_carrera)
                if id_carrera is None:
                    logger.warning(f"Carrera no encontrada: {nombre_carrera}")
                    self.cbx_asignaturas.config(values=lista_aux)
                    return

                asignatura_service = AsignaturaService(ruta_db=None)
                consulta = asignatura_service.obtener_estudiante_asignatura_carrera(id_carrera)

            if consulta:
                for dato in consulta:
                    id_asignatura = dato['id_asignatura']
                    nombre_asignatura = dato['nombre_asignatura']
                    nombre_carrera_resultado = dato['nombre_carrera']
                    estado = dato['estado'] if dato['estado'] else 'no_cursada'

                    # Obtener ícono del estado
                    icon_estado = self._obtener_icono_estado_asignatura(estado)

                    # Formato: "🔵 Nombre Asignatura (Carrera)"
                    label_asignatura = (
                        f"{icon_estado} {nombre_asignatura} ({nombre_carrera_resultado})"
                    )

                    lista_aux.append(label_asignatura)
                    # Mapeo bidireccional
                    self.dict_asignaturas[id_asignatura] = label_asignatura
                    self.dict_asignaturas_inv[label_asignatura] = id_asignatura

                logger.info(f"Se cargaron {len(lista_aux)} asignaturas")
            else:
                logger.warning(f"No se encontraron asignaturas para: {nombre_carrera}")

            # Actualizar combobox
            self.cbx_asignaturas.config(values=lista_aux)
            if lista_aux:
                self.cbx_asignaturas.current(0)

        except Exception as e:
            logger.error(f"Error al cargar asignaturas: {e}", exc_info=True)
            self.cbx_asignaturas.config(values=[])

    def _cargar_tipos_actividad(self) -> None:
        """Carga todos los tipos de actividad disponibles.

        No depende de ningún otro combobox.

        El formato mostrado es: "🔴 Nombre (SIGLA) - Prioridad"
        Ejemplo: "Todos" (opción por defecto)
                 "🔴 Evaluación Parcial (AP) - Alta"
                 "🟡 Trabajo Práctico (TP) - Media"
                 "🟢 Lectura (L) - Baja"

        Nota: Siempre incluye la opción "Todos" como primera opción.
        """
        try:
            # Limpiar diccionarios
            self.dict_tipos_actividad.clear()
            self.dict_tipos_actividad_inv.clear()
            lista = ["Todos"]

            tipo_service = TipoActividadService(ruta_db=None)
            consulta = tipo_service.obtener_todos_por_prioridad()

            if consulta:
                for dato in consulta:
                    id_tipo = dato['id_tipo_actividad']
                    nombre = dato['nombre']
                    siglas = dato['siglas']
                    prioridad = dato['prioridad'] if dato['prioridad'] is not None else 0

                    # Obtener ícono y nombre de la prioridad
                    icon_prioridad = self._obtener_icono_prioridad(prioridad)
                    nombre_prioridad = self._obtener_nombre_prioridad(prioridad)

                    # Formato: "🔴 Nombre (SIGLA) - Prioridad"
                    label = f"{icon_prioridad} {nombre} ({siglas}) - {nombre_prioridad}"

                    lista.append(label)

                    # Mapeo bidireccional
                    self.dict_tipos_actividad[id_tipo] = label
                    self.dict_tipos_actividad_inv[label] = id_tipo

                logger.info(f"Se cargaron {len(lista) - 1} tipos de actividad")
            else:
                logger.warning("No se encontraron tipos de actividad")

            # Actualizar combobox
            self.cbx_tipo_actividades.config(values=lista)
            if lista:
                self.cbx_tipo_actividades.current(0)

        except Exception as e:
            logger.error(f"Error al cargar tipos de actividad: {e}", exc_info=True)
            self.cbx_tipo_actividades.config(values=["Todos"])

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘

    def _on_change_estudiante(self, event=None) -> None:
        """Maneja el evento cuando el usuario selecciona un estudiante.

        Args:
            event: Evento de Tkinter (requerido por bind)
        """
        try:
            nombre_estudiante = self.var_estudiante.get()
            self.id_estudiante_actual = self.dict_estudiantes_inv.get(nombre_estudiante, 0)
            self._cargar_carreras(nombre_estudiante)
            self._filtrar_actividades_detalladas()
            self._mostrar_actividades_filtradas()
            # Mostrar estadísticas
            self._mostrar_estadisticas(self.vista_actual)
            logger.debug(
                f"Estudiante seleccionado: {nombre_estudiante} (ID: {self.id_estudiante_actual})"
            )
        except Exception as e:
            logger.error(f"Error al cambiar estudiante: {e}", exc_info=True)

    def _on_change_carrera(self, event=None) -> None:
        """Maneja el evento cuando el usuario selecciona una carrera.

        Args:
            event: Evento de Tkinter (requerido por bind)
        """
        try:
            nombre_carrera = self.var_carrera.get()
            self.id_carrera_actual = self.dict_carreras_inv.get(nombre_carrera, 0)
            self._cargar_asignaturas(nombre_carrera)
            self._filtrar_actividades_detalladas()
            self._mostrar_actividades_filtradas()
            # Mostrar estadísticas actualizadas
            self._mostrar_estadisticas(self.vista_actual)
            logger.debug(f"Carrera seleccionada: {nombre_carrera} (ID: {self.id_carrera_actual})")
        except Exception as e:
            logger.error(f"Error al cambiar carrera: {e}", exc_info=True)

    def _on_change_asignatura(self, event=None) -> None:
        """Maneja el evento cuando el usuario selecciona una asignatura.

        Args:
            event: Evento de Tkinter (requerido por bind)
        """
        try:
            nombre_asignatura = self.var_asignatura.get()
            self.id_asignatura_actual = self.dict_asignaturas_inv.get(nombre_asignatura, 0)
            self._filtrar_actividades_detalladas()
            self._mostrar_actividades_filtradas()
            # Mostrar estadísticas actualizadas
            self._mostrar_estadisticas(self.vista_actual)
            logger.debug(
                f"Asignatura seleccionada: {nombre_asignatura} (ID: {self.id_asignatura_actual})"
            )
        except Exception as e:
            logger.error(f"Error al cambiar asignatura: {e}", exc_info=True)

    def _on_change_tipo_actividad(self, event=None) -> None:
        """Maneja el evento cuando el usuario selecciona un tipo de actividad.

        Args:
            event: Evento de Tkinter (requerido por bind)
        """
        try:
            nombre_tipo = self.var_tipo_actividad.get()
            self.id_tipo_actividad_actual = self.dict_tipos_actividad_inv.get(nombre_tipo, 0)
            self._filtrar_actividades_detalladas()
            self._mostrar_actividades_filtradas()
            # Mostrar estadísticas actualizadas
            self._mostrar_estadisticas(self.vista_actual)
            logger.debug(
                f"Tipo de actividad seleccionado: {nombre_tipo} (ID: {self.id_tipo_actividad_actual})"
            )
        except Exception as e:
            logger.error(f"Error al cambiar tipo de actividad: {e}", exc_info=True)

    def _vincular_eventos(self) -> None:
        """Vincula los eventos de los comboboxes a sus respectivos manejadores.

        Eventos vinculados:
        - cbx_estudiantes: <<ComboboxSelected>> -> _on_change_estudiante
        - cbx_carreras: <<ComboboxSelected>> -> _on_change_carrera
        - cbx_asignaturas: <<ComboboxSelected>> -> _on_change_asignatura
        - cbx_tipo_actividades: <<ComboboxSelected>> -> _on_change_tipo_actividad
        """
        try:
            self.cbx_estudiantes.bind('<<ComboboxSelected>>', self._on_change_estudiante)
            self.cbx_carreras.bind('<<ComboboxSelected>>', self._on_change_carrera)
            self.cbx_asignaturas.bind('<<ComboboxSelected>>', self._on_change_asignatura)
            self.cbx_tipo_actividades.bind('<<ComboboxSelected>>', self._on_change_tipo_actividad)
            logger.debug("Eventos vinculados correctamente")
        except Exception as e:
            logger.error(f"Error al vincular eventos: {e}", exc_info=True)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Métodos de Estadísticas
    # └────────────────────────────────────────────────────────────┘

    def _crear_botones_estadisticas(self) -> None:
        """Crea los botones para cambiar entre vistas de estadísticas en el frame inferior."""
        try:
            # Crear frame para botones si no existe
            frame_botones = Frame(self.label_frame_datos)
            frame_botones.pack(fill=X, padx=5, pady=5)

            btn_resumen = Button(
                frame_botones,
                text="📊 Resumen",
                command=lambda: self._mostrar_estadisticas("resumen"),
                bootstyle="info-outline",
            )
            btn_resumen.pack(side=LEFT, padx=2)

            btn_desempeño = Button(
                frame_botones,
                text="📈 Desempeño",
                command=lambda: self._mostrar_estadisticas("desempeño"),
                bootstyle="info-outline",
            )
            btn_desempeño.pack(side=LEFT, padx=2)

            btn_timeline = Button(
                frame_botones,
                text="⏱️ Timeline",
                command=lambda: self._mostrar_estadisticas("timeline"),
                bootstyle="info-outline",
            )
            btn_timeline.pack(side=LEFT, padx=2)

            btn_comparativa = Button(
                frame_botones,
                text="👥 Comparativa",
                command=lambda: self._mostrar_estadisticas("comparativa"),
                bootstyle="info-outline",
            )
            btn_comparativa.pack(side=LEFT, padx=2)

            self.map_widgets['frame_botones_estadisticas'] = frame_botones
            logger.info("Botones de estadísticas creados")
        except Exception as e:
            logger.error(f"Error al crear botones de estadísticas: {e}", exc_info=True)

    def _mostrar_estadisticas(self, tipo_vista: str) -> None:
        """Muestra la vista de estadísticas solicitada.

        Args:
            tipo_vista: Tipo de vista ('resumen', 'desempeño', 'timeline', 'comparativa')
        """
        try:
            # Limpiar label_frame_datos
            for widget in self.label_frame_datos.winfo_children():
                if widget != self.map_widgets.get('frame_botones_estadisticas'):
                    widget.destroy()

            self.vista_actual = tipo_vista

            if tipo_vista == "resumen":
                self._mostrar_resumen_general()
            elif tipo_vista == "desempeño":
                self._mostrar_desempeño()
            elif tipo_vista == "timeline":
                self._mostrar_timeline()
            elif tipo_vista == "comparativa":
                self._mostrar_comparativa()

            logger.info(f"Estadísticas mostradas: {tipo_vista}")
        except Exception as e:
            logger.error(f"Error al mostrar estadísticas: {e}", exc_info=True)

    def _calcular_estadisticas_estudiante(self) -> Dict[str, Any]:
        """Calcula las estadísticas generales del estudiante actual."""
        stats = {
            'total': 0,
            'entregadas': 0,
            'pendientes': 0,
            'en_progreso': 0,
            'vencidas': 0,
            'tasa_entrega': 0.0,
            'promedio_nota': 0.0,
        }

        if not self.lista_actividades_detalladas:
            return stats

        actividades = self.lista_actividades_detalladas
        stats['total'] = len(actividades)

        notas_validas = []

        for act in actividades:
            estado = act.get('actividad_estado', 'pendiente')
            if estado == 'entregada':
                stats['entregadas'] += 1
            elif estado == 'pendiente':
                stats['pendientes'] += 1
            elif estado == 'en_progreso':
                stats['en_progreso'] += 1
            elif estado == 'vencida':
                stats['vencidas'] += 1

            # Recopilar notas válidas
            nota = act.get('nota')
            if nota is not None:
                try:
                    notas_validas.append(float(nota))
                except (ValueError, TypeError):
                    pass

        if stats['total'] > 0:
            stats['tasa_entrega'] = round((stats['entregadas'] / stats['total']) * 100, 1)

        if notas_validas:
            stats['promedio_nota'] = round(sum(notas_validas) / len(notas_validas), 2)

        return stats

    def _mostrar_resumen_general(self) -> None:
        """Muestra un resumen general de actividades del estudiante."""
        try:
            stats = self._calcular_estadisticas_estudiante()

            # Título
            lbl_titulo = Label(
                self.label_frame_datos,
                text="📊 Resumen General",
                font=("Helvetica", 11, "bold"),
                bootstyle="info",
            )
            lbl_titulo.pack(fill=X, padx=5, pady=(5, 3))

            # Frame con estadísticas principales - Layout horizontal
            frame_stats = Frame(self.label_frame_datos)
            frame_stats.pack(fill=BOTH, padx=5, pady=3)

            # Columna 1: Total y Tasa
            frame_col1 = Frame(frame_stats)
            frame_col1.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))

            lbl_total = Label(
                frame_col1,
                text=f"📋 Total: {stats['total']}",
                font=("Helvetica", 9),
            )
            lbl_total.pack(fill=X, pady=1)

            lbl_tasa = Label(
                frame_col1,
                text=f"✅ Entrega: {stats['tasa_entrega']}%",
                font=("Helvetica", 9),
                bootstyle="success",
            )
            lbl_tasa.pack(fill=X, pady=1)

            # Columna 2: Estados
            frame_col2 = Frame(frame_stats)
            frame_col2.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))

            lbl_entregadas = Label(
                frame_col2,
                text=f"✅ Ent: {stats['entregadas']}",
                font=("Helvetica", 9),
                bootstyle="success",
            )
            lbl_entregadas.pack(fill=X, pady=1)

            lbl_pendientes = Label(
                frame_col2,
                text=f"⏳ Pend: {stats['pendientes']}",
                font=("Helvetica", 9),
                bootstyle="warning",
            )
            lbl_pendientes.pack(fill=X, pady=1)

            # Columna 3: Más estados
            frame_col3 = Frame(frame_stats)
            frame_col3.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))

            lbl_en_progreso = Label(
                frame_col3,
                text=f"🔄 Prog: {stats['en_progreso']}",
                font=("Helvetica", 9),
                bootstyle="info",
            )
            lbl_en_progreso.pack(fill=X, pady=1)

            lbl_vencidas = Label(
                frame_col3,
                text=f"❌ Venc: {stats['vencidas']}",
                font=("Helvetica", 9),
                bootstyle="danger",
            )
            lbl_vencidas.pack(fill=X, pady=1)

            # Columna 4: Promedio
            frame_col4 = Frame(frame_stats)
            frame_col4.pack(side=LEFT, fill=BOTH, expand=True)

            if stats['promedio_nota'] > 0:
                lbl_promedio = Label(
                    frame_col4,
                    text=f"⭐ Prom: {stats['promedio_nota']}",
                    font=("Helvetica", 9),
                    bootstyle="primary",
                )
                lbl_promedio.pack(fill=X, pady=1)

        except Exception as e:
            logger.error(f"Error al mostrar resumen general: {e}", exc_info=True)

    def _mostrar_desempeño(self) -> None:
        """Muestra métricas de desempeño del estudiante."""
        try:
            # Título
            lbl_titulo = Label(
                self.label_frame_datos,
                text="📈 Desempeño",
                font=("Helvetica", 11, "bold"),
                bootstyle="info",
            )
            lbl_titulo.pack(fill=X, padx=5, pady=(5, 3))

            # Frame de desempeño - Layout horizontal
            frame_desemp = Frame(self.label_frame_datos)
            frame_desemp.pack(fill=BOTH, padx=5, pady=3)

            stats = self._calcular_estadisticas_estudiante()
            velocidad_promedio = self._calcular_velocidad_promedio()

            # Columna 1: Velocidad y Promedio
            frame_col1 = Frame(frame_desemp)
            frame_col1.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))

            lbl_velocidad = Label(
                frame_col1,
                text=f"⚡ Velocidad: {velocidad_promedio}d",
                font=("Helvetica", 9),
            )
            lbl_velocidad.pack(fill=X, pady=1)

            lbl_promedio = Label(
                frame_col1,
                text=f"⭐ Prom: {stats['promedio_nota']}",
                font=("Helvetica", 9),
                bootstyle="primary",
            )
            lbl_promedio.pack(fill=X, pady=1)

            # Columna 2: Clasificación y Prioridades
            frame_col2 = Frame(frame_desemp)
            frame_col2.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))

            clasificacion = self._obtener_clasificacion_desempeño(stats)
            lbl_clasificacion = Label(
                frame_col2,
                text=f"🏆 {clasificacion}",
                font=("Helvetica", 9, "bold"),
                bootstyle="info",
            )
            lbl_clasificacion.pack(fill=X, pady=1)

            prioridades = self._contar_por_prioridad()
            lbl_prior_text = Label(
                frame_col2,
                text=f"🔴{prioridades['Alta']} 🟡{prioridades['Media']} 🟢{prioridades['Baja']}",
                font=("Helvetica", 9),
            )
            lbl_prior_text.pack(fill=X, pady=1)

        except Exception as e:
            logger.error(f"Error al mostrar desempeño: {e}", exc_info=True)

    def _mostrar_timeline(self) -> None:
        """Muestra información de cronograma y fechas."""
        try:
            # Título
            lbl_titulo = Label(
                self.label_frame_datos,
                text="⏱️ Timeline",
                font=("Helvetica", 11, "bold"),
                bootstyle="info",
            )
            lbl_titulo.pack(fill=X, padx=5, pady=(5, 3))

            frame_timeline = Frame(self.label_frame_datos)
            frame_timeline.pack(fill=BOTH, padx=5, pady=3)

            # Actividades próximas a vencer
            proximas = self._obtener_actividades_proximas_vencer()
            duracion_promedio = self._calcular_duracion_promedio()

            # Columna 1: Próximas a vencer (máximo 2)
            frame_col1 = Frame(frame_timeline)
            frame_col1.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))

            lbl_proximas = Label(
                frame_col1,
                text=f"⏰ Próximas: {len(proximas)}",
                font=("Helvetica", 9, "bold"),
                bootstyle="warning",
            )
            lbl_proximas.pack(fill=X, pady=1)

            for act in proximas[:2]:
                titulo = act.get('titulo', 'Sin título')[:20]  # Limitar a 20 caracteres
                dias = act.get('dias_desde_fin', 0)
                lbl_act = Label(
                    frame_col1,
                    text=f"• {titulo}..({dias}d)",
                    font=("Helvetica", 8),
                )
                lbl_act.pack(fill=X, pady=0)

            # Columna 2: Duración promedio
            frame_col2 = Frame(frame_timeline)
            frame_col2.pack(side=LEFT, fill=BOTH, expand=True)

            lbl_duracion = Label(
                frame_col2,
                text=f"📊 Dur.Prom: {duracion_promedio}d",
                font=("Helvetica", 9),
            )
            lbl_duracion.pack(fill=X, pady=1)

        except Exception as e:
            logger.error(f"Error al mostrar timeline: {e}", exc_info=True)

    def _mostrar_comparativa(self) -> None:
        """Muestra información comparativa con otros estudiantes."""
        try:
            # Título
            lbl_titulo = Label(
                self.label_frame_datos,
                text="👥 Comparativa",
                font=("Helvetica", 11, "bold"),
                bootstyle="info",
            )
            lbl_titulo.pack(fill=X, padx=5, pady=(5, 3))

            frame_comparativa = Frame(self.label_frame_datos)
            frame_comparativa.pack(fill=BOTH, padx=5, pady=3)

            stats = self._calcular_estadisticas_estudiante()
            promedio_clase = self._obtener_promedio_clase()
            diferencia = stats['promedio_nota'] - promedio_clase

            # Columna 1: Notas
            frame_col1 = Frame(frame_comparativa)
            frame_col1.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))

            lbl_tu_nota = Label(
                frame_col1,
                text=f"📊 Tu Nota: {stats['promedio_nota']}",
                font=("Helvetica", 9),
            )
            lbl_tu_nota.pack(fill=X, pady=1)

            lbl_clase = Label(
                frame_col1,
                text=f"👥 Prom.Clase: {promedio_clase}",
                font=("Helvetica", 9),
            )
            lbl_clase.pack(fill=X, pady=1)

            # Columna 2: Diferencia y Posición
            frame_col2 = Frame(frame_comparativa)
            frame_col2.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))

            if diferencia > 0:
                lbl_diff = Label(
                    frame_col2,
                    text=f"✅ +{diferencia:.2f}pts",
                    font=("Helvetica", 9),
                    bootstyle="success",
                )
            elif diferencia < 0:
                lbl_diff = Label(
                    frame_col2,
                    text=f"⚠️ {diferencia:.2f}pts",
                    font=("Helvetica", 9),
                    bootstyle="warning",
                )
            else:
                lbl_diff = Label(
                    frame_col2,
                    text=f"➖ Igual",
                    font=("Helvetica", 9),
                    bootstyle="info",
                )
            lbl_diff.pack(fill=X, pady=1)

            # Columna 3: Posición
            frame_col3 = Frame(frame_comparativa)
            frame_col3.pack(side=LEFT, fill=BOTH, expand=True)

            posicion = self._estimar_posicion_clase(stats['promedio_nota'])
            lbl_posicion = Label(
                frame_col3,
                text=f"🎯 {posicion}",
                font=("Helvetica", 9),
            )
            lbl_posicion.pack(fill=X, pady=1)

        except Exception as e:
            logger.error(f"Error al mostrar comparativa: {e}", exc_info=True)

    def _calcular_velocidad_promedio(self) -> float:
        """Calcula la velocidad promedio de entrega en días."""
        try:
            entregadas = [
                a
                for a in self.lista_actividades_detalladas
                if a.get('actividad_estado') == 'entregada'
            ]

            if not entregadas:
                return 0.0

            velocidades = []
            for act in entregadas:
                dias = act.get('dias_desde_fin', 0)
                velocidades.append(dias)

            return round(sum(velocidades) / len(velocidades), 1) if velocidades else 0.0
        except Exception as e:
            logger.error(f"Error al calcular velocidad promedio: {e}", exc_info=True)
            return 0.0

    def _calcular_duracion_promedio(self) -> float:
        """Calcula la duración promedio de las actividades."""
        try:
            duraciones = []
            for act in self.lista_actividades_detalladas:
                dias = act.get('dias_duracion', 0)
                if dias:
                    duraciones.append(dias)

            return round(sum(duraciones) / len(duraciones), 1) if duraciones else 0.0
        except Exception as e:
            logger.error(f"Error al calcular duración promedio: {e}", exc_info=True)
            return 0.0

    def _contar_por_prioridad(self) -> Dict[str, int]:
        """Cuenta actividades por nivel de prioridad."""
        conteos = {'Alta': 0, 'Media': 0, 'Baja': 0}

        for act in self.lista_actividades_detalladas:
            prioridad = act.get('prioridad', 0)
            if prioridad == 2:
                conteos['Alta'] += 1
            elif prioridad == 1:
                conteos['Media'] += 1
            else:
                conteos['Baja'] += 1

        return conteos

    def _obtener_actividades_proximas_vencer(self, limite_dias: int = 7) -> List[Dict[str, Any]]:
        """Obtiene actividades próximas a vencer (dentro de X días)."""
        proximas = []

        for act in self.lista_actividades_detalladas:
            dias = act.get('dias_desde_fin', 0)
            if 0 <= dias <= limite_dias:
                proximas.append(act)

        return sorted(proximas, key=lambda x: x.get('dias_desde_fin', 0))

    def _obtener_clasificacion_desempeño(self, stats: Dict[str, Any]) -> str:
        """Obtiene la clasificación de desempeño del estudiante."""
        if stats['promedio_nota'] >= 9:
            return "Excelente 🌟"
        elif stats['promedio_nota'] >= 8:
            return "Muy Bueno 👍"
        elif stats['promedio_nota'] >= 7:
            return "Bueno ✅"
        elif stats['promedio_nota'] >= 6:
            return "Satisfactorio ⚠️"
        else:
            return "Necesita Mejorar 📚"

    def _obtener_promedio_clase(self) -> float:
        """Obtiene el promedio aproximado de la clase (simulado)."""
        try:
            # Aquí se podría hacer una consulta a la BD para obtener el promedio real
            # Por ahora retorna un valor simulado
            return 7.5
        except Exception as e:
            logger.error(f"Error al obtener promedio de clase: {e}", exc_info=True)
            return 7.5

    def _estimar_posicion_clase(self, nota_estudiante: float) -> str:
        """Estima la posición del estudiante en la clase."""
        promedio_clase = self._obtener_promedio_clase()

        if nota_estudiante > promedio_clase + 1:
            return "Top 25% 🏆"
        elif nota_estudiante > promedio_clase:
            return "Top 50% 📈"
        elif nota_estudiante == promedio_clase:
            return "Promedio 📊"
        else:
            return "Bajo promedio 📚"
