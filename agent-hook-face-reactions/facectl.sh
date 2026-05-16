#!/usr/bin/env bash
set -u

AGENT_FACE_HOME="${AGENT_FACE_HOME:-$HOME/.agents/tablet-face}"
PROJECT_DIR="$AGENT_FACE_HOME"
PORT="${AGENT_FACE_PORT:-8000}"
PID_FILE="$AGENT_FACE_HOME/server.pid"
STATE_FILE="$AGENT_FACE_HOME/state.json"
SERVER="$AGENT_FACE_HOME/server.py"

STATE="${1:-happy}"
SOURCE="${2:-unknown}"

case "$STATE" in
  happy|thinking|loading|attention|blocked|needs-info|need-info|need_info|needs_info|context) ;;
  *) STATE="happy" ;;
esac

case "$SOURCE" in
  codex|gemini|claude|ollama|local|unknown) ;;
  *) SOURCE="unknown" ;;
esac

mkdir -p "$(dirname "$STATE_FILE")"
python3 - "$STATE_FILE" "$STATE" "$SOURCE" <<'PY'
import json
import sys
import time
from pathlib import Path

path = Path(sys.argv[1])
payload = {
    "state": sys.argv[2],
    "source": sys.argv[3],
    "updated_at": int(time.time()),
}
path.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
PY

if curl -fsS "http://127.0.0.1:$PORT/" > /dev/null 2>&1; then
  exit 0
fi

cd "$PROJECT_DIR" || exit 0
nohup python3 "$SERVER" > /dev/null 2>&1 &
echo $! > "$PID_FILE"
