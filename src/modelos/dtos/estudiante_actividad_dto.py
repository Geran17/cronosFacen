import dataclasses
from typing import Optional, Dict, Any


@dataclasses.dataclass
class EstudianteActividadDTO:
    """
    Data Transfer Object para Estudiante-Actividad.

    Representa el progreso de un estudiante en una actividad específica.
    Almacena información sobre el estado de entrega y fecha de entrega.

    Attributes:
        id_estudiante (Optional[int]): ID del estudiante. Defaults to None.
        id_actividad (Optional[int]): ID de la actividad. Defaults to None.
        estado (Optional[str]): Estado de la actividad
            ('pendiente', 'en_progreso', 'entregada', 'vencida').
            Defaults to None.
        fecha_entrega (Optional[str]): Fecha de entrega real en formato ISO
            (YYYY-MM-DD). Defaults to None.
    """

    id_estudiante: Optional[int] = None
    id_actividad: Optional[int] = None
    estado: Optional[str] = None
    fecha_entrega: Optional[str] = None

    def get_data(self) -> Dict[str, Any]:
        """
        Obtiene los datos del DTO en formato de diccionario.

        Returns:
            Dict[str, Any]: Diccionario con todos los atributos del DTO.
                Las claves corresponden a los nombres de los atributos.

        Example:
            >>> actividad = EstudianteActividadDTO(
            ...     id_estudiante=1,
            ...     id_actividad=1,
            ...     estado='entregada',
            ...     fecha_entrega='2025-01-20'
            ... )
            >>> actividad.get_data()
            {
                'id_estudiante': 1,
                'id_actividad': 1,
                'estado': 'entregada',
                'fecha_entrega': '2025-01-20'
            }
        """
        return {
            'id_estudiante': self.id_estudiante,
            'id_actividad': self.id_actividad,
            'estado': self.estado,
            'fecha_entrega': self.fecha_entrega,
        }

    def set_data(self, data: Dict[str, Any]) -> None:
        """
        Establece los atributos del DTO a partir de un diccionario.

        Args:
            data (Dict[str, Any]): Diccionario con los datos a asignar.
                Las claves deben corresponder a los nombres de los atributos.

        Example:
            >>> actividad = EstudianteActividadDTO()
            >>> actividad.set_data({
            ...     'id_estudiante': 1,
            ...     'id_actividad': 1,
            ...     'estado': 'entregada',
            ...     'fecha_entrega': '2025-01-20'
            ... })
        """
        if data:
            self.id_estudiante = data.get('id_estudiante', self.id_estudiante)
            self.id_actividad = data.get('id_actividad', self.id_actividad)
            self.estado = data.get('estado', self.estado)
            self.fecha_entrega = data.get('fecha_entrega', self.fecha_entrega)
