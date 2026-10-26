# Benchmark findings (automatic)

Generated: 2026-10-27 00:36:29 · source: `batch/model_bench_20261026` · read-only scan (`scripts/scan_findings.py`)

Fake-value rule: if a measure is `failed` and `vos/gaincm/gainpsrr/psrr/vfin/cl_gain` is 25.0 or 1.0, that is the temperature/alter# column, not a real measurement (see `20_Observed_Errors.md`, A).

## qwen2.5-coder_7b

| Circuit | Run | Status | Time | Clusters | Majority | Fake values | Failed .meas | Tests that fell back to drafts |
|---|---|---|---|---|---|---|---|---|
| DA | 1 | done | 1186 s | [[1, 2]] | yes | 0 | 0 | 0 |
| DA | 2 | done | 1677 s | [[1]] | no | 0 | 0 | 0 |
| DA | 3 | done | 1472 s | [[1], [2]] | no | 0 | 0 | 0 |
| FCO | 1 | done | 1291 s | [[1], [2]] | no | 0 | 0 | 0 |
| FCO | 2 | done | 1361 s | [[2]] | no | 0 | 0 | 0 |
| FCO | 3 | done | 1862 s | [[1]] | no | 1 | 1 | 0 |
| TSO | 1 | done | 1490 s | [[1, 2]] | yes | 0 | 0 | 0 |
| TSO | 2 | done | 1033 s | [[1, 2], [0]] | yes | 0 | 0 | 0 |
| TSO | 3 | failed | 1891 s | [] | no | 0 | 0 | 0 |

Most frequent candidate problems:

- 11x candidat# fail#d: Stag# 'm#asur#' did not produc# valid output in # att#mpts#
- 1x cl_gain_#rr=# is outsid# th# plausibl# rang# (#, #)
- 1x vos=# is outsid# th# plausibl# rang# (#, #)

HSPICE measurement warnings:

- 1x **warning**  Measurement time value specified exceeds analysis limit in measure variable v

## qwen2.5_7b

| Circuit | Run | Status | Time | Clusters | Majority | Fake values | Failed .meas | Tests that fell back to drafts |
|---|---|---|---|---|---|---|---|---|
| DA | 1 | done | 784 s | [[0], [1], [2]] | no | 3 | 3 | 0 |
| DA | 2 | done | 771 s | [[0, 1], [2]] | yes | 0 | 6 | 0 |
| DA | 3 | done | 786 s | [[0, 1], [2]] | yes | 6 | 6 | 0 |
| FCO | 1 | failed | 2455 s | [] | no | 9 | 9 | 1 |
| FCO | 2 | failed | 2435 s | [] | no | 5 | 12 | 3 |
| FCO | 3 | done | 1885 s | [[1]] | no | 2 | 8 | 0 |
| TSO | 1 | done | 775 s | [[0], [1], [2]] | no | 3 | 3 | 0 |
| TSO | 2 | done | 787 s | [[0], [1], [2]] | no | 0 | 6 | 0 |
| TSO | 3 | done | 793 s | [[0], [1], [2]] | no | 0 | 6 | 2 |

Most frequent candidate problems:

- 8x vos=# is outsid# th# plausibl# rang# (#, #)

HSPICE measurement warnings:

- 8x **warning**  Measurement time value specified exceeds analysis limit in measure variable v

## qwen3.5_4b

| Circuit | Run | Status | Time | Clusters | Majority | Fake values | Failed .meas | Tests that fell back to drafts |
|---|---|---|---|---|---|---|---|---|
| DA | 1 | done | 798 s | [[0]] | no | 0 | 0 | 0 |
| DA | 2 | done | 1003 s | [[0], [1]] | no | 2 | 7 | 0 |
| DA | 3 | done | 1052 s | [[1], [2]] | no | 0 | 3 | 1 |
| FCO | 1 | done | 598 s | [[0, 2], [1]] | yes | 4 | 18 | 0 |
| FCO | 2 | done | 607 s | [[0], [1], [2]] | no | 4 | 18 | 0 |
| FCO | 3 | done | 590 s | [[0, 2], [1]] | yes | 4 | 18 | 0 |
| TSO | 1 | done | 1092 s | [[0]] | no | 0 | 3 | 1 |
| TSO | 2 | done | 1023 s | [[2]] | no | 2 | 6 | 5 |
| TSO | 3 | done | 1096 s | [[1]] | no | 0 | 12 | 0 |

Most frequent candidate problems:

- 7x cl_gain=# is outsid# th# plausibl# rang# (#, #)
- 6x cl_gain_#rr=# is outsid# th# plausibl# rang# (#, #)
- 2x candidat# fail#d: Stag# 'm#asur#' did not produc# valid output in # att#mpts#
- 1x candidat# fail#d: Stag# 'stimulus' did not produc# valid output in # att#mpts#
- 1x vos=# is outsid# th# plausibl# rang# (#, #)

HSPICE measurement warnings:

- 9x **warning**  Measurement time value specified exceeds analysis limit in measure variable v

## qwen3.5_4b-q8_0

| Circuit | Run | Status | Time | Clusters | Majority | Fake values | Failed .meas | Tests that fell back to drafts |
|---|---|---|---|---|---|---|---|---|
| DA | 1 | done | 1207 s | [[0], [1]] | no | 2 | 2 | 1 |
| DA | 2 | done | 1232 s | [[2]] | no | 0 | 0 | 1 |
| DA | 3 | done | 1345 s | [[0, 1]] | yes | 4 | 4 | 0 |
| FCO | 1 | done | 1123 s | [[0, 2], [1]] | yes | 0 | 6 | 0 |

Most frequent candidate problems:

- 3x cl_gain=# is outsid# th# plausibl# rang# (#, #)
- 3x cl_gain_#rr=# is outsid# th# plausibl# rang# (#, #)
- 1x vos=# is outsid# th# plausibl# rang# (#, #)

HSPICE measurement warnings:

- 1x **warning**  Measurement time value specified exceeds analysis limit in measure variable v

## qwen3_4b-instruct

| Circuit | Run | Status | Time | Clusters | Majority | Fake values | Failed .meas | Tests that fell back to drafts |
|---|---|---|---|---|---|---|---|---|
| DA | 1 | done | 474 s | [[0, 1, 2]] | yes | 0 | 0 | 0 |
| DA | 2 | done | 728 s | [[0, 2], [1]] | yes | 0 | 0 | 1 |
| DA | 3 | done | 730 s | [[0, 1], [2]] | yes | 0 | 0 | 1 |
| FCO | 1 | done | 624 s | [[0, 1, 2]] | yes | 0 | 0 | 1 |
| FCO | 2 | done | 1048 s | [[0, 2]] | yes | 1 | 1 | 1 |
| FCO | 3 | done | 1107 s | [[0, 1], [2]] | yes | 0 | 0 | 3 |
| TSO | 1 | done | 634 s | [[0, 1], [2]] | yes | 0 | 0 | 3 |
| TSO | 2 | done | 767 s | [[1, 2], [0]] | yes | 0 | 0 | 2 |
| TSO | 3 | done | 748 s | [[0, 1, 2]] | yes | 0 | 0 | 3 |

Most frequent candidate problems:

- 1x vos=# is outsid# th# plausibl# rang# (#, #)

HSPICE measurement warnings:

- 1x **warning**  Measurement time value specified exceeds analysis limit in measure variable v

## qwen3_4b-instruct-2507-q8_0

| Circuit | Run | Status | Time | Clusters | Majority | Fake values | Failed .meas | Tests that fell back to drafts |
|---|---|---|---|---|---|---|---|---|
| DA | 1 | done | 851 s | [[1, 2], [0]] | yes | 1 | 1 | 7 |
| DA | 2 | done | 745 s | [[0, 1], [2]] | yes | 0 | 0 | 6 |
| DA | 3 | done | 792 s | [[0], [1], [2]] | no | 2 | 2 | 5 |
| FCO | 1 | done | 659 s | [[0, 1, 2]] | yes | 0 | 0 | 4 |
| FCO | 2 | done | 613 s | [[0, 1, 2]] | yes | 0 | 0 | 4 |
| FCO | 3 | done | 661 s | [[0, 1, 2]] | yes | 0 | 0 | 4 |
| TSO | 1 | done | 696 s | [[0, 1, 2]] | yes | 0 | 0 | 3 |
| TSO | 2 | done | 668 s | [[0, 2], [1]] | yes | 0 | 0 | 3 |
| TSO | 3 | done | 703 s | [[0, 1, 2]] | yes | 0 | 0 | 3 |
