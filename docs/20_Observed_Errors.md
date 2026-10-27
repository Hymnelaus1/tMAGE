# Observed errors and fixes

Detailed context: `17_Handoff_for_new_chat.md` sections 7-8. Prompts: `19_Agent_Prompts.md`.

## Model output
| Error | Fix |
|---|---|
| Unresolved template placeholders (`{context.analyses[0]...}`) | a "known errors" list in the prompt, static check |
| String concatenation inside JSON (mistral) | mistral only for measure |
| Output degeneration with consecutive `\n\n\n...`, token limit | stop sequence, retry without the schema |
| Double-escaped `\\n` | repaired in `post()` |
| HTTP 500 with a schema (command-r7b), truncated string (mistral) | schema only on the first attempt |
| A "keep it short" sentence made the model skip tests | ask for completeness instead of brevity |
| Missing tests (1 out of 8) | the missing ones are completed from the script draft, the "model contribution" is reported |
| qwen2.5:7b on the DA: CMRR 17.6 dB, PSRR 1.0 dB (the others 67.8/72.4) | **not examined yet**; the vote caught it (probably the parser bug A below) |

## Testbench / HSPICE
| Error | Fix |
|---|---|
| Missing source, DUT instance or analysis card; no AC source | static check |
| PSRR with the AC source on the input (instead of the supply) | prompt rule, sanity (PSRR 560 dB) |
| `.meas`: `v(out)(12u)`, `when` for min/max, `fall=last` for settling | `max/min`, `vfin` + `when ... rise=last` |
| CMRR referencing across testbenches | CMRR is derived by the system |
| Dual supply copied from the 130 nm examples | circuit-aware supply (`supply_hint`) |
| FCO at -7 dB with VSS=0 (ground-referenced bias) | symmetric +/-VDD/2 supply |
| A candidate crash dropped the run | only that candidate is dropped, the vote goes on |
| A zombie `pipeline.py` made the run look "running" | reaper thread + pid check |

## Infrastructure
| Error | Fix |
|---|---|
| `gpt-oss:20b` crashes Ollama | excluded |
| When the VPN drops HSPICE waits about 120 s and reports `Unable to checkout` | license port pre-check |
| Verilog-A: no `stdio.h` | `gcc glibc-devel` installed; **the smoke test passed on 2026-10-26** |

## Found in benchmark 20261026 (model_bench_20261026)

### A. Code bug (FIXED 2026-10-27, commit 070b21b): `engine/sim.py read_measures()` turned a failed measurement into a wrong number
HSPICE writes a failed measurement as `failed`. The parser counts this word as a separate "name", the number columns shift, and the `temper` (25) / `alter#` (1) value is read as a measurement:
```
 vos     temper    alter#
    failed  25.0000  1        ->  vos = 25.0   (in fact: the measure failed)
```
Effect: fake `vos=25`, `gaincm=25`, `gainpsrr=25`, `psrr=1`, `vfin=25`, `cl_gain=25`. This was seen in 26+ candidate results (qwen3:4b-instruct 1, qwen3.5:4b 8, qwen2.5:7b 17). The sanity rules caught some of them (vos) and missed others (for example vfin=25 V may not hit a range).
**Probably** the old "qwen2.5:7b PSRR 1.0 dB / CMRR 17.6 dB" disagreement has the same cause: the parser, not the model. Not verified, the old batch files must be checked.
Proposed fix: accept the `failed` token as the value of that column (NaN), map the `temper`/`alter#` columns by name, and report a failed measurement as "no measurement". The fix will be made when the benchmark ends; the results can be recomputed from the saved `.ms0/.mt0` files without re-running HSPICE.

### B. Model error: the `at=` value of the offset measurement is outside the sweep range
qwen2.5:7b on the FCO: a `.dc Vin -0.05 0.05` sweep + `.meas ... at=0.6`. 0.6 is outside the range, so the measure fails (HSPICE warning: "Measurement time value specified exceeds analysis limit"). 3 candidates x 3 attempts were wasted, the run took about 41 minutes and failed (FCO runs 1 and 2). Root cause: the single-supply (VDD/2=0.6) common mode was carried over to the FCO, which has a symmetric supply (+/-0.6 V, centre 0).
Proposed pitfalls: `config/prompt_versions/v3_pending_pitfalls.json` (not active yet).
