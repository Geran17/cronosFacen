from modelos.daos.base_dao import DAO
from modelos.dtos.consulta_dto import (
    EventosUnificadosDTO,
)
from typing import Optional, List, Dict, Any
from sqlite3 import Error
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class ConsultaDAO(DAO):
    """
    DAO para ejecutar consultas complejas del MVP de Organización Académica.

    Este DAO proporciona métodos read-only para obtener información agregada
    sobre progreso académico, actividades pendientes y calendarios.
    """

    def __init__(self, ruta_db=None):
        super().__init__(ruta_db)

    def crear_tabla(self, sql: Optional[str] = None) -> bool:
        """
        No aplica para ConsultaDAO ya que solo realiza consultas read-only.

        Returns:
            bool: Siempre retorna True.
        """
        logger.info("ConsultaDAO no requiere creación de tablas (read-only)")
        return True

    def insertar(self, dto=None) -> Optional[int]:
        """
        No aplica para ConsultaDAO (read-only).

        Returns:
            None: Siempre retorna None.
        """
        logger.warning("ConsultaDAO no soporta inserciones (read-only)")
        return None

    def eliminar(self, dto=None) -> bool:
        """
        No aplica para ConsultaDAO (read-only).

        Returns:
            bool: Siempre retorna False.
        """
        logger.warning("ConsultaDAO no soporta eliminaciones (read-only)")
        return False

    def instanciar(self, dto=None) -> bool:
        """
        No aplica para ConsultaDAO (read-only).

        Returns:
            bool: Siempre retorna False.
        """
        logger.warning("ConsultaDAO no soporta instanciación directa")
        return False

    def existe(self, dto=None) -> bool:
        """
        No aplica para ConsultaDAO (read-only).

        Returns:
            bool: Siempre retorna False.
        """
        logger.warning("ConsultaDAO no soporta verificación de existencia")
        return False


class EventosUnificadosDAO(DAO):
    """
    DAO para consultar la vista vw_eventos_unificados.

    Proporciona acceso a eventos unificados (Actividades + Eventos de Calendario)
    con filtros por fecha, tipo y mes.
    """

    def __init__(self, ruta_db=None):
        super().__init__(ruta_db)

    def crear_tabla(self, sql: Optional[str] = None) -> bool:
        """
        No aplica para EventosUnificadosDAO (solo consulta la vista, read-only).

        Returns:
            bool: Siempre retorna True.
        """
        logger.info("EventosUnificadosDAO no requiere creación de tablas (read-only)")
        return True

    def insertar(self, dto=None) -> Optional[int]:
        """
        No aplica para EventosUnificadosDAO (read-only).

        Returns:
            None: Siempre retorna None.
        """
        logger.warning("EventosUnificadosDAO no soporta inserciones (read-only)")
        return None

    def eliminar(self, dto=None) -> bool:
        """
        No aplica para EventosUnificadosDAO (read-only).

        Returns:
            bool: Siempre retorna False.
        """
        logger.warning("EventosUnificadosDAO no soporta eliminaciones (read-only)")
        return False

    def instanciar(self, dto=None) -> bool:
        """
        No aplica para EventosUnificadosDAO (read-only).

        Returns:
            bool: Siempre retorna False.
        """
        logger.warning("EventosUnificadosDAO no soporta instanciación directa")
        return False

    def existe(self, dto=None) -> bool:
        """
        No aplica para EventosUnificadosDAO (read-only).

        Returns:
            bool: Siempre retorna False.
        """
        logger.warning("EventosUnificadosDAO no soporta verificación de existencia")
        return False

    # ┌────────────────────────────────────────────────────────────┐
    # │ Métodos de Consulta (Read-Only)
    # └────────────────────────────────────────────────────────────┘

    def obtener_todos(self) -> List[EventosUnificadosDTO]:
        """
        Obtiene todos los eventos unificados ordenados por fecha.

        Returns:
            List[EventosUnificadosDTO]: Lista de eventos unificados.
        """
        try:
            with self.get_conexion() as con:
                cursor = con.cursor()

                sql = """
                SELECT tipo_evento, id_evento, titulo, descripcion, 
                       fecha_inicio, fecha_fin, tipo_actividad, observaciones,
                       carrera, id_carrera, asignatura, id_asignatura
                FROM vw_eventos_unificados
                ORDER BY fecha_inicio ASC;
                """

                cursor.execute(sql)
                rows = cursor.fetchall()

                eventos = [EventosUnificadosDTO.from_row(row) for row in rows]
                logger.debug(f"Obtenidos {len(eventos)} eventos unificados")
                return eventos

        except Error as ex:
            logger.error(f"Error al obtener eventos unificados: {ex}")
            return []

    def obtener_por_rango_fechas(
        self, fecha_inicio: str, fecha_fin: str
    ) -> List[EventosUnificadosDTO]:
        """
        Obtiene eventos dentro de un rango de fechas.

        Args:
            fecha_inicio (str): Fecha inicial en formato YYYY-MM-DD
            fecha_fin (str): Fecha final en formato YYYY-MM-DD

        Returns:
            List[EventosUnificadosDTO]: Lista de eventos en el rango.
        """
        try:
            with self.get_conexion() as con:
                cursor = con.cursor()

                sql = """
                SELECT tipo_evento, id_evento, titulo, descripcion,
                       fecha_inicio, fecha_fin, tipo_actividad, observaciones,
                       carrera, id_carrera, asignatura, id_asignatura
                FROM vw_eventos_unificados
                WHERE fecha_inicio >= ? AND fecha_fin <= ?
                ORDER BY fecha_inicio ASC;
                """

                cursor.execute(sql, (fecha_inicio, fecha_fin))
                rows = cursor.fetchall()

                eventos = [EventosUnificadosDTO.from_row(row) for row in rows]
                logger.debug(f"Obtenidos {len(eventos)} eventos entre {fecha_inicio} y {fecha_fin}")
                return eventos

        except Error as ex:
            logger.error(f"Error al obtener eventos por rango: {ex}")
            return []

    def obtener_por_tipo(self, tipo_evento: str) -> List[EventosUnificadosDTO]:
        """
        Obtiene eventos de un tipo específico.

        Args:
            tipo_evento (str): 'Actividad' o 'Evento Calendario'

        Returns:
            List[EventosUnificadosDTO]: Lista de eventos del tipo especificado.
        """
        try:
            with self.get_conexion() as con:
                cursor = con.cursor()

                sql = """
                SELECT tipo_evento, id_evento, titulo, descripcion,
                       fecha_inicio, fecha_fin, tipo_actividad, observaciones,
                       carrera, id_carrera, asignatura, id_asignatura
                FROM vw_eventos_unificados
                WHERE tipo_evento = ?
                ORDER BY fecha_inicio ASC;
                """

                cursor.execute(sql, (tipo_evento,))
                rows = cursor.fetchall()

                eventos = [EventosUnificadosDTO.from_row(row) for row in rows]
                logger.debug(f"Obtenidos {len(eventos)} eventos de tipo '{tipo_evento}'")
                return eventos

        except Error as ex:
            logger.error(f"Error al obtener eventos por tipo: {ex}")
            return []

    def obtener_por_mes(self, ano: int, mes: int) -> List[EventosUnificadosDTO]:
        """
        Obtiene eventos de un mes específico.

        Args:
            ano (int): Año (ej: 2026)
            mes (int): Mes (1-12)

        Returns:
            List[EventosUnificadosDTO]: Lista de eventos del mes.
        """
        try:
            with self.get_conexion() as con:
                cursor = con.cursor()

                # Construir fechas de inicio y fin del mes
                fecha_inicio = f"{ano:04d}-{mes:02d}-01"
                if mes == 12:
                    fecha_fin = f"{ano + 1:04d}-01-01"
                else:
                    fecha_fin = f"{ano:04d}-{mes + 1:02d}-01"

                sql = """
                SELECT tipo_evento, id_evento, titulo, descripcion,
                       fecha_inicio, fecha_fin, tipo_actividad, observaciones,
                       carrera, id_carrera, asignatura, id_asignatura
                FROM vw_eventos_unificados
                WHERE fecha_inicio >= ? AND fecha_inicio < ?
                ORDER BY fecha_inicio ASC;
                """

                cursor.execute(sql, (fecha_inicio, fecha_fin))
                rows = cursor.fetchall()

                eventos = [EventosUnificadosDTO.from_row(row) for row in rows]
                logger.debug(f"Obtenidos {len(eventos)} eventos para {ano}-{mes:02d}")
                return eventos

        except Error as ex:
            logger.error(f"Error al obtener eventos por mes: {ex}")
            return []

    def obtener_actividades(self) -> List[EventosUnificadosDTO]:
        """
        Obtiene solo las actividades.

        Returns:
            List[EventosUnificadosDTO]: Lista de actividades.
        """
        return self.obtener_por_tipo('Actividad')

    def obtener_eventos_calendario(self) -> List[EventosUnificadosDTO]:
        """
        Obtiene solo los eventos de calendario.

        Returns:
            List[EventosUnificadosDTO]: Lista de eventos de calendario.
        """
        return self.obtener_por_tipo('Evento Calendario')

    def obtener_eventos_proximos(self, dias: int = 7) -> List[EventosUnificadosDTO]:
        """
        Obtiene eventos de los próximos N días.

        Args:
            dias (int): Número de días a considerar. Por defecto 7.

        Returns:
            List[EventosUnificadosDTO]: Lista de eventos próximos.
        """
        from datetime import datetime, timedelta

        try:
            hoy = datetime.now().date()
            fin = hoy + timedelta(days=dias)

            return self.obtener_por_rango_fechas(str(hoy), str(fin))
        except Exception as ex:
            logger.error(f"Error al obtener eventos próximos: {ex}")
            return []

    def obtener_por_tipo_actividad(self, tipo_actividad: str) -> List[EventosUnificadosDTO]:
        """
        Obtiene eventos de un tipo de actividad específico.

        Args:
            tipo_actividad (str): Tipo de actividad (Quiz, Tarea, Examen, etc.)

        Returns:
            List[EventosUnificadosDTO]: Lista de eventos del tipo especificado.
        """
        try:
            with self.get_conexion() as con:
                cursor = con.cursor()

                sql = """
                SELECT tipo_evento, id_evento, titulo, descripcion,
                       fecha_inicio, fecha_fin, tipo_actividad, observaciones,
                       carrera, id_carrera, asignatura, id_asignatura
                FROM vw_eventos_unificados
                WHERE tipo_actividad = ?
                ORDER BY fecha_inicio ASC;
                """

                cursor.execute(sql, (tipo_actividad,))
                rows = cursor.fetchall()

                eventos = [EventosUnificadosDTO.from_row(row) for row in rows]
                logger.debug(
                    f"Obtenidos {len(eventos)} eventos de tipo actividad '{tipo_actividad}'"
                )
                return eventos

        except Error as ex:
            logger.error(f"Error al obtener eventos por tipo de actividad: {ex}")
            return []

    def obtener_por_id(self, id_evento: int, tipo: str) -> Optional[EventosUnificadosDTO]:
        """
        Obtiene un evento específico por su ID.

        Args:
            id_evento (int): ID del evento
            tipo (str): 'Actividad' o 'Evento Calendario'

        Returns:
            Optional[EventosUnificadosDTO]: El evento si existe, None en caso contrario.
        """
        try:
            with self.get_conexion() as con:
                cursor = con.cursor()

                sql = """
                SELECT tipo_evento, id_evento, titulo, descripcion,
                       fecha_inicio, fecha_fin, tipo_actividad, observaciones,
                       carrera, id_carrera, asignatura, id_asignatura
                FROM vw_eventos_unificados
                WHERE id_evento = ? AND tipo_evento = ?;
                """

                cursor.execute(sql, (id_evento, tipo))
                row = cursor.fetchone()

                if row:
                    return EventosUnificadosDTO.from_row(row)

                logger.debug(f"Evento {tipo}:{id_evento} no encontrado")
                return None

        except Error as ex:
            logger.error(f"Error al obtener evento por ID: {ex}")
            return None
