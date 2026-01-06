import logging
from typing import Optional, List, Dict, Any
from modelos.daos.consulta_dao import ConsultaDAO
from modelos.dtos.consulta_dto import ConsultasDTO

logger = logging.getLogger(__name__)


class ConsultaService(ConsultasDTO):
    """
    Servicio de Consultas para el MVP de Organización Académica.

    Encapsula toda la lógica de consultas agregadas, proporcionando una interfaz
    limpia para obtener información sobre progreso académico, actividades y calendarios.
    """

    def __init__(self, ruta_db: Optional[str] = None):
        """
        Inicializa el servicio de consultas.

        Args:
            ruta_db (Optional[str]): Ruta a la base de datos SQLite.
                Si es None, usa la ruta por defecto.
        """
        self.dao = ConsultaDAO(ruta_db=ruta_db)
        logger.debug("ConsultaService inicializado")
