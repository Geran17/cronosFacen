import logging
from typing import Optional
from modelos.dtos.estudiante_dto import EstudianteDTO
from modelos.daos.estudiante_dao import EstudianteDAO


logger = logging.getLogger(__name__)


class EstudianteService(EstudianteDTO):
    """Servicio de Estudiante que extiende EstudianteDTO."""

    def __init__(self, ruta_db: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.dao = EstudianteDAO(ruta_db=ruta_db)
        logger.debug("EstudianteService inicializado")

    def crear_tabla(self) -> None:
        """Crea la tabla de estudiantes en la base de datos."""
        try:
            self.dao.crear_tabla()
            logger.info("Tabla 'estudiante' creada exitosamente")
        except Exception as e:
            logger.error(f"Error al crear tabla de estudiantes: {e}")
            raise

    def insertar(self) -> Optional[int]:
        """Inserta el estudiante actual en la base de datos."""
        try:
            id_estudiante = self.dao.insertar(dto=self)
            if id_estudiante:
                self.id_estudiante = id_estudiante
                logger.info(f"Estudiante insertado con ID: {id_estudiante}")
            return id_estudiante
        except Exception as e:
            logger.error(f"Error al insertar estudiante: {e}")
            return None

    def actualizar(self) -> bool:
        """Actualiza los datos del estudiante actual en la base de datos."""
        if not self.id_estudiante:
            logger.warning("No se puede actualizar estudiante sin ID")
            return False
        try:
            resultado = self.dao.actualizar(dto=self)
            if resultado:
                logger.info(f"Estudiante {self.id_estudiante} actualizado exitosamente")
            return resultado
        except Exception as e:
            logger.error(f"Error al actualizar estudiante: {e}")
            return False

    def eliminar(self) -> bool:
        """Elimina el estudiante actual de la base de datos."""
        if not self.id_estudiante:
            logger.warning("No se puede eliminar estudiante sin ID")
            return False
        try:
            resultado = self.dao.eliminar(dto=self)
            if resultado:
                logger.info(f"Estudiante {self.id_estudiante} eliminado exitosamente")
            return resultado
        except Exception as e:
            logger.error(f"Error al eliminar estudiante: {e}")
            return False

    def instanciar(self) -> bool:
        """Carga los datos del estudiante desde la base de datos."""
        if not self.id_estudiante:
            logger.warning("No se puede instanciar estudiante sin ID")
            return False
        try:
            resultado = self.dao.instanciar(dto=self)
            if resultado:
                logger.info(f"Estudiante {self.id_estudiante} cargado desde BD")
            return resultado
        except Exception as e:
            logger.error(f"Error al instanciar estudiante: {e}")
            return False

    def existe(self) -> bool:
        """Verifica si el estudiante existe en la base de datos."""
        if not self.id_estudiante:
            logger.warning("No se puede verificar existencia de estudiante sin ID")
            return False
        try:
            resultado = self.dao.existe(dto=self)
            logger.debug(f"Estudiante {self.id_estudiante} existe: {resultado}")
            return resultado
        except Exception as e:
            logger.error(f"Error al verificar existencia de estudiante: {e}")
            return False

    def es_valida(self) -> bool:
        """Valida que los datos del estudiante sean correctos."""
        if not self.nombre or len(str(self.nombre).strip()) == 0:
            logger.warning("Nombre de estudiante vacío o inválido")
            return False
        if not self.correo or len(str(self.correo).strip()) == 0:
            logger.warning("Correo de estudiante vacío o inválido")
            return False
        if "@" not in str(self.correo):
            logger.warning("Correo de estudiante inválido")
            return False
        logger.debug(f"Estudiante válido: {self.nombre}")
        return True

    def __str__(self) -> str:
        """Representación en string del estudiante."""
        return (
            f"EstudianteService(id={self.id_estudiante}, nombre={self.nombre}, "
            f"correo={self.correo})"
        )

    def __repr__(self) -> str:
        """Representación técnica del estudiante."""
        return self.__str__()
