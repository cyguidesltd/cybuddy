#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PATH="${VENV_PATH:-"$PROJECT_ROOT/.venv"}"

if [ ! -d "$VENV_PATH" ]; then
  python -m venv "$VENV_PATH"
fi

# shellcheck disable=SC1090
source "$VENV_PATH/bin/activate"

python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r "$PROJECT_ROOT/requirements.txt"

if ! python -m pip show --quiet cybuddy >/dev/null 2>&1; then
  python -m pip install --quiet "$PROJECT_ROOT"
fi

exec "$VENV_PATH/bin/cybuddy" "$@"
