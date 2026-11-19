# Run coverage

Generated 2026-11-20 00:52 by `scripts/run_coverage.py`. Cell = runs finished `done` / runs planned (3 per circuit); the status `failed` or a timeout counts as not done.

## 1. Single-model benchmark (each model alone, 3 candidates, 3 runs per circuit)

| Model | Prompts v2 (DA / FCO / TSO) | Prompts v3 (DA / FCO / TSO) |
|---|---|---|
| command-r7b:latest | 3/3 / 3/3 / 3/3 | **missing** |
| deepseek-coder:6.7b | 3/3 / 3/3 / 3/3 | **missing** |
| gemma4:e4b | **missing** | 3/3 / 1/3 / 0/3 |
| glm4:9b | **missing** | 2/3 / 3/3 / 3/3 |
| llama3.1:8b | **missing** | 3/3 / 3/3 / 3/3 |
| ministral-3:8b | 2/3 / 3/3 / 1/3 | **missing** |
| nemotron-3-nano:4b | **missing** | 1/3 / 0/3 / 1/3 |
| qwen2.5-coder:7b | 3/3 / 3/3 / 2/3 | **missing** |
| qwen2.5:7b | 3/3 / 1/3 / 3/3 | **missing** |
| qwen3.5:4b | 3/3 / 3/3 / 3/3 | **missing** |
| qwen3.5:4b-q8_0 | 3/3 / 3/3 / 3/3 | **missing** |
| qwen3:4b-instruct | 3/3 / 3/3 / 3/3 | **missing** |
| qwen3:4b-instruct-2507-q8_0 | 3/3 / 3/3 / 3/3 | **missing** |
| qwen3:8b | **missing** | 3/3 / 3/3 / 3/3 |
| yi-coder:9b | **missing** | 3/3 / 2/3 / 2/3 |

## 2. Mixed votes (different model per candidate)

| Batch | Voters | DA | FCO | TSO | Prompts |
|---|---|---|---|---|---|
| mixed_vote_20261027 | qwen3:4b-instruct, command-r7b, deepseek-coder:6.7b | 3/3 | 3/3 | 3/3 | v3 |
| random_triples T1 | llama3.1:8b, qwen3:8b, deepseek-coder:6.7b | 3/3 | 2/3 | **missing** | v3 |
| random_triples T2 | deepseek-coder:6.7b, qwen3:4b-instruct-2507-q8_0, qwen3:8b | **missing** | **missing** | **missing** | v3 |
| random_triples T3 | qwen3:8b, command-r7b:latest, qwen3:4b-instruct-2507-q8_0 | **missing** | **missing** | **missing** | v3 |
| random_triples T4 | qwen3:4b-instruct-2507-q8_0, llama3.1:8b, qwen3:4b-instruct | **missing** | **missing** | **missing** | v3 |

The random triples were interrupted by a reboot on 2026-11-09 (T1 FCO stopped at run 3 of 3 started; TSO and T2-T4 never ran).

## 3. What is missing

1. **Prompt versions are not comparable between model groups:** the four earlier models (qwen3:4b-instruct Q4/Q8, command-r7b, deepseek-coder:6.7b) were measured alone only with prompts v2, the six new models only with v3. A fair ranking needs both groups on the same prompts.
2. **Random 3-model votes:** T1 incomplete, T2, T3, T4 not run (see section 2).
3. **Models taken offline** (qwen3.5:4b, qwen3.5:4b Q8, qwen2.5:7b, qwen2.5-coder:7b, ministral-3:8b) have v2 data only, by decision.
4. **Circuits never run:** BGR, LNA (script drafts missing), COMP and OSC (flat netlists need a `.subckt` wrapper).
5. **No ablation runs** yet (no RAG / no pitfalls / no sanity rules / single candidate vs vote).
6. **No CLI-model runs** (`cli:claude`, `cli:codex`) yet; the backend exists since 2026-11-20, `codex` is not installed on this machine.
