from modelos.dtos.asignatura_dto import AsignaturaDTO
from modelos.daos.base_dao import DAO
from typing import Optional, List, Dict, Any
from sqlite3 import Error
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class AsignaturaDAO(DAO):
    def __init__(self, ruta_db=None):
        super().__init__(ruta_db)

        # creamos la tabla
        self.crear_tabla()

    def crear_tabla(self, sql: Optional[str] = None) -> bool:
        """
        Crea la tabla de asignatura en la base de datos si no existe.

        Args:
            sql (Optional[str]): SQL personalizado para crear la tabla.
                Si es None, usa el SQL por defecto.

        Returns:
            bool: True si la tabla se creó o ya existe, False en caso de error.
        """
        if sql is None:
            sql = """CREATE TABLE IF NOT EXISTS asignatura (
                id_asignatura INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT NOT NULL UNIQUE,
                nombre TEXT NOT NULL,
                creditos INTEGER NOT NULL,
                horas_semanales INTEGER,
                tipo TEXT CHECK (tipo IN ('obligatoria', 'electiva')),
                semestre INTEGER,
                id_carrera INTEGER NOT NULL,
                FOREIGN KEY (id_carrera)
                    REFERENCES carrera(id_carrera)
                    ON DELETE CASCADE
            )"""

        return self.ejecutar_actualizacion(sql=sql, params=())

    def insertar(self, dto: AsignaturaDTO) -> Optional[int]:
        """
        Inserta un nuevo registro de asignatura en la base de datos.

        Args:
            dto (AsignaturaDTO): DTO con los datos de la asignatura a insertar.

        Returns:
            Optional[int]: ID del registro insertado o None si hay error.
        """
        sql = """INSERT INTO asignatura (codigo, nombre, creditos, horas_semanales, tipo, semestre, id_carrera)
                 VALUES (?, ?, ?, ?, ?, ?, ?)"""
        params = (
            dto.codigo,
            dto.nombre,
            dto.creditos,
            dto.horas_semanales,
            dto.tipo,
            dto.semestre,
            dto.id_carrera,
        )

        return self.ejecutar_insertar(sql, params)

    def actualizar(self, dto: AsignaturaDTO) -> bool:
        """
        Actualiza un registro de asignatura en la base de datos.

        Args:
            dto (AsignaturaDTO): DTO con los datos de la asignatura a actualizar.
                Debe incluir id_asignatura.

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario.
        """
        sql = """UPDATE asignatura 
                 SET codigo = ?, nombre = ?, creditos = ?, horas_semanales = ?, tipo = ?, semestre = ?, id_carrera = ?
                 WHERE id_asignatura = ?"""
        params = (
            dto.codigo,
            dto.nombre,
            dto.creditos,
            dto.horas_semanales,
            dto.tipo,
            dto.semestre,
            dto.id_carrera,
            dto.id_asignatura,
        )

        return self.ejecutar_actualizacion(sql, params)

    def eliminar(self, dto: AsignaturaDTO) -> bool:
        """
        Elimina un registro de asignatura de la base de datos por su ID.

        Args:
            dto (AsignaturaDTO): DTO con el id_asignatura a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario.
        """
        sql = "DELETE FROM asignatura WHERE id_asignatura = ?"
        params = (dto.id_asignatura,)

        return self.ejecutar_actualizacion(sql, params)

    def instanciar(self, dto: AsignaturaDTO) -> bool:
        """
        Consulta un registro de asignatura de la base de datos y carga los datos en el DTO.

        Args:
            dto (AsignaturaDTO): DTO con el id_asignatura a consultar. Se llena con los datos obtenidos.

        Returns:
            bool: True si se encontró y cargó la asignatura, False en caso contrario.
        """
        if dto.id_asignatura != 0 and dto.id_asignatura is not None:
            sql = "SELECT * FROM asignatura WHERE id_asignatura = ?"
            params = (dto.id_asignatura,)
            lista_data = self.ejecutar_consulta(sql, params)
            if lista_data:
                data = lista_data[0]
                dto.set_data(data=data)
                return True
            return False
        else:
            logger.warning("ID de asignatura no válido para instanciar")
            return False

    def existe(self, dto: AsignaturaDTO) -> bool:
        """
        Verifica si existe una asignatura con el ID especificado.

        Args:
            dto (AsignaturaDTO): DTO con el id_asignatura a verificar.

        Returns:
            bool: True si existe la asignatura, False en caso contrario.
        """
        if dto.id_asignatura != 0 and dto.id_asignatura is not None:
            sql = "SELECT COUNT(*) as count FROM asignatura WHERE id_asignatura = ?"
            params = (dto.id_asignatura,)

            try:
                resultado = self.ejecutar_consulta(sql, params)
                return len(resultado) > 0 and resultado[0].get('count', 0) > 0
            except Error as ex:
                logger.error(f"Error al verificar existencia: {ex}", exc_info=True)
                return False
        else:
            logger.warning("ID de asignatura no válido para verificar existencia")
            return False

    def obtener_por_id(self, id_asignatura: int) -> Optional[AsignaturaDTO]:
        """
        Obtiene una asignatura por su ID.

        Args:
            id_asignatura (int): ID de la asignatura.

        Returns:
            Optional[AsignaturaDTO]: DTO de la asignatura o None si no existe.
        """
        dto = AsignaturaDTO(id_asignatura=id_asignatura)
        if self.instanciar(dto):
            return dto
        return None
