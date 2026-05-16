# Agent Hook Face Reactions

Turn an old tablet into an ambient face display for AI agent hooks.

The tablet only needs a browser. Your computer runs a tiny local server, and any CLI agent hook can call one shared command:

```bash
~/.agents/tablet-face/facectl.sh <state> <source>
```

That makes the display useful across Codex, Claude, Gemini, local Ollama models, or any other tool that can run a shell command.

## Why `~/.agents`

Use `~/.agents/tablet-face` as the shared runtime folder so the face display is not owned by one CLI.

```text
~/.agents/
  tablet-face/
    facectl.sh
    index.html
    server.py
    state.json
```

Codex, Claude, Gemini, and local model tools can all write to the same `state.json`. The tablet watches one browser page instead of needing separate displays per agent.

## Install

Copy the runtime files:

```bash
mkdir -p ~/.agents/tablet-face
cp index.html facectl.sh server.py ~/.agents/tablet-face/
chmod +x ~/.agents/tablet-face/facectl.sh ~/.agents/tablet-face/server.py
```

Trigger the first face:

```bash
~/.agents/tablet-face/facectl.sh happy codex
```

Open the display on the same machine:

```text
http://127.0.0.1:8000/
```

Open it from a tablet on the same Wi-Fi:

```text
http://<your-computer-lan-ip>:8000/
```

On macOS, one way to find your LAN IP is:

```bash
ifconfig | grep "inet "
```

## States

Supported states:

```text
happy
thinking
loading
attention
blocked
needs-info
```

Aliases for `needs-info`:

```text
need-info
need_info
needs_info
context
```

Examples:

```bash
~/.agents/tablet-face/facectl.sh thinking codex
~/.agents/tablet-face/facectl.sh needs-info claude
~/.agents/tablet-face/facectl.sh blocked gemini
~/.agents/tablet-face/facectl.sh happy ollama
```

## Sources

Supported sources:

```text
codex
claude
gemini
ollama
local
unknown
```

The demo theme currently keeps one visual identity while still accepting source names, so hooks can record who triggered the face without needing separate browser pages.

## Hook Examples

Example snippets live in:

```text
examples/codex/
examples/claude/
examples/gemini/
```

### Codex

The Codex example includes:

```text
examples/codex/tablet_face.py
examples/codex/notification_audio_minimal.py
```

The minimal notification hook maps:

```text
agent-turn-complete -> happy
approval-requested -> needs-info
fallback -> thinking
```

### Claude

See:

```text
examples/claude/settings-snippet.json
```

It shows commands like:

```bash
~/.agents/tablet-face/facectl.sh thinking claude
```

### Gemini

See:

```text
examples/gemini/settings-snippet.json
```

It shows commands like:

```bash
~/.agents/tablet-face/facectl.sh thinking gemini
```

## File Preview Mode

You can open `index.html` directly with `file://` to preview the face pool. In file preview mode, the page randomly rotates through available face states because it cannot fetch `/state.json`.

For the real display, use the local server URL:

```text
http://<your-computer-lan-ip>:8000/
```

## Old Tablet Notes

This works well for old tablets because the tablet only needs to:

- connect to Wi-Fi
- open a browser
- stay plugged in
- display a simple local network page

Chrome on an old Android tablet is usually enough. A kiosk APK could be a later upgrade, but the first version does not need one.

## Safety

Hooks should be fast and non-blocking. If a hook calls this command, it should not depend on the tablet being awake. `facectl.sh` writes state and starts the server opportunistically; failures should not break the agent workflow.
