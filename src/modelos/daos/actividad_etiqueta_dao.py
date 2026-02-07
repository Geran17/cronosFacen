from typing import Optional, List, Dict, Any

from modelos.daos.base_dao import DAO
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class ActividadEtiquetaDAO(DAO):
    def __init__(self, ruta_db=None):
        super().__init__(ruta_db)
        self.crear_tabla()

    def crear_tabla(self, sql: Optional[str] = None) -> bool:
        if sql is None:
            sql = """CREATE TABLE IF NOT EXISTS actividad_etiqueta (
                id_actividad INTEGER NOT NULL,
                id_etiqueta INTEGER NOT NULL,
                PRIMARY KEY (id_actividad, id_etiqueta),
                FOREIGN KEY (id_actividad) REFERENCES actividad(id_actividad) ON DELETE CASCADE,
                FOREIGN KEY (id_etiqueta) REFERENCES etiqueta(id_etiqueta) ON DELETE CASCADE
            )"""
        return self.ejecutar_actualizacion(sql=sql, params=())

    def asignar(self, id_actividad: int, id_etiqueta: int) -> bool:
        sql = "INSERT OR IGNORE INTO actividad_etiqueta (id_actividad, id_etiqueta) VALUES (?, ?)"
        return self.ejecutar_actualizacion(sql, (id_actividad, id_etiqueta))

    def limpiar_por_actividad(self, id_actividad: int) -> bool:
        sql = "DELETE FROM actividad_etiqueta WHERE id_actividad = ?"
        return self.ejecutar_actualizacion(sql, (id_actividad,))

    def obtener_etiquetas_por_actividad(self, id_actividad: int) -> List[Dict[str, Any]]:
        sql = """
            SELECT e.id_etiqueta, e.nombre
            FROM etiqueta e
            INNER JOIN actividad_etiqueta ae ON ae.id_etiqueta = e.id_etiqueta
            WHERE ae.id_actividad = ?
            ORDER BY e.nombre
        """
        return self.ejecutar_consulta(sql, (id_actividad,))
