#!/usr/bin/env python3
"""Tiny bridge from Codex hooks to the shared agent face display."""
from __future__ import annotations

import subprocess
from pathlib import Path

FACECTL = Path.home() / ".agents" / "tablet-face" / "facectl.sh"


def trigger_face(state: str | None, source: str = "codex") -> None:
    if not state or not FACECTL.exists():
        return

    try:
        subprocess.Popen(
            [str(FACECTL), state, source],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    except Exception:
        pass
