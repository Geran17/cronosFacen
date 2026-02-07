import dataclasses
from typing import Optional, Dict, Any


@dataclasses.dataclass
class EtiquetaDTO:
    """
    Data Transfer Object para Etiqueta.

    Attributes:
        id_etiqueta (Optional[int]): Identificador único de la etiqueta.
        nombre (Optional[str]): Nombre de la etiqueta.
    """

    id_etiqueta: Optional[int] = None
    nombre: Optional[str] = None

    def get_data(self) -> Dict[str, Any]:
        return {
            "id_etiqueta": self.id_etiqueta,
            "nombre": self.nombre,
        }

    def set_data(self, data: Dict[str, Any]) -> None:
        if data:
            self.id_etiqueta = data.get("id_etiqueta", self.id_etiqueta)
            self.nombre = data.get("nombre", self.nombre)
