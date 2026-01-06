import logging
from typing import Optional
from modelos.dtos.eje_tematico_dto import EjeTematicoDTO
from modelos.daos.eje_tematico_dao import EjeTematicoDAO


logger = logging.getLogger(__name__)


class EjeTematicoService(EjeTematicoDTO):
    """Servicio de Eje Temático que extiende EjeTematicoDTO."""

    def __init__(self, ruta_db: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.dao = EjeTematicoDAO(ruta_db=ruta_db)
        logger.debug("EjeTematicoService inicializado")

    def crear_tabla(self) -> None:
        """Crea la tabla de ejes temáticos en la base de datos."""
        try:
            self.dao.crear_tabla()
            logger.info("Tabla 'eje_tematico' creada exitosamente")
        except Exception as e:
            logger.error(f"Error al crear tabla de ejes temáticos: {e}")
            raise

    def insertar(self) -> Optional[int]:
        """Inserta el eje temático actual en la base de datos."""
        try:
            id_eje = self.dao.insertar(dto=self)
            if id_eje:
                self.id_eje = id_eje
                logger.info(f"Eje temático insertado con ID: {id_eje}")
            return id_eje
        except Exception as e:
            logger.error(f"Error al insertar eje temático: {e}")
            return None

    def actualizar(self) -> bool:
        """Actualiza el eje temático actual en la base de datos."""
        if not self.id_eje:
            logger.warning("No se puede actualizar eje temático sin ID")
            return False
        try:
            resultado = self.dao.actualizar(dto=self)
            if resultado:
                logger.info(f"Eje temático {self.id_eje} actualizado exitosamente")
            return resultado
        except Exception as e:
            logger.error(f"Error al actualizar eje temático: {e}")
            return False

    def eliminar(self) -> bool:
        """Elimina el eje temático actual de la base de datos."""
        if not self.id_eje:
            logger.warning("No se puede eliminar eje temático sin ID")
            return False
        try:
            resultado = self.dao.eliminar(dto=self)
            if resultado:
                logger.info(f"Eje temático {self.id_eje} eliminado exitosamente")
            return resultado
        except Exception as e:
            logger.error(f"Error al eliminar eje temático: {e}")
            return False

    def instanciar(self) -> bool:
        """Carga los datos del eje temático desde la base de datos."""
        if not self.id_eje:
            logger.warning("No se puede instanciar eje temático sin ID")
            return False
        try:
            resultado = self.dao.instanciar(dto=self)
            if resultado:
                logger.info(f"Eje temático {self.id_eje} cargado desde BD")
            return resultado
        except Exception as e:
            logger.error(f"Error al instanciar eje temático: {e}")
            return False

    def existe(self) -> bool:
        """Verifica si el eje temático existe en la base de datos."""
        if not self.id_eje:
            logger.warning("No se puede verificar existencia de eje temático sin ID")
            return False
        try:
            resultado = self.dao.existe(dto=self)
            logger.debug(f"Eje temático {self.id_eje} existe: {resultado}")
            return resultado
        except Exception as e:
            logger.error(f"Error al verificar existencia de eje temático: {e}")
            return False

    def es_valida(self) -> bool:
        """Valida que los datos del eje temático sean correctos."""
        if not self.nombre or len(str(self.nombre).strip()) == 0:
            logger.warning("Nombre de eje temático vacío o inválido")
            return False
        if self.orden is None or self.orden < 0:
            logger.warning("Orden de eje temático inválido")
            return False
        if self.id_asignatura is None:
            logger.warning("ID de asignatura no está definido")
            return False
        logger.debug(f"Eje temático válido: {self.nombre}")
        return True

    def __str__(self) -> str:
        """Representación en string del eje temático."""
        return (
            f"EjeTematicoService(id={self.id_eje}, nombre={self.nombre}, "
            f"orden={self.orden}, id_asignatura={self.id_asignatura})"
        )

    def __repr__(self) -> str:
        """Representación técnica del eje temático."""
        return self.__str__()
