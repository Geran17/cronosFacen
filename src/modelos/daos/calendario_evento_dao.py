from modelos.dtos.calendario_evento_dto import CalendarioEventoDTO
from modelos.daos.base_dao import DAO
from typing import Optional, List, Dict, Any
from sqlite3 import Error
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class CalendarioEventoDAO(DAO):
    def __init__(self, ruta_db=None):
        super().__init__(ruta_db)

        # creamos la tabla
        self.crear_tabla()

    def crear_tabla(self, sql: Optional[str] = None) -> bool:
        """
        Crea la tabla de evento del calendario en la base de datos si no existe.

        Args:
            sql (Optional[str]): SQL personalizado para crear la tabla.
                Si es None, usa el SQL por defecto.

        Returns:
            bool: True si la tabla se creó o ya existe, False en caso de error.
        """
        if sql is None:
            sql = """CREATE TABLE IF NOT EXISTS calendario_evento (
                id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                tipo TEXT NOT NULL,
                fecha_inicio TEXT NOT NULL,
                fecha_fin TEXT NOT NULL,
                afecta_actividades INTEGER DEFAULT 0
            )"""

        return self.ejecutar_actualizacion(sql=sql, params=())

    def insertar(self, dto: CalendarioEventoDTO) -> Optional[int]:
        """
        Inserta un nuevo registro de evento del calendario en la base de datos.

        Args:
            dto (CalendarioEventoDTO): DTO con los datos del evento a insertar.

        Returns:
            Optional[int]: ID del registro insertado o None si hay error.
        """
        sql = """INSERT INTO calendario_evento (titulo, tipo, fecha_inicio, fecha_fin, afecta_actividades)
                 VALUES (?, ?, ?, ?, ?)"""
        params = (
            dto.titulo,
            dto.tipo,
            dto.fecha_inicio,
            dto.fecha_fin,
            dto.afecta_actividades,
        )

        return self.ejecutar_insertar(sql, params)

    def actualizar(self, dto: CalendarioEventoDTO) -> bool:
        """
        Actualiza un registro de evento del calendario en la base de datos.

        Args:
            dto (CalendarioEventoDTO): DTO con los datos del evento a actualizar.

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario.
        """
        sql = """UPDATE calendario_evento 
                 SET titulo = ?, tipo = ?, fecha_inicio = ?, fecha_fin = ?, afecta_actividades = ?
                 WHERE id_evento = ?"""
        params = (
            dto.titulo,
            dto.tipo,
            dto.fecha_inicio,
            dto.fecha_fin,
            dto.afecta_actividades,
            dto.id_evento,
        )

        return self.ejecutar_actualizacion(sql, params)

    def eliminar(self, dto: CalendarioEventoDTO) -> bool:
        """
        Elimina un registro de evento del calendario de la base de datos por su ID.

        Args:
            dto (CalendarioEventoDTO): DTO con el id_evento a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario.
        """
        sql = "DELETE FROM calendario_evento WHERE id_evento = ?"
        params = (dto.id_evento,)

        return self.ejecutar_actualizacion(sql, params)

    def instanciar(self, dto: CalendarioEventoDTO) -> bool:
        """
        Consulta un registro de evento del calendario de la base de datos y carga los datos en el DTO.

        Args:
            dto (CalendarioEventoDTO): DTO con el id_evento a consultar. Se llena con los datos obtenidos.

        Returns:
            bool: True si se encontró y cargó el evento, False en caso contrario.
        """
        if dto.id_evento != 0 and dto.id_evento is not None:
            sql = "SELECT * FROM calendario_evento WHERE id_evento = ?"
            params = (dto.id_evento,)
            lista_data = self.ejecutar_consulta(sql, params)
            if lista_data:
                data = lista_data[0]
                dto.set_data(data=data)
                return True
            return False
        else:
            logger.warning("ID de evento no válido para instanciar")
            return False

    def existe(self, dto: CalendarioEventoDTO) -> bool:
        """
        Verifica si existe un evento del calendario con el ID especificado.

        Args:
            dto (CalendarioEventoDTO): DTO con el id_evento a verificar.

        Returns:
            bool: True si existe el evento, False en caso contrario.
        """
        if dto.id_evento != 0 and dto.id_evento is not None:
            sql = "SELECT COUNT(*) as count FROM calendario_evento WHERE id_evento = ?"
            params = (dto.id_evento,)

            try:
                resultado = self.ejecutar_consulta(sql, params)
                return len(resultado) > 0 and resultado[0].get('count', 0) > 0
            except Error as ex:
                logger.error(f"Error al verificar existencia: {ex}", exc_info=True)
                return False
        else:
            logger.warning("ID de evento no válido para verificar existencia")
            return False
