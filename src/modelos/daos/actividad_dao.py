from modelos.dtos.actividad_dto import ActividadDTO
from modelos.daos.base_dao import DAO
from typing import Optional, List, Dict, Any
from sqlite3 import Error
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class ActividadDAO(DAO):
    def __init__(self, ruta_db=None):
        super().__init__(ruta_db)

        # creamos la tabla
        self.crear_tabla()

    def crear_tabla(self, sql: Optional[str] = None) -> bool:
        """
        Crea la tabla de actividad en la base de datos si no existe.

        Args:
            sql (Optional[str]): SQL personalizado para crear la tabla.
                Si es None, usa el SQL por defecto.

        Returns:
            bool: True si la tabla se creó o ya existe, False en caso de error.
        """
        if sql is None:
            sql = """CREATE TABLE IF NOT EXISTS actividad (
                id_actividad INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descripcion TEXT,
                fecha_inicio TEXT NOT NULL,
                fecha_fin TEXT NOT NULL,
                id_eje INTEGER NOT NULL,
                id_tipo_actividad INTEGER NOT NULL,
                nota INTEGER DEFAULT 0,
                FOREIGN KEY (id_eje)
                    REFERENCES eje_tematico(id_eje)
                    ON DELETE CASCADE,
                FOREIGN KEY (id_tipo_actividad)
                    REFERENCES tipo_actividad(id_tipo_actividad)
            )"""

        return self.ejecutar_actualizacion(sql=sql, params=())

    def insertar(self, dto: ActividadDTO) -> Optional[int]:
        """
        Inserta un nuevo registro de actividad en la base de datos.

        Args:
            dto (ActividadDTO): DTO con los datos de la actividad a insertar.

        Returns:
            Optional[int]: ID del registro insertado o None si hay error.
        """
        sql = """INSERT INTO actividad (titulo, descripcion, fecha_inicio, fecha_fin, id_eje, id_tipo_actividad, nota)
                 VALUES (?, ?, ?, ?, ?, ?, ?)"""
        params = (
            dto.titulo,
            dto.descripcion,
            dto.fecha_inicio,
            dto.fecha_fin,
            dto.id_eje,
            dto.id_tipo_actividad,
            dto.nota if dto.nota is not None else 0,
        )

        return self.ejecutar_insertar(sql, params)

    def eliminar(self, dto: ActividadDTO) -> bool:
        """
        Elimina un registro de actividad de la base de datos por su ID.

        Args:
            dto (ActividadDTO): DTO con el id_actividad a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario.
        """
        sql = "DELETE FROM actividad WHERE id_actividad = ?"
        params = (dto.id_actividad,)

        return self.ejecutar_actualizacion(sql, params)

    def actualizar(self, dto: ActividadDTO) -> bool:
        """
        Actualiza un registro de actividad en la base de datos.

        Args:
            dto (ActividadDTO): DTO con los datos a actualizar.

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario.
        """
        sql = """UPDATE actividad 
                 SET titulo = ?, descripcion = ?, fecha_inicio = ?, fecha_fin = ?, 
                     id_eje = ?, id_tipo_actividad = ?, nota = ?
                 WHERE id_actividad = ?"""
        params = (
            dto.titulo,
            dto.descripcion,
            dto.fecha_inicio,
            dto.fecha_fin,
            dto.id_eje,
            dto.id_tipo_actividad,
            dto.nota if dto.nota is not None else 0,
            dto.id_actividad,
        )

        return self.ejecutar_actualizacion(sql, params)

    def instanciar(self, dto: ActividadDTO) -> bool:
        """
        Consulta un registro de actividad de la base de datos y carga los datos en el DTO.

        Args:
            dto (ActividadDTO): DTO con el id_actividad a consultar. Se llena con los datos obtenidos.

        Returns:
            bool: True si se encontró y cargó la actividad, False en caso contrario.
        """
        if dto.id_actividad != 0 and dto.id_actividad is not None:
            sql = "SELECT * FROM actividad WHERE id_actividad = ?"
            params = (dto.id_actividad,)
            lista_data = self.ejecutar_consulta(sql, params)
            if lista_data:
                data = lista_data[0]
                dto.set_data(data=data)
                return True
            return False
        else:
            logger.warning("ID de actividad no válido para instanciar")
            return False

    def existe(self, dto: ActividadDTO) -> bool:
        """
        Verifica si existe una actividad con el ID especificado.

        Args:
            dto (ActividadDTO): DTO con el id_actividad a verificar.

        Returns:
            bool: True si existe la actividad, False en caso contrario.
        """
        if dto.id_actividad != 0 and dto.id_actividad is not None:
            sql = "SELECT COUNT(*) as count FROM actividad WHERE id_actividad = ?"
            params = (dto.id_actividad,)

            try:
                resultado = self.ejecutar_consulta(sql, params)
                return len(resultado) > 0 and resultado[0].get('count', 0) > 0
            except Error as ex:
                logger.error(f"Error al verificar existencia: {ex}", exc_info=True)
                return False
        else:
            logger.warning("ID de actividad no válido para verificar existencia")
            return False

    def obtener_todas(self) -> List[Dict[str, Any]]:
        """
        Obtiene todas las actividades ordenadas por fecha de inicio descendente.
        """
        sql = "SELECT * FROM actividad ORDER BY fecha_inicio DESC"
        return self.ejecutar_consulta(sql, ())

    def obtener_detalladas_filtradas(
        self,
        id_estudiante: int,
        id_carrera: Optional[int] = None,
        id_asignatura: Optional[int] = None,
        id_tipo_actividad: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Obtiene actividades detalladas desde la VIEW con filtros opcionales.
        """
        sql = "SELECT * FROM vw_estudiante_actividades_detalladas WHERE id_estudiante = ?"
        params: List[Any] = [id_estudiante]

        if id_carrera:
            sql += " AND carrera_id = ?"
            params.append(id_carrera)

        if id_asignatura:
            sql += " AND id_asignatura = ?"
            params.append(id_asignatura)

        if id_tipo_actividad:
            sql += " AND tipo_actividad_id = ?"
            params.append(id_tipo_actividad)

        sql += " ORDER BY fecha_fin DESC, titulo"
        return self.ejecutar_consulta(sql, tuple(params))

    def obtener_con_detalle(self, id_carrera: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Obtiene actividades con detalles de eje, asignatura y tipo.
        """
        if id_carrera:
            sql = """
                SELECT a.id_actividad, a.titulo, a.descripcion, 
                       a.fecha_inicio, a.fecha_fin, a.id_eje, a.id_tipo_actividad, a.nota,
                       e.nombre as nombre_eje, asig.nombre as nombre_asignatura,
                       ta.siglas as sigla_tipo
                FROM actividad a
                INNER JOIN eje_tematico e ON a.id_eje = e.id_eje
                INNER JOIN asignatura asig ON e.id_asignatura = asig.id_asignatura
                LEFT JOIN tipo_actividad ta ON a.id_tipo_actividad = ta.id_tipo_actividad
                WHERE asig.id_carrera = ?
                ORDER BY a.fecha_fin DESC, a.titulo
            """
            params = (id_carrera,)
        else:
            sql = """
                SELECT a.id_actividad, a.titulo, a.descripcion, 
                       a.fecha_inicio, a.fecha_fin, a.id_eje, a.id_tipo_actividad, a.nota,
                       e.nombre as nombre_eje, asig.nombre as nombre_asignatura,
                       ta.siglas as sigla_tipo
                FROM actividad a
                INNER JOIN eje_tematico e ON a.id_eje = e.id_eje
                INNER JOIN asignatura asig ON e.id_asignatura = asig.id_asignatura
                LEFT JOIN tipo_actividad ta ON a.id_tipo_actividad = ta.id_tipo_actividad
                ORDER BY a.fecha_fin DESC, a.titulo
            """
            params = ()

        return self.ejecutar_consulta(sql, params)

    def obtener_por_filtros(
        self, id_carrera: Optional[int] = None, id_asignatura: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtiene actividades aplicando filtros de carrera y/o asignatura.
        """
        if id_carrera and id_carrera > 0:
            if id_asignatura and id_asignatura > 0:
                sql = """
                    SELECT a.* 
                    FROM actividad a
                    INNER JOIN eje_tematico et ON a.id_eje = et.id_eje
                    INNER JOIN asignatura asig ON et.id_asignatura = asig.id_asignatura
                    WHERE asig.id_carrera = ? AND asig.id_asignatura = ?
                    ORDER BY a.fecha_inicio DESC
                """
                params = (id_carrera, id_asignatura)
            else:
                sql = """
                    SELECT a.* 
                    FROM actividad a
                    INNER JOIN eje_tematico et ON a.id_eje = et.id_eje
                    INNER JOIN asignatura asig ON et.id_asignatura = asig.id_asignatura
                    WHERE asig.id_carrera = ?
                    ORDER BY a.fecha_inicio DESC
                """
                params = (id_carrera,)
        elif id_asignatura and id_asignatura > 0:
            sql = """
                SELECT a.* 
                FROM actividad a
                INNER JOIN eje_tematico et ON a.id_eje = et.id_eje
                INNER JOIN asignatura asig ON et.id_asignatura = asig.id_asignatura
                WHERE asig.id_asignatura = ?
                ORDER BY a.fecha_inicio DESC
            """
            params = (id_asignatura,)
        else:
            sql = "SELECT * FROM actividad ORDER BY fecha_inicio DESC"
            params = ()

        return self.ejecutar_consulta(sql, params)
