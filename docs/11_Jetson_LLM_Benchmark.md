---
tags: [tmage, llm, benchmark, jetson]
---
# Jetson LLM comparison

**Goal:** Find the best local model for each agent (spec, scenario, stimulus, measure). Tool: `engine/bench.py`. The larger per-model benchmark on DA/FCO/TSO is described in [[22_Benchmark_Findings]].

## Models (Orin Nano, Ollama)
qwen2.5:0.5b · llama3.2:1b · qwen3:4b-instruct · qwen3.5:4b · mistral · qwen2.5:7b · command-r7b · ministral-3:8b · gpt-oss:20b (13.8 GB, crashes Ollama on this device).

## Fair comparison method
Every agent is tested **with the reference outputs of the other stages**:
| Agent | Input | Score |
|---|---|---|
| spec | circuit | share of correct port roles |
| scenario | reference spec | coverage of the selected analyses |
| stimulus | reference spec/scenario + reference `.meas` | are the HSPICE measurements within 10 % of the reference |
| measure | reference testbench | same |

Reference: a hand-written DA testbench (single supply 1.2 V, Vcm=0.6 V) is run first; its measurements are the target. Recorded: score, duration, number of attempts, tokens/s.

## Running
```bash
python3 engine/bench.py                 # all models
python3 engine/bench.py --models qwen3.5:4b,mistral:latest --timeout 420
```
Output: `bench/<date>/report.md` (table + recommendation per agent), `results.json`, full logs per model. The VPN must be connected.

## First observations (qwen3.5:4b, single run)
| Stage | Duration | Tokens |
|---|---|---|
| spec | 96 s | 633 |
| scenario | 39 s | 408 |
| stimulus | 131 s | 1321 |
| measure | 33 s | 283 |
About 6.6 tokens/s. The JSON was valid, but the testbench had placeholders and a missing source, so the rules in [[08_Agent_Data_Handoff]] and a pre-validation were added.

Results and recommendations: [[16_Report_Jetson_LLM]].
