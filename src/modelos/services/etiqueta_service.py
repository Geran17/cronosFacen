import logging
from typing import Optional, List, Dict, Any

from modelos.dtos.etiqueta_dto import EtiquetaDTO
from modelos.daos.etiqueta_dao import EtiquetaDAO

logger = logging.getLogger(__name__)


class EtiquetaService(EtiquetaDTO):
    """Servicio de Etiqueta que extiende EtiquetaDTO."""

    def __init__(self, ruta_db: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.dao = EtiquetaDAO(ruta_db=ruta_db)
        logger.debug("EtiquetaService inicializado")

    def crear_tabla(self) -> None:
        try:
            self.dao.crear_tabla()
        except Exception as e:
            logger.error(f"Error al crear tabla de etiquetas: {e}")
            raise

    def insertar(self) -> Optional[int]:
        try:
            id_etiqueta = self.dao.insertar(dto=self)
            if id_etiqueta:
                self.id_etiqueta = id_etiqueta
            return id_etiqueta
        except Exception as e:
            logger.error(f"Error al insertar etiqueta: {e}")
            return None

    def eliminar(self) -> bool:
        if not self.id_etiqueta:
            return False
        try:
            return self.dao.eliminar(dto=self)
        except Exception as e:
            logger.error(f"Error al eliminar etiqueta: {e}")
            return False

    def actualizar(self) -> bool:
        if not self.id_etiqueta:
            return False
        try:
            return self.dao.actualizar(dto=self)
        except Exception as e:
            logger.error(f"Error al actualizar etiqueta: {e}")
            return False

    def instanciar(self) -> bool:
        try:
            return self.dao.instanciar(dto=self)
        except Exception as e:
            logger.error(f"Error al instanciar etiqueta: {e}")
            return False

    def existe(self) -> bool:
        try:
            return self.dao.existe(dto=self)
        except Exception as e:
            logger.error(f"Error al verificar etiqueta: {e}")
            return False

    def obtener_todas(self) -> List[Dict[str, Any]]:
        try:
            return self.dao.obtener_todas()
        except Exception as e:
            logger.error(f"Error al obtener etiquetas: {e}")
            return []

    def crear_si_no_existe(self, nombre: str) -> Optional[int]:
        nombre = (nombre or "").strip()
        if not nombre:
            return None
        existente = self.dao.obtener_por_nombre(nombre)
        if existente:
            return existente.get("id_etiqueta")
        self.nombre = nombre
        return self.insertar()
