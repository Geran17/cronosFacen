from abc import ABC, abstractmethod
from .conexion_sqlite import ConexionSQLite
from typing import Optional, Dict, Any, List
from sqlite3 import Error
from contextlib import contextmanager
from scripts.logging_config import obtener_logger_modulo, registrar_error_critico

logger = obtener_logger_modulo(__name__)


class DAO(ABC):

    def __init__(self, ruta_db: Optional[str] = None):
        self.ruta_db = ruta_db

    @contextmanager
    def get_conexion(self):
        db = ConexionSQLite(ruta_db=self.ruta_db)
        con = db.obtener_conexion()
        try:
            yield con
            con.commit()
        except Exception as ex:
            try:
                con.rollback()
            except Exception:
                # Si la conexión está cerrada, ignorar el error en rollback
                pass
            raise

    @abstractmethod
    def crear_tabla(self):
        """
        Método abstracto para crear la tabla específica del DAO.
        """
        pass

    @abstractmethod
    def insertar(self, sql: str, params: tuple = ()) -> Optional[int]:
        """
        Método abstracto para insertar un registro.
        """
        pass

    @abstractmethod
    def eliminar(self, sql: str, params: tuple = ()) -> bool:
        """
        Método abstracto para eliminar un registro.
        """
        pass

    @abstractmethod
    def instanciar(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Método abstracto para consultar registros.
        """
        pass

    @abstractmethod
    def existe(self, sql: str, params: tuple = ()) -> bool:
        """
        Método abstracto para verificar existencia.
        """
        pass

    def ejecutar_insertar(self, sql: str, params: tuple = ()) -> Optional[int]:
        """
        Ejecuta una sentencia de inserción thread-safe.
        """
        try:
            logger.debug(f"Insertando: {sql} | Parámetros: {params}")
            with self.get_conexion() as con:
                cursor = con.cursor()
                cursor.execute(sql, params)
                id_generado = cursor.lastrowid
                logger.info(f"Registro insertado exitosamente - ID: {id_generado}")
                return id_generado
        except Error as ex:
            logger.error(f"Error al ejecutar inserción: {ex}", exc_info=True)
            registrar_error_critico(ex, f"Insertar en {self.__class__.__name__}")
            return None

    def ejecutar_consulta(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Ejecuta una consulta SELECT thread-safe.
        """
        try:
            logger.debug(f"Consultando: {sql} | Parámetros: {params}")
            with self.get_conexion() as con:
                cursor = con.cursor()
                cursor.execute(sql, params)
                rows = cursor.fetchall()
                resultado = [dict(row) for row in rows]
                logger.info(f"Consulta exitosa - Registros retornados: {len(resultado)}")
                return resultado
        except Error as ex:
            logger.error(f"Error al ejecutar consulta: {ex}", exc_info=True)
            registrar_error_critico(ex, f"Consultar en {self.__class__.__name__}")
            return []

    def ejecutar_actualizacion(self, sql: str, params: tuple = ()) -> bool:
        """
        Ejecuta una actualización o eliminación thread-safe.
        """
        try:
            logger.debug(f"Actualizando/Eliminando: {sql} | Parámetros: {params}")
            with self.get_conexion() as con:
                cursor = con.cursor()
                cursor.execute(sql, params)
                filas_afectadas = cursor.rowcount
                if filas_afectadas > 0:
                    logger.info(f"Operación exitosa - Filas afectadas: {filas_afectadas}")
                else:
                    logger.debug(f"No se afectaron registros en la operación")
                return filas_afectadas > 0
        except Error as ex:
            logger.error(f"Error al ejecutar actualización: {ex}", exc_info=True)
            registrar_error_critico(ex, f"Actualización/Eliminación en {self.__class__.__name__}")
            return False
