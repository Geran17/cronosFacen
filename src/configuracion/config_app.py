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
