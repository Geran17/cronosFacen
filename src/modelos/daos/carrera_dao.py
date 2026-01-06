from modelos.dtos.carrera_dto import CarreraDTO
from modelos.daos.base_dao import DAO
from typing import Optional, List, Dict, Any
from sqlite3 import Error
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class CarreraDAO(DAO):
    def __init__(self, ruta_db=None):
        super().__init__(ruta_db)

        # creamos la tabla
        self.crear_tabla()

    def crear_tabla(self, sql: Optional[str] = None) -> bool:
        """
        Crea la tabla de carrera en la base de datos si no existe.

        Args:
            sql (Optional[str]): SQL personalizado para crear la tabla.
                Si es None, usa el SQL por defecto.

        Returns:
            bool: True si la tabla se creó o ya existe, False en caso de error.
        """
        if sql is None:
            sql = """CREATE TABLE IF NOT EXISTS carrera (
                id_carrera INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE,
                nombre TEXT NOT NULL,
                plan TEXT NOT NULL,
                modalidad TEXT NOT NULL,
                creditos_totales INTEGER
            )"""

        return self.ejecutar_actualizacion(sql=sql, params=())

    def insertar(self, dto: CarreraDTO) -> Optional[int]:
        """
        Inserta un nuevo registro de carrera en la base de datos.

        Args:
            dto (CarreraDTO): DTO con los datos de la carrera a insertar.

        Returns:
            Optional[int]: ID del registro insertado o None si hay error.
        """
        sql = """INSERT INTO carrera (codigo, nombre, plan, modalidad, creditos_totales)
                 VALUES (?, ?, ?, ?, ?)"""
        params = (dto.codigo, dto.nombre, dto.plan, dto.modalidad, dto.creditos_totales)

        return self.ejecutar_insertar(sql, params)

    def actualizar(self, dto: CarreraDTO) -> bool:
        """
        Actualiza un registro de carrera en la base de datos.

        Args:
            dto (CarreraDTO): DTO con los datos de la carrera a actualizar.

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario.
        """
        sql = """UPDATE carrera 
                 SET codigo = ?, nombre = ?, plan = ?, modalidad = ?, creditos_totales = ?
                 WHERE id_carrera = ?"""
        params = (
            dto.codigo,
            dto.nombre,
            dto.plan,
            dto.modalidad,
            dto.creditos_totales,
            dto.id_carrera,
        )

        return self.ejecutar_actualizacion(sql, params)

    def eliminar(self, dto: CarreraDTO) -> bool:
        """
        Elimina un registro de carrera de la base de datos por su ID.

        Args:
            id_carrera (int): ID de la carrera a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario.
        """
        sql = "DELETE FROM carrera WHERE id_carrera = ?"
        params = (dto.id_carrera,)

        return self.ejecutar_actualizacion(sql, params)

    def instanciar(self, dto: CarreraDTO) -> bool:
        """
        Consulta un registro de carrera de la base de datos y carga los datos en el DTO.

        Args:
            dto (CarreraDTO): DTO con el id_carrera a consultar. Se llena con los datos obtenidos.

        Returns:
            bool: True si se encontró y cargó la carrera, False en caso contrario.
        """
        if dto.id_carrera != 0 and dto.id_carrera is not None:
            sql = "SELECT * FROM carrera WHERE id_carrera = ?"
            params = (dto.id_carrera,)
            lista_data = self.ejecutar_consulta(sql, params)
            if lista_data:
                data = lista_data[0]
                dto.set_data(data=data)
                return True
            return False
        else:
            logger.warning("ID de carrera no válido para instanciar")
            return False

    def existe(self, dto: CarreraDTO) -> bool:
        """
        Verifica si existe una carrera con el ID especificado.

        Args:
            dto (CarreraDTO): DTO con el id_carrera a verificar.

        Returns:
            bool: True si existe la carrera, False en caso contrario.
        """
        if dto.id_carrera != 0 and dto.id_carrera is not None:
            sql = "SELECT COUNT(*) as count FROM carrera WHERE id_carrera = ?"
            params = (dto.id_carrera,)

            try:
                resultado = self.ejecutar_consulta(sql, params)
                return len(resultado) > 0 and resultado[0].get('count', 0) > 0
            except Error as ex:
                logger.error(f"Error al verificar existencia: {ex}", exc_info=True)
                return False
        else:
            logger.warning("ID de carrera no válido para verificar existencia")
            return False

    def obtener_por_id(self, id_carrera: int) -> Optional[CarreraDTO]:
        """
        Obtiene una carrera por su ID.

        Args:
            id_carrera (int): ID de la carrera.

        Returns:
            Optional[CarreraDTO]: DTO de la carrera o None si no existe.
        """
        dto = CarreraDTO(id_carrera=id_carrera)
        if self.instanciar(dto):
            return dto
        return None
