import dataclasses
from typing import Optional, Dict, Any


@dataclasses.dataclass
class EstudianteAsignaturaDTO:
    """
    Data Transfer Object para Estudiante-Asignatura.

    Representa el registro del progreso de un estudiante en una asignatura.
    Almacena información sobre el estado, calificación y período de cursada.

    Attributes:
        id_estudiante (Optional[int]): ID del estudiante. Defaults to None.
        id_asignatura (Optional[int]): ID de la asignatura. Defaults to None.
        estado (Optional[str]): Estado actual de la asignatura
            ('no_cursada', 'cursando', 'aprobada', 'reprobada').
            Defaults to None.
        nota_final (Optional[float]): Nota final obtenida en la asignatura.
            Defaults to None.
        periodo (Optional[str]): Período académico en que fue cursada
            (ej: "2025-I"). Defaults to None.
    """

    id_estudiante: Optional[int] = None
    id_asignatura: Optional[int] = None
    estado: Optional[str] = None
    nota_final: Optional[float] = None
    periodo: Optional[str] = None

    def get_data(self) -> Dict[str, Any]:
        """
        Obtiene los datos del DTO en formato de diccionario.

        Returns:
            Dict[str, Any]: Diccionario con todos los atributos del DTO.
                Las claves corresponden a los nombres de los atributos.

        Example:
            >>> reg = EstudianteAsignaturaDTO(
            ...     id_estudiante=1,
            ...     id_asignatura=1,
            ...     estado='aprobada',
            ...     nota_final=85.5,
            ...     periodo='2025-I'
            ... )
            >>> reg.get_data()
            {
                'id_estudiante': 1,
                'id_asignatura': 1,
                'estado': 'aprobada',
                'nota_final': 85.5,
                'periodo': '2025-I'
            }
        """
        return {
            'id_estudiante': self.id_estudiante,
            'id_asignatura': self.id_asignatura,
            'estado': self.estado,
            'nota_final': self.nota_final,
            'periodo': self.periodo,
        }

    def set_data(self, data: Dict[str, Any]) -> None:
        """
        Establece los atributos del DTO a partir de un diccionario.

        Args:
            data (Dict[str, Any]): Diccionario con los datos a asignar.
                Las claves deben corresponder a los nombres de los atributos.

        Example:
            >>> reg = EstudianteAsignaturaDTO()
            >>> reg.set_data({
            ...     'id_estudiante': 1,
            ...     'id_asignatura': 1,
            ...     'estado': 'aprobada',
            ...     'nota_final': 85.5,
            ...     'periodo': '2025-I'
            ... })
        """
        if data:
            self.id_estudiante = data.get('id_estudiante', self.id_estudiante)
            self.id_asignatura = data.get('id_asignatura', self.id_asignatura)
            self.estado = data.get('estado', self.estado)
            self.nota_final = data.get('nota_final', self.nota_final)
            self.periodo = data.get('periodo', self.periodo)
