from modelos.daos.base_dao import DAO
from typing import Optional, List, Dict, Any
from sqlite3 import Error
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class ConsultaDAO(DAO):
    """
    DAO para ejecutar consultas complejas del MVP de Organización Académica.

    Este DAO proporciona métodos read-only para obtener información agregada
    sobre progreso académico, actividades pendientes y calendarios.
    """

    def __init__(self, ruta_db=None):
        super().__init__(ruta_db)

    def crear_tabla(self, sql: Optional[str] = None) -> bool:
        """
        No aplica para ConsultaDAO ya que solo realiza consultas read-only.

        Returns:
            bool: Siempre retorna True.
        """
        logger.info("ConsultaDAO no requiere creación de tablas (read-only)")
        return True

    def insertar(self, dto=None) -> Optional[int]:
        """
        No aplica para ConsultaDAO (read-only).

        Returns:
            None: Siempre retorna None.
        """
        logger.warning("ConsultaDAO no soporta inserciones (read-only)")
        return None

    def eliminar(self, dto=None) -> bool:
        """
        No aplica para ConsultaDAO (read-only).

        Returns:
            bool: Siempre retorna False.
        """
        logger.warning("ConsultaDAO no soporta eliminaciones (read-only)")
        return False

    def instanciar(self, dto=None) -> bool:
        """
        No aplica para ConsultaDAO (read-only).

        Returns:
            bool: Siempre retorna False.
        """
        logger.warning("ConsultaDAO no soporta instanciación directa")
        return False

    def existe(self, dto=None) -> bool:
        """
        No aplica para ConsultaDAO (read-only).

        Returns:
            bool: Siempre retorna False.
        """
        logger.warning("ConsultaDAO no soporta verificación de existencia")
        return False
