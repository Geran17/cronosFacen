from modelos.dtos.estudiante_actividad_dto import EstudianteActividadDTO
from modelos.daos.base_dao import DAO
from typing import Optional, List, Dict, Any
from sqlite3 import Error
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class EstudianteActividadDAO(DAO):
    def __init__(self, ruta_db=None):
        super().__init__(ruta_db)

        # creamos la tabla
        self.crear_tabla()

    def crear_tabla(self, sql: Optional[str] = None) -> bool:
        """
        Crea la tabla de estudiante-actividad en la base de datos si no existe.

        Args:
            sql (Optional[str]): SQL personalizado para crear la tabla.
                Si es None, usa el SQL por defecto.

        Returns:
            bool: True si la tabla se creó o ya existe, False en caso de error.
        """
        if sql is None:
            sql = """CREATE TABLE IF NOT EXISTS estudiante_actividad (
                id_estudiante INTEGER NOT NULL,
                id_actividad INTEGER NOT NULL,
                estado TEXT CHECK (
                    estado IN ('pendiente', 'en_progreso', 'entregada', 'vencida')
                ),
                fecha_entrega TEXT,
                PRIMARY KEY (id_estudiante, id_actividad),
                FOREIGN KEY (id_estudiante)
                    REFERENCES estudiante(id_estudiante)
                    ON DELETE CASCADE,
                FOREIGN KEY (id_actividad)
                    REFERENCES actividad(id_actividad)
                    ON DELETE CASCADE
            )"""

        return self.ejecutar_actualizacion(sql=sql, params=())

    def insertar(self, dto: EstudianteActividadDTO) -> bool:
        """
        Inserta un nuevo registro de estudiante-actividad en la base de datos.

        Args:
            dto (EstudianteActividadDTO): DTO con los datos a insertar.

        Returns:
            bool: True si se insertó correctamente, False en caso de error.
        """
        sql = """INSERT INTO estudiante_actividad (id_estudiante, id_actividad, estado, fecha_entrega)
                 VALUES (?, ?, ?, ?)"""
        params = (dto.id_estudiante, dto.id_actividad, dto.estado, dto.fecha_entrega)

        resultado = self.ejecutar_insertar(sql, params)
        return resultado is not None

    def eliminar(self, dto: EstudianteActividadDTO) -> bool:
        """
        Elimina un registro de estudiante-actividad de la base de datos.

        Args:
            dto (EstudianteActividadDTO): DTO con los IDs a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario.
        """
        sql = "DELETE FROM estudiante_actividad WHERE id_estudiante = ? AND id_actividad = ?"
        params = (dto.id_estudiante, dto.id_actividad)

        return self.ejecutar_actualizacion(sql, params)

    def instanciar(self, dto: EstudianteActividadDTO) -> bool:
        """
        Consulta un registro de estudiante-actividad de la base de datos y carga los datos en el DTO.

        Args:
            dto (EstudianteActividadDTO): DTO con los IDs a consultar. Se llena con los datos obtenidos.

        Returns:
            bool: True si se encontró y cargó el registro, False en caso contrario.
        """
        if (
            dto.id_estudiante != 0
            and dto.id_estudiante is not None
            and dto.id_actividad != 0
            and dto.id_actividad is not None
        ):
            sql = "SELECT * FROM estudiante_actividad WHERE id_estudiante = ? AND id_actividad = ?"
            params = (dto.id_estudiante, dto.id_actividad)
            lista_data = self.ejecutar_consulta(sql, params)
            if lista_data:
                data = lista_data[0]
                dto.set_data(data=data)
                return True
            return False
        else:
            logger.warning("IDs de estudiante-actividad no válidos para instanciar")
            return False

    def existe(self, dto: EstudianteActividadDTO) -> bool:
        """
        Verifica si existe un registro de estudiante-actividad con los IDs especificados.

        Args:
            dto (EstudianteActividadDTO): DTO con los IDs a verificar.

        Returns:
            bool: True si existe el registro, False en caso contrario.
        """
        if (
            dto.id_estudiante != 0
            and dto.id_estudiante is not None
            and dto.id_actividad != 0
            and dto.id_actividad is not None
        ):
            sql = "SELECT COUNT(*) as count FROM estudiante_actividad WHERE id_estudiante = ? AND id_actividad = ?"
            params = (dto.id_estudiante, dto.id_actividad)

            try:
                resultado = self.ejecutar_consulta(sql, params)
                return len(resultado) > 0 and resultado[0].get('count', 0) > 0
            except Error as ex:
                logger.error(f"Error al verificar existencia: {ex}", exc_info=True)
                return False
        else:
            logger.warning("IDs de estudiante-actividad no válidos para verificar existencia")
            return False

    def actualizar(self, dto: EstudianteActividadDTO) -> bool:
        """
        Actualiza un registro de estudiante-actividad en la base de datos.

        Args:
            dto (EstudianteActividadDTO): DTO con los datos a actualizar.

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario.
        """
        sql = """UPDATE estudiante_actividad 
                 SET estado = ?, fecha_entrega = ?
                 WHERE id_estudiante = ? AND id_actividad = ?"""
        params = (
            dto.estado,
            dto.fecha_entrega,
            dto.id_estudiante,
            dto.id_actividad,
        )

        return self.ejecutar_actualizacion(sql, params)
