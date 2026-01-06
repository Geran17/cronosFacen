import logging
from typing import Optional
from modelos.dtos.carrera_dto import CarreraDTO
from modelos.daos.carrera_dao import CarreraDAO


logger = logging.getLogger(__name__)


class CarreraService(CarreraDTO):
    """
    Servicio de Carrera que extiende CarreraDTO.
    Proporciona métodos de acceso a datos delegando al DAO.
    """

    def __init__(self, ruta_db: Optional[str] = None, **kwargs):
        """
        Inicializa el servicio de carrera.

        Args:
            ruta_db: Ruta opcional a la base de datos SQLite
            **kwargs: Argumentos adicionales para CarreraDTO
        """
        super().__init__(**kwargs)
        self.dao = CarreraDAO(ruta_db=ruta_db)
        logger.debug("CarreraService inicializado")

    def crear_tabla(self) -> None:
        """Crea la tabla de carreras en la base de datos."""
        try:
            self.dao.crear_tabla()
            logger.info("Tabla 'carrera' creada exitosamente")
        except Exception as e:
            logger.error(f"Error al crear tabla de carreras: {e}")
            raise

    def insertar(self) -> Optional[int]:
        """
        Inserta la carrera actual en la base de datos.

        Returns:
            ID de la carrera insertada, o None si falla.
        """
        try:
            id_carrera = self.dao.insertar(dto=self)
            if id_carrera:
                self.id_carrera = id_carrera
                logger.info(f"Carrera insertada con ID: {id_carrera}")
            return id_carrera
        except Exception as e:
            logger.error(f"Error al insertar carrera: {e}")
            return None

    def actualizar(self) -> bool:
        try:
            valor = self.dao.actualizar(dto=self)
            logger.info("Carrera carrera actulizadad correctamente")
            return valor
        except Exception as e:
            logger.error(f"Error al actualizar carrera: {e}")
            return False

    def eliminar(self) -> bool:
        """
        Elimina la carrera actual de la base de datos.

        Returns:
            True si la eliminación fue exitosa, False en caso contrario.
        """
        if not self.id_carrera:
            logger.warning("No se puede eliminar carrera sin ID")
            return False

        try:
            resultado = self.dao.eliminar(dto=self)
            if resultado:
                logger.info(f"Carrera {self.id_carrera} eliminada exitosamente")
            return resultado
        except Exception as e:
            logger.error(f"Error al eliminar carrera: {e}")
            return False

    def instanciar(self) -> bool:
        """
        Carga los datos de la carrera desde la base de datos.
        Requiere que id_carrera esté establecido.

        Returns:
            True si se cargaron los datos, False en caso contrario.
        """
        if not self.id_carrera:
            logger.warning("No se puede instanciar carrera sin ID")
            return False

        try:
            resultado = self.dao.instanciar(dto=self)
            if resultado:
                logger.info(f"Carrera {self.id_carrera} cargada desde BD")
            return resultado
        except Exception as e:
            logger.error(f"Error al instanciar carrera: {e}")
            return False

    def existe(self) -> bool:
        """
        Verifica si la carrera existe en la base de datos.
        Requiere que id_carrera esté establecido.

        Returns:
            True si la carrera existe, False en caso contrario.
        """
        if not self.id_carrera:
            logger.warning("No se puede verificar existencia de carrera sin ID")
            return False

        try:
            resultado = self.dao.existe(dto=self)
            logger.debug(f"Carrera {self.id_carrera} existe: {resultado}")
            return resultado
        except Exception as e:
            logger.error(f"Error al verificar existencia de carrera: {e}")
            return False

    def es_valida(self) -> bool:
        """
        Valida que los datos de la carrera sean correctos.

        Returns:
            True si la carrera es válida, False en caso contrario.
        """
        if not self.codigo or len(str(self.codigo).strip()) == 0:
            logger.warning("Código de carrera vacío o inválido")
            return False

        if not self.nombre or len(str(self.nombre).strip()) == 0:
            logger.warning("Nombre de carrera vacío o inválido")
            return False

        if not self.plan or len(str(self.plan).strip()) == 0:
            logger.warning("Plan de carrera vacío o inválido")
            return False

        if not self.modalidad or len(str(self.modalidad).strip()) == 0:
            logger.warning("Modalidad de carrera vacía o inválida")
            return False

        logger.debug(f"Carrera válida: {self.codigo} - {self.nombre}")
        return True

    def __str__(self) -> str:
        """Representación en string de la carrera."""
        return (
            f"CarreraService(id={self.id_carrera}, codigo={self.codigo}, "
            f"nombre={self.nombre}, plan={self.plan}, modalidad={self.modalidad})"
        )

    def __repr__(self) -> str:
        """Representación técnica de la carrera."""
        return self.__str__()
