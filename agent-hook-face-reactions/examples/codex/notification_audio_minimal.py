#!/usr/bin/env python3
"""Example Codex notify hook that triggers the shared face display.

Codex config example:
notify = ["python3", "/path/to/notification_audio_minimal.py"]
"""
from __future__ import annotations

import json
import sys

from tablet_face import trigger_face

FACE_BY_EVENT = {
    "agent-turn-complete": "happy",
    "approval-requested": "needs-info",
}


def main() -> int:
    if len(sys.argv) < 2:
        return 0

    try:
        payload = json.loads(sys.argv[1])
    except Exception:
        return 0

    trigger_face(FACE_BY_EVENT.get(payload.get("type"), "thinking"), "codex")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
