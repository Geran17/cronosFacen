import dataclasses
from typing import Optional, Dict, Any


@dataclasses.dataclass
class AsignaturaDTO:
    """
    Data Transfer Object para Asignatura.

    Representa la información de una asignatura que será transferida
    entre las capas de la aplicación.

    Attributes:
        id_asignatura (Optional[int]): Identificador único de la asignatura.
            Se genera automáticamente en la base de datos. Defaults to None.
        codigo (Optional[str]): Código único de la asignatura
            (ej: "SIS101"). Defaults to None.
        nombre (Optional[str]): Nombre de la asignatura
            (ej: "Programación I"). Defaults to None.
        creditos (Optional[int]): Número de créditos de la asignatura.
            Defaults to None.
        horas_semanales (Optional[int]): Horas de clase por semana.
            Defaults to None.
        tipo (Optional[str]): Tipo de asignatura ("obligatoria" o "electiva").
            Defaults to None.
        id_carrera (Optional[int]): ID de la carrera a la que pertenece.
            Defaults to None.
    """

    id_asignatura: Optional[int] = None
    codigo: Optional[str] = None
    nombre: Optional[str] = None
    creditos: Optional[int] = None
    horas_semanales: Optional[int] = None
    tipo: Optional[str] = None
    semestre: Optional[int] = None
    id_carrera: Optional[int] = None

    def get_data(self) -> Dict[str, Any]:
        """
        Obtiene los datos del DTO en formato de diccionario.

        Returns:
            Dict[str, Any]: Diccionario con todos los atributos del DTO.
                Las claves corresponden a los nombres de los atributos.

        Example:
            >>> asignatura = AsignaturaDTO(
            ...     id_asignatura=1,
            ...     codigo='SIS101',
            ...     nombre='Programación I',
            ...     creditos=4,
            ...     horas_semanales=3,
            ...     tipo='obligatoria',
            ...     id_carrera=1
            ... )
            >>> asignatura.get_data()
            {
                'id_asignatura': 1,
                'codigo': 'SIS101',
                'nombre': 'Programación I',
                'creditos': 4,
                'horas_semanales': 3,
                'tipo': 'obligatoria',
                'id_carrera': 1
            }
        """
        return {
            'id_asignatura': self.id_asignatura,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'creditos': self.creditos,
            'horas_semanales': self.horas_semanales,
            'tipo': self.tipo,
            'semestre': self.semestre,
            'id_carrera': self.id_carrera,
        }

    def set_data(self, data: Dict[str, Any]) -> None:
        """
        Establece los atributos del DTO a partir de un diccionario.

        Args:
            data (Dict[str, Any]): Diccionario con los datos a asignar.
                Las claves deben corresponder a los nombres de los atributos.

        Example:
            >>> asignatura = AsignaturaDTO()
            >>> asignatura.set_data({
            ...     'id_asignatura': 1,
            ...     'codigo': 'SIS101',
            ...     'nombre': 'Programación I',
            ...     'creditos': 4,
            ...     'horas_semanales': 3,
            ...     'tipo': 'obligatoria',
            ...     'id_carrera': 1
            ... })
        """
        if data:
            self.id_asignatura = data.get('id_asignatura', self.id_asignatura)
            self.codigo = data.get('codigo', self.codigo)
            self.nombre = data.get('nombre', self.nombre)
            self.creditos = data.get('creditos', self.creditos)
            self.horas_semanales = data.get('horas_semanales', self.horas_semanales)
            self.tipo = data.get('tipo', self.tipo)
            self.semestre = data.get('semestre', self.semestre)
            self.id_carrera = data.get('id_carrera', self.id_carrera)
