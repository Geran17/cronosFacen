import dataclasses
from typing import Optional, Dict, Any


@dataclasses.dataclass
class TipoActividadDTO:
    """
    Data Transfer Object para Tipo de Actividad.

    Representa los diferentes tipos de actividades académicas
    que pueden asignarse en una asignatura.

    Attributes:
        id_tipo_actividad (Optional[int]): Identificador único del tipo.
            Se genera automáticamente en la base de datos. Defaults to None.
        nombre (Optional[str]): Nombre del tipo de actividad
            (ej: "Tarea", "Quiz", "Examen"). Defaults to None.
        siglas (Optional[str]): Siglas o abreviatura única
            (ej: "TAR", "QZ", "EXN"). Defaults to None.
        descripcion (Optional[str]): Descripción detallada del tipo
            de actividad. Defaults to None.
        prioridad (Optional[int]): Nivel de prioridad de la actividad.
            Escala: 0 = baja, 1 = media, 2 = alta. Defaults to None.
    """

    id_tipo_actividad: Optional[int] = None
    nombre: Optional[str] = None
    siglas: Optional[str] = None
    descripcion: Optional[str] = None
    prioridad: Optional[int] = None

    def get_data(self) -> Dict[str, Any]:
        """
        Obtiene los datos del DTO en formato de diccionario.

        Returns:
            Dict[str, Any]: Diccionario con todos los atributos del DTO.
                Las claves corresponden a los nombres de los atributos.

        Example:
            >>> tipo = TipoActividadDTO(
            ...     id_tipo_actividad=1,
            ...     nombre='Tarea',
            ...     siglas='TAR',
            ...     descripcion='Actividad de refuerzo enviada a casa',
            ...     prioridad=1
            ... )
            >>> tipo.get_data()
            {
                'id_tipo_actividad': 1,
                'nombre': 'Tarea',
                'siglas': 'TAR',
                'descripcion': 'Actividad de refuerzo enviada a casa',
                'prioridad': 1
            }
        """
        return {
            'id_tipo_actividad': self.id_tipo_actividad,
            'nombre': self.nombre,
            'siglas': self.siglas,
            'descripcion': self.descripcion,
            'prioridad': self.prioridad,
        }

    def set_data(self, data: Dict[str, Any]) -> None:
        """
        Establece los atributos del DTO a partir de un diccionario.

        Args:
            data (Dict[str, Any]): Diccionario con los datos a asignar.
                Las claves deben corresponder a los nombres de los atributos.

        Example:
            >>> tipo = TipoActividadDTO()
            >>> tipo.set_data({
            ...     'id_tipo_actividad': 1,
            ...     'nombre': 'Tarea',
            ...     'siglas': 'TAR',
            ...     'descripcion': 'Actividad de refuerzo enviada a casa',
            ...     'prioridad': 1
            ... })
        """
        if data:
            self.id_tipo_actividad = data.get('id_tipo_actividad', self.id_tipo_actividad)
            self.nombre = data.get('nombre', self.nombre)
            self.siglas = data.get('siglas', self.siglas)
            self.descripcion = data.get('descripcion', self.descripcion)
            self.prioridad = data.get('prioridad', self.prioridad)
