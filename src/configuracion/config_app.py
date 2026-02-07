from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path
from typing import Optional


CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "settings.conf"


def _load_config() -> ConfigParser:
    config = ConfigParser()
    config.read(CONFIG_PATH)
    return config


def get_tema() -> Optional[str]:
    config = _load_config()
    return config.get("UI", "tema", fallback=None)


def set_tema(tema: str) -> None:
    config = _load_config()
    if "UI" not in config:
        config["UI"] = {}
    config["UI"]["tema"] = tema
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        config.write(f)


DEFAULT_TABS = {
    "dashboard": True,
    "bienvenida": True,
    "calendario": True,
    "actividades": True,
    "alertas": True,
    "carreras": True,
    "cuellos": True,
    "configuraciones": True,
}


def get_tabs_visibility() -> dict:
    config = _load_config()
    vis = DEFAULT_TABS.copy()
    for key in DEFAULT_TABS:
        val = config.get("UI", f"tab_{key}", fallback=str(DEFAULT_TABS[key]))
        vis[key] = str(val).strip().lower() in ("1", "true", "yes", "y", "on")
    return vis


def set_tabs_visibility(visibility: dict) -> None:
    config = _load_config()
    if "UI" not in config:
        config["UI"] = {}
    for key, value in visibility.items():
        config["UI"][f"tab_{key}"] = "True" if value else "False"
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        config.write(f)


def get_pin_hash() -> Optional[str]:
    config = _load_config()
    val = config.get("UI", "pin_hash", fallback="").strip()
    return val or None


def set_pin_hash(pin_hash: Optional[str]) -> None:
    config = _load_config()
    if "UI" not in config:
        config["UI"] = {}
    config["UI"]["pin_hash"] = pin_hash or ""
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        config.write(f)


def get_actividades_tipo_filtro() -> int:
    config = _load_config()
    val = config.get("UI", "filtro_tipo_actividad", fallback="0").strip()
    try:
        return int(val)
    except ValueError:
        return 0


def set_actividades_tipo_filtro(id_tipo: Optional[int]) -> None:
    config = _load_config()
    if "UI" not in config:
        config["UI"] = {}
    config["UI"]["filtro_tipo_actividad"] = str(id_tipo or 0)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        config.write(f)


def get_alertas_filtros() -> dict:
    config = _load_config()
    return {
        "carrera": config.get("UI", "alertas_carrera", fallback="Todos").strip(),
        "asignatura": config.get("UI", "alertas_asignatura", fallback="Todos").strip(),
        "tipo": config.get("UI", "alertas_tipo", fallback="Todos").strip(),
        "rango": config.get("UI", "alertas_rango", fallback="Todas").strip(),
    }


def set_alertas_filtros(
    carrera: str = "Todos",
    asignatura: str = "Todos",
    tipo: str = "Todos",
    rango: str = "Todas",
) -> None:
    config = _load_config()
    if "UI" not in config:
        config["UI"] = {}
    config["UI"]["alertas_carrera"] = carrera or "Todos"
    config["UI"]["alertas_asignatura"] = asignatura or "Todos"
    config["UI"]["alertas_tipo"] = tipo or "Todos"
    config["UI"]["alertas_rango"] = rango or "Todas"
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        config.write(f)


def get_backup_settings() -> dict:
    config = _load_config()
    return {
        "dir": config.get("UI", "backup_dir", fallback="").strip(),
        "keep_days": _get_int(config, "UI", "backup_keep_days", 30),
        "keep_last": _get_int(config, "UI", "backup_keep_last", 5),
    }


def set_backup_settings(backup_dir: str, keep_days: int, keep_last: int) -> None:
    config = _load_config()
    if "UI" not in config:
        config["UI"] = {}
    config["UI"]["backup_dir"] = backup_dir or ""
    config["UI"]["backup_keep_days"] = str(keep_days)
    config["UI"]["backup_keep_last"] = str(keep_last)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        config.write(f)


def get_notificaciones_config() -> dict:
    config = _load_config()
    habilitado = config.get("UI", "notificaciones_habilitadas", fallback="True").strip()
    incluir_hoy = config.get("UI", "notificaciones_incluir_hoy", fallback="True").strip()
    return {
        "habilitado": habilitado.lower() in ("1", "true", "yes", "y", "on"),
        "umbral_dias": _get_int(config, "UI", "notificaciones_umbral_dias", 1),
        "intervalo_min": _get_int(config, "UI", "notificaciones_intervalo_min", 60),
        "incluir_hoy": incluir_hoy.lower() in ("1", "true", "yes", "y", "on"),
        "ultima_fecha": config.get("UI", "notificaciones_ultima_fecha", fallback="").strip(),
        "ids_notificados": config.get("UI", "notificaciones_ids", fallback="").strip(),
    }


def set_notificaciones_config(
    habilitado: Optional[bool] = None,
    umbral_dias: Optional[int] = None,
    intervalo_min: Optional[int] = None,
    incluir_hoy: Optional[bool] = None,
    ultima_fecha: Optional[str] = None,
    ids_notificados: Optional[str] = None,
) -> None:
    config = _load_config()
    if "UI" not in config:
        config["UI"] = {}
    if habilitado is not None:
        config["UI"]["notificaciones_habilitadas"] = "True" if habilitado else "False"
    if umbral_dias is not None:
        config["UI"]["notificaciones_umbral_dias"] = str(int(umbral_dias))
    if intervalo_min is not None:
        config["UI"]["notificaciones_intervalo_min"] = str(int(intervalo_min))
    if incluir_hoy is not None:
        config["UI"]["notificaciones_incluir_hoy"] = "True" if incluir_hoy else "False"
    if ultima_fecha is not None:
        config["UI"]["notificaciones_ultima_fecha"] = ultima_fecha
    if ids_notificados is not None:
        config["UI"]["notificaciones_ids"] = ids_notificados
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        config.write(f)


def _get_int(config: ConfigParser, section: str, key: str, fallback: int) -> int:
    val = config.get(section, key, fallback=str(fallback)).strip()
    try:
        return int(val)
    except ValueError:
        return fallback
