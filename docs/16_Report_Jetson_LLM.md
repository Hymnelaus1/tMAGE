---
tags: [tmage, report, llm, benchmark]
---
# Report: Jetson LLM comparison and improvements (2026-10-25)

Method: [[11_Jetson_LLM_Benchmark]]. Task: an `ac_loop` + `power_area` testbench for the DA (differential amplifier) on SAED90nm. Score = share of measurements within 10 % of the hand-written reference. **A single run, a single topology (DA).** The larger benchmark on DA, FCO and TSO is in [[22_Benchmark_Findings]].

## Hardware characteristics
- Jetson Orin Nano (8 GB): about 4 to 13 tokens per second (4B models 7 to 13, 7B to 8B models 4 to 7). The duration depends mostly on the output length.
- All the models are **Q4_K_M** (gpt-oss MXFP4). `gpt-oss:20b` (13.8 GB) does not fit in memory and crashes the Ollama server: unusable.
- Models below 4B (0.5B, 1B) were dropped (they could not produce valid JSON on the first try).

## Before / after (total time and score)
| Model | Baseline mode | Improved mode |
|---|---|---|
| qwen3:4b-instruct | stimulus 0.00, measure 0.00 · 319 s | **1.00 / 1.00 · 78 s** |
| qwen3.5:4b | stimulus 0.75, measure 0.00 · 150 s | **1.00 / 1.00 · 91 s** |
| qwen2.5:7b | stimulus 0.25, measure 0.00 · 252 s | **1.00 / 1.00 · 91 s** |

Other models in improved mode: command-r7b 1.00/1.00 (131 s) · mistral stimulus 0.00 (it writes the testbench like code), measure 1.00 · ministral-3:8b 0.75/0.25 (`.meas` syntax errors).

## Failure patterns in baseline mode
`{context...}` placeholders, a missing source, `duplicated subckt`, `.meas` syntax errors, long/loose JSON.

## Improvements made (`TMAGE_IMPROVED=1`)
1. **Script first:** spec (port roles) and scenario (selected analyses) by script; no LLM call was needed (a gain of 96 s + 39 s).
2. **Draft, then the LLM corrects:** the script produces a draft testbench and `.meas` lines with verified syntax; the model builds on the draft.
3. **RAG:** real testbench and `.meas` examples from the kit are added to the prompt by topology/metric (`knowledge/`, `engine/rag.py`).
4. **Schema + example:** an Ollama JSON schema (first attempt only), a format example, a token limit, detection of truncated output.

Note: the improvements were measured as one bundle; the contribution of each one (ablation) has not been separated yet.

## Recommendation per agent
| Agent | Recommendation |
|---|---|
| spec | Script (port-name hints); `qwen2.5:7b` if a port is ambiguous |
| scenario | Script; `qwen3:4b-instruct` for a custom topology |
| stimulus | `qwen3:4b-instruct` ≈ `qwen3.5:4b` ≈ `qwen2.5:7b` (46 to 52 s); backup `command-r7b` |
| measure | `qwen3:4b-instruct` (27 s); backup `mistral` (33 s) |
| verification | For voting, from different families: `qwen3:4b-instruct`, `qwen2.5:7b`, `command-r7b` ([[10_Verification_Voting]]) |

## Limits
A single run (LLM variance), only the DA, the reference testbench is my own design, the mistral/ministral results are valid for this task. The draft templates exist for DA-like circuits (`ac_loop`, `cmrr`, `psrr`, `power_area`) for now.

## Next improvements
- Draft templates and RAG examples for FCO, TSO, BGR, COMP, OSC, LNA
- Ablation: the effect of each improvement on its own
- Repeated runs (variance), benchmarks on different topologies
- Embedding-based search for the RAG (an embedding model on the Jetson)
- Q8 versions of the 4B models (download approval was pending; they were tested later, see [[22_Benchmark_Findings]])
