import logging
from typing import Optional
from modelos.dtos.calendario_evento_dto import CalendarioEventoDTO
from modelos.daos.calendario_evento_dao import CalendarioEventoDAO


logger = logging.getLogger(__name__)


class CalendarioEventoService(CalendarioEventoDTO):
    """Servicio de Calendario Evento que extiende CalendarioEventoDTO."""

    def __init__(self, ruta_db: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.dao = CalendarioEventoDAO(ruta_db=ruta_db)
        logger.debug("CalendarioEventoService inicializado")

    def crear_tabla(self) -> None:
        """Crea la tabla de eventos de calendario en la base de datos."""
        try:
            self.dao.crear_tabla()
            logger.info("Tabla 'calendario_evento' creada exitosamente")
        except Exception as e:
            logger.error(f"Error al crear tabla de eventos de calendario: {e}")
            raise

    def insertar(self) -> Optional[int]:
        """Inserta el evento de calendario actual en la base de datos."""
        try:
            id_evento = self.dao.insertar(dto=self)
            if id_evento:
                self.id_evento = id_evento
                logger.info(f"Evento de calendario insertado con ID: {id_evento}")
            return id_evento
        except Exception as e:
            logger.error(f"Error al insertar evento de calendario: {e}")
            return None

    def actualizar(self) -> bool:
        """Actualiza el evento de calendario actual en la base de datos."""
        if not self.id_evento:
            logger.warning("No se puede actualizar evento de calendario sin ID")
            return False
        try:
            resultado = self.dao.actualizar(dto=self)
            if resultado:
                logger.info(f"Evento de calendario {self.id_evento} actualizado exitosamente")
            return resultado
        except Exception as e:
            logger.error(f"Error al actualizar evento de calendario: {e}")
            return False

    def eliminar(self) -> bool:
        """Elimina el evento de calendario actual de la base de datos."""
        if not self.id_evento:
            logger.warning("No se puede eliminar evento de calendario sin ID")
            return False
        try:
            resultado = self.dao.eliminar(dto=self)
            if resultado:
                logger.info(f"Evento de calendario {self.id_evento} eliminado exitosamente")
            return resultado
        except Exception as e:
            logger.error(f"Error al eliminar evento de calendario: {e}")
            return False

    def instanciar(self) -> bool:
        """Carga los datos del evento de calendario desde la base de datos."""
        if not self.id_evento:
            logger.warning("No se puede instanciar evento de calendario sin ID")
            return False
        try:
            resultado = self.dao.instanciar(dto=self)
            if resultado:
                logger.info(f"Evento de calendario {self.id_evento} cargado desde BD")
            return resultado
        except Exception as e:
            logger.error(f"Error al instanciar evento de calendario: {e}")
            return False

    def existe(self) -> bool:
        """Verifica si el evento de calendario existe en la base de datos."""
        if not self.id_evento:
            logger.warning("No se puede verificar existencia de evento de calendario sin ID")
            return False
        try:
            resultado = self.dao.existe(dto=self)
            logger.debug(f"Evento de calendario {self.id_evento} existe: {resultado}")
            return resultado
        except Exception as e:
            logger.error(f"Error al verificar existencia de evento de calendario: {e}")
            return False

    def es_valida(self) -> bool:
        """Valida que los datos del evento de calendario sean correctos."""
        if not self.titulo or len(str(self.titulo).strip()) == 0:
            logger.warning("Título de evento de calendario vacío o inválido")
            return False
        if not self.fecha_inicio:
            logger.warning("Fecha de inicio de evento de calendario no definida")
            return False
        logger.debug(f"Evento de calendario válido: {self.titulo}")
        return True

    def __str__(self) -> str:
        """Representación en string del evento de calendario."""
        return (
            f"CalendarioEventoService(id={self.id_evento}, titulo={self.titulo}, "
            f"fecha_inicio={self.fecha_inicio}, fecha_fin={self.fecha_fin})"
        )

    def __repr__(self) -> str:
        """Representación técnica del evento de calendario."""
        return self.__str__()
