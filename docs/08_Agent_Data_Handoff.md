---
tags: [tmage, agents, schema]
---
# Data hand-off between agents

User choices are saved and passed to the agents in a **fixed format** (`engine/handoff.py`, `config/stages.json`).

## Run folder (`runs/<date>_<name>/`)
| File | Meaning |
|---|---|
| `job.json` | The user's choices (immutable) |
| `circuit.sp` | The circuit (the adapted version if it was adapted) |
| `context.json` | Standard summary given to the LLMs (immutable) |
| `stages/NN_name.json` | Output of each stage |
| `trace.jsonl` | Who, when, which model |

## Contents of `context.json`
Technology (VDD, `.lib` line per corner, device names, notes) · circuit (subckt, ports, **port-role hints produced by the script**, parameters) · topology · selected analyses (metrics, parameters) · verification settings · agent-to-model mapping.

## Stages
`spec -> scenario -> stimulus -> measure -> verify -> report`. Each stage has a `needs` list; an agent sees only `context` + the outputs of those stages. Asking for an unfinished stage is an error.

## Rules
- The output is a single JSON object; the fields in the schema are required (a missing field makes the write be rejected).
- To the agents: use only the information in the context, do not invent, write uncertainty into `open_questions` / `assumptions`.
- **stimulus:** placeholders (`{...}`, `context.`) are forbidden and numbers are written literally; the DUT call is `X0 <ports> <subckt>`; `.lib/.inc/.end/.meas` are not written (the system adds them); a concrete example is in the prompt.
- **report** and **verify** are produced by script; the numbers come from the HSPICE output.
