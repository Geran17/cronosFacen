import dataclasses
from typing import Optional, Dict, Any


@dataclasses.dataclass
class EstudianteDTO:
    """
    Data Transfer Object para Estudiante.

    Representa la información básica de un estudiante.

    Attributes:
        id_estudiante (Optional[int]): Identificador único del estudiante.
            Se genera automáticamente en la base de datos. Defaults to None.
        nombre (Optional[str]): Nombre completo del estudiante.
            Defaults to None.
        correo (Optional[str]): Correo electrónico único del estudiante.
            Defaults to None.

    Note:
        Para gestionar las carreras del estudiante, usar la tabla estudiante_carrera
        a través de EstudianteCarreraService.
    """

    id_estudiante: Optional[int] = None
    nombre: Optional[str] = None
    correo: Optional[str] = None

    def get_data(self) -> Dict[str, Any]:
        """
        Obtiene los datos del DTO en formato de diccionario.

        Returns:
            Dict[str, Any]: Diccionario con todos los atributos del DTO.
                Las claves corresponden a los nombres de los atributos.

        Example:
            >>> estudiante = EstudianteDTO(
            ...     id_estudiante=1,
            ...     nombre='Juan Pérez',
            ...     correo='juan.perez@universidad.edu'
            ... )
            >>> estudiante.get_data()
            {
                'id_estudiante': 1,
                'nombre': 'Juan Pérez',
                'correo': 'juan.perez@universidad.edu'
            }
        """
        return {
            'id_estudiante': self.id_estudiante,
            'nombre': self.nombre,
            'correo': self.correo,
        }

    def set_data(self, data: Dict[str, Any]) -> None:
        """
        Establece los atributos del DTO a partir de un diccionario.

        Args:
            data (Dict[str, Any]): Diccionario con los datos a asignar.
                Las claves deben corresponder a los nombres de los atributos.

        Example:
            >>> estudiante = EstudianteDTO()
            >>> estudiante.set_data({
            ...     'id_estudiante': 1,
            ...     'nombre': 'Juan Pérez',
            ...     'correo': 'juan.perez@universidad.edu'
            ... })
        """
        if data:
            self.id_estudiante = data.get('id_estudiante', self.id_estudiante)
            self.nombre = data.get('nombre', self.nombre)
            self.correo = data.get('correo', self.correo)
