import dataclasses
from typing import Optional, Dict, Any


@dataclasses.dataclass
class EstudianteCarreraDTO:
    """
    Data Transfer Object para EstudianteCarrera.

    Representa la relación entre un estudiante y una carrera, permitiendo
    que un estudiante pueda estar inscrito en múltiples carreras.

    Attributes:
        id_estudiante (Optional[int]): ID del estudiante.
            Defaults to None.
        id_carrera (Optional[int]): ID de la carrera.
            Defaults to None.
        estado (Optional[str]): Estado de la inscripción.
            Valores: 'activa', 'inactiva', 'suspendida', 'completada', 'abandonada'.
            Defaults to 'activa'.
        fecha_inscripcion (Optional[str]): Fecha de inscripción formal en formato ISO (YYYY-MM-DD).
            Defaults to None.
        fecha_inicio (Optional[str]): Fecha de inicio de cursado en formato ISO (YYYY-MM-DD).
            Defaults to None.
        fecha_fin (Optional[str]): Fecha de finalización/egreso en formato ISO (YYYY-MM-DD).
            Defaults to None.
        es_carrera_principal (Optional[int]): Indica si es la carrera principal (1) o no (0).
            Defaults to 1.
        periodo_ingreso (Optional[str]): Periodo académico de ingreso (ej: "2024-1", "2024-2").
            Defaults to None.
        observaciones (Optional[str]): Notas o comentarios adicionales.
            Defaults to None.
    """

    id_estudiante: Optional[int] = None
    id_carrera: Optional[int] = None
    estado: Optional[str] = 'activa'
    fecha_inscripcion: Optional[str] = None
    fecha_inicio: Optional[str] = None
    fecha_fin: Optional[str] = None
    es_carrera_principal: Optional[int] = 1
    periodo_ingreso: Optional[str] = None
    observaciones: Optional[str] = None

    def get_data(self) -> Dict[str, Any]:
        """
        Obtiene los datos del DTO en formato de diccionario.

        Returns:
            Dict[str, Any]: Diccionario con todos los atributos del DTO.

        Example:
            >>> ec = EstudianteCarreraDTO(
            ...     id_estudiante=1,
            ...     id_carrera=5,
            ...     estado='activa',
            ...     fecha_inscripcion='2024-03-01',
            ...     es_carrera_principal=1,
            ...     periodo_ingreso='2024-1'
            ... )
            >>> ec.get_data()
            {
                'id_estudiante': 1,
                'id_carrera': 5,
                'estado': 'activa',
                'fecha_inscripcion': '2024-03-01',
                'fecha_inicio': None,
                'fecha_fin': None,
                'es_carrera_principal': 1,
                'periodo_ingreso': '2024-1',
                'observaciones': None
            }
        """
        return {
            'id_estudiante': self.id_estudiante,
            'id_carrera': self.id_carrera,
            'estado': self.estado,
            'fecha_inscripcion': self.fecha_inscripcion,
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
            'es_carrera_principal': self.es_carrera_principal,
            'periodo_ingreso': self.periodo_ingreso,
            'observaciones': self.observaciones,
        }

    def set_data(self, data: Dict[str, Any]) -> None:
        """
        Establece los atributos del DTO a partir de un diccionario.

        Args:
            data (Dict[str, Any]): Diccionario con los datos a asignar.

        Example:
            >>> ec = EstudianteCarreraDTO()
            >>> ec.set_data({
            ...     'id_estudiante': 1,
            ...     'id_carrera': 5,
            ...     'estado': 'activa',
            ...     'fecha_inscripcion': '2024-03-01'
            ... })
        """
        if data:
            self.id_estudiante = data.get('id_estudiante', self.id_estudiante)
            self.id_carrera = data.get('id_carrera', self.id_carrera)
            self.estado = data.get('estado', self.estado)
            self.fecha_inscripcion = data.get('fecha_inscripcion', self.fecha_inscripcion)
            self.fecha_inicio = data.get('fecha_inicio', self.fecha_inicio)
            self.fecha_fin = data.get('fecha_fin', self.fecha_fin)
            self.es_carrera_principal = data.get('es_carrera_principal', self.es_carrera_principal)
            self.periodo_ingreso = data.get('periodo_ingreso', self.periodo_ingreso)
            self.observaciones = data.get('observaciones', self.observaciones)
