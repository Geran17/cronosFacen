from modelos.dtos.estudiante_carrera_dto import EstudianteCarreraDTO
from modelos.daos.base_dao import DAO
from typing import Optional, List, Dict, Any
from sqlite3 import Error
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class EstudianteCarreraDAO(DAO):
    def __init__(self, ruta_db=None):
        super().__init__(ruta_db)
        self.crear_tabla()

    def crear_tabla(self, sql: Optional[str] = None) -> bool:
        """
        Crea la tabla estudiante_carrera en la base de datos si no existe.

        Args:
            sql (Optional[str]): SQL personalizado para crear la tabla.
                Si es None, usa el SQL por defecto.

        Returns:
            bool: True si la tabla se creó o ya existe, False en caso de error.
        """
        if sql is None:
            sql = """CREATE TABLE IF NOT EXISTS estudiante_carrera (
                id_estudiante INTEGER NOT NULL,
                id_carrera INTEGER NOT NULL,
                estado TEXT NOT NULL CHECK (
                    estado IN ('activa', 'inactiva', 'suspendida', 'completada', 'abandonada')
                ),
                fecha_inscripcion TEXT NOT NULL,
                fecha_inicio TEXT,
                fecha_fin TEXT,
                es_carrera_principal INTEGER DEFAULT 1,
                periodo_ingreso TEXT,
                observaciones TEXT,
                PRIMARY KEY (id_estudiante, id_carrera),
                FOREIGN KEY (id_estudiante)
                    REFERENCES estudiante(id_estudiante)
                    ON DELETE CASCADE,
                FOREIGN KEY (id_carrera)
                    REFERENCES carrera(id_carrera)
                    ON DELETE RESTRICT
            )"""

        return self.ejecutar_actualizacion(sql=sql, params=())

    def insertar(self, dto: EstudianteCarreraDTO) -> Optional[int]:
        """
        Inserta un nuevo registro de estudiante-carrera en la base de datos.

        Args:
            dto (EstudianteCarreraDTO): DTO con los datos a insertar.

        Returns:
            Optional[int]: 1 si se insertó correctamente, None si hay error.
        """
        sql = """INSERT INTO estudiante_carrera 
                 (id_estudiante, id_carrera, estado, fecha_inscripcion, fecha_inicio, 
                  fecha_fin, es_carrera_principal, periodo_ingreso, observaciones)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        params = (
            dto.id_estudiante,
            dto.id_carrera,
            dto.estado,
            dto.fecha_inscripcion,
            dto.fecha_inicio,
            dto.fecha_fin,
            dto.es_carrera_principal,
            dto.periodo_ingreso,
            dto.observaciones,
        )

        result = self.ejecutar_insertar(sql, params)
        return result if result else None

    def actualizar(self, dto: EstudianteCarreraDTO) -> bool:
        """
        Actualiza un registro de estudiante-carrera en la base de datos.

        Args:
            dto (EstudianteCarreraDTO): DTO con los datos a actualizar.
                Debe incluir id_estudiante e id_carrera.

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario.
        """
        sql = """UPDATE estudiante_carrera 
                 SET estado = ?, fecha_inscripcion = ?, fecha_inicio = ?, 
                     fecha_fin = ?, es_carrera_principal = ?, periodo_ingreso = ?, 
                     observaciones = ?
                 WHERE id_estudiante = ? AND id_carrera = ?"""
        params = (
            dto.estado,
            dto.fecha_inscripcion,
            dto.fecha_inicio,
            dto.fecha_fin,
            dto.es_carrera_principal,
            dto.periodo_ingreso,
            dto.observaciones,
            dto.id_estudiante,
            dto.id_carrera,
        )

        return self.ejecutar_actualizacion(sql, params)

    def eliminar(self, dto: EstudianteCarreraDTO) -> bool:
        """
        Elimina un registro de estudiante-carrera de la base de datos.

        Args:
            dto (EstudianteCarreraDTO): DTO con id_estudiante e id_carrera a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario.
        """
        sql = "DELETE FROM estudiante_carrera WHERE id_estudiante = ? AND id_carrera = ?"
        params = (dto.id_estudiante, dto.id_carrera)

        return self.ejecutar_actualizacion(sql, params)

    def instanciar(self, dto: EstudianteCarreraDTO) -> bool:
        """
        Consulta un registro de estudiante-carrera y carga los datos en el DTO.

        Args:
            dto (EstudianteCarreraDTO): DTO con id_estudiante e id_carrera a consultar.

        Returns:
            bool: True si se encontró y cargó el registro, False en caso contrario.
        """
        if dto.id_estudiante is not None and dto.id_carrera is not None:
            sql = """SELECT * FROM estudiante_carrera 
                     WHERE id_estudiante = ? AND id_carrera = ?"""
            params = (dto.id_estudiante, dto.id_carrera)
            lista_data = self.ejecutar_consulta(sql, params)
            if lista_data:
                data = lista_data[0]
                dto.set_data(data=data)
                return True
            return False
        else:
            logger.warning("IDs de estudiante y carrera requeridos para instanciar")
            return False

    def existe(self, dto: EstudianteCarreraDTO) -> bool:
        """
        Verifica si existe un registro con los IDs especificados.

        Args:
            dto (EstudianteCarreraDTO): DTO con id_estudiante e id_carrera a verificar.

        Returns:
            bool: True si existe el registro, False en caso contrario.
        """
        if dto.id_estudiante is not None and dto.id_carrera is not None:
            sql = """SELECT COUNT(*) as count FROM estudiante_carrera 
                     WHERE id_estudiante = ? AND id_carrera = ?"""
            params = (dto.id_estudiante, dto.id_carrera)

            try:
                resultado = self.ejecutar_consulta(sql, params)
                return len(resultado) > 0 and resultado[0].get('count', 0) > 0
            except Error as ex:
                logger.error(f"Error al verificar existencia: {ex}", exc_info=True)
                return False
        else:
            logger.warning("IDs de estudiante y carrera requeridos para verificar existencia")
            return False

    def obtener_carreras_por_estudiante(
        self, id_estudiante: int, estado: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtiene todas las carreras de un estudiante.

        Args:
            id_estudiante (int): ID del estudiante.
            estado (Optional[str]): Filtrar por estado específico. Si es None, trae todos.

        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con los datos de las carreras.
        """
        if estado:
            sql = """SELECT ec.*, c.nombre as nombre_carrera, c.plan, c.creditos_totales
                     FROM estudiante_carrera ec
                     JOIN carrera c ON ec.id_carrera = c.id_carrera
                     WHERE ec.id_estudiante = ? AND ec.estado = ?
                     ORDER BY ec.es_carrera_principal DESC, ec.fecha_inscripcion"""
            params = (id_estudiante, estado)
        else:
            sql = """SELECT ec.*, c.nombre as nombre_carrera, c.plan, c.creditos_totales
                     FROM estudiante_carrera ec
                     JOIN carrera c ON ec.id_carrera = c.id_carrera
                     WHERE ec.id_estudiante = ?
                     ORDER BY ec.es_carrera_principal DESC, ec.fecha_inscripcion DESC"""
            params = (id_estudiante,)

        return self.ejecutar_consulta(sql, params)

    def obtener_estudiantes_por_carrera(
        self, id_carrera: int, estado: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtiene todos los estudiantes de una carrera.

        Args:
            id_carrera (int): ID de la carrera.
            estado (Optional[str]): Filtrar por estado específico. Si es None, trae todos.

        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con los datos de los estudiantes.
        """
        if estado:
            sql = """SELECT ec.*, e.nombre, e.correo
                     FROM estudiante_carrera ec
                     JOIN estudiante e ON ec.id_estudiante = e.id_estudiante
                     WHERE ec.id_carrera = ? AND ec.estado = ?
                     ORDER BY e.nombre"""
            params = (id_carrera, estado)
        else:
            sql = """SELECT ec.*, e.nombre, e.correo
                     FROM estudiante_carrera ec
                     JOIN estudiante e ON ec.id_estudiante = e.id_estudiante
                     WHERE ec.id_carrera = ?
                     ORDER BY e.nombre"""
            params = (id_carrera,)

        return self.ejecutar_consulta(sql, params)

    def obtener_carrera_principal(self, id_estudiante: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene la carrera principal activa de un estudiante.

        Args:
            id_estudiante (int): ID del estudiante.

        Returns:
            Optional[Dict[str, Any]]: Datos de la carrera principal o None si no existe.
        """
        sql = """SELECT ec.*, c.nombre as nombre_carrera, c.plan, c.creditos_totales
                 FROM estudiante_carrera ec
                 JOIN carrera c ON ec.id_carrera = c.id_carrera
                 WHERE ec.id_estudiante = ? 
                 AND ec.estado = 'activa' 
                 AND ec.es_carrera_principal = 1"""
        params = (id_estudiante,)

        resultado = self.ejecutar_consulta(sql, params)
        return resultado[0] if resultado else None
