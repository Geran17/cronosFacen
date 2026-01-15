import dataclasses
from typing import Optional, Dict, Any, List
from datetime import date


@dataclasses.dataclass
class ConsultasDTO:
    """DTO para consultas generales."""

    pass


@dataclasses.dataclass
class EventosUnificadosDTO:
    """
    DTO que representa un evento unificado (Actividad o Evento de Calendario).

    Atributos:
        tipo_evento (str): 'Actividad' o 'Evento Calendario'
        id_evento (int): ID único del evento
        titulo (str): Título del evento
        descripcion (Optional[str]): Descripción detallada (solo para actividades)
        fecha_inicio (str): Fecha de inicio en formato ISO (YYYY-MM-DD)
        fecha_fin (str): Fecha de fin en formato ISO (YYYY-MM-DD)
        tipo_actividad (str): Tipo de actividad (Quiz, Tarea, Examen, etc.) o tipo de evento
        observaciones (Optional[str]): Observaciones adicionales (ej: "Afecta actividades")
        carrera (Optional[str]): Nombre de la carrera asociada (solo para actividades)
        id_carrera (Optional[int]): ID de la carrera asociada (solo para actividades)
        asignatura (Optional[str]): Nombre de la asignatura asociada (solo para actividades)
        id_asignatura (Optional[int]): ID de la asignatura asociada (solo para actividades)
    """

    tipo_evento: str  # 'Actividad' o 'Evento Calendario'
    id_evento: int
    titulo: str
    fecha_inicio: str
    fecha_fin: str
    tipo_actividad: str
    descripcion: Optional[str] = None
    observaciones: Optional[str] = None
    carrera: Optional[str] = None
    id_carrera: Optional[int] = None
    asignatura: Optional[str] = None
    id_asignatura: Optional[int] = None

    def es_actividad(self) -> bool:
        """Verifica si el evento es una actividad."""
        return self.tipo_evento == 'Actividad'

    def es_evento_calendario(self) -> bool:
        """Verifica si el evento es un evento de calendario."""
        return self.tipo_evento == 'Evento Calendario'

    def obtener_carrera_display(self) -> str:
        """Retorna el nombre de la carrera o 'Sin carrera' si no existe."""
        return self.carrera if self.carrera else 'Sin carrera'

    def obtener_asignatura_display(self) -> str:
        """Retorna el nombre de la asignatura o 'Sin asignatura' si no existe."""
        return self.asignatura if self.asignatura else 'Sin asignatura'

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el DTO a diccionario."""
        return dataclasses.asdict(self)

    @classmethod
    def from_row(cls, row: tuple) -> 'EventosUnificadosDTO':
        """
        Crea una instancia desde una fila de la base de datos.

        Esperado: (tipo_evento, id_evento, titulo, descripcion, fecha_inicio, fecha_fin, tipo_actividad,
                   observaciones, carrera, id_carrera, asignatura, id_asignatura)

        Args:
            row (tuple): Fila obtenida de la vista vw_eventos_unificados

        Returns:
            EventosUnificadosDTO: Instancia con los datos de la fila
        """
        return cls(
            tipo_evento=row[0],
            id_evento=row[1],
            titulo=row[2],
            descripcion=row[3],
            fecha_inicio=row[4],
            fecha_fin=row[5],
            tipo_actividad=row[6],
            observaciones=row[7],
            carrera=row[8] if len(row) > 8 else None,
            id_carrera=row[9] if len(row) > 9 else None,
            asignatura=row[10] if len(row) > 10 else None,
            id_asignatura=row[11] if len(row) > 11 else None,
        )
