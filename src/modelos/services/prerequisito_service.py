import logging
from typing import Optional
from modelos.dtos.prerequisito_dto import PrerrequisitoDTO
from modelos.daos.prerequisito_dao import PrerrequisitoDAO


logger = logging.getLogger(__name__)


class PrerrequisitoService(PrerrequisitoDTO):
    """Servicio de Prerrequisito que extiende PrerrequisitoDTO."""

    def __init__(self, ruta_db: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.dao = PrerrequisitoDAO(ruta_db=ruta_db)
        logger.debug("PrerrequisitoService inicializado")

    def crear_tabla(self) -> None:
        """Crea la tabla de prerrequisitos en la base de datos."""
        try:
            self.dao.crear_tabla()
            logger.info("Tabla 'prerequisito' creada exitosamente")
        except Exception as e:
            logger.error(f"Error al crear tabla de prerrequisitos: {e}")
            raise

    def insertar(self) -> Optional[int]:
        """Inserta el prerrequisito actual en la base de datos."""
        try:
            resultado = self.dao.insertar(dto=self)
            if resultado:
                logger.info(
                    f"Prerrequisito insertado: {self.id_asignatura} -> {self.id_asignatura_prerrequisito}"
                )
            return resultado
        except Exception as e:
            logger.error(f"Error al insertar prerrequisito: {e}")
            return None

    def eliminar(self) -> bool:
        """Elimina el prerrequisito actual de la base de datos."""
        if not self.id_asignatura or not self.id_asignatura_prerrequisito:
            logger.warning("No se puede eliminar prerrequisito sin ambos IDs")
            return False
        try:
            resultado = self.dao.eliminar(dto=self)
            if resultado:
                logger.info(
                    f"Prerrequisito {self.id_asignatura} -> {self.id_asignatura_prerrequisito} eliminado exitosamente"
                )
            return resultado
        except Exception as e:
            logger.error(f"Error al eliminar prerrequisito: {e}")
            return False

    def instanciar(self) -> bool:
        """Carga los datos del prerrequisito desde la base de datos."""
        if not self.id_asignatura or not self.id_asignatura_prerrequisito:
            logger.warning("No se puede instanciar prerrequisito sin ambos IDs")
            return False
        try:
            resultado = self.dao.instanciar(dto=self)
            if resultado:
                logger.info(
                    f"Prerrequisito {self.id_asignatura} -> {self.id_asignatura_prerrequisito} cargado desde BD"
                )
            return resultado
        except Exception as e:
            logger.error(f"Error al instanciar prerrequisito: {e}")
            return False

    def existe(self) -> bool:
        """Verifica si el prerrequisito existe en la base de datos."""
        if not self.id_asignatura or not self.id_asignatura_prerrequisito:
            logger.warning("No se puede verificar existencia de prerrequisito sin ambos IDs")
            return False
        try:
            resultado = self.dao.existe(dto=self)
            logger.debug(
                f"Prerrequisito {self.id_asignatura} -> {self.id_asignatura_prerrequisito} existe: {resultado}"
            )
            return resultado
        except Exception as e:
            logger.error(f"Error al verificar existencia de prerrequisito: {e}")
            return False

    def es_valida(self) -> bool:
        """Valida que los datos del prerrequisito sean correctos."""
        if self.id_asignatura is None:
            logger.warning("ID de asignatura no está definido")
            return False
        if self.id_asignatura_prerrequisito is None:
            logger.warning("ID de asignatura prerrequisito no está definido")
            return False
        if self.id_asignatura == self.id_asignatura_prerrequisito:
            logger.warning("Una asignatura no puede ser prerrequisito de sí misma")
            return False
        logger.debug(
            f"Prerrequisito válido: {self.id_asignatura} -> {self.id_asignatura_prerrequisito}"
        )
        return True

    def __str__(self) -> str:
        """Representación en string del prerrequisito."""
        return (
            f"PrerrequisitoService("
            f"id_asignatura={self.id_asignatura}, "
            f"id_asignatura_prerrequisito={self.id_asignatura_prerrequisito})"
        )

    def __repr__(self) -> str:
        """Representación técnica del prerrequisito."""
        return self.__str__()
