import logging
from typing import Optional, List, Dict, Any

from modelos.daos.actividad_etiqueta_dao import ActividadEtiquetaDAO

logger = logging.getLogger(__name__)


class ActividadEtiquetaService:
    def __init__(self, ruta_db: Optional[str] = None):
        self.dao = ActividadEtiquetaDAO(ruta_db=ruta_db)
        logger.debug("ActividadEtiquetaService inicializado")

    def asignar(self, id_actividad: int, id_etiqueta: int) -> bool:
        if not id_actividad or not id_etiqueta:
            return False
        return self.dao.asignar(id_actividad, id_etiqueta)

    def reemplazar_etiquetas(self, id_actividad: int, ids_etiqueta: List[int]) -> bool:
        if not id_actividad:
            return False
        self.dao.limpiar_por_actividad(id_actividad)
        ok = True
        for id_etiqueta in ids_etiqueta:
            if not self.dao.asignar(id_actividad, id_etiqueta):
                ok = False
        return ok

    def obtener_etiquetas_por_actividad(self, id_actividad: int) -> List[Dict[str, Any]]:
        if not id_actividad:
            return []
        return self.dao.obtener_etiquetas_por_actividad(id_actividad)
