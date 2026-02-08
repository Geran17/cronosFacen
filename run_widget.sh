#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# En lanzadores .desktop, PATH puede no incluir ~/.local/bin.
export PATH="$HOME/.local/bin:$PATH"

if [[ -x "$HOME/.local/bin/pipenv" ]]; then
  exec "$HOME/.local/bin/pipenv" run python3 "$SCRIPT_DIR/src/widget_desktop.py"
fi

if command -v pipenv >/dev/null 2>&1; then
  exec "$(command -v pipenv)" run python3 "$SCRIPT_DIR/src/widget_desktop.py"
fi

exec python3 "$SCRIPT_DIR/src/widget_desktop.py"
