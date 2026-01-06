from modelos.dtos.eje_tematico_dto import EjeTematicoDTO
from modelos.daos.base_dao import DAO
from typing import Optional, List, Dict, Any
from sqlite3 import Error
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class EjeTematicoDAO(DAO):
    def __init__(self, ruta_db=None):
        super().__init__(ruta_db)

        # creamos la tabla
        self.crear_tabla()

    def crear_tabla(self, sql: Optional[str] = None) -> bool:
        """
        Crea la tabla de eje temático en la base de datos si no existe.

        Args:
            sql (Optional[str]): SQL personalizado para crear la tabla.
                Si es None, usa el SQL por defecto.

        Returns:
            bool: True si la tabla se creó o ya existe, False en caso de error.
        """
        if sql is None:
            sql = """CREATE TABLE IF NOT EXISTS eje_tematico (
                id_eje INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                orden INTEGER,
                id_asignatura INTEGER NOT NULL,
                FOREIGN KEY (id_asignatura)
                    REFERENCES asignatura(id_asignatura)
                    ON DELETE CASCADE
            )"""

        return self.ejecutar_actualizacion(sql=sql, params=())

    def insertar(self, dto: EjeTematicoDTO) -> Optional[int]:
        """
        Inserta un nuevo registro de eje temático en la base de datos.

        Args:
            dto (EjeTematicoDTO): DTO con los datos del eje temático a insertar.

        Returns:
            Optional[int]: ID del registro insertado o None si hay error.
        """
        sql = """INSERT INTO eje_tematico (nombre, orden, id_asignatura)
                 VALUES (?, ?, ?)"""
        params = (dto.nombre, dto.orden, dto.id_asignatura)

        return self.ejecutar_insertar(sql, params)

    def actualizar(self, dto: EjeTematicoDTO) -> bool:
        """
        Actualiza un registro de eje temático en la base de datos.

        Args:
            dto (EjeTematicoDTO): DTO con los datos del eje temático a actualizar.

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario.
        """
        sql = """UPDATE eje_tematico 
                 SET nombre = ?, orden = ?, id_asignatura = ?
                 WHERE id_eje = ?"""
        params = (dto.nombre, dto.orden, dto.id_asignatura, dto.id_eje)

        return self.ejecutar_actualizacion(sql, params)

    def eliminar(self, dto: EjeTematicoDTO) -> bool:
        """
        Elimina un registro de eje temático de la base de datos por su ID.

        Args:
            dto (EjeTematicoDTO): DTO con el id_eje a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario.
        """
        sql = "DELETE FROM eje_tematico WHERE id_eje = ?"
        params = (dto.id_eje,)

        return self.ejecutar_actualizacion(sql, params)

    def instanciar(self, dto: EjeTematicoDTO) -> bool:
        """
        Consulta un registro de eje temático de la base de datos y carga los datos en el DTO.

        Args:
            dto (EjeTematicoDTO): DTO con el id_eje a consultar. Se llena con los datos obtenidos.

        Returns:
            bool: True si se encontró y cargó el eje temático, False en caso contrario.
        """
        if dto.id_eje != 0 and dto.id_eje is not None:
            sql = "SELECT * FROM eje_tematico WHERE id_eje = ?"
            params = (dto.id_eje,)
            lista_data = self.ejecutar_consulta(sql, params)
            if lista_data:
                data = lista_data[0]
                dto.set_data(data=data)
                return True
            return False
        else:
            logger.warning("ID de eje temático no válido para instanciar")
            return False

    def existe(self, dto: EjeTematicoDTO) -> bool:
        """
        Verifica si existe un eje temático con el ID especificado.

        Args:
            dto (EjeTematicoDTO): DTO con el id_eje a verificar.

        Returns:
            bool: True si existe el eje temático, False en caso contrario.
        """
        if dto.id_eje != 0 and dto.id_eje is not None:
            sql = "SELECT COUNT(*) as count FROM eje_tematico WHERE id_eje = ?"
            params = (dto.id_eje,)

            try:
                resultado = self.ejecutar_consulta(sql, params)
                return len(resultado) > 0 and resultado[0].get('count', 0) > 0
            except Error as ex:
                logger.error(f"Error al verificar existencia: {ex}", exc_info=True)
                return False
        else:
            logger.warning("ID de eje temático no válido para verificar existencia")
            return False

    def obtener_por_id(self, id_eje: int) -> Optional[EjeTematicoDTO]:
        """
        Obtiene un eje temático por su ID.

        Args:
            id_eje (int): ID del eje temático.

        Returns:
            Optional[EjeTematicoDTO]: DTO del eje temático o None si no existe.
        """
        dto = EjeTematicoDTO(id_eje=id_eje)
        if self.instanciar(dto):
            return dto
        return None
