---
tags: [tmage, logging]
---
# Logging

`engine/log.py`. The `logs/` folder of every run:

| File | Content |
|---|---|
| `run.log` | Human-readable log (time, level, message) |
| `events.jsonl` | The same events, structured (duration, model, tokens, measurements) |
| `llm/NNN_stage_cN_aN.json` | The **full** request/reply of every LLM call, duration, tokens, error list |
| `sim/cand<i>_<test>.txt` | Every HSPICE screen output |
| `status.json` | `running/done/failed`, stage, duration, pid |

General events (saving a job, starting a run): `~/tmage/logs/tmage.log`.

## How to read it
```bash
tail -f runs/<id>/logs/run.log
jq . runs/<id>/logs/llm/003_stimulus_c0_a1.json | less
```
The run panel in the UI shows the same log live.

## Safeguards
- The license port is tried before a run starts and before every HSPICE call; without the VPN the run stops with a clear message (`LicenseError`) and the model is not blamed.
- If `Unable to checkout` is found in the HSPICE output it counts as a license error.
- The process id is recorded; a run that was left half-done does not appear as "running" and block a new one.
