from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timedelta
from typing import Optional

from configuracion.config_app import get_backup_settings
from scripts.logging_config import obtener_logger_modulo
from utilidades.config import RUTA_DB

logger = obtener_logger_modulo(__name__)

BACKUP_PREFIX = "cronos_backup_"
BACKUP_EXT = ".sqlite"


def crear_backup_al_cerrar() -> Optional[str]:
    settings = get_backup_settings()
    backup_dir = settings["dir"]
    if not backup_dir:
        logger.info("Backup omitido: no hay carpeta configurada")
        return None

    if not os.path.exists(RUTA_DB):
        logger.warning(f"Backup omitido: no existe la base de datos {RUTA_DB}")
        return None

    try:
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{BACKUP_PREFIX}{timestamp}{BACKUP_EXT}"
        backup_path = os.path.join(backup_dir, backup_name)

        with sqlite3.connect(RUTA_DB, timeout=10.0) as src_conn:
            with sqlite3.connect(backup_path) as dst_conn:
                src_conn.backup(dst_conn)

        _aplicar_retencion(backup_dir, settings["keep_days"], settings["keep_last"])
        logger.info(f"Backup creado: {backup_path}")
        return backup_path
    except Exception as e:
        logger.error(f"Error al crear backup: {e}", exc_info=True)
        return None


def crear_backup_ahora() -> Optional[str]:
    return crear_backup_al_cerrar()


def _aplicar_retencion(backup_dir: str, keep_days: int, keep_last: int) -> None:
    archivos = _listar_backups(backup_dir)
    if not archivos:
        return

    now = datetime.now()

    if keep_days and keep_days > 0:
        limite = now - timedelta(days=keep_days)
        for path in list(archivos):
            try:
                mtime = datetime.fromtimestamp(os.path.getmtime(path))
                if mtime < limite:
                    os.remove(path)
                    archivos.remove(path)
            except Exception as e:
                logger.warning(f"No se pudo borrar backup antiguo {path}: {e}")

    if keep_last and keep_last > 0:
        archivos.sort(key=lambda p: os.path.getmtime(p), reverse=True)
        for path in archivos[keep_last:]:
            try:
                os.remove(path)
            except Exception as e:
                logger.warning(f"No se pudo borrar backup excedente {path}: {e}")


def _listar_backups(backup_dir: str) -> list[str]:
    try:
        return [
            os.path.join(backup_dir, f)
            for f in os.listdir(backup_dir)
            if f.startswith(BACKUP_PREFIX) and f.endswith(BACKUP_EXT)
        ]
    except Exception:
        return []
