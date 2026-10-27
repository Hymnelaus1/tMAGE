# Benchmark findings (automatic)

Generated: 2026-10-27 15:25:41 · source: `batch/model_bench_20261026` · read-only scan (`scripts/scan_findings.py`)

Fake-value rule: if a measure is `failed` and `vos/gaincm/gainpsrr/psrr/vfin/cl_gain` is 25.0 or 1.0, that is the temperature/alter# column, not a real measurement (see `20_Observed_Errors.md`, A).

## command-r7b_latest

| Circuit | Run | Status | Time | Clusters | Majority | Fake values | Failed .meas | Tests that fell back to drafts |
|---|---|---|---|---|---|---|---|---|
| DA | 1 | done | 1128 s | [[0, 1], [2]] | yes | 0 | 0 | 1 |
| DA | 2 | done | 1413 s | [[0, 1]] | yes | 0 | 0 | 0 |
| DA | 3 | done | 1268 s | [[0, 1], [2]] | yes | 0 | 0 | 0 |
| FCO | 1 | done | 1328 s | [[0, 1]] | yes | 0 | 3 | 2 |
| FCO | 2 | done | 1135 s | [[0, 1, 2]] | yes | 0 | 0 | 2 |
| FCO | 3 | done | 1146 s | [[0, 1, 2]] | yes | 0 | 0 | 3 |
| TSO | 1 | done | 1084 s | [[0, 1], [2]] | yes | 0 | 0 | 0 |
| TSO | 2 | done | 802 s | [[0, 1]] | yes | 0 | 0 | 0 |
| TSO | 3 | done | 1047 s | [[0, 1, 2]] | yes | 0 | 0 | 0 |

Most frequent candidate problems:

- 2x candidat# fail#d: Stag# 'm#asur#' did not produc# valid output in # att#mpts#
- 1x candidat# fail#d: Stag# 'stimulus' did not produc# valid output in # att#mpts#

## deepseek-coder_6.7b

| Circuit | Run | Status | Time | Clusters | Majority | Fake values | Failed .meas | Tests that fell back to drafts |
|---|---|---|---|---|---|---|---|---|
| DA | 1 | done | 2384 s | [[1, 2]] | yes | 0 | 0 | 2 |
| DA | 2 | done | 1856 s | [[2]] | no | 0 | 0 | 0 |
| DA | 3 | done | 1908 s | [[0, 1], [2]] | yes | 0 | 0 | 0 |
| FCO | 1 | done | 1721 s | [[2]] | no | 0 | 3 | 0 |
| FCO | 2 | done | 1796 s | [[0, 2]] | yes | 0 | 0 | 0 |
| FCO | 3 | done | 1800 s | [[1, 2]] | yes | 0 | 0 | 0 |
| TSO | 1 | done | 1430 s | [[0], [1], [2]] | no | 0 | 0 | 2 |
| TSO | 2 | done | 1526 s | [[0], [2]] | no | 0 | 0 | 2 |
| TSO | 3 | done | 1001 s | [[2]] | no | 0 | 0 | 0 |

Most frequent candidate problems:

- 9x candidat# fail#d: Stag# 'm#asur#' did not produc# valid output in # att#mpts#
- 1x candidat# fail#d: Stag# 'stimulus' did not produc# valid output in # att#mpts#

HSPICE measurement warnings:

- 1x **warning**  Measurement time value specified exceeds analysis limit in measure variable p

## ministral-3_8b

| Circuit | Run | Status | Time | Clusters | Majority | Fake values | Failed .meas | Tests that fell back to drafts |
|---|---|---|---|---|---|---|---|---|
| DA | 1 | done | 2074 s | [[0], [1]] | no | 4 | 4 | 5 |
| DA | 2 | running | - s | None | no | 4 | 4 | 6 |
| DA | 3 | done | 2636 s | [[0, 1], [2]] | yes | 0 | 5 | 11 |
| FCO | 1 | done | 1022 s | [[1]] | no | 5 | 5 | 2 |
| FCO | 2 | done | 1432 s | [[2]] | no | 1 | 1 | 3 |
| FCO | 3 | done | 1894 s | [[0], [1]] | no | 4 | 4 | 4 |
| TSO | 1 | done | 2178 s | [[0], [1]] | no | 6 | 6 | 5 |
| TSO | 2 | running | - s | None | no | 5 | 8 | 2 |
| TSO | 3 | running | - s | None | no | 1 | 1 | 5 |

Most frequent candidate problems:

- 7x candidat# fail#d: Stag# 'stimulus' did not produc# valid output in # att#mpts#
- 1x candidat# fail#d: Stag# 'm#asur#' did not produc# valid output in # att#mpts#

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
| FCO | 2 | done | 854 s | [[0, 2], [1]] | yes | 0 | 21 | 0 |
| FCO | 3 | done | 1442 s | [[0]] | no | 0 | 6 | 1 |
| TSO | 1 | done | 1640 s | [[0]] | no | 0 | 6 | 0 |
| TSO | 2 | done | 2152 s | [[0, 2]] | yes | 4 | 8 | 0 |
| TSO | 3 | done | 1499 s | [[0], [1], [2]] | no | 4 | 9 | 1 |

Most frequent candidate problems:

- 6x cl_gain=# is outsid# th# plausibl# rang# (#, #)
- 6x cl_gain_#rr=# is outsid# th# plausibl# rang# (#, #)
- 1x vos=# is outsid# th# plausibl# rang# (#, #)
- 1x s#ttl#: no m#asur#m#nt stat#m#nts
- 1x tr_sl#w: no m#asur#m#nt stat#m#nts
- 1x cmrr=# is outsid# th# plausibl# rang# (#, #)

HSPICE measurement warnings:

- 5x **warning**  Measurement time value specified exceeds analysis limit in measure variable v

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
