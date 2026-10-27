# Prompt versions
- v1_old: before 2026-10-26 (Turkish stage goals in stages.json, no HSPICE-manual rules in the measure agent).
- v2_manual: English stage goals + 8 measure rules and 3 pitfalls taken from the HSPICE manual. Used by batch/model_bench_20261026.
To roll back: copy the two JSON files from v1_old into config/. Do NOT edit config/ while a benchmark is running; prompts are read on every call.
- v3_pitfalls: v2 plus 6 measure and 4 stimulus pitfalls from the benchmark (active from 2026-10-27, commit "Add benchmark pitfalls"). The fake 25.0/1.0 pitfall was not added because the parser bug is fixed; the cross-testbench cmrr pitfall already existed. v3_pending_pitfalls.json is the source list.
