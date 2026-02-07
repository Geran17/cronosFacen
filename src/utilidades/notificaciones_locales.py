from __future__ import annotations

from datetime import date, datetime
from typing import List, Tuple

from tkinter.messagebox import showinfo

from configuracion.config_app import get_notificaciones_config, set_notificaciones_config
from modelos.services.consulta_service import EventosUnificadosService
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


def _parse_fecha(fecha_iso: str) -> date | None:
    try:
        return datetime.strptime(fecha_iso, "%Y-%m-%d").date()
    except Exception:
        return None


def _dias_restantes(fecha_fin: str) -> int | None:
    fecha = _parse_fecha(fecha_fin)
    if not fecha:
        return None
    return (fecha - date.today()).days


def _cargar_estado_notificaciones() -> tuple[str, set[int]]:
    cfg = get_notificaciones_config()
    fecha_actual = date.today().isoformat()
    ids_raw = cfg.get("ids_notificados") or ""
    ids = set()
    for item in ids_raw.split(","):
        item = item.strip()
        if not item:
            continue
        try:
            ids.add(int(item))
        except ValueError:
            continue
    if cfg.get("ultima_fecha") != fecha_actual:
        return fecha_actual, set()
    return fecha_actual, ids


def _guardar_estado_notificaciones(fecha: str, ids: set[int]) -> None:
    ids_str = ",".join(str(i) for i in sorted(ids))
    set_notificaciones_config(ultima_fecha=fecha, ids_notificados=ids_str)


def _formatear_alertas(alertas: List[Tuple[object, int]]) -> str:
    lineas = []
    for evento, dias in alertas[:5]:
        fecha = evento.fecha_fin
        detalle = evento.asignatura or evento.carrera or ""
        sufijo = f" • {detalle}" if detalle else ""
        lineas.append(f"- {evento.titulo} (vence {fecha}, {dias}d){sufijo}")
    extra = ""
    if len(alertas) > 5:
        extra = f"\n... y {len(alertas) - 5} más"
    return "\n".join(lineas) + extra


def revisar_y_notificar(parent=None) -> int:
    cfg = get_notificaciones_config()
    if not cfg.get("habilitado", True):
        return 0

    umbral = int(cfg.get("umbral_dias") or 1)
    incluir_hoy = bool(cfg.get("incluir_hoy", True))

    servicio = EventosUnificadosService(ruta_db=None)
    eventos = servicio.obtener_actividades()

    alertas: List[Tuple[object, int]] = []
    for evento in eventos:
        dias = _dias_restantes(evento.fecha_fin)
        if dias is None:
            continue
        if dias < 0:
            continue
        if not incluir_hoy and dias == 0:
            continue
        if dias <= umbral:
            alertas.append((evento, dias))

    if not alertas:
        return 0

    fecha_hoy, ids_notificados = _cargar_estado_notificaciones()
    nuevas = [(e, d) for (e, d) in alertas if e.id_evento not in ids_notificados]

    if not nuevas:
        return 0

    mensaje = _formatear_alertas(sorted(nuevas, key=lambda x: x[1]))
    try:
        showinfo(
            "Actividades próximas a vencer",
            mensaje,
            parent=parent,
        )
    except Exception as e:
        logger.error(f"Error al mostrar notificación: {e}", exc_info=True)
        return 0

    for evento, _ in nuevas:
        ids_notificados.add(evento.id_evento)
    _guardar_estado_notificaciones(fecha_hoy, ids_notificados)
    return len(nuevas)


def obtener_intervalo_ms() -> int:
    cfg = get_notificaciones_config()
    intervalo_min = int(cfg.get("intervalo_min") or 60)
    return max(1, intervalo_min) * 60 * 1000
