import logging
from typing import Optional
from modelos.dtos.tipo_actividad_dto import TipoActividadDTO
from modelos.daos.tipo_actividad_dao import TipoActividadDAO


logger = logging.getLogger(__name__)


class TipoActividadService(TipoActividadDTO):
    """Servicio de Tipo de Actividad que extiende TipoActividadDTO."""

    def __init__(self, ruta_db: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.dao = TipoActividadDAO(ruta_db=ruta_db)
        logger.debug("TipoActividadService inicializado")

    def crear_tabla(self) -> None:
        """Crea la tabla de tipos de actividad en la base de datos."""
        try:
            self.dao.crear_tabla()
            logger.info("Tabla 'tipo_actividad' creada exitosamente")
        except Exception as e:
            logger.error(f"Error al crear tabla de tipos de actividad: {e}")
            raise

    def insertar(self) -> Optional[int]:
        """Inserta el tipo de actividad actual en la base de datos."""
        try:
            id_tipo_actividad = self.dao.insertar(dto=self)
            if id_tipo_actividad:
                self.id_tipo_actividad = id_tipo_actividad
                logger.info(f"Tipo de actividad insertado con ID: {id_tipo_actividad}")
            return id_tipo_actividad
        except Exception as e:
            logger.error(f"Error al insertar tipo de actividad: {e}")
            return None

    def actualizar(self) -> bool:
        """Actualiza el tipo de actividad actual en la base de datos."""
        if not self.id_tipo_actividad:
            logger.warning("No se puede actualizar tipo de actividad sin ID")
            return False
        try:
            resultado = self.dao.actualizar(dto=self)
            if resultado:
                logger.info(f"Tipo de actividad {self.id_tipo_actividad} actualizado exitosamente")
            return resultado
        except Exception as e:
            logger.error(f"Error al actualizar tipo de actividad: {e}")
            return False

    def eliminar(self) -> bool:
        """Elimina el tipo de actividad actual de la base de datos."""
        if not self.id_tipo_actividad:
            logger.warning("No se puede eliminar tipo de actividad sin ID")
            return False
        try:
            resultado = self.dao.eliminar(dto=self)
            if resultado:
                logger.info(f"Tipo de actividad {self.id_tipo_actividad} eliminado exitosamente")
            return resultado
        except Exception as e:
            logger.error(f"Error al eliminar tipo de actividad: {e}")
            return False

    def instanciar(self) -> bool:
        """Carga los datos del tipo de actividad desde la base de datos."""
        if not self.id_tipo_actividad:
            logger.warning("No se puede instanciar tipo de actividad sin ID")
            return False
        try:
            resultado = self.dao.instanciar(dto=self)
            if resultado:
                logger.info(f"Tipo de actividad {self.id_tipo_actividad} cargado desde BD")
            return resultado
        except Exception as e:
            logger.error(f"Error al instanciar tipo de actividad: {e}")
            return False

    def existe(self) -> bool:
        """Verifica si el tipo de actividad existe en la base de datos."""
        if not self.id_tipo_actividad:
            logger.warning("No se puede verificar existencia de tipo de actividad sin ID")
            return False
        try:
            resultado = self.dao.existe(dto=self)
            logger.debug(f"Tipo de actividad {self.id_tipo_actividad} existe: {resultado}")
            return resultado
        except Exception as e:
            logger.error(f"Error al verificar existencia de tipo de actividad: {e}")
            return False

    def es_valida(self) -> bool:
        """Valida que los datos del tipo de actividad sean correctos."""
        if not self.nombre or len(str(self.nombre).strip()) == 0:
            logger.warning("Nombre de tipo de actividad vacío o inválido")
            return False
        if not self.siglas or len(str(self.siglas).strip()) == 0:
            logger.warning("Siglas de tipo de actividad vacías o inválidas")
            return False
        logger.debug(f"Tipo de actividad válido: {self.nombre}")
        return True

    def __str__(self) -> str:
        """Representación en string del tipo de actividad."""
        return (
            f"TipoActividadService(id={self.id_tipo_actividad}, nombre={self.nombre}, "
            f"siglas={self.siglas}, prioridad={self.prioridad})"
        )

    def __repr__(self) -> str:
        """Representación técnica del tipo de actividad."""
        return self.__str__()
