import dataclasses
from typing import Optional, Dict, Any


@dataclasses.dataclass
class ActividadDTO:
    """
    Data Transfer Object para Actividad.

    Representa una actividad académica específica dentro de un eje temático.
    Las actividades son tareas, exámenes, proyectos, etc. asignados a estudiantes.

    Attributes:
        id_actividad (Optional[int]): Identificador único de la actividad.
            Se genera automáticamente en la base de datos. Defaults to None.
        titulo (Optional[str]): Título o nombre de la actividad
            (ej: "Tarea 1 - Algoritmos"). Defaults to None.
        descripcion (Optional[str]): Descripción detallada de la actividad
            y sus requisitos. Defaults to None.
        fecha_inicio (Optional[str]): Fecha de inicio en formato ISO
            (YYYY-MM-DD). Defaults to None.
        fecha_fin (Optional[str]): Fecha de vencimiento en formato ISO
            (YYYY-MM-DD). Defaults to None.
        id_eje (Optional[int]): ID del eje temático al que pertenece.
            Defaults to None.
        id_tipo_actividad (Optional[int]): ID del tipo de actividad.
            Defaults to None.
        nota (Optional[int]): Nota o puntuación asociada a la actividad.
            Valor por defecto 0. Defaults to None.
    """

    id_actividad: Optional[int] = None
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_inicio: Optional[str] = None
    fecha_fin: Optional[str] = None
    id_eje: Optional[int] = None
    id_tipo_actividad: Optional[int] = None
    nota: Optional[int] = None

    def get_data(self) -> Dict[str, Any]:
        """
        Obtiene los datos del DTO en formato de diccionario.

        Returns:
            Dict[str, Any]: Diccionario con todos los atributos del DTO.
                Las claves corresponden a los nombres de los atributos.

        Example:
            >>> actividad = ActividadDTO(
            ...     id_actividad=1,
            ...     titulo='Tarea 1 - Algoritmos',
            ...     descripcion='Implementar tres algoritmos de ordenamiento',
            ...     fecha_inicio='2025-01-15',
            ...     fecha_fin='2025-01-22',
            ...     id_eje=1,
            ...     id_tipo_actividad=1,
            ...     nota=0
            ... )
            >>> actividad.get_data()
            {
                'id_actividad': 1,
                'titulo': 'Tarea 1 - Algoritmos',
                'descripcion': 'Implementar tres algoritmos de ordenamiento',
                'fecha_inicio': '2025-01-15',
                'fecha_fin': '2025-01-22',
                'id_eje': 1,
                'id_tipo_actividad': 1,
                'nota': 0
            }
        """
        return {
            'id_actividad': self.id_actividad,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
            'id_eje': self.id_eje,
            'id_tipo_actividad': self.id_tipo_actividad,
            'nota': self.nota,
        }

    def set_data(self, data: Dict[str, Any]) -> None:
        """
        Establece los atributos del DTO a partir de un diccionario.

        Args:
            data (Dict[str, Any]): Diccionario con los datos a asignar.
                Las claves deben corresponder a los nombres de los atributos.

        Example:
            >>> actividad = ActividadDTO()
            >>> actividad.set_data({
            ...     'id_actividad': 1,
            ...     'titulo': 'Tarea 1 - Algoritmos',
            ...     'descripcion': 'Implementar tres algoritmos de ordenamiento',
            ...     'fecha_inicio': '2025-01-15',
            ...     'fecha_fin': '2025-01-22',
            ...     'id_eje': 1,
            ...     'id_tipo_actividad': 1,
            ...     'nota': 0
            ... })
        """
        if data:
            self.id_actividad = data.get('id_actividad', self.id_actividad)
            self.titulo = data.get('titulo', self.titulo)
            self.descripcion = data.get('descripcion', self.descripcion)
            self.fecha_inicio = data.get('fecha_inicio', self.fecha_inicio)
            self.fecha_fin = data.get('fecha_fin', self.fecha_fin)
            self.id_eje = data.get('id_eje', self.id_eje)
            self.id_tipo_actividad = data.get('id_tipo_actividad', self.id_tipo_actividad)
            self.nota = data.get('nota', self.nota)
