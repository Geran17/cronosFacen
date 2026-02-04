import logging
from typing import Optional
from modelos.dtos.asignatura_dto import AsignaturaDTO
from modelos.daos.asignatura_dao import AsignaturaDAO


logger = logging.getLogger(__name__)


class AsignaturaService(AsignaturaDTO):
    """Servicio de Asignatura que extiende AsignaturaDTO."""

    def __init__(self, ruta_db: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.dao = AsignaturaDAO(ruta_db=ruta_db)
        logger.debug("AsignaturaService inicializado")

    def crear_tabla(self) -> None:
        """Crea la tabla de asignaturas en la base de datos."""
        try:
            self.dao.crear_tabla()
            logger.info("Tabla 'asignatura' creada exitosamente")
        except Exception as e:
            logger.error(f"Error al crear tabla de asignaturas: {e}")
            raise

    def insertar(self) -> Optional[int]:
        """Inserta la asignatura actual en la base de datos."""
        try:
            id_asignatura = self.dao.insertar(dto=self)
            if id_asignatura:
                self.id_asignatura = id_asignatura
                logger.info(f"Asignatura insertada con ID: {id_asignatura}")
            return id_asignatura
        except Exception as e:
            logger.error(f"Error al insertar asignatura: {e}")
            return None

    def actualizar(self) -> bool:
        """Actualiza los datos de la asignatura actual en la base de datos."""
        if not self.id_asignatura:
            logger.warning("No se puede actualizar asignatura sin ID")
            return False
        try:
            resultado = self.dao.actualizar(dto=self)
            if resultado:
                logger.info(f"Asignatura {self.id_asignatura} actualizada exitosamente")
            return resultado
        except Exception as e:
            logger.error(f"Error al actualizar asignatura: {e}")
            return False

    def eliminar(self) -> bool:
        """Elimina la asignatura actual de la base de datos."""
        if not self.id_asignatura:
            logger.warning("No se puede eliminar asignatura sin ID")
            return False
        try:
            resultado = self.dao.eliminar(dto=self)
            if resultado:
                logger.info(f"Asignatura {self.id_asignatura} eliminada exitosamente")
            return resultado
        except Exception as e:
            logger.error(f"Error al eliminar asignatura: {e}")
            return False

    def instanciar(self) -> bool:
        """Carga los datos de la asignatura desde la base de datos."""
        if not self.id_asignatura:
            logger.warning("No se puede instanciar asignatura sin ID")
            return False
        try:
            resultado = self.dao.instanciar(dto=self)
            if resultado:
                logger.info(f"Asignatura {self.id_asignatura} cargada desde BD")
            return resultado
        except Exception as e:
            logger.error(f"Error al instanciar asignatura: {e}")
            return False

    def existe(self) -> bool:
        """Verifica si la asignatura existe en la base de datos."""
        if not self.id_asignatura:
            logger.warning("No se puede verificar existencia de asignatura sin ID")
            return False
        try:
            resultado = self.dao.existe(dto=self)
            logger.debug(f"Asignatura {self.id_asignatura} existe: {resultado}")
            return resultado
        except Exception as e:
            logger.error(f"Error al verificar existencia de asignatura: {e}")
            return False

    def obtener_todas(self) -> list:
        """Obtiene todas las asignaturas como lista de servicios."""
        asignaturas = []
        try:
            for data in self.dao.obtener_todas():
                asignatura = AsignaturaService(ruta_db=self.dao.ruta_db)
                asignatura.set_data(data=data)
                asignaturas.append(asignatura)
        except Exception as e:
            logger.error(f"Error al obtener asignaturas: {e}")
        return asignaturas

    def obtener_id_nombre_codigo(self) -> list:
        """Obtiene id, nombre y código de asignaturas."""
        try:
            return self.dao.obtener_id_nombre_codigo()
        except Exception as e:
            logger.error(f"Error al obtener asignaturas (nombre/código): {e}")
            return []

    def obtener_id_codigo_nombre_carrera(self) -> list:
        """Obtiene id, código, nombre e id_carrera de asignaturas."""
        try:
            return self.dao.obtener_id_codigo_nombre_carrera()
        except Exception as e:
            logger.error(f"Error al obtener asignaturas (código/nombre/carrera): {e}")
            return []

    def obtener_por_carrera(self, id_carrera: int) -> list:
        """Obtiene asignaturas de una carrera (id, nombre, código)."""
        try:
            return self.dao.obtener_por_carrera(id_carrera)
        except Exception as e:
            logger.error(f"Error al obtener asignaturas por carrera: {e}")
            return []

    def obtener_basico_por_carrera(self, id_carrera: int) -> list:
        """Obtiene asignaturas básicas por carrera."""
        try:
            return self.dao.obtener_basico_por_carrera(id_carrera)
        except Exception as e:
            logger.error(f"Error al obtener asignaturas básicas por carrera: {e}")
            return []

    def obtener_basico(self) -> list:
        """Obtiene asignaturas básicas."""
        try:
            return self.dao.obtener_basico()
        except Exception as e:
            logger.error(f"Error al obtener asignaturas básicas: {e}")
            return []

    def obtener_plan_carrera(self, id_carrera: int) -> list:
        """Obtiene plan de estudios completo de la carrera."""
        try:
            return self.dao.obtener_plan_carrera(id_carrera)
        except Exception as e:
            logger.error(f"Error al obtener plan de carrera: {e}")
            return []

    def obtener_asignaturas_estudiante_completo(
        self, id_estudiante: int, id_carrera: int
    ) -> list:
        """Obtiene asignaturas del estudiante con datos completos desde VIEW."""
        try:
            return self.dao.obtener_asignaturas_estudiante_completo(id_estudiante, id_carrera)
        except Exception as e:
            logger.error(f"Error al obtener asignaturas del estudiante: {e}")
            return []

    def obtener_estudiante_asignatura_carrera(self, id_carrera: Optional[int] = None) -> list:
        """Obtiene asignaturas desde la VIEW vw_estudiante_asignatura_carrera."""
        try:
            return self.dao.obtener_estudiante_asignatura_carrera(id_carrera)
        except Exception as e:
            logger.error(f"Error al obtener asignaturas de view estudiante-carrera: {e}")
            return []

    def es_valida(self) -> bool:
        """Valida que los datos de la asignatura sean correctos."""
        if not self.nombre or len(str(self.nombre).strip()) == 0:
            logger.warning("Nombre de asignatura vacío o inválido")
            return False
        if not self.codigo or len(str(self.codigo).strip()) == 0:
            logger.warning("Código de asignatura vacío o inválido")
            return False
        if not self.tipo or len(str(self.tipo).strip()) == 0:
            logger.warning("Tipo de asignatura vacío o inválido")
            return False
        if self.creditos is None or self.creditos <= 0:
            logger.warning("Créditos de asignatura inválidos")
            return False
        if self.id_carrera is None:
            logger.warning("ID de carrera no está definido")
            return False
        logger.debug(f"Asignatura válida: {self.nombre}")
        return True

    def __str__(self) -> str:
        """Representación en string de la asignatura."""
        return (
            f"AsignaturaService(id={self.id_asignatura}, nombre={self.nombre}, "
            f"codigo={self.codigo}, tipo={self.tipo}, creditos={self.creditos})"
        )

    def __repr__(self) -> str:
        """Representación técnica de la asignatura."""
        return self.__str__()
