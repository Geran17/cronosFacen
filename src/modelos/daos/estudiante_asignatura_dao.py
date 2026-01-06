from modelos.dtos.estudiante_asignatura_dto import EstudianteAsignaturaDTO
from modelos.daos.base_dao import DAO
from typing import Optional, List, Dict, Any
from sqlite3 import Error
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class EstudianteAsignaturaDAO(DAO):
    def __init__(self, ruta_db=None):
        super().__init__(ruta_db)

        # creamos la tabla
        self.crear_tabla()

    def crear_tabla(self, sql: Optional[str] = None) -> bool:
        """
        Crea la tabla de estudiante-asignatura en la base de datos si no existe.

        Args:
            sql (Optional[str]): SQL personalizado para crear la tabla.
                Si es None, usa el SQL por defecto.

        Returns:
            bool: True si la tabla se creó o ya existe, False en caso de error.
        """
        if sql is None:
            sql = """CREATE TABLE IF NOT EXISTS estudiante_asignatura (
                id_estudiante INTEGER NOT NULL,
                id_asignatura INTEGER NOT NULL,
                estado TEXT CHECK (
                    estado IN ('no_cursada', 'cursando', 'aprobada', 'reprobada')
                ),
                nota_final REAL,
                periodo TEXT,
                PRIMARY KEY (id_estudiante, id_asignatura),
                FOREIGN KEY (id_estudiante)
                    REFERENCES estudiante(id_estudiante)
                    ON DELETE CASCADE,
                FOREIGN KEY (id_asignatura)
                    REFERENCES asignatura(id_asignatura)
                    ON DELETE CASCADE
            )"""

        return self.ejecutar_actualizacion(sql=sql, params=())

    def insertar(self, dto: EstudianteAsignaturaDTO) -> bool:
        """
        Inserta un nuevo registro de estudiante-asignatura en la base de datos.

        Args:
            dto (EstudianteAsignaturaDTO): DTO con los datos a insertar.

        Returns:
            bool: True si se insertó correctamente, False en caso de error.
        """
        sql = """INSERT INTO estudiante_asignatura (id_estudiante, id_asignatura, estado, nota_final, periodo)
                 VALUES (?, ?, ?, ?, ?)"""
        params = (
            dto.id_estudiante,
            dto.id_asignatura,
            dto.estado,
            dto.nota_final,
            dto.periodo,
        )

        logger.info(f"DAO insertar - SQL: {sql}")
        logger.info(f"DAO insertar - Params: {params}")

        resultado = self.ejecutar_insertar(sql, params)
        resultado_bool = resultado is not None

        logger.info(f"DAO insertar - Resultado: {resultado_bool}")

        return resultado_bool

    def eliminar(self, dto: EstudianteAsignaturaDTO) -> bool:
        """
        Elimina un registro de estudiante-asignatura de la base de datos.

        Args:
            dto (EstudianteAsignaturaDTO): DTO con los IDs a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario.
        """
        sql = "DELETE FROM estudiante_asignatura WHERE id_estudiante = ? AND id_asignatura = ?"
        params = (dto.id_estudiante, dto.id_asignatura)

        return self.ejecutar_actualizacion(sql, params)

    def instanciar(self, dto: EstudianteAsignaturaDTO) -> bool:
        """
        Consulta un registro de estudiante-asignatura de la base de datos y carga los datos en el DTO.

        Args:
            dto (EstudianteAsignaturaDTO): DTO con los IDs a consultar. Se llena con los datos obtenidos.

        Returns:
            bool: True si se encontró y cargó el registro, False en caso contrario.
        """
        if (
            dto.id_estudiante != 0
            and dto.id_estudiante is not None
            and dto.id_asignatura != 0
            and dto.id_asignatura is not None
        ):
            sql = (
                "SELECT * FROM estudiante_asignatura WHERE id_estudiante = ? AND id_asignatura = ?"
            )
            params = (dto.id_estudiante, dto.id_asignatura)
            lista_data = self.ejecutar_consulta(sql, params)
            if lista_data:
                data = lista_data[0]
                dto.set_data(data=data)
                return True
            return False
        else:
            logger.warning("IDs de estudiante-asignatura no válidos para instanciar")
            return False

    def existe(self, dto: EstudianteAsignaturaDTO) -> bool:
        """
        Verifica si existe un registro de estudiante-asignatura con los IDs especificados.

        Args:
            dto (EstudianteAsignaturaDTO): DTO con los IDs a verificar.

        Returns:
            bool: True si existe el registro, False en caso contrario.
        """
        if (
            dto.id_estudiante != 0
            and dto.id_estudiante is not None
            and dto.id_asignatura != 0
            and dto.id_asignatura is not None
        ):
            sql = "SELECT COUNT(*) as count FROM estudiante_asignatura WHERE id_estudiante = ? AND id_asignatura = ?"
            params = (dto.id_estudiante, dto.id_asignatura)

            logger.info(f"DAO existe - SQL: {sql}")
            logger.info(f"DAO existe - Params: {params}")

            try:
                resultado = self.ejecutar_consulta(sql, params)
                existe = len(resultado) > 0 and resultado[0].get('count', 0) > 0
                logger.info(f"DAO existe - Resultado consulta: {resultado}, Existe: {existe}")
                return existe
            except Error as ex:
                logger.error(f"Error al verificar existencia: {ex}", exc_info=True)
                return False
        else:
            logger.warning("IDs de estudiante-asignatura no válidos para verificar existencia")
            return False

    def actualizar(self, dto: EstudianteAsignaturaDTO) -> bool:
        """
        Actualiza un registro de estudiante-asignatura en la base de datos.

        Args:
            dto (EstudianteAsignaturaDTO): DTO con los datos a actualizar.

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario.
        """
        sql = """UPDATE estudiante_asignatura 
                 SET estado = ?, nota_final = ?, periodo = ?
                 WHERE id_estudiante = ? AND id_asignatura = ?"""
        params = (
            dto.estado,
            dto.nota_final,
            dto.periodo,
            dto.id_estudiante,
            dto.id_asignatura,
        )

        logger.info(f"DAO actualizar - SQL: {sql}")
        logger.info(f"DAO actualizar - Params: {params}")

        resultado = self.ejecutar_actualizacion(sql, params)
        logger.info(f"DAO actualizar - Resultado: {resultado}")

        return resultado
