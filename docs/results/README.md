# Benchmark results (summaries)

Small result files of every batch. Raw run data (`batch/`, about 200 MB of HSPICE output) stays local and is not in the repository.

| Folder | What | Prompts |
|---|---|---|
| `model_bench_20261026/` | 9 models alone, DA/FCO/TSO x 3 runs | v2 |
| `mixed_vote_20261027/` | qwen3:4b-instruct + command-r7b + deepseek-coder:6.7b | v3 |
| `model_bench_new_20261028/` | 6 new models alone (qwen3:8b, llama3.1:8b, gemma4:e4b, nemotron-3-nano:4b, yi-coder:9b, glm4:9b) | v3 |
| `random_triples_20261028/` | random 3-model votes; **interrupted** by a reboot: T1 DA done, FCO 2 of 3 runs, T2-T4 never ran | v3 |

`recomputed.json` = per run: candidates ok, majority, winner, accuracy vs the hand reference, dropped-candidate causes (made by `scripts/recompute_scores.py`).
Reports: `../23_Model_Benchmark_Report.md`, `../27_New_Models_Benchmark_Report.md`; all logs: `../24_All_Runs_Log.md`.
