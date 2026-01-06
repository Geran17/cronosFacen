from modelos.dtos.prerequisito_dto import PrerrequisitoDTO
from modelos.daos.base_dao import DAO
from typing import Optional, List, Dict, Any
from sqlite3 import Error
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class PrerrequisitoDAO(DAO):
    def __init__(self, ruta_db=None):
        super().__init__(ruta_db)

        # creamos la tabla
        self.crear_tabla()

    def crear_tabla(self, sql: Optional[str] = None) -> bool:
        """
        Crea la tabla de prerequisito en la base de datos si no existe.

        Args:
            sql (Optional[str]): SQL personalizado para crear la tabla.
                Si es None, usa el SQL por defecto.

        Returns:
            bool: True si la tabla se creó o ya existe, False en caso de error.
        """
        if sql is None:
            sql = """CREATE TABLE IF NOT EXISTS prerrequisito (
                id_asignatura INTEGER NOT NULL,
                id_asignatura_prerrequisito INTEGER NOT NULL,
                PRIMARY KEY (id_asignatura, id_asignatura_prerrequisito),
                FOREIGN KEY (id_asignatura)
                    REFERENCES asignatura(id_asignatura)
                    ON DELETE CASCADE,
                FOREIGN KEY (id_asignatura_prerrequisito)
                    REFERENCES asignatura(id_asignatura)
                    ON DELETE CASCADE,
                CHECK (id_asignatura <> id_asignatura_prerrequisito)
            )"""

        return self.ejecutar_actualizacion(sql=sql, params=())

    def insertar(self, dto: PrerrequisitoDTO) -> bool:
        """
        Inserta un nuevo registro de prerequisito en la base de datos.

        Args:
            dto (PrerrequisitoDTO): DTO con los datos del prerequisito a insertar.

        Returns:
            bool: True si se insertó correctamente, False en caso de error.
        """
        sql = """INSERT INTO prerrequisito (id_asignatura, id_asignatura_prerrequisito)
                 VALUES (?, ?)"""
        params = (dto.id_asignatura, dto.id_asignatura_prerrequisito)

        resultado = self.ejecutar_insertar(sql, params)
        return resultado is not None

    def eliminar(self, dto: PrerrequisitoDTO) -> bool:
        """
        Elimina un registro de prerequisito de la base de datos.

        Args:
            dto (PrerrequisitoDTO): DTO con los IDs del prerequisito a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario.
        """
        sql = (
            "DELETE FROM prerrequisito WHERE id_asignatura = ? AND id_asignatura_prerrequisito = ?"
        )
        params = (dto.id_asignatura, dto.id_asignatura_prerrequisito)

        return self.ejecutar_actualizacion(sql, params)

    def instanciar(self, dto: PrerrequisitoDTO) -> bool:
        """
        Consulta un registro de prerequisito de la base de datos y carga los datos en el DTO.

        Args:
            dto (PrerrequisitoDTO): DTO con los IDs a consultar. Se llena con los datos obtenidos.

        Returns:
            bool: True si se encontró y cargó el prerequisito, False en caso contrario.
        """
        if (
            dto.id_asignatura != 0
            and dto.id_asignatura is not None
            and dto.id_asignatura_prerrequisito != 0
            and dto.id_asignatura_prerrequisito is not None
        ):
            sql = "SELECT * FROM prerrequisito WHERE id_asignatura = ? AND id_asignatura_prerrequisito = ?"
            params = (dto.id_asignatura, dto.id_asignatura_prerrequisito)
            lista_data = self.ejecutar_consulta(sql, params)
            if lista_data:
                data = lista_data[0]
                dto.set_data(data=data)
                return True
            return False
        else:
            logger.warning("IDs de asignatura no válidos para instanciar")
            return False

    def existe(self, dto: PrerrequisitoDTO) -> bool:
        """
        Verifica si existe un prerequisito con los IDs especificados.

        Args:
            dto (PrerrequisitoDTO): DTO con los IDs a verificar.

        Returns:
            bool: True si existe el prerequisito, False en caso contrario.
        """
        if (
            dto.id_asignatura != 0
            and dto.id_asignatura is not None
            and dto.id_asignatura_prerrequisito != 0
            and dto.id_asignatura_prerrequisito is not None
        ):
            sql = "SELECT COUNT(*) as count FROM prerrequisito WHERE id_asignatura = ? AND id_asignatura_prerrequisito = ?"
            params = (dto.id_asignatura, dto.id_asignatura_prerrequisito)

            try:
                resultado = self.ejecutar_consulta(sql, params)
                return len(resultado) > 0 and resultado[0].get('count', 0) > 0
            except Error as ex:
                logger.error(f"Error al verificar existencia: {ex}", exc_info=True)
                return False
        else:
            logger.warning("IDs de asignatura no válidos para verificar existencia")
            return False
