import logging
from typing import Optional
from modelos.dtos.estudiante_asignatura_dto import EstudianteAsignaturaDTO
from modelos.daos.estudiante_asignatura_dao import EstudianteAsignaturaDAO


logger = logging.getLogger(__name__)


class EstudianteAsignaturaService(EstudianteAsignaturaDTO):
    """Servicio de Estudiante Asignatura que extiende EstudianteAsignaturaDTO."""

    def __init__(self, ruta_db: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.dao = EstudianteAsignaturaDAO(ruta_db=ruta_db)
        logger.debug("EstudianteAsignaturaService inicializado")

    def crear_tabla(self) -> None:
        """Crea la tabla de estudiante asignatura en la base de datos."""
        try:
            self.dao.crear_tabla()
            logger.info("Tabla 'estudiante_asignatura' creada exitosamente")
        except Exception as e:
            logger.error(f"Error al crear tabla de estudiante asignatura: {e}")
            raise

    def insertar(self) -> bool:
        """Inserta la relación estudiante asignatura actual en la base de datos."""
        try:
            resultado = self.dao.insertar(dto=self)
            if resultado:
                logger.info(
                    f"Estudiante asignatura insertado: Estudiante={self.id_estudiante}, "
                    f"Asignatura={self.id_asignatura}"
                )
            return resultado
        except Exception as e:
            logger.error(f"Error al insertar estudiante asignatura: {e}")
            return False

    def actualizar(self) -> bool:
        """Actualiza la relación estudiante asignatura actual en la base de datos."""
        if not self.id_estudiante or not self.id_asignatura:
            logger.warning("No se puede actualizar sin IDs de estudiante y asignatura")
            return False
        try:
            resultado = self.dao.actualizar(dto=self)
            if resultado:
                logger.info(
                    f"Estudiante asignatura actualizado: Estudiante={self.id_estudiante}, "
                    f"Asignatura={self.id_asignatura}"
                )
            return resultado
        except Exception as e:
            logger.error(f"Error al actualizar estudiante asignatura: {e}")
            return False

    def eliminar(self) -> bool:
        """Elimina la relación estudiante asignatura actual de la base de datos."""
        if not self.id_estudiante or not self.id_asignatura:
            logger.warning("No se puede eliminar sin IDs de estudiante y asignatura")
            return False
        try:
            resultado = self.dao.eliminar(dto=self)
            if resultado:
                logger.info(
                    f"Estudiante asignatura eliminado: Estudiante={self.id_estudiante}, "
                    f"Asignatura={self.id_asignatura}"
                )
            return resultado
        except Exception as e:
            logger.error(f"Error al eliminar estudiante asignatura: {e}")
            return False

    def instanciar(self) -> bool:
        """Carga los datos de la relación estudiante asignatura desde la base de datos."""
        if not self.id_estudiante or not self.id_asignatura:
            logger.warning("No se puede instanciar sin IDs de estudiante y asignatura")
            return False
        try:
            resultado = self.dao.instanciar(dto=self)
            if resultado:
                logger.info(
                    f"Estudiante asignatura cargado: Estudiante={self.id_estudiante}, "
                    f"Asignatura={self.id_asignatura}"
                )
            return resultado
        except Exception as e:
            logger.error(f"Error al instanciar estudiante asignatura: {e}")
            return False

    def existe(self) -> bool:
        """Verifica si la relación estudiante asignatura existe en la base de datos."""
        if not self.id_estudiante or not self.id_asignatura:
            logger.warning("No se puede verificar existencia sin IDs de estudiante y asignatura")
            return False
        try:
            resultado = self.dao.existe(dto=self)
            logger.debug(
                f"Estudiante asignatura existe: Estudiante={self.id_estudiante}, "
                f"Asignatura={self.id_asignatura}, Existe={resultado}"
            )
            return resultado
        except Exception as e:
            logger.error(f"Error al verificar existencia de estudiante asignatura: {e}")
            return False

    def es_valida(self) -> bool:
        """Valida que los datos de la relación estudiante asignatura sean correctos."""
        if self.id_estudiante is None:
            logger.warning("ID de estudiante no está definido")
            return False
        if self.id_asignatura is None:
            logger.warning("ID de asignatura no está definido")
            return False
        logger.debug(f"Estudiante asignatura válido: {self.id_estudiante} -> {self.id_asignatura}")
        return True

    def __str__(self) -> str:
        """Representación en string de la relación estudiante asignatura."""
        return (
            f"EstudianteAsignaturaService("
            f"id_estudiante={self.id_estudiante}, "
            f"id_asignatura={self.id_asignatura}, "
            f"estado={self.estado}, "
            f"nota_final={self.nota_final})"
        )

    def __repr__(self) -> str:
        """Representación técnica de la relación estudiante asignatura."""
        return self.__str__()
