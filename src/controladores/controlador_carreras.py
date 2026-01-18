from ttkbootstrap import Combobox, StringVar
from typing import Dict, Any, List
from tkinter.messagebox import showwarning
from modelos.daos.estudiante_dao import EstudianteDAO
from modelos.daos.carrera_dao import CarreraDAO
from modelos.daos.asignatura_dao import AsignaturaDAO
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class ControladorCarreras:
    """Controlador para el Frame de Carreras.

    Maneja la carga y visualización de:
    - Estudiantes disponibles
    - Carreras asociadas a cada estudiante
    """

    def __init__(self, map_vars: Dict[str, Any], map_widgets: Dict[str, Any]):
        self.map_vars: Dict[str, Any] = map_vars
        self.map_widgets: Dict[str, Any] = map_widgets

        # Diccionarios para estudiantes
        self.dict_estudiantes: Dict[int, str] = {}  # id -> "Nombre - Correo"
        self.dict_estudiantes_inv: Dict[str, int] = {}  # "Nombre - Correo" -> id

        # Diccionarios para carreras
        self.dict_carreras: Dict[int, str] = {}  # id -> "Nombre - Plan"
        self.dict_carreras_inv: Dict[str, int] = {}  # "Nombre - Plan" -> id

        # IDs actuales
        self.id_estudiante_actual: int = 0
        self.id_carrera_actual: int = 0

        # Cargar datos iniciales
        self._cargar_vars()
        self._cargar_widgets()
        self._cargar_estudiantes()
        # Vincular eventos
        self._vincular_eventos()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Métodos de Carga
    # └────────────────────────────────────────────────────────────┘

    def _cargar_vars(self) -> None:
        """Carga las variables StringVar desde el diccionario de variables."""
        try:
            self.var_estudiante: StringVar = self.map_vars.get('var_estudiante')
            self.var_carrera: StringVar = self.map_vars.get('var_carrera')
            logger.info("Variables cargadas correctamente")
        except Exception as e:
            logger.error(f"Error al cargar variables: {e}")
            showwarning("Error", f"Error al cargar variables: {e}")

    def _cargar_widgets(self) -> None:
        """Carga los widgets combobox desde el diccionario de widgets."""
        try:
            self.cbx_estudiante: Combobox = self.map_widgets.get('cbx_estudiante')
            self.cbx_carrera: Combobox = self.map_widgets.get('cbx_carrera')
            logger.info("Widgets cargados correctamente")
        except Exception as e:
            logger.error(f"Error al cargar widgets: {e}")
            showwarning("Error", f"Error al cargar widgets: {e}")

    def _cargar_estudiantes(self) -> None:
        """Carga todos los estudiantes de la base de datos.

        Obtiene la lista de estudiantes y la muestra en el combobox.
        El formato mostrado es: "Nombre - Correo"
        """
        try:
            estudiante_dao = EstudianteDAO(ruta_db=None)
            sql = "SELECT id_estudiante, nombre, correo FROM estudiante ORDER BY nombre"
            params = ()
            lista_estudiantes = estudiante_dao.ejecutar_consulta(sql=sql, params=params)

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
            self.cbx_estudiante.config(values=lista)
            if lista:
                self.cbx_estudiante.current(0)
                # Cargar carreras del primer estudiante
                self._on_change_estudiante()

        except Exception as e:
            logger.error(f"Error al cargar estudiantes: {e}", exc_info=True)
            self.cbx_estudiante.config(values=[])

    def _cargar_carreras(self, nombre_estudiante: str) -> None:
        """Carga las carreras del estudiante seleccionado.

        Args:
            nombre_estudiante (str): Nombre del estudiante en formato "Nombre - Correo"
        """
        try:
            # Limpiar diccionarios
            self.dict_carreras.clear()
            self.dict_carreras_inv.clear()
            lista_aux = []

            if not nombre_estudiante:
                self.cbx_carrera.config(values=lista_aux)
                return

            # Obtener ID del estudiante
            id_estudiante = self.dict_estudiantes_inv.get(nombre_estudiante, 0)
            if id_estudiante == 0:
                logger.warning(f"Estudiante no encontrado: {nombre_estudiante}")
                self.cbx_carrera.config(values=lista_aux)
                return

            # Consultar carreras del estudiante
            sql = """SELECT ec.id_carrera, ec.estado, c.nombre, c.plan
                     FROM estudiante_carrera ec
                     JOIN carrera c ON ec.id_carrera = c.id_carrera
                     WHERE ec.id_estudiante = ?
                     ORDER BY ec.es_carrera_principal DESC, c.nombre"""
            params = (id_estudiante,)
            dao_carrera = CarreraDAO(ruta_db=None)
            consulta = dao_carrera.ejecutar_consulta(sql=sql, params=params)

            if consulta:
                for dato in consulta:
                    id_carrera = dato['id_carrera']
                    nombre_carrera = dato['nombre']
                    plan = dato['plan']
                    estado = dato['estado']

                    # Formato: "✓ Nombre (plan) - activa" o "✗ Nombre (plan) - inactiva"
                    icon = "✓" if estado == "activa" else "✗"
                    label = f"{icon} {nombre_carrera} ({plan}) - {estado}"
                    lista_aux.append(label)

                    # Mapeo bidireccional
                    self.dict_carreras[id_carrera] = label
                    self.dict_carreras_inv[label] = id_carrera

                logger.info(
                    f"Se cargaron {len(lista_aux)} carreras para el estudiante {nombre_estudiante}"
                )
            else:
                logger.warning(f"El estudiante {nombre_estudiante} no tiene carreras asociadas")

            # Actualizar combobox
            self.cbx_carrera.config(values=lista_aux)
            if lista_aux:
                self.cbx_carrera.current(0)

        except Exception as e:
            logger.error(f"Error al cargar carreras: {e}", exc_info=True)
            self.cbx_carrera.config(values=[])

    def _vincular_eventos(self) -> None:
        """Vincula los eventos de los comboboxes y botones a sus respectivos manejadores."""
        try:
            self.cbx_estudiante.bind('<<ComboboxSelected>>', self._on_change_estudiante)
            self.cbx_carrera.bind('<<ComboboxSelected>>', self._on_change_carrera)

            # Vincular botón Refrescar
            btn_refrescar = self.map_widgets.get('btn_refrescar')
            if btn_refrescar:
                btn_refrescar.config(command=self._refrescar_datos)

            logger.debug("Eventos vinculados correctamente")
        except Exception as e:
            logger.error(f"Error al vincular eventos: {e}", exc_info=True)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Manejadores de Eventos
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
            logger.debug(f"Carrera seleccionada: {nombre_carrera} (ID: {self.id_carrera_actual})")

            # Cargar asignaturas de la carrera seleccionada
            self._cargar_asignaturas()
        except Exception as e:
            logger.error(f"Error al cambiar carrera: {e}", exc_info=True)

    def _refrescar_datos(self) -> None:
        """Recarga los datos de asignaturas para la carrera y estudiante actual.

        Se ejecuta cuando el usuario hace clic en el botón Refrescar.
        Vuelve a cargar todas las asignaturas sin cambiar la selección actual.
        """
        try:
            if not self.id_estudiante_actual or not self.id_carrera_actual:
                logger.warning("ID de estudiante o carrera no definido. No se puede refrescar.")
                return

            logger.info(
                f"Refrescando datos para estudiante {self.id_estudiante_actual}, carrera {self.id_carrera_actual}"
            )
            self._cargar_asignaturas()
            logger.info("Datos refrescados exitosamente")
        except Exception as e:
            logger.error(f"Error al refrescar datos: {e}", exc_info=True)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Métodos para Asignaturas
    # └────────────────────────────────────────────────────────────┘

    def _cargar_asignaturas(self) -> None:
        """Carga TODAS las asignaturas de la carrera agrupadas por semestre.

        Muestra el plan de estudios completo con todas las asignaturas,
        indicando cuáles ha cursado el estudiante y cuáles aún están disponibles.
        Además, calcula qué prerequisitos ya están completados.
        """
        try:
            if not self.id_estudiante_actual or not self.id_carrera_actual:
                logger.warning("ID de estudiante o carrera no definido")
                return

            asignatura_dao = AsignaturaDAO(ruta_db=None)

            # 1. Obtener TODAS las asignaturas de la carrera con sus prerequisitos
            sql_todas_asignaturas = """SELECT 
                a.id_asignatura,
                a.nombre,
                a.codigo,
                a.semestre,
                a.tipo,
                a.creditos,
                COALESCE(aprereq.prerequisitos, '-') AS prerequisitos
            FROM asignatura a
            LEFT JOIN vw_asignatura_prerequisitos aprereq ON a.id_asignatura = aprereq.id_asignatura
            WHERE a.id_carrera = ?
            ORDER BY a.semestre, a.nombre"""
            params_asignaturas = (self.id_carrera_actual,)
            todas_asignaturas = asignatura_dao.ejecutar_consulta(
                sql=sql_todas_asignaturas, params=params_asignaturas
            )

            # 2. Obtener asignaturas cursadas por el estudiante con datos completos
            sql_estudiante = """SELECT * FROM vw_asignaturas_estudiante_completo
                     WHERE id_estudiante = ? AND id_carrera = ?
                     ORDER BY semestre, nombre_asignatura"""
            params_estudiante = (self.id_estudiante_actual, self.id_carrera_actual)
            asignaturas_cursadas = asignatura_dao.ejecutar_consulta(
                sql=sql_estudiante, params=params_estudiante
            )

            # 3. Crear diccionarios para acceso rápido
            dict_cursadas = {}
            dict_asignaturas_por_nombre = {}

            for asig in asignaturas_cursadas:
                dict_cursadas[asig['id_asignatura']] = asig
                # Mantener el nombre de la asignatura con su estado (importante para prerequisitos)
                dict_asignaturas_por_nombre[asig['nombre_asignatura']] = asig

            # NOTA: No sobrescribir dict_asignaturas_por_nombre con todas las asignaturas
            # porque necesitamos mantener la información de ESTADO de las cursadas
            # Solo agregar las no cursadas si no existen
            for asig in todas_asignaturas:
                # Solo agregar si no está ya en el diccionario (es decir, no fue cursada)
                if asig['nombre'] not in dict_asignaturas_por_nombre:
                    dict_asignaturas_por_nombre[asig['nombre']] = asig

            # 4. Agrupar TODAS las asignaturas por semestre y combinar info del estudiante
            estructura_completa = {}
            for asig in todas_asignaturas:
                semestre = asig['semestre']
                id_asignatura = asig['id_asignatura']

                if semestre not in estructura_completa:
                    estructura_completa[semestre] = []

                # Combinar datos: base de la asignatura + info del estudiante si existe
                if id_asignatura in dict_cursadas:
                    # Asignatura cursada: usar datos completos
                    asig_combinada = dict_cursadas[id_asignatura]
                else:
                    # Asignatura no cursada: usar solo datos básicos
                    asig_combinada = {
                        'nombre_asignatura': asig['nombre'],
                        'codigo': asig['codigo'],
                        'semestre': asig['semestre'],
                        'tipo': asig['tipo'],
                        'creditos': asig['creditos'],
                        'id_asignatura': id_asignatura,
                        'estado': 'disponible',
                        'nota_final': None,
                        'cantidad_ejes_tematicos': 0,
                        'cantidad_actividades': 0,
                        'prerequisitos': asig.get('prerequisitos', '-'),
                        'progreso_actividades': 0.0,
                    }

                # 5. Calcular progreso de prerequisitos
                prereq_str = asig_combinada.get('prerequisitos', '-')
                if prereq_str and prereq_str != '-':
                    # Parsear prerequisitos (pueden ser separados por comas)
                    prereqs_list = [p.strip() for p in prereq_str.split(',')]
                    prereqs_completados = 0

                    for prereq_nombre in prereqs_list:
                        # Buscar si el prerequisito está en asignaturas cursadas
                        if prereq_nombre in dict_asignaturas_por_nombre:
                            prereq_data = dict_asignaturas_por_nombre[prereq_nombre]
                            # Verificar si está completada o aprobada
                            if prereq_data.get('estado') in ['completada', 'aprobada']:
                                prereqs_completados += 1

                    total_prereqs = len(prereqs_list)
                    progreso_prereqs = (
                        (prereqs_completados / total_prereqs * 100) if total_prereqs > 0 else 0.0
                    )

                    # Agregar campos de progreso de prerequisitos
                    asig_combinada['prerequisitos_completados'] = prereqs_completados
                    asig_combinada['prerequisitos_totales'] = total_prereqs
                    asig_combinada['progreso_prerequisitos'] = progreso_prereqs

                    # Log para debug
                    if 'Probabilidad' in asig_combinada.get('nombre_asignatura', ''):
                        logger.debug(
                            f"DEBUG: {asig_combinada['nombre_asignatura']} - "
                            f"Prerequisitos: {prereq_str} - "
                            f"Completados: {prereqs_completados}/{total_prereqs} ({progreso_prereqs:.0f}%)"
                        )
                else:
                    # Sin prerequisitos
                    asig_combinada['prerequisitos_completados'] = 0
                    asig_combinada['prerequisitos_totales'] = 0
                    asig_combinada['progreso_prerequisitos'] = 0.0

                estructura_completa[semestre].append(asig_combinada)

            # Mostrar en el frame
            frame_carreras = self.map_widgets.get('frame_carreras')
            if frame_carreras:
                frame_carreras.mostrar_asignaturas_reales(estructura_completa)

            total_asignaturas = len(todas_asignaturas)
            total_cursadas = len(asignaturas_cursadas)
            logger.info(
                f"Se cargaron {total_asignaturas} asignaturas del plan de estudios "
                f"({total_cursadas} cursadas) en {len(estructura_completa)} semestres para "
                f"estudiante {self.id_estudiante_actual}, carrera {self.id_carrera_actual}"
            )

        except Exception as e:
            logger.error(f"Error al cargar asignaturas: {e}", exc_info=True)
            # Mostrar frame vacío en caso de error
            frame_carreras = self.map_widgets.get('frame_carreras')
            if frame_carreras:
                frame_carreras.limpiar_asignaturas()

    def _agrupar_asignaturas_por_semestre(self, asignaturas: List[Dict]) -> Dict[int, List[Dict]]:
        """Agrupa las asignaturas por semestre.

        Args:
            asignaturas (List[Dict]): Lista de asignaturas con datos de la vista

        Returns:
            Dict[int, List[Dict]]: Diccionario {semestre: [asignaturas]}
        """
        resultado = {}

        for asignatura in asignaturas:
            semestre = asignatura.get('semestre', 0)

            if semestre not in resultado:
                resultado[semestre] = []

            resultado[semestre].append(asignatura)

        # Ordenar por semestre
        return dict(sorted(resultado.items()))

    def obtener_progreso_semestre(self, semestre: int) -> float:
        """Calcula el porcentaje de progreso promedio de un semestre.

        Args:
            semestre (int): Número del semestre

        Returns:
            float: Porcentaje de progreso (0-100)
        """
        try:
            # Esta información debería venir de las asignaturas
            # Por ahora retornamos un valor placeholder
            # En una implementación real, se calcularía del promedio de nota_final
            return 0.0
        except Exception as e:
            logger.error(f"Error al obtener progreso del semestre: {e}", exc_info=True)
            return 0.0
