#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

AGENT_FACE_HOME = Path(os.environ.get("AGENT_FACE_HOME", Path.home() / ".agents" / "tablet-face"))
PROJECT_DIR = AGENT_FACE_HOME
STATE_FILE = AGENT_FACE_HOME / "state.json"
PORT = int(os.environ.get("AGENT_FACE_PORT", "8000"))


class AgentFaceHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PROJECT_DIR), **kwargs)

    def do_GET(self):
        if self.path.split("?", 1)[0] in {"/state.json", "/state.txt"}:
            self.send_state()
            return
        super().do_GET()

    def send_state(self):
        if STATE_FILE.exists():
            body = STATE_FILE.read_bytes()
        else:
            body = json.dumps({"state": "happy", "source": "unknown"}).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", PORT), AgentFaceHandler)
    server.serve_forever()
