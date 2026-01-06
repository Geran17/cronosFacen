import logging
from typing import Optional
from modelos.dtos.estudiante_actividad_dto import EstudianteActividadDTO
from modelos.daos.estudiante_actividad_dao import EstudianteActividadDAO


logger = logging.getLogger(__name__)


class EstudianteActividadService(EstudianteActividadDTO):
    """Servicio de Estudiante Actividad que extiende EstudianteActividadDTO."""

    def __init__(self, ruta_db: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.dao = EstudianteActividadDAO(ruta_db=ruta_db)
        logger.debug("EstudianteActividadService inicializado")

    def crear_tabla(self) -> None:
        """Crea la tabla de estudiante actividad en la base de datos."""
        try:
            self.dao.crear_tabla()
            logger.info("Tabla 'estudiante_actividad' creada exitosamente")
        except Exception as e:
            logger.error(f"Error al crear tabla de estudiante actividad: {e}")
            raise

    def insertar(self) -> bool:
        """Inserta la relación estudiante actividad actual en la base de datos."""
        try:
            resultado = self.dao.insertar(dto=self)
            if resultado:
                logger.info(
                    f"Estudiante-Actividad insertado: estudiante={self.id_estudiante}, actividad={self.id_actividad}"
                )
            return resultado
        except Exception as e:
            logger.error(f"Error al insertar estudiante actividad: {e}")
            return False

    def actualizar(self) -> bool:
        """Actualiza la relación estudiante actividad actual en la base de datos."""
        try:
            resultado = self.dao.actualizar(dto=self)
            if resultado:
                logger.info(
                    f"Estudiante-Actividad actualizado: estudiante={self.id_estudiante}, actividad={self.id_actividad}"
                )
            return resultado
        except Exception as e:
            logger.error(f"Error al actualizar estudiante actividad: {e}")
            return False

    def eliminar(self) -> bool:
        """Elimina la relación estudiante actividad actual de la base de datos."""
        if not self.id_estudiante or not self.id_actividad:
            logger.warning("No se puede eliminar estudiante actividad sin IDs")
            return False
        try:
            resultado = self.dao.eliminar(dto=self)
            if resultado:
                logger.info(
                    f"Estudiante-Actividad eliminado: estudiante={self.id_estudiante}, actividad={self.id_actividad}"
                )
            return resultado
        except Exception as e:
            logger.error(f"Error al eliminar estudiante actividad: {e}")
            return False

    def instanciar(self) -> bool:
        """Carga los datos de la relación estudiante actividad desde la base de datos."""
        if not self.id_estudiante or not self.id_actividad:
            logger.warning("No se puede instanciar estudiante actividad sin IDs")
            return False
        try:
            resultado = self.dao.instanciar(dto=self)
            if resultado:
                logger.info(
                    f"Estudiante-Actividad cargado: estudiante={self.id_estudiante}, actividad={self.id_actividad}"
                )
            return resultado
        except Exception as e:
            logger.error(f"Error al instanciar estudiante actividad: {e}")
            return False

    def existe(self) -> bool:
        """Verifica si la relación estudiante actividad existe en la base de datos."""
        if not self.id_estudiante or not self.id_actividad:
            logger.debug("No se puede verificar existencia sin IDs")
            return False
        try:
            resultado = self.dao.existe(dto=self)
            logger.debug(
                f"Estudiante-Actividad (estudiante={self.id_estudiante}, actividad={self.id_actividad}) existe: {resultado}"
            )
            return resultado
        except Exception as e:
            logger.error(f"Error al verificar existencia de estudiante actividad: {e}")
            return False

    def es_valida(self) -> bool:
        """Valida que los datos de la relación estudiante actividad sean correctos."""
        if self.id_estudiante is None:
            logger.warning("ID de estudiante no está definido")
            return False
        if self.id_actividad is None:
            logger.warning("ID de actividad no está definido")
            return False
        logger.debug(
            f"Estudiante actividad válido: estudiante={self.id_estudiante}, actividad={self.id_actividad}"
        )
        return True

    def __str__(self) -> str:
        """Representación en string de la relación estudiante actividad."""
        return (
            f"EstudianteActividadService("
            f"id_estudiante={self.id_estudiante}, id_actividad={self.id_actividad}, "
            f"estado={self.estado}, fecha_entrega={self.fecha_entrega})"
        )

    def __repr__(self) -> str:
        """Representación técnica de la relación estudiante actividad."""
        return self.__str__()
