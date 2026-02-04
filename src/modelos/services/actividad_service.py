import logging
from typing import Optional
from modelos.dtos.actividad_dto import ActividadDTO
from modelos.daos.actividad_dao import ActividadDAO


logger = logging.getLogger(__name__)


class ActividadService(ActividadDTO):
    """Servicio de Actividad que extiende ActividadDTO."""

    def __init__(self, ruta_db: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.dao = ActividadDAO(ruta_db=ruta_db)
        logger.debug("ActividadService inicializado")

    def crear_tabla(self) -> None:
        """Crea la tabla de actividades en la base de datos."""
        try:
            self.dao.crear_tabla()
            logger.info("Tabla 'actividad' creada exitosamente")
        except Exception as e:
            logger.error(f"Error al crear tabla de actividades: {e}")
            raise

    def insertar(self) -> Optional[int]:
        """Inserta la actividad actual en la base de datos."""
        try:
            id_actividad = self.dao.insertar(dto=self)
            if id_actividad:
                self.id_actividad = id_actividad
                logger.info(f"Actividad insertada con ID: {id_actividad}")
            return id_actividad
        except Exception as e:
            logger.error(f"Error al insertar actividad: {e}")
            return None

    def actualizar(self) -> bool:
        """Actualiza la actividad actual en la base de datos."""
        if not self.id_actividad:
            logger.warning("No se puede actualizar actividad sin ID")
            return False
        try:
            resultado = self.dao.actualizar(dto=self)
            if resultado:
                logger.info(f"Actividad {self.id_actividad} actualizada exitosamente")
            return resultado
        except Exception as e:
            logger.error(f"Error al actualizar actividad: {e}")
            return False

    def eliminar(self) -> bool:
        """Elimina la actividad actual de la base de datos."""
        if not self.id_actividad:
            logger.warning("No se puede eliminar actividad sin ID")
            return False
        try:
            resultado = self.dao.eliminar(dto=self)
            if resultado:
                logger.info(f"Actividad {self.id_actividad} eliminada exitosamente")
            return resultado
        except Exception as e:
            logger.error(f"Error al eliminar actividad: {e}")
            return False

    def instanciar(self) -> bool:
        """Carga los datos de la actividad desde la base de datos."""
        if not self.id_actividad:
            logger.warning("No se puede instanciar actividad sin ID")
            return False
        try:
            resultado = self.dao.instanciar(dto=self)
            if resultado:
                logger.info(f"Actividad {self.id_actividad} cargada desde BD")
            return resultado
        except Exception as e:
            logger.error(f"Error al instanciar actividad: {e}")
            return False

    def existe(self) -> bool:
        """Verifica si la actividad existe en la base de datos."""
        if not self.id_actividad:
            logger.warning("No se puede verificar existencia de actividad sin ID")
            return False
        try:
            resultado = self.dao.existe(dto=self)
            logger.debug(f"Actividad {self.id_actividad} existe: {resultado}")
            return resultado
        except Exception as e:
            logger.error(f"Error al verificar existencia de actividad: {e}")
            return False

    def obtener_todas(self) -> list:
        """Obtiene todas las actividades."""
        try:
            return self.dao.obtener_todas()
        except Exception as e:
            logger.error(f"Error al obtener actividades: {e}")
            return []

    def obtener_detalladas_filtradas(
        self,
        id_estudiante: int,
        id_carrera: Optional[int] = None,
        id_asignatura: Optional[int] = None,
        id_tipo_actividad: Optional[int] = None,
    ) -> list:
        """Obtiene actividades detalladas desde la VIEW con filtros opcionales."""
        try:
            return self.dao.obtener_detalladas_filtradas(
                id_estudiante=id_estudiante,
                id_carrera=id_carrera,
                id_asignatura=id_asignatura,
                id_tipo_actividad=id_tipo_actividad,
            )
        except Exception as e:
            logger.error(f"Error al obtener actividades detalladas: {e}")
            return []

    def obtener_con_detalle(self, id_carrera: Optional[int] = None) -> list:
        """Obtiene actividades con detalles de eje, asignatura y tipo."""
        try:
            return self.dao.obtener_con_detalle(id_carrera=id_carrera)
        except Exception as e:
            logger.error(f"Error al obtener actividades con detalle: {e}")
            return []

    def obtener_por_filtros(
        self, id_carrera: Optional[int] = None, id_asignatura: Optional[int] = None
    ) -> list:
        """Obtiene actividades aplicando filtros de carrera y/o asignatura."""
        try:
            return self.dao.obtener_por_filtros(id_carrera=id_carrera, id_asignatura=id_asignatura)
        except Exception as e:
            logger.error(f"Error al obtener actividades por filtros: {e}")
            return []

    def es_valida(self) -> bool:
        """Valida que los datos de la actividad sean correctos."""
        if not self.titulo or len(str(self.titulo).strip()) == 0:
            logger.warning("Título de actividad vacío o inválido")
            return False
        if self.id_eje is None:
            logger.warning("ID de eje temático no está definido")
            return False
        if self.id_tipo_actividad is None:
            logger.warning("ID de tipo de actividad no está definido")
            return False
        logger.debug(f"Actividad válida: {self.titulo}")
        return True

    def __str__(self) -> str:
        """Representación en string de la actividad."""
        return (
            f"ActividadService(id={self.id_actividad}, titulo={self.titulo}, "
            f"id_eje={self.id_eje}, id_tipo_actividad={self.id_tipo_actividad}, nota={self.nota})"
        )

    def __repr__(self) -> str:
        """Representación técnica de la actividad."""
        return self.__str__()
