from modelos.dtos.actividad_dto import ActividadDTO
from modelos.daos.base_dao import DAO
from typing import Optional, List, Dict, Any
from sqlite3 import Error
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class ActividadDAO(DAO):
    def __init__(self, ruta_db=None):
        super().__init__(ruta_db)

        # creamos la tabla
        self.crear_tabla()

    def crear_tabla(self, sql: Optional[str] = None) -> bool:
        """
        Crea la tabla de actividad en la base de datos si no existe.

        Args:
            sql (Optional[str]): SQL personalizado para crear la tabla.
                Si es None, usa el SQL por defecto.

        Returns:
            bool: True si la tabla se creó o ya existe, False en caso de error.
        """
        if sql is None:
            sql = """CREATE TABLE IF NOT EXISTS actividad (
                id_actividad INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descripcion TEXT,
                fecha_inicio TEXT NOT NULL,
                fecha_fin TEXT NOT NULL,
                id_eje INTEGER NOT NULL,
                id_tipo_actividad INTEGER NOT NULL,
                FOREIGN KEY (id_eje)
                    REFERENCES eje_tematico(id_eje)
                    ON DELETE CASCADE,
                FOREIGN KEY (id_tipo_actividad)
                    REFERENCES tipo_actividad(id_tipo_actividad)
            )"""

        return self.ejecutar_actualizacion(sql=sql, params=())

    def insertar(self, dto: ActividadDTO) -> Optional[int]:
        """
        Inserta un nuevo registro de actividad en la base de datos.

        Args:
            dto (ActividadDTO): DTO con los datos de la actividad a insertar.

        Returns:
            Optional[int]: ID del registro insertado o None si hay error.
        """
        sql = """INSERT INTO actividad (titulo, descripcion, fecha_inicio, fecha_fin, id_eje, id_tipo_actividad)
                 VALUES (?, ?, ?, ?, ?, ?)"""
        params = (
            dto.titulo,
            dto.descripcion,
            dto.fecha_inicio,
            dto.fecha_fin,
            dto.id_eje,
            dto.id_tipo_actividad,
        )

        return self.ejecutar_insertar(sql, params)

    def eliminar(self, dto: ActividadDTO) -> bool:
        """
        Elimina un registro de actividad de la base de datos por su ID.

        Args:
            dto (ActividadDTO): DTO con el id_actividad a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario.
        """
        sql = "DELETE FROM actividad WHERE id_actividad = ?"
        params = (dto.id_actividad,)

        return self.ejecutar_actualizacion(sql, params)

    def instanciar(self, dto: ActividadDTO) -> bool:
        """
        Consulta un registro de actividad de la base de datos y carga los datos en el DTO.

        Args:
            dto (ActividadDTO): DTO con el id_actividad a consultar. Se llena con los datos obtenidos.

        Returns:
            bool: True si se encontró y cargó la actividad, False en caso contrario.
        """
        if dto.id_actividad != 0 and dto.id_actividad is not None:
            sql = "SELECT * FROM actividad WHERE id_actividad = ?"
            params = (dto.id_actividad,)
            lista_data = self.ejecutar_consulta(sql, params)
            if lista_data:
                data = lista_data[0]
                dto.set_data(data=data)
                return True
            return False
        else:
            logger.warning("ID de actividad no válido para instanciar")
            return False

    def existe(self, dto: ActividadDTO) -> bool:
        """
        Verifica si existe una actividad con el ID especificado.

        Args:
            dto (ActividadDTO): DTO con el id_actividad a verificar.

        Returns:
            bool: True si existe la actividad, False en caso contrario.
        """
        if dto.id_actividad != 0 and dto.id_actividad is not None:
            sql = "SELECT COUNT(*) as count FROM actividad WHERE id_actividad = ?"
            params = (dto.id_actividad,)

            try:
                resultado = self.ejecutar_consulta(sql, params)
                return len(resultado) > 0 and resultado[0].get('count', 0) > 0
            except Error as ex:
                logger.error(f"Error al verificar existencia: {ex}", exc_info=True)
                return False
        else:
            logger.warning("ID de actividad no válido para verificar existencia")
            return False
