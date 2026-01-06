import dataclasses
from typing import Optional, Dict, Any


@dataclasses.dataclass
class EjeTematicoDTO:
    """
    Data Transfer Object para Eje Temático.

    Representa un eje temático o módulo dentro de una asignatura.
    Los ejes temáticos organizan los contenidos de la asignatura.

    Attributes:
        id_eje (Optional[int]): Identificador único del eje temático.
            Se genera automáticamente en la base de datos. Defaults to None.
        nombre (Optional[str]): Nombre del eje temático
            (ej: "Introducción a la Programación"). Defaults to None.
        orden (Optional[int]): Orden de presentación del eje
            dentro de la asignatura. Defaults to None.
        id_asignatura (Optional[int]): ID de la asignatura a la que
            pertenece el eje. Defaults to None.
    """

    id_eje: Optional[int] = None
    nombre: Optional[str] = None
    orden: Optional[int] = None
    id_asignatura: Optional[int] = None

    def get_data(self) -> Dict[str, Any]:
        """
        Obtiene los datos del DTO en formato de diccionario.

        Returns:
            Dict[str, Any]: Diccionario con todos los atributos del DTO.
                Las claves corresponden a los nombres de los atributos.

        Example:
            >>> eje = EjeTematicoDTO(
            ...     id_eje=1,
            ...     nombre='Introducción a la Programación',
            ...     orden=1,
            ...     id_asignatura=1
            ... )
            >>> eje.get_data()
            {
                'id_eje': 1,
                'nombre': 'Introducción a la Programación',
                'orden': 1,
                'id_asignatura': 1
            }
        """
        return {
            'id_eje': self.id_eje,
            'nombre': self.nombre,
            'orden': self.orden,
            'id_asignatura': self.id_asignatura,
        }

    def set_data(self, data: Dict[str, Any]) -> None:
        """
        Establece los atributos del DTO a partir de un diccionario.

        Args:
            data (Dict[str, Any]): Diccionario con los datos a asignar.
                Las claves deben corresponder a los nombres de los atributos.

        Example:
            >>> eje = EjeTematicoDTO()
            >>> eje.set_data({
            ...     'id_eje': 1,
            ...     'nombre': 'Introducción a la Programación',
            ...     'orden': 1,
            ...     'id_asignatura': 1
            ... })
        """
        if data:
            self.id_eje = data.get('id_eje', self.id_eje)
            self.nombre = data.get('nombre', self.nombre)
            self.orden = data.get('orden', self.orden)
            self.id_asignatura = data.get('id_asignatura', self.id_asignatura)
