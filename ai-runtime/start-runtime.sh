#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
CONFIG_PATH=${INFINITY_AI_CONFIG:-"$SCRIPT_DIR/runtime-config.json"}

exec python3 "$SCRIPT_DIR/server.py" --config "$CONFIG_PATH" "$@"
