import dataclasses
from typing import Optional, Dict, Any


@dataclasses.dataclass
class PrerrequisitoDTO:
    """
    Data Transfer Object para Prerrequisito.

    Representa la relación de prerequisito entre dos asignaturas.
    Una asignatura puede requerir que se haya aprobado otra previamente.

    Attributes:
        id_asignatura (Optional[int]): ID de la asignatura que requiere
            el prerequisito. Defaults to None.
        id_asignatura_prerrequisito (Optional[int]): ID de la asignatura
            que debe cursarse primero. Defaults to None.
    """

    id_asignatura: Optional[int] = None
    id_asignatura_prerrequisito: Optional[int] = None

    def get_data(self) -> Dict[str, Any]:
        """
        Obtiene los datos del DTO en formato de diccionario.

        Returns:
            Dict[str, Any]: Diccionario con todos los atributos del DTO.
                Las claves corresponden a los nombres de los atributos.

        Example:
            >>> prerequisito = PrerrequisiteDTO(
            ...     id_asignatura=2,
            ...     id_asignatura_prerrequisito=1
            ... )
            >>> prerequisito.get_data()
            {
                'id_asignatura': 2,
                'id_asignatura_prerrequisito': 1
            }
        """
        return {
            'id_asignatura': self.id_asignatura,
            'id_asignatura_prerrequisito': self.id_asignatura_prerrequisito,
        }

    def set_data(self, data: Dict[str, Any]) -> None:
        """
        Establece los atributos del DTO a partir de un diccionario.

        Args:
            data (Dict[str, Any]): Diccionario con los datos a asignar.
                Las claves deben corresponder a los nombres de los atributos.

        Example:
            >>> prerequisito = PrerrequisiteDTO()
            >>> prerequisito.set_data({
            ...     'id_asignatura': 2,
            ...     'id_asignatura_prerrequisito': 1
            ... })
        """
        if data:
            self.id_asignatura = data.get('id_asignatura', self.id_asignatura)
            self.id_asignatura_prerrequisito = data.get(
                'id_asignatura_prerrequisito', self.id_asignatura_prerrequisito
            )
