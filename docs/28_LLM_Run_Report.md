# LLM run report (all runs)

Generated 2026-11-20 00:36 by `scripts/llm_run_report.py` from 166 runs in `runs/` and 1715 saved LLM calls (`logs/llm/*.json`). Includes runs of every prompt version (v1, v2, v3) and every phase; for the corrected per-model score use `23_Model_Benchmark_Report.md` and `27_New_Models_Benchmark_Report.md`.

## 1. How a testbench is produced

```
job.json -> context.json -> spec (script) -> scenario (script: which tests) -> DUT precheck (script draft simulated, no LLM)
   -> N candidates, each:  stimulus agent (LLM)  : writes one testbench per test, refining the script draft, with RAG examples
                           measure agent  (LLM)  : writes the .meas statements per test, refining the script draft
                           static checks (CUT instance, AC source, .meas form, analysis card)  -> retry up to 3 times
                           HSPICE per test  -> .ms0/.mt0/.ma0 values
   -> verify: sanity rules + cluster vote (5 %) -> report
```

* The **script draft** (deterministic, from the circuit topology and the catalog) is the basis: it fixes the ports, the supply (`supply_hint`), the test list and a working testbench for every test.
* The **LLM only refines**: it must return JSON (`testbenches[]`, `measurements[]`). Anything it leaves out or breaks falls back to the script draft and is **flagged**, so a candidate can look healthy while most of it is the script's work.
* The model sees: the system prompt with the pitfalls (`config/agent_prompts.json`), the circuit/context JSON, the script draft and retrieved examples. The HSPICE manual is not given to it.

## 2. What is tested and measured

| Test (analysis) | Setup | Measured names |
|---|---|---|
| `ac_loop` | open loop, differential AC | gain, bw, phase_margin |
| `cmrr` | common-mode AC | gaincm (CMRR = gain - gaincm, computed by the system) |
| `psrr` | AC 1 on the supply | gainpsrr, psrr |
| `tran_slew` | pulse on the buffer | slewrate, tsettle |
| `cl_gain` | closed loop (unity feedback) | cl_gain, cl_gain_err, cl_bw |
| `offset` | DC sweep | vos |
| `vos_temp` | DC temperature sweep | vos_max, vos_min, vos_drift |
| `power_area` | quiescent transient | zpower |

Hand reference (DA): 42.58 dB, 70 MHz, 63.6 deg, PSRR 72.4 dB, Vos -1.6 mV, 0.161 mW.

## 3. LLM calls per model and agent

A call is *failed* when the static checker rejected the reply (the stage then retries, up to 3 attempts).

| Model | Agent | Calls | Failed calls | Cut off at token limit | Avg time | Avg output tokens |
|---|---|---|---|---|---|---|
| command-r7b:latest | stimulus | 81 | 34 (41 %) | 24 | 82 s | 527 |
| command-r7b:latest | measure | 88 | 43 (48 %) | 39 | 111 s | 760 |
| deepseek-coder:6.7b | stimulus | 62 | 2 (3 %) | 0 | 120 s | 818 |
| deepseek-coder:6.7b | measure | 106 | 62 (58 %) | 44 | 156 s | 1151 |
| qwen3.5:4b-q8_0 | stimulus | 75 | 24 (32 %) | 24 | 67 s | 521 |
| qwen3.5:4b-q8_0 | measure | 70 | 16 (22 %) | 16 | 97 s | 718 |
| qwen3.5:4b | stimulus | 72 | 26 (36 %) | 21 | 47 s | 567 |
| qwen3.5:4b | measure | 61 | 17 (27 %) | 13 | 67 s | 724 |
| qwen3:4b-instruct | stimulus | 77 | 21 (27 %) | 2 | 94 s | 930 |
| qwen3:4b-instruct | measure | 57 | 1 (1 %) | 1 | 90 s | 937 |
| gemma4:e4b | stimulus | 49 | 24 (48 %) | 18 | 34 s | 666 |
| gemma4:e4b | measure | 75 | 66 (88 %) | 32 | 45 s | 995 |
| nemotron-3-nano:4b | stimulus | 50 | 25 (50 %) | 3 | 63 s | 1006 |
| nemotron-3-nano:4b | measure | 69 | 49 (71 %) | 20 | 77 s | 1189 |
| qwen2.5:7b | stimulus | 55 | 0 (0 %) | 0 | 103 s | 877 |
| qwen2.5:7b | measure | 55 | 0 (0 %) | 0 | 153 s | 1325 |
| glm4:9b | stimulus | 66 | 45 (68 %) | 36 | 169 s | 1362 |
| glm4:9b | measure | 43 | 21 (48 %) | 14 | 123 s | 969 |
| ministral-3:8b | stimulus | 68 | 43 (63 %) | 22 | 134 s | 602 |
| ministral-3:8b | measure | 39 | 17 (43 %) | 17 | 240 s | 997 |
| yi-coder:9b | stimulus | 27 | 0 (0 %) | 0 | 105 s | 1016 |
| yi-coder:9b | measure | 66 | 57 (86 %) | 57 | 154 s | 1458 |
| qwen2.5-coder:7b | stimulus | 31 | 0 (0 %) | 0 | 110 s | 886 |
| qwen2.5-coder:7b | measure | 61 | 41 (67 %) | 41 | 157 s | 1384 |
| llama3.1:8b | stimulus | 43 | 3 (6 %) | 0 | 116 s | 881 |
| llama3.1:8b | measure | 41 | 0 (0 %) | 0 | 127 s | 1021 |
| qwen3:8b | stimulus | 35 | 0 (0 %) | 0 | 162 s | 846 |
| qwen3:8b | measure | 36 | 2 (5 %) | 2 | 210 s | 1219 |
| qwen3:4b-instruct-2507-q8_0 | stimulus | 28 | 1 (3 %) | 1 | 115 s | 999 |
| qwen3:4b-instruct-2507-q8_0 | measure | 27 | 0 (0 %) | 0 | 104 s | 991 |

## 4. Why calls fail (checker errors)

A call can carry several errors, so rows add up to more than the failed calls.

| Model | output cut off at the token limit | invalid JSON | missing CUT instance | AC source missing / PSRR supply without AC 1 | `.meas` statement malformed | no analysis card | value outside the plausible range | other |
|---|---|---|---|---|---|---|---|---|
| command-r7b:latest | 63 | 4 | 4 | 6 | 0 | 0 | 0 | 0 |
| deepseek-coder:6.7b | 44 | 18 | 1 | 0 | 1 | 0 | 0 | 0 |
| qwen3.5:4b-q8_0 | 40 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| qwen3.5:4b | 34 | 2 | 0 | 2 | 2 | 3 | 0 | 0 |
| qwen3:4b-instruct | 3 | 15 | 2 | 2 | 0 | 2 | 0 | 0 |
| gemma4:e4b | 50 | 35 | 0 | 5 | 0 | 0 | 0 | 0 |
| nemotron-3-nano:4b | 23 | 27 | 5 | 15 | 5 | 1 | 0 | 0 |
| qwen2.5:7b | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| glm4:9b | 50 | 5 | 1 | 2 | 7 | 1 | 0 | 2 |
| ministral-3:8b | 39 | 1 | 16 | 6 | 0 | 0 | 0 | 1 |
| yi-coder:9b | 57 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| qwen2.5-coder:7b | 41 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| llama3.1:8b | 0 | 0 | 3 | 0 | 0 | 1 | 0 | 0 |
| qwen3:8b | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| qwen3:4b-instruct-2507-q8_0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Cause key: **output cut off at the token limit** = output cut off at the token limit; **invalid JSON** = invalid JSON (other); **missing CUT instance** = missing CUT instance (testbench does not instantiate the circuit); **AC source missing / PSRR supply without AC 1** = AC source missing / PSRR supply without AC 1; **`.meas` statement malformed** = `.meas` statement malformed (does not start with .meas); **no analysis card** = no analysis card (.ac/.tran/.dc/.op); **value outside the plausible range** = value outside the plausible range (sanity rule)

## 5. What the models skip or break (script-draft fallbacks)

Counted from the run logs, attributed to the model of the candidate that was running. *stimulus missing* = the testbench is absent from the model's JSON; *measure missing* = no `.meas` for the test; *failed in HSPICE* = the model's testbench or `.meas` did not simulate (no value or HSPICE error), the draft replaced it.

| Model | Fallbacks | Most affected tests (count) |
|---|---|---|
| nemotron-3-nano:4b | 330 | stimulus missing:cl_gain (29), stimulus missing:power_area (28), stimulus missing:vos_temp (27), stimulus missing:tran_slew (26), stimulus missing:ac_loop (21) |
| command-r7b:latest | 328 | measure missing:power_area (37), measure missing:offset (34), measure missing:vos_temp (34), stimulus missing:tran_slew (29), stimulus missing:cl_gain (29) |
| glm4:9b | 310 | stimulus missing:cmrr (24), stimulus missing:psrr (24), stimulus missing:tran_slew (24), stimulus missing:cl_gain (24), stimulus missing:offset (24) |
| qwen3.5:4b-q8_0 | 279 | measure missing:power_area (24), measure missing:vos_temp (23), stimulus missing:power_area (21), stimulus missing:vos_temp (20), measure missing:offset (20) |
| deepseek-coder:6.7b | 261 | measure missing:power_area (26), measure missing:tran_slew (19), measure missing:cmrr (18), measure missing:vos_temp (18), measure missing:psrr (17) |
| qwen3.5:4b | 181 | measure missing:vos_temp (18), measure missing:psrr (15), measure missing:offset (15), stimulus missing:offset (15), stimulus missing:vos_temp (15) |
| ministral-3:8b | 169 | stimulus missing:power_area (24), failed in HSPICE:ac_loop (20), failed in HSPICE:tran_slew (19), stimulus missing:vos_temp (16), stimulus missing:tran_slew (14) |
| qwen3:4b-instruct | 115 | measure missing:tran_slew (24), measure missing:cl_gain (17), failed in HSPICE:tran_slew (10), failed in HSPICE:cl_gain (9), stimulus missing:cl_gain (7) |
| gemma4:e4b | 98 | stimulus missing:cl_gain (17), stimulus missing:power_area (14), stimulus missing:offset (12), stimulus missing:vos_temp (12), measure missing:offset (7) |
| qwen3:8b | 79 | failed in HSPICE:tran_slew (31), failed in HSPICE:ac_loop (30), failed in HSPICE:power_area (7), stimulus missing:ac_loop (1), stimulus missing:cmrr (1) |
| qwen3:4b-instruct-2507-q8_0 | 53 | failed in HSPICE:tran_slew (20), failed in HSPICE:cl_gain (10), failed in HSPICE:psrr (6), measure missing:tran_slew (6), failed in HSPICE:vos_temp (3) |
| llama3.1:8b | 50 | failed in HSPICE:tran_slew (25), measure missing:power_area (9), measure missing:offset (3), measure missing:cmrr (2), measure missing:cl_gain (2) |
| qwen2.5-coder:7b | 32 | measure missing:power_area (7), measure missing:offset (4), measure missing:vos_temp (4), measure missing:tran_slew (3), measure missing:cl_gain (2) |
| yi-coder:9b | 14 | measure missing:cmrr (2), measure missing:psrr (2), measure missing:tran_slew (2), measure missing:cl_gain (2), measure missing:offset (2) |
| qwen2.5:7b | 11 | failed in HSPICE:tran_slew (7), failed in HSPICE:cmrr (2), failed in HSPICE:power_area (1), failed in HSPICE:cl_gain (1) |

Fallbacks per test over all models: `tran_slew` 415, `power_area` 360, `vos_temp` 329, `cl_gain` 313, `offset` 304, `psrr` 208, `ac_loop` 208, `cmrr` 173.
