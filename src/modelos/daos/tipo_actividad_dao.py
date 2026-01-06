from modelos.dtos.tipo_actividad_dto import TipoActividadDTO
from modelos.daos.base_dao import DAO
from typing import Optional, List, Dict, Any
from sqlite3 import Error
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class TipoActividadDAO(DAO):
    def __init__(self, ruta_db=None):
        super().__init__(ruta_db)

        # creamos la tabla
        self.crear_tabla()

    def crear_tabla(self, sql: Optional[str] = None) -> bool:
        """
        Crea la tabla de tipo de actividad en la base de datos si no existe.

        Args:
            sql (Optional[str]): SQL personalizado para crear la tabla.
                Si es None, usa el SQL por defecto.

        Returns:
            bool: True si la tabla se creó o ya existe, False en caso de error.
        """
        if sql is None:
            sql = """CREATE TABLE IF NOT EXISTS tipo_actividad (
                id_tipo_actividad INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                siglas TEXT NOT NULL UNIQUE,
                descripcion TEXT
            )"""

        return self.ejecutar_actualizacion(sql=sql, params=())

    def insertar(self, dto: TipoActividadDTO) -> Optional[int]:
        """
        Inserta un nuevo registro de tipo de actividad en la base de datos.

        Args:
            dto (TipoActividadDTO): DTO con los datos del tipo de actividad a insertar.

        Returns:
            Optional[int]: ID del registro insertado o None si hay error.
        """
        sql = """INSERT INTO tipo_actividad (nombre, siglas, descripcion)
                 VALUES (?, ?, ?)"""
        params = (dto.nombre, dto.siglas, dto.descripcion)

        return self.ejecutar_insertar(sql, params)

    def eliminar(self, dto: TipoActividadDTO) -> bool:
        """
        Elimina un registro de tipo de actividad de la base de datos por su ID.

        Args:
            dto (TipoActividadDTO): DTO con el id_tipo_actividad a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario.
        """
        sql = "DELETE FROM tipo_actividad WHERE id_tipo_actividad = ?"
        params = (dto.id_tipo_actividad,)

        return self.ejecutar_actualizacion(sql, params)

    def instanciar(self, dto: TipoActividadDTO) -> bool:
        """
        Consulta un registro de tipo de actividad de la base de datos y carga los datos en el DTO.

        Args:
            dto (TipoActividadDTO): DTO con el id_tipo_actividad a consultar. Se llena con los datos obtenidos.

        Returns:
            bool: True si se encontró y cargó el tipo de actividad, False en caso contrario.
        """
        if dto.id_tipo_actividad != 0 and dto.id_tipo_actividad is not None:
            sql = "SELECT * FROM tipo_actividad WHERE id_tipo_actividad = ?"
            params = (dto.id_tipo_actividad,)
            lista_data = self.ejecutar_consulta(sql, params)
            if lista_data:
                data = lista_data[0]
                dto.set_data(data=data)
                return True
            return False
        else:
            logger.warning("ID de tipo de actividad no válido para instanciar")
            return False

    def existe(self, dto: TipoActividadDTO) -> bool:
        """
        Verifica si existe un tipo de actividad con el ID especificado.

        Args:
            dto (TipoActividadDTO): DTO con el id_tipo_actividad a verificar.

        Returns:
            bool: True si existe el tipo de actividad, False en caso contrario.
        """
        if dto.id_tipo_actividad != 0 and dto.id_tipo_actividad is not None:
            sql = "SELECT COUNT(*) as count FROM tipo_actividad WHERE id_tipo_actividad = ?"
            params = (dto.id_tipo_actividad,)

            try:
                resultado = self.ejecutar_consulta(sql, params)
                return len(resultado) > 0 and resultado[0].get('count', 0) > 0
            except Error as ex:
                logger.error(f"Error al verificar existencia: {ex}", exc_info=True)
                return False
        else:
            logger.warning("ID de tipo de actividad no válido para verificar existencia")
            return False
