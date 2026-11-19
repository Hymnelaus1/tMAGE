# Model benchmark report

Generated 2026-11-09 11:32 by `scripts/recompute_scores.py` from `batch/model_bench_new_20261028` (saved `.ms0/.mt0` files re-parsed with the fixed parser; no HSPICE or LLM calls).

Setup: each model alone (3 voters = the same model), circuits DA / FCO / TSO, 3 runs each, 3 voted candidates per run, SAED 90 nm, HSPICE X-2025.06, prompts v2 (`config/prompt_versions/v2_manual`). Reference values come from the hand-simulated reference (`knowledge/ref_da.json`, `docs/17_Handoff_for_new_chat.md`).

Definitions: **clean majority** = a run where at least 2 of 3 candidates passed the sanity rules (no failed `.meas`, values in range) and agree within 5 %. **Accuracy** = winner metrics within 10 % of the reference. **Draft fallbacks** = tests where the model output did not run and the script draft was used (the model's own contribution is lower than the majority suggests).

## Summary per model

| Model | Clean majority (of 9) | DA | FCO | TSO | Accuracy | Timeouts/failed runs | Draft fallbacks | Avg time per run |
|---|---|---|---|---|---|---|---|---|
| gemma4:e4b | 0 | 0/3 | 0/3 | 0/3 | 0/0 | 5 | 6 | 580 s |
| glm4:9b | 3 | 1/3 | 1/3 | 1/3 | 16/16 | 1 | 13 | 1863 s |
| llama3.1:8b | 6 | 3/3 | 1/3 | 2/3 | 33/33 | 0 | 14 | 998 s |
| nemotron-3-nano:4b | 0 | 0/3 | 0/3 | 0/3 | 0/0 | 7 | 25 | 981 s |
| qwen3:8b | 7 | 3/3 | 2/3 | 2/3 | 38/38 | 0 | 55 | 1309 s |
| yi-coder:9b | 2 | 1/3 | 1/3 | 0/3 | 11/11 | 2 | 2 | 1456 s |

## Where and why models failed

Candidates dropped by the sanity check (count over 27 runs x 3 candidates = 81 per model), grouped by cause:

* **qwen3:8b**: 1x cl_gain_err out of range
* **llama3.1:8b**: 3x cmrr out of range; 1x cmrr_fixed: no measurement statements; 1x psrr_fixed: no measurement statements; 1x no measurements
* **glm4:9b**: 15x no measurements
* **yi-coder:9b**: 18x no measurements
* **gemma4:e4b**: 21x no measurements; 1x vos_max out of range; 1x vos_min out of range; 1x cl_gain_1: no measurement statements; 1x cl_gain_10: no measurement statements
* **nemotron-3-nano:4b**: 21x no measurements; 2x vos_vel: simulation error: **error** (vos_vel.sp:48) string misses dexter quotation mark, error is  before or at "'v(vout)-v(vinp)) at=0"; 1x cl_vel: no measurement statements; 1x ac_phase_margin: no measurement statements; 1x ac_phase_margin: no measurement produced (.meas statements gave no result)

## Per circuit: runs with a clean majority (of 3)

| Model | DA | FCO | TSO |
|---|---|---|---|
| qwen3:8b | 3/3 (8/9 cands ok) | 2/3 (9/9 cands ok) | 2/3 (9/9 cands ok) |
| llama3.1:8b | 3/3 (9/9 cands ok) | 1/3 (6/9 cands ok) | 2/3 (8/9 cands ok) |
| glm4:9b | 1/3 (3/9 cands ok) | 1/3 (4/9 cands ok) | 1/3 (5/9 cands ok) |
| yi-coder:9b | 1/3 (4/9 cands ok) | 1/3 (3/9 cands ok) | 0/3 (2/9 cands ok) |
| gemma4:e4b | 0/3 (4/9 cands ok) | 0/3 (1/9 cands ok) | 0/3 (0/9 cands ok) |
| nemotron-3-nano:4b | 0/3 (2/9 cands ok) | 0/3 (0/9 cands ok) | 0/3 (1/9 cands ok) |

## Reading the table

* Scores before the parser fix are **not comparable**: they counted the 25.0 / 1.0 artefact as a measurement. Use this report, not `22_Benchmark_Findings.md`, for conclusions.
* Timeouts: runs cut by the 45-minute batch cap are listed separately; they say the model was too slow on the Jetson, not that it was wrong.
* Details of the individual errors and the resulting prompt pitfalls: `20_Observed_Errors.md`, `config/prompt_versions/v3_pending_pitfalls.json`.
