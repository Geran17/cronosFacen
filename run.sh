#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_BIN="$SCRIPT_DIR/dist/cronosFacen/cronosFacen"

if [[ ! -x "$APP_BIN" ]]; then
  echo "No se encontró el ejecutable en: $APP_BIN"
  echo "Genera el build primero con PyInstaller."
  exit 1
fi

exec "$APP_BIN"
