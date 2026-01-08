import logging
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from modelos.daos.consulta_dao import ConsultaDAO, EventosUnificadosDAO
from modelos.dtos.consulta_dto import ConsultasDTO, EventosUnificadosDTO

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


class EventosUnificadosService:
    """
    Servicio de Eventos Unificados para el MVP de Organización Académica.

    Proporciona métodos de alto nivel para obtener, filtrar y manipular
    eventos unificados (Actividades + Eventos de Calendario) de manera
    segura y eficiente.
    """

    def __init__(self, ruta_db: Optional[str] = None):
        """
        Inicializa el servicio de eventos unificados.

        Args:
            ruta_db (Optional[str]): Ruta a la base de datos SQLite.
                Si es None, usa la ruta por defecto.
        """
        self.dao = EventosUnificadosDAO(ruta_db=ruta_db)
        logger.debug("EventosUnificadosService inicializado")

    # ┌────────────────────────────────────────────────────────────┐
    # │ Métodos de Obtención de Datos
    # └────────────────────────────────────────────────────────────┘

    def obtener_todos(self) -> List[EventosUnificadosDTO]:
        """
        Obtiene todos los eventos unificados.

        Returns:
            List[EventosUnificadosDTO]: Lista de todos los eventos.
        """
        logger.info("Obteniendo todos los eventos unificados")
        return self.dao.obtener_todos()

    def obtener_por_mes(self, ano: int, mes: int) -> List[EventosUnificadosDTO]:
        """
        Obtiene eventos de un mes específico.

        Args:
            ano (int): Año (ej: 2026)
            mes (int): Mes (1-12)

        Returns:
            List[EventosUnificadosDTO]: Lista de eventos del mes.
        """
        logger.info(f"Obteniendo eventos para {ano}-{mes:02d}")
        if not (1 <= mes <= 12):
            logger.warning(f"Mes inválido: {mes}")
            return []
        return self.dao.obtener_por_mes(ano, mes)

    def obtener_eventos_proximos(self, dias: int = 7) -> List[EventosUnificadosDTO]:
        """
        Obtiene eventos de los próximos N días.

        Args:
            dias (int): Número de días a considerar. Por defecto 7.

        Returns:
            List[EventosUnificadosDTO]: Lista de eventos próximos.
        """
        logger.info(f"Obteniendo eventos de los próximos {dias} días")
        return self.dao.obtener_eventos_proximos(dias)

    def obtener_actividades(self) -> List[EventosUnificadosDTO]:
        """
        Obtiene solo las actividades.

        Returns:
            List[EventosUnificadosDTO]: Lista de actividades.
        """
        logger.info("Obteniendo solo actividades")
        return self.dao.obtener_actividades()

    def obtener_eventos_calendario(self) -> List[EventosUnificadosDTO]:
        """
        Obtiene solo los eventos de calendario.

        Returns:
            List[EventosUnificadosDTO]: Lista de eventos de calendario.
        """
        logger.info("Obteniendo solo eventos de calendario")
        return self.dao.obtener_eventos_calendario()

    def obtener_por_rango_fechas(
        self, fecha_inicio: str, fecha_fin: str
    ) -> List[EventosUnificadosDTO]:
        """
        Obtiene eventos dentro de un rango de fechas.

        Args:
            fecha_inicio (str): Fecha inicial en formato YYYY-MM-DD
            fecha_fin (str): Fecha final en formato YYYY-MM-DD

        Returns:
            List[EventosUnificadosDTO]: Lista de eventos en el rango.
        """
        logger.info(f"Obteniendo eventos entre {fecha_inicio} y {fecha_fin}")
        return self.dao.obtener_por_rango_fechas(fecha_inicio, fecha_fin)

    def obtener_por_tipo_actividad(self, tipo_actividad: str) -> List[EventosUnificadosDTO]:
        """
        Obtiene eventos de un tipo de actividad específico.

        Args:
            tipo_actividad (str): Tipo de actividad (Quiz, Tarea, Examen, etc.)

        Returns:
            List[EventosUnificadosDTO]: Lista de eventos del tipo especificado.
        """
        logger.info(f"Obteniendo eventos de tipo '{tipo_actividad}'")
        return self.dao.obtener_por_tipo_actividad(tipo_actividad)

    def obtener_por_id(self, id_evento: int, tipo: str) -> Optional[EventosUnificadosDTO]:
        """
        Obtiene un evento específico por su ID.

        Args:
            id_evento (int): ID del evento
            tipo (str): 'Actividad' o 'Evento Calendario'

        Returns:
            Optional[EventosUnificadosDTO]: El evento si existe, None en caso contrario.
        """
        logger.info(f"Obteniendo evento {tipo}:{id_evento}")
        return self.dao.obtener_por_id(id_evento, tipo)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Métodos de Filtrado y Transformación
    # └────────────────────────────────────────────────────────────┘

    def agrupar_por_tipo(
        self, eventos: List[EventosUnificadosDTO]
    ) -> Dict[str, List[EventosUnificadosDTO]]:
        """
        Agrupa eventos por tipo.

        Args:
            eventos (List[EventosUnificadosDTO]): Lista de eventos a agrupar

        Returns:
            Dict[str, List[EventosUnificadosDTO]]: Diccionario agrupado por tipo
        """
        agrupado = {"Actividad": [], "Evento Calendario": []}
        for evento in eventos:
            agrupado[evento.tipo_evento].append(evento)
        logger.debug(
            f"Eventos agrupados: {len(agrupado['Actividad'])} actividades, "
            f"{len(agrupado['Evento Calendario'])} eventos"
        )
        return agrupado

    def agrupar_por_fecha(
        self, eventos: List[EventosUnificadosDTO]
    ) -> Dict[str, List[EventosUnificadosDTO]]:
        """
        Agrupa eventos por fecha de inicio.

        Args:
            eventos (List[EventosUnificadosDTO]): Lista de eventos a agrupar

        Returns:
            Dict[str, List[EventosUnificadosDTO]]: Diccionario agrupado por fecha
        """
        agrupado = {}
        for evento in eventos:
            fecha = evento.fecha_inicio
            if fecha not in agrupado:
                agrupado[fecha] = []
            agrupado[fecha].append(evento)
        logger.debug(f"Eventos agrupados por fecha: {len(agrupado)} días diferentes")
        return agrupado

    def agrupar_por_mes(
        self, eventos: List[EventosUnificadosDTO]
    ) -> Dict[str, List[EventosUnificadosDTO]]:
        """
        Agrupa eventos por mes.

        Args:
            eventos (List[EventosUnificadosDTO]): Lista de eventos a agrupar

        Returns:
            Dict[str, List[EventosUnificadosDTO]]: Diccionario agrupado por mes (YYYY-MM)
        """
        agrupado = {}
        for evento in eventos:
            mes = evento.fecha_inicio[:7]  # Extrae YYYY-MM
            if mes not in agrupado:
                agrupado[mes] = []
            agrupado[mes].append(evento)
        logger.debug(f"Eventos agrupados por mes: {len(agrupado)} meses diferentes")
        return agrupado

    def filtrar_por_tipo(
        self, eventos: List[EventosUnificadosDTO], tipo: str
    ) -> List[EventosUnificadosDTO]:
        """
        Filtra eventos por tipo.

        Args:
            eventos (List[EventosUnificadosDTO]): Lista de eventos a filtrar
            tipo (str): 'Actividad' o 'Evento Calendario'

        Returns:
            List[EventosUnificadosDTO]: Lista filtrada
        """
        filtrados = [e for e in eventos if e.tipo_evento == tipo]
        logger.debug(f"Filtrados {len(filtrados)} eventos de tipo '{tipo}'")
        return filtrados

    def filtrar_por_tipo_actividad(
        self, eventos: List[EventosUnificadosDTO], tipo_actividad: str
    ) -> List[EventosUnificadosDTO]:
        """
        Filtra eventos por tipo de actividad.

        Args:
            eventos (List[EventosUnificadosDTO]): Lista de eventos a filtrar
            tipo_actividad (str): Tipo de actividad (Quiz, Tarea, Examen, etc.)

        Returns:
            List[EventosUnificadosDTO]: Lista filtrada
        """
        filtrados = [e for e in eventos if e.tipo_actividad == tipo_actividad]
        logger.debug(f"Filtrados {len(filtrados)} eventos de tipo actividad '{tipo_actividad}'")
        return filtrados

    # ┌────────────────────────────────────────────────────────────┐
    # │ Métodos de Análisis y Estadísticas
    # └────────────────────────────────────────────────────────────┘

    def contar_eventos(self) -> int:
        """
        Cuenta el total de eventos unificados.

        Returns:
            int: Cantidad total de eventos.
        """
        eventos = self.obtener_todos()
        logger.info(f"Total de eventos: {len(eventos)}")
        return len(eventos)

    def contar_por_tipo(self) -> Dict[str, int]:
        """
        Cuenta eventos por tipo.

        Returns:
            Dict[str, int]: Cantidad de eventos por tipo.
        """
        eventos = self.obtener_todos()
        agrupado = self.agrupar_por_tipo(eventos)
        resultado = {
            "Actividad": len(agrupado["Actividad"]),
            "Evento Calendario": len(agrupado["Evento Calendario"]),
        }
        logger.info(f"Conteo por tipo: {resultado}")
        return resultado

    def obtener_estadisticas(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas generales de eventos.

        Returns:
            Dict[str, Any]: Diccionario con estadísticas.
        """
        eventos = self.obtener_todos()
        agrupado_tipo = self.agrupar_por_tipo(eventos)
        agrupado_mes = self.agrupar_por_mes(eventos)

        estadisticas = {
            "total_eventos": len(eventos),
            "total_actividades": len(agrupado_tipo["Actividad"]),
            "total_eventos_calendario": len(agrupado_tipo["Evento Calendario"]),
            "meses_cubiertos": len(agrupado_mes),
            "tipos_actividad": self._contar_tipos_actividad(eventos),
        }
        logger.info(f"Estadísticas obtenidas: {estadisticas}")
        return estadisticas

    def _contar_tipos_actividad(self, eventos: List[EventosUnificadosDTO]) -> Dict[str, int]:
        """
        Cuenta eventos por tipo de actividad.

        Args:
            eventos (List[EventosUnificadosDTO]): Lista de eventos

        Returns:
            Dict[str, int]: Conteo por tipo de actividad
        """
        conteo = {}
        for evento in eventos:
            tipo = evento.tipo_actividad
            conteo[tipo] = conteo.get(tipo, 0) + 1
        return conteo

    # ┌────────────────────────────────────────────────────────────┐
    # │ Métodos de Utilidad
    # └────────────────────────────────────────────────────────────┘

    def convertir_a_diccionarios(self, eventos: List[EventosUnificadosDTO]) -> List[Dict[str, Any]]:
        """
        Convierte una lista de DTOs a diccionarios.

        Args:
            eventos (List[EventosUnificadosDTO]): Lista de eventos

        Returns:
            List[Dict[str, Any]]: Lista de diccionarios
        """
        return [evento.to_dict() for evento in eventos]

    def ordenar_por_fecha(
        self, eventos: List[EventosUnificadosDTO], descendente: bool = False
    ) -> List[EventosUnificadosDTO]:
        """
        Ordena eventos por fecha.

        Args:
            eventos (List[EventosUnificadosDTO]): Lista de eventos
            descendente (bool): Si True, ordena de más reciente a más antiguo

        Returns:
            List[EventosUnificadosDTO]: Lista ordenada
        """
        ordenados = sorted(eventos, key=lambda x: x.fecha_inicio, reverse=descendente)
        logger.debug(f"Eventos ordenados por fecha ({['ascendente', 'descendente'][descendente]})")
        return ordenados

    def eventos_vencidos(self, eventos: List[EventosUnificadosDTO]) -> List[EventosUnificadosDTO]:
        """
        Filtra eventos vencidos (fecha_fin < hoy).

        Args:
            eventos (List[EventosUnificadosDTO]): Lista de eventos

        Returns:
            List[EventosUnificadosDTO]: Lista de eventos vencidos
        """
        hoy = datetime.now().date().isoformat()
        vencidos = [e for e in eventos if e.fecha_fin < hoy]
        logger.debug(f"Encontrados {len(vencidos)} eventos vencidos")
        return vencidos

    def eventos_proximos_a_vencer(
        self, eventos: List[EventosUnificadosDTO], dias: int = 3
    ) -> List[EventosUnificadosDTO]:
        """
        Filtra eventos próximos a vencer en los próximos N días.

        Args:
            eventos (List[EventosUnificadosDTO]): Lista de eventos
            dias (int): Días para considerar como próximo a vencer

        Returns:
            List[EventosUnificadosDTO]: Lista de eventos próximos a vencer
        """
        hoy = datetime.now().date()
        fecha_limite = (hoy + timedelta(days=dias)).isoformat()
        proximos = [e for e in eventos if hoy.isoformat() <= e.fecha_fin <= fecha_limite]
        logger.debug(f"Encontrados {len(proximos)} eventos próximos a vencer en {dias} días")
        return proximos
