from modelos.dtos.estudiante_dto import EstudianteDTO
from modelos.daos.base_dao import DAO
from typing import Optional, List, Dict, Any
from sqlite3 import Error
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class EstudianteDAO(DAO):
    def __init__(self, ruta_db=None):
        super().__init__(ruta_db)

        # creamos la tabla
        self.crear_tabla()

    def crear_tabla(self, sql: Optional[str] = None) -> bool:
        """
        Crea la tabla de estudiante en la base de datos si no existe.

        Args:
            sql (Optional[str]): SQL personalizado para crear la tabla.
                Si es None, usa el SQL por defecto.

        Returns:
            bool: True si la tabla se creó o ya existe, False en caso de error.
        """
        if sql is None:
            sql = """CREATE TABLE IF NOT EXISTS estudiante (
                id_estudiante INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                correo TEXT NOT NULL UNIQUE
            )"""

        return self.ejecutar_actualizacion(sql=sql, params=())

    def insertar(self, dto: EstudianteDTO) -> Optional[int]:
        """
        Inserta un nuevo registro de estudiante en la base de datos.

        Args:
            dto (EstudianteDTO): DTO con los datos del estudiante a insertar.

        Returns:
            Optional[int]: ID del registro insertado o None si hay error.

        Note:
            Para asignar carreras al estudiante, usar EstudianteCarreraService después de insertar.
        """
        sql = """INSERT INTO estudiante (nombre, correo)
                 VALUES (?, ?)"""
        params = (dto.nombre, dto.correo)

        return self.ejecutar_insertar(sql, params)

    def actualizar(self, dto: EstudianteDTO) -> bool:
        """
        Actualiza un registro de estudiante en la base de datos.

        Args:
            dto (EstudianteDTO): DTO con los datos del estudiante a actualizar.
                Debe incluir id_estudiante.

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario.

        Note:
            Para actualizar carreras, usar EstudianteCarreraService.
        """
        sql = """UPDATE estudiante 
                 SET nombre = ?, correo = ?
                 WHERE id_estudiante = ?"""
        params = (dto.nombre, dto.correo, dto.id_estudiante)

        return self.ejecutar_actualizacion(sql, params)

    def eliminar(self, dto: EstudianteDTO) -> bool:
        """
        Elimina un registro de estudiante de la base de datos por su ID.

        Args:
            dto (EstudianteDTO): DTO con el id_estudiante a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario.
        """
        sql = "DELETE FROM estudiante WHERE id_estudiante = ?"
        params = (dto.id_estudiante,)

        return self.ejecutar_actualizacion(sql, params)

    def instanciar(self, dto: EstudianteDTO) -> bool:
        """
        Consulta un registro de estudiante de la base de datos y carga los datos en el DTO.

        Args:
            dto (EstudianteDTO): DTO con el id_estudiante a consultar. Se llena con los datos obtenidos.

        Returns:
            bool: True si se encontró y cargó el estudiante, False en caso contrario.
        """
        if dto.id_estudiante != 0 and dto.id_estudiante is not None:
            sql = "SELECT * FROM estudiante WHERE id_estudiante = ?"
            params = (dto.id_estudiante,)
            lista_data = self.ejecutar_consulta(sql, params)
            if lista_data:
                data = lista_data[0]
                dto.set_data(data=data)
                return True
            return False
        else:
            logger.warning("ID de estudiante no válido para instanciar")
            return False

    def existe(self, dto: EstudianteDTO) -> bool:
        """
        Verifica si existe un estudiante con el ID especificado.

        Args:
            dto (EstudianteDTO): DTO con el id_estudiante a verificar.

        Returns:
            bool: True si existe el estudiante, False en caso contrario.
        """
        if dto.id_estudiante != 0 and dto.id_estudiante is not None:
            sql = "SELECT COUNT(*) as count FROM estudiante WHERE id_estudiante = ?"
            params = (dto.id_estudiante,)

            try:
                resultado = self.ejecutar_consulta(sql, params)
                return len(resultado) > 0 and resultado[0].get('count', 0) > 0
            except Error as ex:
                logger.error(f"Error al verificar existencia: {ex}", exc_info=True)
                return False
        else:
            logger.warning("ID de estudiante no válido para verificar existencia")
            return False
