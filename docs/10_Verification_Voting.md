---
tags: [tmage, verification, decision]
---
# Verification: voting instead of LLM-as-judge

**Decision (2026-10-25):** The LLM-as-judge in the presentation was replaced by **majority voting + rule checks** as the main verification. The LLM stays only for an optional explanation.

## Reasoning
- We have an objective signal: the simulation numbers.
- No dependence on the bias of a judge model; it suits small local models.
- Errors such as a wrong bias make the numbers disagree.

## Method
1. N independent testbench candidates are generated (each by a different voter model).
2. Every candidate is run in HSPICE; the measurements are collected.
3. **Rule check (script):** gain >= 0 dB, phase margin 0 to 180 degrees, power > 0, no `.meas` error, measurements produced. A candidate that fails does not enter the vote.
4. The measurements are clustered with a tolerance (default 5 %); the largest cluster wins.
5. The report uses only the HSPICE numbers of the winning candidate.

## Limits
- If all models make the same mistake the majority can be wrong (model diversity reduces this).
- A run costs N times as much; since the Jetson is slow the starting default was N=1, and with N=1 the report carries a "no voting was done" flag.
- The settings are in `context.json -> verification` (`method`, `n`, `tolerance_pct`); the UI now has selectors for N, tolerance and the voter models.
