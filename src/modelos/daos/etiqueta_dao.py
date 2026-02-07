from typing import Optional, List, Dict, Any
from sqlite3 import Error

from modelos.dtos.etiqueta_dto import EtiquetaDTO
from modelos.daos.base_dao import DAO
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class EtiquetaDAO(DAO):
    def __init__(self, ruta_db=None):
        super().__init__(ruta_db)
        self.crear_tabla()

    def crear_tabla(self, sql: Optional[str] = None) -> bool:
        if sql is None:
            sql = """CREATE TABLE IF NOT EXISTS etiqueta (
                id_etiqueta INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE
            )"""
        return self.ejecutar_actualizacion(sql=sql, params=())

    def insertar(self, dto: EtiquetaDTO) -> Optional[int]:
        sql = "INSERT INTO etiqueta (nombre) VALUES (?)"
        params = (dto.nombre,)
        return self.ejecutar_insertar(sql, params)

    def eliminar(self, dto: EtiquetaDTO) -> bool:
        sql = "DELETE FROM etiqueta WHERE id_etiqueta = ?"
        params = (dto.id_etiqueta,)
        return self.ejecutar_actualizacion(sql, params)

    def actualizar(self, dto: EtiquetaDTO) -> bool:
        sql = "UPDATE etiqueta SET nombre = ? WHERE id_etiqueta = ?"
        params = (dto.nombre, dto.id_etiqueta)
        return self.ejecutar_actualizacion(sql, params)

    def instanciar(self, dto: EtiquetaDTO) -> bool:
        if dto.id_etiqueta:
            sql = "SELECT * FROM etiqueta WHERE id_etiqueta = ?"
            params = (dto.id_etiqueta,)
        elif dto.nombre:
            sql = "SELECT * FROM etiqueta WHERE nombre = ?"
            params = (dto.nombre,)
        else:
            return False

        lista = self.ejecutar_consulta(sql, params)
        if lista:
            dto.set_data(lista[0])
            return True
        return False

    def existe(self, dto: EtiquetaDTO) -> bool:
        if dto.id_etiqueta:
            sql = "SELECT COUNT(*) as count FROM etiqueta WHERE id_etiqueta = ?"
            params = (dto.id_etiqueta,)
        elif dto.nombre:
            sql = "SELECT COUNT(*) as count FROM etiqueta WHERE nombre = ?"
            params = (dto.nombre,)
        else:
            return False
        try:
            resultado = self.ejecutar_consulta(sql, params)
            return len(resultado) > 0 and resultado[0].get("count", 0) > 0
        except Error as ex:
            logger.error(f"Error al verificar existencia: {ex}", exc_info=True)
            return False

    def obtener_todas(self) -> List[Dict[str, Any]]:
        sql = "SELECT * FROM etiqueta ORDER BY nombre"
        return self.ejecutar_consulta(sql, ())

    def obtener_por_nombre(self, nombre: str) -> Optional[Dict[str, Any]]:
        sql = "SELECT * FROM etiqueta WHERE nombre = ?"
        resultado = self.ejecutar_consulta(sql, (nombre,))
        return resultado[0] if resultado else None
