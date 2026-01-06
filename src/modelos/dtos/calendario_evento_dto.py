import dataclasses
from typing import Optional, Dict, Any


@dataclasses.dataclass
class CalendarioEventoDTO:
    """
    Data Transfer Object para Evento del Calendario.

    Representa eventos importantes en el calendario académico
    que pueden afectar el cronograma de actividades.

    Attributes:
        id_evento (Optional[int]): Identificador único del evento.
            Se genera automáticamente en la base de datos. Defaults to None.
        titulo (Optional[str]): Título del evento
            (ej: "Período de Exámenes"). Defaults to None.
        tipo (Optional[str]): Tipo de evento
            (ej: "receso", "examen", "entrega"). Defaults to None.
        fecha_inicio (Optional[str]): Fecha de inicio en formato ISO
            (YYYY-MM-DD). Defaults to None.
        fecha_fin (Optional[str]): Fecha de fin en formato ISO
            (YYYY-MM-DD). Defaults to None.
        afecta_actividades (Optional[int]): Indica si el evento afecta
            las actividades (0 = no, 1 = sí). Defaults to None.
    """

    id_evento: Optional[int] = None
    titulo: Optional[str] = None
    tipo: Optional[str] = None
    fecha_inicio: Optional[str] = None
    fecha_fin: Optional[str] = None
    afecta_actividades: Optional[int] = None

    def get_data(self) -> Dict[str, Any]:
        """
        Obtiene los datos del DTO en formato de diccionario.

        Returns:
            Dict[str, Any]: Diccionario con todos los atributos del DTO.
                Las claves corresponden a los nombres de los atributos.

        Example:
            >>> evento = CalendarioEventoDTO(
            ...     id_evento=1,
            ...     titulo='Período de Exámenes',
            ...     tipo='examen',
            ...     fecha_inicio='2025-06-01',
            ...     fecha_fin='2025-06-15',
            ...     afecta_actividades=1
            ... )
            >>> evento.get_data()
            {
                'id_evento': 1,
                'titulo': 'Período de Exámenes',
                'tipo': 'examen',
                'fecha_inicio': '2025-06-01',
                'fecha_fin': '2025-06-15',
                'afecta_actividades': 1
            }
        """
        return {
            'id_evento': self.id_evento,
            'titulo': self.titulo,
            'tipo': self.tipo,
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
            'afecta_actividades': self.afecta_actividades,
        }

    def set_data(self, data: Dict[str, Any]) -> None:
        """
        Establece los atributos del DTO a partir de un diccionario.

        Args:
            data (Dict[str, Any]): Diccionario con los datos a asignar.
                Las claves deben corresponder a los nombres de los atributos.

        Example:
            >>> evento = CalendarioEventoDTO()
            >>> evento.set_data({
            ...     'id_evento': 1,
            ...     'titulo': 'Período de Exámenes',
            ...     'tipo': 'examen',
            ...     'fecha_inicio': '2025-06-01',
            ...     'fecha_fin': '2025-06-15',
            ...     'afecta_actividades': 1
            ... })
        """
        if data:
            self.id_evento = data.get('id_evento', self.id_evento)
            self.titulo = data.get('titulo', self.titulo)
            self.tipo = data.get('tipo', self.tipo)
            self.fecha_inicio = data.get('fecha_inicio', self.fecha_inicio)
            self.fecha_fin = data.get('fecha_fin', self.fecha_fin)
            self.afecta_actividades = data.get('afecta_actividades', self.afecta_actividades)
