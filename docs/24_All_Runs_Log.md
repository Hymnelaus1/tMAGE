# All runs: consolidated log

Generated 2026-10-28 23:40 by `scripts/collect_logs.py`. 106 distinct runs from `runs/` and `batch/`; 11044 log lines; 53 errors; 4864 warnings.

* Full text of every run: `docs/logs/all_runs_raw.log.gz` (`zcat docs/logs/all_runs_raw.log.gz | less`). License server and home path are scrubbed.
* Logs of the first two days (2026-10-25) are Turkish, later ones English; they are kept as recorded.
* Per-model results of the benchmark: `23_Model_Benchmark_Report.md`. Aggregated problems per run: `22_Benchmark_Findings.md`.

## 1. Overview by group

| Group | Runs | Errors | Warnings | Runs with a winner |
|---|---|---|---|---|
| runs | 9 | 1 | 99 | 0/9 |
| batch/20261025_204154 | 4 | 1 | 194 | 0/4 |
| batch/20261025_220928_v2 | 3 | 0 | 162 | 3/3 |
| batch/model_bench_20261026 | 81 | 46 | 4070 | 78/81 |
| batch/mixed_vote_20261027 | 9 | 5 | 339 | 9/9 |

## 2. Index of all runs

| # | Start | Group | Run | Circuit | Models | Err | Warn | Winner | Clusters |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-25 18:19:58 | runs | 20261025_181948_da_test1 | DA | qwen3.5:4b | 0 | 0 | - | - |
| 2 | 2026-10-25 19:50:43 | runs | 20261025_194626_da_ui_deneme | DA | qwen3:4b-instruct | 0 | 7 | - | - |
| 3 | 2026-10-25 19:58:54 | runs | 20261025_195854_da_oylama | DA | command-r7b:latest, qwen2.5:7b, qwen3:4b-instruct | 0 | 9 | - | - |
| 4 | 2026-10-25 20:10:59 | runs | 20261025_201059_da_yeni_analizler | DA | ajan, qwen3:4b-instruct | 0 | 29 | - | - |
| 5 | 2026-10-25 20:25:36 | runs | 20261025_202536_da_prompt_testi | DA | qwen3:4b-instruct | 1 | 0 | - | - |
| 6 | 2026-10-25 20:29:57 | runs | 20261025_202957_da_prompt_testi2 | DA | qwen3:4b-instruct | 0 | 15 | - | - |
| 7 | 2026-10-25 20:32:48 | runs | 20261025_203248_da_prompt_testi3 | DA | qwen3:4b-instruct | 0 | 10 | - | - |
| 8 | 2026-10-25 20:41:54 | batch/20261025_204154 | DA/rep1 | DA | command-r7b:latest, qwen2.5:7b, qwen3:4b-instruct | 0 | 36 | - | - |
| 9 | 2026-10-25 20:57:25 | batch/20261025_204154 | DA/rep2 | DA | command-r7b:latest, qwen2.5:7b, qwen3:4b-instruct | 1 | 26 | - | - |
| 10 | 2026-10-25 21:10:26 | batch/20261025_204154 | DA/rep3 | DA | command-r7b:latest, qwen2.5:7b, qwen3:4b-instruct | 0 | 32 | - | - |
| 11 | 2026-10-25 21:25:37 | batch/20261025_204154 | FCO/rep1 | FCO | command-r7b:latest, qwen2.5:7b, qwen3:4b-instruct | 0 | 100 | - | - |
| 12 | 2026-10-25 22:06:49 | runs | 20261025_220649_batch_FCO_r2 | FCO | qwen3:4b-instruct | 0 | 0 | - | - |
| 13 | 2026-10-25 22:09:28 | batch/20261025_220928_v2 | DA/rep1 | DA | command-r7b:latest, qwen2.5:7b, qwen3:4b-instruct | 0 | 38 | 0 | [[0, 2], [1]] |
| 14 | 2026-10-25 22:22:49 | batch/20261025_220928_v2 | DA/rep2 | DA | command-r7b:latest, qwen2.5:7b, qwen3:4b-instruct | 0 | 56 | 0 | [[0, 2], [1]] |
| 15 | 2026-10-25 22:38:20 | batch/20261025_220928_v2 | DA/rep3 | DA | command-r7b:latest, qwen2.5:7b, qwen3:4b-instruct | 0 | 68 | 0 | [[0], [1]] |
| 16 | 2026-10-25 23:00:41 | runs | 20261025_230041_batch_FCO_r1 | FCO | qwen2.5:7b, qwen3:4b-instruct | 0 | 29 | - | - |
| 17 | 2026-10-26 10:24:50 | batch/model_bench_20261026 | qwen3_4b-instruct/DA/rep1 | DA | qwen3:4b-instruct | 0 | 51 | 0 | [[0, 1, 2]] |
| 18 | 2026-10-26 10:32:50 | batch/model_bench_20261026 | qwen3_4b-instruct/DA/rep2 | DA | qwen3:4b-instruct | 0 | 27 | 0 | [[0, 2], [1]] |
| 19 | 2026-10-26 10:45:00 | batch/model_bench_20261026 | qwen3_4b-instruct/DA/rep3 | DA | qwen3:4b-instruct | 0 | 34 | 0 | [[0, 1], [2]] |
| 20 | 2026-10-26 10:57:21 | batch/model_bench_20261026 | qwen3_4b-instruct/FCO/rep1 | FCO | qwen3:4b-instruct | 0 | 29 | 0 | [[0, 1, 2]] |
| 21 | 2026-10-26 11:07:51 | batch/model_bench_20261026 | qwen3_4b-instruct/FCO/rep2 | FCO | qwen3:4b-instruct | 0 | 53 | 0 | [[0, 2]] |
| 22 | 2026-10-26 11:25:21 | batch/model_bench_20261026 | qwen3_4b-instruct/FCO/rep3 | FCO | qwen3:4b-instruct | 0 | 46 | 0 | [[0, 1], [2]] |
| 23 | 2026-10-26 11:43:51 | batch/model_bench_20261026 | qwen3_4b-instruct/TSO/rep1 | TSO | qwen3:4b-instruct | 0 | 36 | 0 | [[0, 1], [2]] |
| 24 | 2026-10-26 11:54:31 | batch/model_bench_20261026 | qwen3_4b-instruct/TSO/rep2 | TSO | qwen3:4b-instruct | 0 | 28 | 1 | [[1, 2], [0]] |
| 25 | 2026-10-26 12:07:21 | batch/model_bench_20261026 | qwen3_4b-instruct/TSO/rep3 | TSO | qwen3:4b-instruct | 0 | 29 | 0 | [[0, 1, 2]] |
| 26 | 2026-10-26 12:19:51 | batch/model_bench_20261026 | qwen3.5_4b/DA/rep1 | DA | qwen3.5:4b | 1 | 53 | 0 | [[0]] |
| 27 | 2026-10-26 12:33:11 | batch/model_bench_20261026 | qwen3.5_4b/DA/rep2 | DA | qwen3.5:4b | 1 | 61 | 0 | [[0], [1]] |
| 28 | 2026-10-26 12:50:01 | batch/model_bench_20261026 | qwen3.5_4b/DA/rep3 | DA | qwen3.5:4b | 0 | 76 | 1 | [[1], [2]] |
| 29 | 2026-10-26 13:07:41 | batch/model_bench_20261026 | qwen3.5_4b/FCO/rep1 | FCO | qwen3.5:4b | 0 | 40 | 0 | [[0, 2], [1]] |
| 30 | 2026-10-26 13:17:41 | batch/model_bench_20261026 | qwen3.5_4b/FCO/rep2 | FCO | qwen3.5:4b | 0 | 44 | 0 | [[0], [1], [2]] |
| 31 | 2026-10-26 13:27:51 | batch/model_bench_20261026 | qwen3.5_4b/FCO/rep3 | FCO | qwen3.5:4b | 0 | 39 | 0 | [[0, 2], [1]] |
| 32 | 2026-10-26 13:37:51 | batch/model_bench_20261026 | qwen3.5_4b/TSO/rep1 | TSO | qwen3.5:4b | 0 | 97 | 0 | [[0]] |
| 33 | 2026-10-26 13:56:12 | batch/model_bench_20261026 | qwen3.5_4b/TSO/rep2 | TSO | qwen3.5:4b | 0 | 116 | 2 | [[2]] |
| 34 | 2026-10-26 14:13:22 | batch/model_bench_20261026 | qwen3.5_4b/TSO/rep3 | TSO | qwen3.5:4b | 1 | 91 | 1 | [[1]] |
| 35 | 2026-10-26 14:31:42 | batch/model_bench_20261026 | qwen2.5_7b/DA/rep1 | DA | qwen2.5:7b | 0 | 27 | 0 | [[0], [1], [2]] |
| 36 | 2026-10-26 14:44:52 | batch/model_bench_20261026 | qwen2.5_7b/DA/rep2 | DA | qwen2.5:7b | 0 | 24 | 0 | [[0, 1], [2]] |
| 37 | 2026-10-26 14:57:52 | batch/model_bench_20261026 | qwen2.5_7b/DA/rep3 | DA | qwen2.5:7b | 0 | 28 | 0 | [[0, 1], [2]] |
| 38 | 2026-10-26 15:11:02 | batch/model_bench_20261026 | qwen2.5_7b/FCO/rep1 | FCO | qwen2.5:7b | 0 | 115 | None | [] |
| 39 | 2026-10-26 15:52:02 | batch/model_bench_20261026 | qwen2.5_7b/FCO/rep2 | FCO | qwen2.5:7b | 0 | 105 | None | [] |
| 40 | 2026-10-26 16:32:42 | batch/model_bench_20261026 | qwen2.5_7b/FCO/rep3 | FCO | qwen2.5:7b | 0 | 76 | 1 | [[1]] |
| 41 | 2026-10-26 17:04:12 | batch/model_bench_20261026 | qwen2.5_7b/TSO/rep1 | TSO | qwen2.5:7b | 0 | 26 | 0 | [[0], [1], [2]] |
| 42 | 2026-10-26 17:17:12 | batch/model_bench_20261026 | qwen2.5_7b/TSO/rep2 | TSO | qwen2.5:7b | 0 | 25 | 0 | [[0], [1], [2]] |
| 43 | 2026-10-26 17:30:22 | batch/model_bench_20261026 | qwen2.5_7b/TSO/rep3 | TSO | qwen2.5:7b | 0 | 26 | 0 | [[0], [1], [2]] |
| 44 | 2026-10-26 17:43:43 | batch/model_bench_20261026 | qwen2.5-coder_7b/DA/rep1 | DA | qwen2.5-coder:7b | 1 | 16 | 1 | [[1, 2]] |
| 45 | 2026-10-26 18:03:33 | batch/model_bench_20261026 | qwen2.5-coder_7b/DA/rep2 | DA | qwen2.5-coder:7b | 2 | 8 | 1 | [[1]] |
| 46 | 2026-10-26 18:31:33 | batch/model_bench_20261026 | qwen2.5-coder_7b/DA/rep3 | DA | qwen2.5-coder:7b | 1 | 17 | 1 | [[1], [2]] |
| 47 | 2026-10-26 18:56:13 | batch/model_bench_20261026 | qwen2.5-coder_7b/FCO/rep1 | FCO | qwen2.5-coder:7b | 1 | 21 | 1 | [[1], [2]] |
| 48 | 2026-10-26 19:17:53 | batch/model_bench_20261026 | qwen2.5-coder_7b/FCO/rep2 | FCO | qwen2.5-coder:7b | 1 | 59 | 2 | [[2]] |
| 49 | 2026-10-26 19:40:43 | batch/model_bench_20261026 | qwen2.5-coder_7b/FCO/rep3 | FCO | qwen2.5-coder:7b | 1 | 42 | 1 | [[1]] |
| 50 | 2026-10-26 20:11:53 | batch/model_bench_20261026 | qwen2.5-coder_7b/TSO/rep1 | TSO | qwen2.5-coder:7b | 1 | 23 | 1 | [[1, 2]] |
| 51 | 2026-10-26 20:36:53 | batch/model_bench_20261026 | qwen2.5-coder_7b/TSO/rep2 | TSO | qwen2.5-coder:7b | 0 | 24 | 1 | [[1, 2], [0]] |
| 52 | 2026-10-26 20:54:13 | batch/model_bench_20261026 | qwen2.5-coder_7b/TSO/rep3 | TSO | qwen2.5-coder:7b | 3 | 0 | None | [] |
| 53 | 2026-10-26 21:25:54 | batch/model_bench_20261026 | qwen3_4b-instruct-2507-q8_0/DA/rep1 | DA | qwen3:4b-instruct-2507-q8_0 | 0 | 41 | 1 | [[1, 2], [0]] |
| 54 | 2026-10-26 21:40:14 | batch/model_bench_20261026 | qwen3_4b-instruct-2507-q8_0/DA/rep2 | DA | qwen3:4b-instruct-2507-q8_0 | 0 | 31 | 0 | [[0, 1], [2]] |
| 55 | 2026-10-26 21:52:44 | batch/model_bench_20261026 | qwen3_4b-instruct-2507-q8_0/DA/rep3 | DA | qwen3:4b-instruct-2507-q8_0 | 0 | 32 | 0 | [[0], [1], [2]] |
| 56 | 2026-10-26 22:06:04 | batch/model_bench_20261026 | qwen3_4b-instruct-2507-q8_0/FCO/rep1 | FCO | qwen3:4b-instruct-2507-q8_0 | 0 | 30 | 0 | [[0, 1, 2]] |
| 57 | 2026-10-26 22:17:14 | batch/model_bench_20261026 | qwen3_4b-instruct-2507-q8_0/FCO/rep2 | FCO | qwen3:4b-instruct-2507-q8_0 | 0 | 30 | 0 | [[0, 1, 2]] |
| 58 | 2026-10-26 22:27:34 | batch/model_bench_20261026 | qwen3_4b-instruct-2507-q8_0/FCO/rep3 | FCO | qwen3:4b-instruct-2507-q8_0 | 0 | 28 | 0 | [[0, 1, 2]] |
| 59 | 2026-10-26 22:38:44 | batch/model_bench_20261026 | qwen3_4b-instruct-2507-q8_0/TSO/rep1 | TSO | qwen3:4b-instruct-2507-q8_0 | 0 | 27 | 0 | [[0, 1, 2]] |
| 60 | 2026-10-26 22:50:24 | batch/model_bench_20261026 | qwen3_4b-instruct-2507-q8_0/TSO/rep2 | TSO | qwen3:4b-instruct-2507-q8_0 | 0 | 27 | 0 | [[0, 2], [1]] |
| 61 | 2026-10-26 23:01:34 | batch/model_bench_20261026 | qwen3_4b-instruct-2507-q8_0/TSO/rep3 | TSO | qwen3:4b-instruct-2507-q8_0 | 0 | 27 | 0 | [[0, 1, 2]] |
| 62 | 2026-10-26 23:13:24 | batch/model_bench_20261026 | qwen3.5_4b-q8_0/DA/rep1 | DA | qwen3.5:4b-q8_0 | 0 | 94 | 0 | [[0], [1]] |
| 63 | 2026-10-26 23:33:34 | batch/model_bench_20261026 | qwen3.5_4b-q8_0/DA/rep2 | DA | qwen3.5:4b-q8_0 | 0 | 122 | 2 | [[2]] |
| 64 | 2026-10-26 23:54:15 | batch/model_bench_20261026 | qwen3.5_4b-q8_0/DA/rep3 | DA | qwen3.5:4b-q8_0 | 0 | 121 | 0 | [[0, 1]] |
| 65 | 2026-10-27 00:16:45 | batch/model_bench_20261026 | qwen3.5_4b-q8_0/FCO/rep1 | FCO | qwen3.5:4b-q8_0 | 0 | 64 | 0 | [[0, 2], [1]] |
| 66 | 2026-10-27 00:35:35 | batch/model_bench_20261026 | qwen3.5_4b-q8_0/FCO/rep2 | FCO | qwen3.5:4b-q8_0 | 0 | 41 | 0 | [[0, 2], [1]] |
| 67 | 2026-10-27 00:49:55 | batch/model_bench_20261026 | qwen3.5_4b-q8_0/FCO/rep3 | FCO | qwen3.5:4b-q8_0 | 0 | 107 | 0 | [[0]] |
| 68 | 2026-10-27 01:14:05 | batch/model_bench_20261026 | qwen3.5_4b-q8_0/TSO/rep1 | TSO | qwen3.5:4b-q8_0 | 0 | 101 | 0 | [[0]] |
| 69 | 2026-10-27 01:41:35 | batch/model_bench_20261026 | qwen3.5_4b-q8_0/TSO/rep2 | TSO | qwen3.5:4b-q8_0 | 0 | 91 | 0 | [[0, 2]] |
| 70 | 2026-10-27 02:17:35 | batch/model_bench_20261026 | qwen3.5_4b-q8_0/TSO/rep3 | TSO | qwen3.5:4b-q8_0 | 0 | 56 | 0 | [[0], [1], [2]] |
| 71 | 2026-10-27 02:42:35 | batch/model_bench_20261026 | command-r7b_latest/DA/rep1 | DA | command-r7b:latest | 0 | 59 | 0 | [[0, 1], [2]] |
| 72 | 2026-10-27 03:01:25 | batch/model_bench_20261026 | command-r7b_latest/DA/rep2 | DA | command-r7b:latest | 1 | 59 | 0 | [[0, 1]] |
| 73 | 2026-10-27 03:25:05 | batch/model_bench_20261026 | command-r7b_latest/DA/rep3 | DA | command-r7b:latest | 0 | 68 | 0 | [[0, 1], [2]] |
| 74 | 2026-10-27 03:46:16 | batch/model_bench_20261026 | command-r7b_latest/FCO/rep1 | FCO | command-r7b:latest | 1 | 26 | 0 | [[0, 1]] |
| 75 | 2026-10-27 04:08:26 | batch/model_bench_20261026 | command-r7b_latest/FCO/rep2 | FCO | command-r7b:latest | 0 | 38 | 0 | [[0, 1, 2]] |
| 76 | 2026-10-27 04:27:26 | batch/model_bench_20261026 | command-r7b_latest/FCO/rep3 | FCO | command-r7b:latest | 0 | 38 | 0 | [[0, 1, 2]] |
| 77 | 2026-10-27 04:46:36 | batch/model_bench_20261026 | command-r7b_latest/TSO/rep1 | TSO | command-r7b:latest | 0 | 64 | 0 | [[0, 1], [2]] |
| 78 | 2026-10-27 05:04:46 | batch/model_bench_20261026 | command-r7b_latest/TSO/rep2 | TSO | command-r7b:latest | 1 | 54 | 0 | [[0, 1]] |
| 79 | 2026-10-27 05:18:16 | batch/model_bench_20261026 | command-r7b_latest/TSO/rep3 | TSO | command-r7b:latest | 0 | 59 | 0 | [[0, 1, 2]] |
| 80 | 2026-10-27 05:35:46 | batch/model_bench_20261026 | ministral-3_8b/DA/rep1 | DA | ministral-3:8b | 1 | 26 | 0 | [[0], [1]] |
| 81 | 2026-10-27 06:10:26 | batch/model_bench_20261026 | ministral-3_8b/DA/rep2 | DA | ministral-3:8b | 0 | 27 | - | - |
| 82 | 2026-10-27 06:55:26 | batch/model_bench_20261026 | ministral-3_8b/DA/rep3 | DA | ministral-3:8b | 0 | 51 | 0 | [[0, 1], [2]] |
| 83 | 2026-10-27 07:39:27 | batch/model_bench_20261026 | ministral-3_8b/FCO/rep1 | FCO | ministral-3:8b | 2 | 43 | 1 | [[1]] |
| 84 | 2026-10-27 07:56:37 | batch/model_bench_20261026 | ministral-3_8b/FCO/rep2 | FCO | ministral-3:8b | 4 | 44 | 2 | [[2]] |
| 85 | 2026-10-27 08:20:37 | batch/model_bench_20261026 | ministral-3_8b/FCO/rep3 | FCO | ministral-3:8b | 1 | 80 | 0 | [[0], [1]] |
| 86 | 2026-10-27 08:52:17 | batch/model_bench_20261026 | ministral-3_8b/TSO/rep1 | TSO | ministral-3:8b | 1 | 32 | 0 | [[0], [1]] |
| 87 | 2026-10-27 09:28:37 | batch/model_bench_20261026 | ministral-3_8b/TSO/rep2 | TSO | ministral-3:8b | 1 | 29 | - | - |
| 88 | 2026-10-27 10:13:37 | batch/model_bench_20261026 | ministral-3_8b/TSO/rep3 | TSO | ministral-3:8b | 0 | 61 | - | - |
| 89 | 2026-10-27 10:58:37 | batch/model_bench_20261026 | deepseek-coder_6.7b/DA/rep1 | DA | deepseek-coder:6.7b | 1 | 39 | 1 | [[1, 2]] |
| 90 | 2026-10-27 11:38:27 | batch/model_bench_20261026 | deepseek-coder_6.7b/DA/rep2 | DA | deepseek-coder:6.7b | 2 | 32 | 2 | [[2]] |
| 91 | 2026-10-27 12:09:28 | batch/model_bench_20261026 | deepseek-coder_6.7b/DA/rep3 | DA | deepseek-coder:6.7b | 1 | 113 | 0 | [[0, 1], [2]] |
| 92 | 2026-10-27 12:41:18 | batch/model_bench_20261026 | deepseek-coder_6.7b/FCO/rep1 | FCO | deepseek-coder:6.7b | 5 | 64 | 2 | [[2]] |
| 93 | 2026-10-27 13:10:08 | batch/model_bench_20261026 | deepseek-coder_6.7b/FCO/rep2 | FCO | deepseek-coder:6.7b | 3 | 84 | 0 | [[0, 2]] |
| 94 | 2026-10-27 13:40:08 | batch/model_bench_20261026 | deepseek-coder_6.7b/FCO/rep3 | FCO | deepseek-coder:6.7b | 2 | 91 | 1 | [[1, 2]] |
| 95 | 2026-10-27 14:10:18 | batch/model_bench_20261026 | deepseek-coder_6.7b/TSO/rep1 | TSO | deepseek-coder:6.7b | 0 | 78 | 0 | [[0], [1], [2]] |
| 96 | 2026-10-27 14:34:18 | batch/model_bench_20261026 | deepseek-coder_6.7b/TSO/rep2 | TSO | deepseek-coder:6.7b | 1 | 21 | 0 | [[0], [2]] |
| 97 | 2026-10-27 14:59:48 | batch/model_bench_20261026 | deepseek-coder_6.7b/TSO/rep3 | TSO | deepseek-coder:6.7b | 4 | 8 | 2 | [[2]] |
| 98 | 2026-10-27 16:41:46 | batch/mixed_vote_20261027 | DA/DA/rep1 | DA | command-r7b:latest, deepseek-coder:6.7b, qwen3:4b-instruct | 0 | 58 | 0 | [[0], [1]] |
| 99 | 2026-10-27 17:11:26 | batch/mixed_vote_20261027 | DA/DA/rep2 | DA | command-r7b:latest, deepseek-coder:6.7b, qwen3:4b-instruct | 0 | 36 | 0 | [[0], [1], [2]] |
| 100 | 2026-10-27 17:29:26 | batch/mixed_vote_20261027 | DA/DA/rep3 | DA | command-r7b:latest, deepseek-coder:6.7b, qwen3:4b-instruct | 1 | 25 | 0 | [[0, 1]] |
| 101 | 2026-10-27 17:51:26 | batch/mixed_vote_20261027 | FCO/FCO/rep1 | FCO | command-r7b:latest, deepseek-coder:6.7b, qwen3:4b-instruct | 0 | 71 | 0 | [[0, 1]] |
| 102 | 2026-10-27 18:17:16 | batch/mixed_vote_20261027 | FCO/FCO/rep2 | FCO | command-r7b:latest, deepseek-coder:6.7b, qwen3:4b-instruct | 0 | 37 | 0 | [[0, 1, 2]] |
| 103 | 2026-10-27 18:38:46 | batch/mixed_vote_20261027 | FCO/FCO/rep3 | FCO | command-r7b:latest, deepseek-coder:6.7b, qwen3:4b-instruct | 1 | 32 | 0 | [[0, 1]] |
| 104 | 2026-10-27 18:53:07 | batch/mixed_vote_20261027 | TSO/TSO/rep1 | TSO | command-r7b:latest, deepseek-coder:6.7b, qwen3:4b-instruct | 1 | 30 | 0 | [[0, 1]] |
| 105 | 2026-10-27 19:14:27 | batch/mixed_vote_20261027 | TSO/TSO/rep2 | TSO | command-r7b:latest, deepseek-coder:6.7b, qwen3:4b-instruct | 1 | 26 | 0 | [[0, 1]] |
| 106 | 2026-10-27 19:37:37 | batch/mixed_vote_20261027 | TSO/TSO/rep3 | TSO | command-r7b:latest, deepseek-coder:6.7b, qwen3:4b-instruct | 1 | 24 | 0 | [[0, 1]] |

## 3. Most frequent errors and warnings (all runs)

Numbers are normalised (digits → `#`).

### Errors

* 40x `Candidate # could not be produced and was dropped: Stage '..' did not produce valid output in # attempts.`
* 4x `LLM call failed: Remote end closed connection without response`
* 4x `LLM call failed: <urlopen error [Errno #] Connection refused>`
* 3x `LLM call failed: HTTP Error #: Internal Server Error`
* 2x `Koşu hatası: '..' aşaması # denemede geçerli çıktı üretemedi.`

### Warnings

* 634x `measure: model wrote no measurements for '..'; completed from the script draft`
* 608x `stimulus: testbench '..' was missing from the model output; completed from the script draft`
* 231x `cmrr: **warning** (p#:x#m# (cmrr.sp:#)) Warning:  Acde = # may be too small in BSIM# model with w=# l=#.`
* 228x `power_area: **warning** (p#:x#m# (power_area.sp:#)) Warning:  Acde = # may be too small in BSIM# model with w=# l=#.`
* 226x `offset: **warning** (p#:x#m# (offset.sp:#)) Warning:  Acde = # may be too small in BSIM# model with w=# l=#.`
* 223x `vos_temp: **warning** (p#:x#m# (vos_temp.sp:#)) Warning:  Acde = # may be too small in BSIM# model with w=# l=#.`
* 215x `ac_loop: **warning** (p#:x#m# (ac_loop.sp:#)) Warning:  Acde = # may be too small in BSIM# model with w=# l=#.`
* 214x `psrr: **warning** (p#:x#m# (psrr.sp:#)) Warning:  Acde = # may be too small in BSIM# model with w=# l=#.`
* 205x `cl_gain: **warning** (p#:x#m# (cl_gain.sp:#)) Warning:  Acde = # may be too small in BSIM# model with w=# l=#.`
* 187x `tran_slew: **warning** (p#:x#m# (tran_slew.sp:#)) Warning:  Acde = # may be too small in BSIM# model with w=# l=#.`
* 127x `power_area: **warning** (n#:x#m# (power_area.sp:#)) Warning:  Acde = # may be too small in BSIM# model with w=# l=#.`
* 126x `cmrr: **warning** (n#:x#m# (cmrr.sp:#)) Warning:  Acde = # may be too small in BSIM# model with w=# l=#.`
* 126x `psrr: **warning** (n#:x#m# (psrr.sp:#)) Warning:  Acde = # may be too small in BSIM# model with w=# l=#.`
* 126x `vos_temp: **warning** (n#:x#m# (vos_temp.sp:#)) Warning:  Acde = # may be too small in BSIM# model with w=# l=#.`
* 123x `offset: **warning** (n#:x#m# (offset.sp:#)) Warning:  Acde = # may be too small in BSIM# model with w=# l=#.`
* 122x `cl_gain: **warning** (n#:x#m# (cl_gain.sp:#)) Warning:  Acde = # may be too small in BSIM# model with w=# l=#.`
* 117x `ac_loop: **warning** (n#:x#m# (ac_loop.sp:#)) Warning:  Acde = # may be too small in BSIM# model with w=# l=#.`
* 93x `tran_slew: **warning** (n#:x#m# (tran_slew.sp:#)) Warning:  Acde = # may be too small in BSIM# model with w=# l=#.`
* 52x `tran_slew: model output failed (no measures); script draft used`
* 42x `candidate N attempt N failed: cl_gain=# is outside the plausible range (#, #); cl_gain_err=# is outside the plausible range (#, #)`
* 41x `tran_slew: **warning** (p#:x#m# (tran_slew_taslak.sp:#)) Warning:  Acde = # may be too small in BSIM# model with w=# l=#.`
* 35x `tran_slew: **warning** (n#:x#m# (tran_slew_taslak.sp:#)) Warning:  Acde = # may be too small in BSIM# model with w=# l=#.`
* 33x `candidate N attempt N failed: vos=# is outside the plausible range (#, #)`
* 32x `offset: **warning** (offset.sp:#) Measurement time value specified exceeds analysis limit in measure variable vos. .measure has been ignored. Enter a `
* 31x `ac_loop: **warning** (ac_loop.sp:#) Undefined parameter or function definition "bw_#db" for "phase_margin". Please enter a defined name. .measure "pha`
* 30x `cmrr: **warning** (cmrr.sp:#) Undefined parameter or function definition "gain" for "cmrr". Please enter a defined name. .measure "cmrr" is ignored.`
* 26x `cl_gain: **warning** (p#:x#m# (cl_gain_taslak.sp:#)) Warning:  Acde = # may be too small in BSIM# model with w=# l=#.`
* 22x `ac_loop: **warning** (ac_loop.sp:#) measure result bw redefined, ignored the previous.`
* 21x `cl_gain: **warning** (cl_gain.sp:#) Value of resistance #:rf defined is limited to # (RESMIN). Please specify a resistor value larger than the value o`
* 20x `stimulus: '..' testbench'i model çıktısında yoktu; script taslağıyla tamamlandı`

## 4. Errors and fixes (all phases)

Status: **fixed** = in code or prompts, **pitfall** = told to the model in `config/agent_prompts.json`, **open** = still to do.

| # | Phase | Error seen in the logs | Cause | Fix | Status |
|---|---|---|---|---|---|
| 1 | early | `{context.analyses[0]...}` placeholders left in netlist or `.meas` | model copied the template | static check (`check_stimulus`, `check_measure`) + pitfall | fixed, pitfall |
| 2 | early | invalid JSON: string concatenation, double-escaped `\\n`, `\n\n\n...` degeneration | small models | repair in `post()`, stop sequence, retry without schema | fixed |
| 3 | early | HTTP 500 with a JSON schema (command-r7b), truncated strings (mistral) | schema + long output | schema only on the first attempt | fixed |
| 4 | early | tests missing from the stimulus (e.g. 1 of 8) | "keep it short" wording; model skips tests | ask for completeness; missing tests come from the script draft and are reported | fixed, pitfall |
| 5 | early | AC source on the input for PSRR (PSRR 560 dB) | wrong test setup | prompt rule + sanity range | fixed |
| 6 | early | `.meas` written as `v(out)(12u)`, `when` for min/max, `fall=last` for settling | invalid HSPICE forms | `find ... at=`, `max/min`, `vfin` + `when ... rise=last` | pitfall |
| 7 | early | CMRR referenced across testbenches (`Undefined parameter gainvv`) | each testbench runs alone | CMRR = gain − gaincm computed by the system | fixed, pitfall |
| 8 | early | dual supply copied from 130 nm examples; FCO −7 dB with VSS = 0 | no circuit-aware supply | `supply_hint` (symmetric ±VDD/2) | fixed |
| 9 | early | a candidate crash dropped the whole run; zombie `pipeline.py` shown as "running" | no isolation | only the candidate is dropped; reaper thread + pid check | fixed |
| 10 | infra | HSPICE waits ~120 s, `Unable to checkout` when the VPN is down | license unreachable | license port pre-check before each run | fixed |
| 11 | infra | `gpt-oss:20b` crashes Ollama on 8 GB | memory | excluded | fixed |
| 12 | infra | Verilog-A compile: no `stdio.h` | missing C headers | `gcc glibc-devel` installed, smoke test passed | fixed |
| 13 | benchmark | fake `vos=25`, `gaincm=25`, `psrr=1`, `vfin=25` (26+ candidates); old "qwen2.5:7b PSRR 1.0 dB" dissent | `sim.py read_measures()` read the `temper`/`alter#` column when a `.meas` printed `failed` | `parse_measure_file()` matches values to names by position and drops `failed`; the test falls back to the script draft (commit `070b21b`) | fixed |
| 14 | benchmark | `Measurement time value specified exceeds analysis limit` (offset `at=0.6` with `.dc -0.05..0.05`; `vfin` after `.tran` end) | `at=` outside the sweep | pitfalls in measure and stimulus agent (v3_pitfalls) | pitfall |
| 15 | benchmark | `Invalid keyword td in .MEASURE Equation Evaluation` (qwen2.5:7b, 12x) | `td=` inside `param=` | pitfall | pitfall |
| 16 | benchmark | `Unable to find referenced node vout#` (qwen2.5:7b, 25x) | invented node names | pitfall: copy node names letter for letter | pitfall |
| 17 | benchmark | `Value of resistance rf ... limited to RESMIN`, `cl_gain = −560 dB` (qwen3.5:4b) | feedback resistor written as 0 | pitfall: Rf, Rg ≥ 1k | pitfall |
| 18 | benchmark | `pulse vin period too small, reset` (qwen3.5:4b) | pulse period < rise + width + fall | pitfall | pitfall |
| 19 | benchmark | `Stage 'measure' did not produce valid output in 3 attempts` (deepseek-coder 10x, qwen2.5-coder 11x) | non-JSON or over-long output | pitfall "compact JSON only"; **deepseek still fails 7 of 9 mixed-vote runs** | open |
| 20 | benchmark | ministral-3:8b runs hit the 45 min cap (3 timeouts); status stayed `running` | too slow on the Jetson | batch cap kept; timeouts reported separately in `23_Model_Benchmark_Report.md` | open (state name) |
| 21 | mixed vote | DA runs 1 and 2 without majority although all metrics agree | `zpower` differs by 7 % (1.726e-4 vs 1.614e-4), tolerance is 5 % | proposal: per-metric tolerance or leave `zpower` out of the clustering | open |
| 22 | mixed vote | cluster compares only the metrics both candidates have (command-r7b has no `phase_margin`) | `cluster()` uses the key intersection | proposal: require a minimum common set | open |
| 23 | mixed vote | winner is always candidate 0; agreement partly comes from the shared script draft | drafts fill missing tests for every candidate | proposal: report the model's own contribution per candidate | open |
| 24 | infra | `LLM call failed: Connection refused` (4x), `Remote end closed connection` (4x) | Ollama restarted / model swap on the Jetson | the stage retries (3 attempts) and the candidate is dropped only after that; the vote goes on | fixed |
| 25 | git | commits carried a co-author trailer and a session link | default attribution | history rewritten, rule saved; commits have no attribution | fixed |

