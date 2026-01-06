from modelos.dtos.estudiante_carrera_dto import EstudianteCarreraDTO
from modelos.daos.estudiante_carrera_dao import EstudianteCarreraDAO
from typing import Optional, List, Dict, Any
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class EstudianteCarreraService:
    """
    Servicio para gestionar la relación entre estudiantes y carreras.

    Proporciona métodos de alto nivel para operaciones CRUD y consultas
    sobre la tabla estudiante_carrera.
    """

    def __init__(self, ruta_db: Optional[str] = None):
        """
        Inicializa el servicio con una conexión a la base de datos.

        Args:
            ruta_db (Optional[str]): Ruta a la base de datos SQLite.
                Si es None, usa la configuración por defecto.
        """
        self.dao = EstudianteCarreraDAO(ruta_db)

    def inscribir_estudiante(self, dto: EstudianteCarreraDTO) -> bool:
        """
        Inscribe un estudiante en una carrera.

        Args:
            dto (EstudianteCarreraDTO): DTO con los datos de la inscripción.

        Returns:
            bool: True si se inscribió correctamente, False en caso contrario.
        """
        try:
            if self.dao.existe(dto):
                logger.warning(
                    f"El estudiante {dto.id_estudiante} ya está inscrito en la carrera {dto.id_carrera}"
                )
                return False

            resultado = self.dao.insertar(dto)
            if resultado:
                logger.info(f"Estudiante {dto.id_estudiante} inscrito en carrera {dto.id_carrera}")
                return True
            return False
        except Exception as ex:
            logger.error(f"Error al inscribir estudiante: {ex}", exc_info=True)
            return False

    def actualizar_inscripcion(self, dto: EstudianteCarreraDTO) -> bool:
        """
        Actualiza los datos de una inscripción existente.

        Args:
            dto (EstudianteCarreraDTO): DTO con los datos actualizados.

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario.
        """
        try:
            if not self.dao.existe(dto):
                logger.warning(
                    f"No existe inscripción del estudiante {dto.id_estudiante} en carrera {dto.id_carrera}"
                )
                return False

            resultado = self.dao.actualizar(dto)
            if resultado:
                logger.info(
                    f"Actualizada inscripción: estudiante {dto.id_estudiante}, carrera {dto.id_carrera}"
                )
                return True
            return False
        except Exception as ex:
            logger.error(f"Error al actualizar inscripción: {ex}", exc_info=True)
            return False

    def eliminar_inscripcion(self, dto: EstudianteCarreraDTO) -> bool:
        """
        Elimina una inscripción de estudiante-carrera.

        Args:
            dto (EstudianteCarreraDTO): DTO con id_estudiante e id_carrera a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario.
        """
        try:
            if not self.dao.existe(dto):
                logger.warning(
                    f"No existe inscripción del estudiante {dto.id_estudiante} en carrera {dto.id_carrera}"
                )
                return False

            resultado = self.dao.eliminar(dto)
            if resultado:
                logger.info(
                    f"Eliminada inscripción: estudiante {dto.id_estudiante}, carrera {dto.id_carrera}"
                )
                return True
            return False
        except Exception as ex:
            logger.error(f"Error al eliminar inscripción: {ex}", exc_info=True)
            return False

    def obtener_inscripcion(
        self, id_estudiante: int, id_carrera: int
    ) -> Optional[EstudianteCarreraDTO]:
        """
        Obtiene los datos de una inscripción específica.

        Args:
            id_estudiante (int): ID del estudiante.
            id_carrera (int): ID de la carrera.

        Returns:
            Optional[EstudianteCarreraDTO]: DTO con los datos o None si no existe.
        """
        try:
            dto = EstudianteCarreraDTO(id_estudiante=id_estudiante, id_carrera=id_carrera)
            if self.dao.instanciar(dto):
                return dto
            return None
        except Exception as ex:
            logger.error(f"Error al obtener inscripción: {ex}", exc_info=True)
            return None

    def obtener_carreras_estudiante(
        self, id_estudiante: int, estado: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtiene todas las carreras de un estudiante.

        Args:
            id_estudiante (int): ID del estudiante.
            estado (Optional[str]): Filtrar por estado ('activa', 'completada', etc.).

        Returns:
            List[Dict[str, Any]]: Lista de carreras con sus datos.
        """
        try:
            return self.dao.obtener_carreras_por_estudiante(id_estudiante, estado)
        except Exception as ex:
            logger.error(f"Error al obtener carreras del estudiante: {ex}", exc_info=True)
            return []

    def obtener_estudiantes_carrera(
        self, id_carrera: int, estado: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtiene todos los estudiantes de una carrera.

        Args:
            id_carrera (int): ID de la carrera.
            estado (Optional[str]): Filtrar por estado ('activa', 'completada', etc.).

        Returns:
            List[Dict[str, Any]]: Lista de estudiantes con sus datos.
        """
        try:
            return self.dao.obtener_estudiantes_por_carrera(id_carrera, estado)
        except Exception as ex:
            logger.error(f"Error al obtener estudiantes de la carrera: {ex}", exc_info=True)
            return []

    def obtener_carrera_principal(self, id_estudiante: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene la carrera principal activa de un estudiante.

        Args:
            id_estudiante (int): ID del estudiante.

        Returns:
            Optional[Dict[str, Any]]: Datos de la carrera principal o None.
        """
        try:
            return self.dao.obtener_carrera_principal(id_estudiante)
        except Exception as ex:
            logger.error(f"Error al obtener carrera principal: {ex}", exc_info=True)
            return None

    def cambiar_estado(self, id_estudiante: int, id_carrera: int, nuevo_estado: str) -> bool:
        """
        Cambia el estado de una inscripción.

        Args:
            id_estudiante (int): ID del estudiante.
            id_carrera (int): ID de la carrera.
            nuevo_estado (str): Nuevo estado ('activa', 'inactiva', 'suspendida',
                               'completada', 'abandonada').

        Returns:
            bool: True si se cambió correctamente, False en caso contrario.
        """
        try:
            estados_validos = ['activa', 'inactiva', 'suspendida', 'completada', 'abandonada']
            if nuevo_estado not in estados_validos:
                logger.warning(f"Estado inválido: {nuevo_estado}")
                return False

            dto = EstudianteCarreraDTO(id_estudiante=id_estudiante, id_carrera=id_carrera)
            if not self.dao.instanciar(dto):
                logger.warning(f"No existe inscripción para cambiar estado")
                return False

            dto.estado = nuevo_estado
            return self.dao.actualizar(dto)
        except Exception as ex:
            logger.error(f"Error al cambiar estado: {ex}", exc_info=True)
            return False

    def completar_carrera(self, id_estudiante: int, id_carrera: int, fecha_fin: str) -> bool:
        """
        Marca una carrera como completada (graduación).

        Args:
            id_estudiante (int): ID del estudiante.
            id_carrera (int): ID de la carrera.
            fecha_fin (str): Fecha de finalización en formato ISO (YYYY-MM-DD).

        Returns:
            bool: True si se marcó como completada, False en caso contrario.
        """
        try:
            dto = EstudianteCarreraDTO(id_estudiante=id_estudiante, id_carrera=id_carrera)
            if not self.dao.instanciar(dto):
                logger.warning(f"No existe inscripción para completar")
                return False

            dto.estado = 'completada'
            dto.fecha_fin = fecha_fin
            return self.dao.actualizar(dto)
        except Exception as ex:
            logger.error(f"Error al completar carrera: {ex}", exc_info=True)
            return False

    def validar_carrera_principal_unica(self, id_estudiante: int) -> bool:
        """
        Valida que un estudiante tenga solo una carrera principal activa.

        Args:
            id_estudiante (int): ID del estudiante.

        Returns:
            bool: True si la validación es correcta, False si hay múltiples o ninguna.
        """
        try:
            carreras_activas = self.dao.obtener_carreras_por_estudiante(id_estudiante, 'activa')
            principales = [c for c in carreras_activas if c.get('es_carrera_principal') == 1]

            if len(principales) == 1:
                return True
            elif len(principales) == 0:
                logger.warning(f"Estudiante {id_estudiante} no tiene carrera principal activa")
                return False
            else:
                logger.error(
                    f"Estudiante {id_estudiante} tiene múltiples carreras principales activas"
                )
                return False
        except Exception as ex:
            logger.error(f"Error al validar carrera principal: {ex}", exc_info=True)
            return False
