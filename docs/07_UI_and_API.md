---
tags: [tmage, ui]
---
# UI and API

A local web UI: a single file (`app/static/index.html`, dependency-free JS) + Python `http.server` (`app/server.py`). Start with `~/tmage/run.sh`, then open `http://127.0.0.1:8765`. From another PC: `TMAGE_HOST=0.0.0.0 ./run.sh` (Tailscale/local network only).

## Sections
1. **Circuit:** file browser (shortcut to the USB `tb/inputs`) or paste; `.subckt`, ports, `.param` and available analyses are extracted; an adaptation band appears if the technology does not match.
2. **Topology:** DA, FCO, TSO, BGR, COMP, OSC, LNA, custom. Guessed from the file name/subckt.
3. **Technology:** SAED90 / SKY130 / 130 nm, simulator, VDD, PDK path, temperatures, corners.
4. **Analyses:** the analyses in the catalog, defaults ticked per topology, parameters editable.
5. **LLM:** Ollama (Jetson, models listed live), OpenAI-compatible; a separate model for each agent.
Right panel: summary, missing-item warnings, save, recent jobs, and the **run panel** (live log, stage status, report).

## API
| Endpoint | Job |
|---|---|
| `GET /api/config` | Catalog + environment |
| `GET /api/fs`, `/api/file` | File browser (only home, `/run/media`, `/data`, `/opt/synopsys`) |
| `POST /api/parse`, `/api/adapt` | Netlist parsing, adaptation to the technology |
| `GET /api/models?url=` | Ollama model list (private/Tailscale addresses only: SSRF protection) |
| `GET/POST /api/state` | UI state (`config/ui_state.json`) |
| `POST /api/jobs`, `GET /api/jobs` | Save/list jobs |
| `POST /api/run/start`, `GET /api/run/log` | Start a run, follow the log |

## Security notes
Only `127.0.0.1` by default. File access is limited to the allowed roots; file reading is text extensions only, 2 MB at most.

## Test method
Screenshot with headless Firefox: `MOZ_HEADLESS=1 firefox --no-remote --profile <temp> --screenshot out.png URL` (a temporary delay hook is needed for asynchronous loading).
