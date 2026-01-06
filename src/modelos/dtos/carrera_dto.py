import dataclasses
from typing import Optional, Dict, Any


@dataclasses.dataclass
class CarreraDTO:
    """
    Data Transfer Object para Carrera.

    Representa la información de una carrera académica que será transferida
    entre las capas de la aplicación.

    Attributes:
        id_carrera (Optional[int]): Identificador único de la carrera.
            Se genera automáticamente en la base de datos. Defaults to None.
        codigo (Optional[str]): Código único de la carrera
            (ej: "09MED", "CUNS"). Defaults to None.
        nombre (Optional[str]): Nombre de la carrera
            (ej: "Ingeniería en Sistemas"). Defaults to None.
        plan (Optional[str]): Plan o código del plan de estudios
            (ej: "Plan 2023"). Defaults to None.
        modalidad (Optional[str]): Modalidad de estudio
            (ej: "Presencial", "Virtual", "Híbrida"). Defaults to None.
        creditos_totales (Optional[int]): Total de créditos requeridos
            para completar la carrera. Defaults to None.
    """

    id_carrera: Optional[int] = None
    codigo: Optional[str] = None
    nombre: Optional[str] = None
    plan: Optional[str] = None
    modalidad: Optional[str] = None
    creditos_totales: Optional[int] = None

    def get_data(self) -> Dict[str, Any]:
        """
        Obtiene los datos del DTO en formato de diccionario.

        Returns:
            Dict[str, Any]: Diccionario con todos los atributos del DTO.
                Las claves corresponden a los nombres de los atributos.

        Example:
            >>> carrera = CarreraDTO(
            ...     id_carrera=1,
            ...     codigo='09MED',
            ...     nombre='Ingeniería en Sistemas',
            ...     plan='Plan 2023',
            ...     modalidad='Presencial',
            ...     creditos_totales=240
            ... )
            >>> carrera.get_data()
            {
                'id_carrera': 1,
                'codigo': '09MED',
                'nombre': 'Ingeniería en Sistemas',
                'plan': 'Plan 2023',
                'modalidad': 'Presencial',
                'creditos_totales': 240
            }
        """
        return {
            'id_carrera': self.id_carrera,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'plan': self.plan,
            'modalidad': self.modalidad,
            'creditos_totales': self.creditos_totales,
        }

    def set_data(self, data: Dict[str, Any]) -> None:
        """
        Establece los atributos del DTO a partir de un diccionario.

        Args:
            data (Dict[str, Any]): Diccionario con los datos a asignar.
                Las claves deben corresponder a los nombres de los atributos.

        Example:
            >>> carrera = CarreraDTO()
            >>> carrera.set_data({
            ...     'id_carrera': 1,
            ...     'codigo': '09MED',
            ...     'nombre': 'Ingeniería en Sistemas',
            ...     'plan': 'Plan 2023',
            ...     'modalidad': 'Presencial',
            ...     'creditos_totales': 240
            ... })
        """
        if data:
            self.id_carrera = data.get('id_carrera', self.id_carrera)
            self.codigo = data.get('codigo', self.codigo)
            self.nombre = data.get('nombre', self.nombre)
            self.plan = data.get('plan', self.plan)
            self.modalidad = data.get('modalidad', self.modalidad)
            self.creditos_totales = data.get('creditos_totales', self.creditos_totales)
