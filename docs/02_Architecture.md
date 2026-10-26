---
tags: [tmage, architecture]
---
# Architecture

```
Web UI  ──job.json──▶  runs/<id>/
                         │  context.json  (standard summary for the LLMs)
                         ▼
 spec ─▶ scenario ─▶ stimulus ─▶ measure ─▶ [HSPICE] ─▶ verify (rules + vote) ─▶ report
(script)  (script)     (LLM)       (LLM)       script        script                 script
```

The figures in the README ([architecture](images/architecture.png), [pipeline](images/pipeline.png)) show the same flow. In the first version spec and scenario were also LLM stages; they are done by script now.

## Folders (`~/tmage`)
| Path | Role |
|---|---|
| `app/server.py`, `app/static/index.html` | Web UI and API ([[07_UI_and_API]]) |
| `config/catalog.json` | Topologies, technologies, analyses, agents, providers |
| `config/stages.json` | Stage schemas and agent tasks ([[08_Agent_Data_Handoff]]) |
| `config/env.sh` | HSPICE path, license, PDK (example: `env.sh.example`) |
| `engine/handoff.py` | Context generation, stage validation, prompt building |
| `engine/pipeline.py` | The pipeline ([[09_Logging]], [[10_Verification_Voting]]) |
| `engine/llm.py`, `sim.py`, `log.py` | Ollama call, HSPICE run, logging |
| `engine/bench.py` | Model comparison ([[11_Jetson_LLM_Benchmark]]) |
| `runs/` | Run outputs (not committed) |

## Design decisions
- **Whatever a script can do, a script does:** netlist parsing, the PDK line, the corner loop, the HSPICE run, reading measurements, rules, report format. The LLM is used only where judgement or creativity is needed.
- **No dependencies:** the server and the engine use only the Python standard library (3.9).
- **Hand-off with a fixed schema:** [[08_Agent_Data_Handoff]].
- **Verification:** voting + rule checks instead of LLM-as-judge ([[10_Verification_Voting]]).
