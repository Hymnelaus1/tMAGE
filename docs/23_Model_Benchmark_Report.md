# Model benchmark report

Generated 2026-10-27 16:40 by `scripts/recompute_scores.py` from `batch/model_bench_20261026` (saved `.ms0/.mt0` files re-parsed with the fixed parser; no HSPICE or LLM calls).

Setup: each model alone (3 voters = the same model), circuits DA / FCO / TSO, 3 runs each, 3 voted candidates per run, SAED 90 nm, HSPICE X-2025.06, prompts v2 (`config/prompt_versions/v2_manual`). Reference values come from the hand-simulated reference (`knowledge/ref_da.json`, `docs/17_Handoff_for_new_chat.md`).

Definitions: **clean majority** = a run where at least 2 of 3 candidates passed the sanity rules (no failed `.meas`, values in range) and agree within 5 %. **Accuracy** = winner metrics within 10 % of the reference. **Draft fallbacks** = tests where the model output did not run and the script draft was used (the model's own contribution is lower than the majority suggests).

## Summary per model

| Model | Clean majority (of 9) | DA | FCO | TSO | Accuracy | Timeouts/failed runs | Draft fallbacks | Avg time per run |
|---|---|---|---|---|---|---|---|---|
| command-r7b | 8 | 3/3 | 2/3 | 3/3 | 32/35 | 0 | 8 | 1150 s |
| deepseek-coder:6.7b | 4 | 2/3 | 2/3 | 0/3 | 20/20 | 0 | 6 | 1713 s |
| ministral-3:8b | 0 | 0/3 | 0/3 | 0/3 | 0/0 | 3 | 43 | 1872 s |
| qwen2.5-coder:7b | 3 | 1/3 | 0/3 | 2/3 | 16/16 | 1 | 0 | 1473 s |
| qwen2.5:7b | 1 | 1/3 | 0/3 | 0/3 | 6/6 | 2 | 6 | 1274 s |
| qwen3.5:4b | 0 | 0/3 | 0/3 | 0/3 | 0/0 | 0 | 7 | 873 s |
| qwen3.5:4b Q8 | 0 | 0/3 | 0/3 | 0/3 | 0/0 | 0 | 4 | 1388 s |
| qwen3:4b-instruct (Q4) | 9 | 3/3 | 3/3 | 3/3 | 48/48 | 0 | 15 | 762 s |
| qwen3:4b-instruct Q8 | 8 | 2/3 | 3/3 | 3/3 | 42/42 | 0 | 39 | 709 s |

## Where and why models failed

Candidates dropped by the sanity check (count over 27 runs x 3 candidates = 81 per model), grouped by cause:

* **qwen3:4b-instruct (Q4)**: 1x failed .meas vos
* **qwen3:4b-instruct Q8**: 3x failed .meas gaincm
* **command-r7b**: 3x no measurements; 1x failed .meas cl_bw
* **deepseek-coder:6.7b**: 10x no measurements
* **qwen2.5-coder:7b**: 11x no measurements; 1x cl_gain_err out of range; 1x failed .meas vos
* **qwen2.5:7b**: 8x failed .meas vos; 7x failed .meas gainpsrr; 7x failed .meas psrr; 6x failed .meas gaincm; 5x failed .meas t80
* **qwen3.5:4b**: 9x failed .meas t20; 9x failed .meas slewrate; 9x failed .meas tsettle_abs; 9x failed .meas tsettle; 8x failed .meas vfin
* **qwen3.5:4b Q8**: 7x failed .meas cl_gain; 7x failed .meas cl_gain_err; 7x failed .meas cl_bw; 6x cl_gain out of range; 6x cl_gain_err out of range
* **ministral-3:8b**: 9x failed .meas gaincm; 8x no measurements; 7x failed .meas gainpsrr; 6x failed .meas cl_gain; 5x failed .meas cl_bw

## Per circuit: runs with a clean majority (of 3)

| Model | DA | FCO | TSO |
|---|---|---|---|
| qwen3:4b-instruct (Q4) | 3/3 (9/9 cands ok) | 3/3 (8/9 cands ok) | 3/3 (9/9 cands ok) |
| qwen3:4b-instruct Q8 | 2/3 (6/9 cands ok) | 3/3 (9/9 cands ok) | 3/3 (9/9 cands ok) |
| command-r7b | 3/3 (8/9 cands ok) | 2/3 (7/9 cands ok) | 3/3 (8/9 cands ok) |
| deepseek-coder:6.7b | 2/3 (6/9 cands ok) | 2/3 (5/9 cands ok) | 0/3 (6/9 cands ok) |
| qwen2.5-coder:7b | 1/3 (5/9 cands ok) | 0/3 (4/9 cands ok) | 2/3 (5/9 cands ok) |
| qwen2.5:7b | 1/3 (5/9 cands ok) | 0/3 (1/9 cands ok) | 0/3 (6/9 cands ok) |
| qwen3.5:4b | 0/3 (3/9 cands ok) | 0/3 (0/9 cands ok) | 0/3 (2/9 cands ok) |
| qwen3.5:4b Q8 | 0/3 (2/9 cands ok) | 0/3 (2/9 cands ok) | 0/3 (2/9 cands ok) |
| ministral-3:8b | 0/3 (4/9 cands ok) | 0/3 (1/9 cands ok) | 0/3 (1/9 cands ok) |

## Reading the table

* Scores before the parser fix are **not comparable**: they counted the 25.0 / 1.0 artefact as a measurement. Use this report, not `22_Benchmark_Findings.md`, for conclusions.
* Timeouts: runs cut by the 45-minute batch cap are listed separately; they say the model was too slow on the Jetson, not that it was wrong.
* Details of the individual errors and the resulting prompt pitfalls: `20_Observed_Errors.md`, `config/prompt_versions/v3_pending_pitfalls.json`.
