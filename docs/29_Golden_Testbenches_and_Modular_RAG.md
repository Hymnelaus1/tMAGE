# Golden testbenches and Modular RAG for small models

Question: small local models need a description of *how* to build a testbench plus retrieval of golden testbenches (Modular RAG, arXiv 2407.21059). Can golden testbenches be found at Synopsys, IEEE or arXiv?

Answer: there is no public library of golden testbenches, so most of them have to be built in-house. Searched 2026-11-20 (search summaries only; the papers themselves were not opened).

## 1. Sources

| Source | What exists | Use |
|---|---|---|
| Synopsys web | No public example library. Official examples are behind SolvNet (login). Public: reference PDFs such as the HSPICE quick reference card. | Nothing to scrape; the manual stays away from the models. |
| Local HSPICE install | `hspice/demo/hspice/` has 361 `.sp` files, 120 with `.meas` (e.g. `apps/alm124.sp`, `apps/ampg.sp`, `apps/mcdiff.sp`, `behave/op_amp.sp`). | `.meas` and analysis syntax patterns. Not SAED90 and not our metrics. Synopsys material: keep local, never commit. |
| arXiv / IEEE | Masala-CHAI (arXiv 2411.14299): about 7,500 textbook SPICE netlists (circuits, not testbenches). NetlistBench (arXiv 2608.12197) and an op-amp netlist benchmark (arXiv 2508.19393): netlist recognition. | No dataset that pairs circuits with testbenches was found. |
| Course / application material | TI SPICE Universal Test Circuits (snoa475), Berkeley EE105 op-amp lab, Stanford HSPICE sample (`.meas ac` UGB and phase margin). | Test ideas (slew, offset, bandwidth); rewrite for SAED90; licenses not checked. |

## 2. Where golden testbenches come from

1. Hand-verified ones: `knowledge/examples` (8 circuits); DA, FCO, TSO have hand references.
2. Winners of clean majorities that are within 10 % of the hand reference (self-distillation: always verify against the reference).
3. Patterns from the local demos, rewritten by us (`.meas` forms only).

## 3. Shape for small models, mapped to Modular RAG

Modular RAG (Gao et al. 2024) decomposes a RAG system into operators in a graph with routing, scheduling and fusion, and patterns linear, conditional, branching and looping.

| Modular RAG element | In tMAGE |
|---|---|
| Router | Pick knowledge by `test_id` and topology, not by embedding similarity over a whole testbench |
| Module = knowledge card | One recipe card per test: purpose, setup rules (e.g. PSRR needs `AC 1` on the supply), one working SAED90 testbench, the `.meas` pattern, expected range, known pitfalls |
| Per-agent index | Separate cards for the stimulus agent and the measure agent |
| Loop | The checker retry (3 attempts) already is the loop; a failure could pull a more specific card on the next attempt |
| Switchable modules | Each module can be turned off: this gives the ablation |

Why cards: the main failure cause in `28_LLM_Run_Report.md` is output cut off at the token limit (447 calls). Short cards keep prompt and reply short.

First cards to write (the tests models skip or break most): `tran_slew`, `power_area`, `vos_temp`, `cl_gain`, `offset`. Each card is verified on DA, FCO and TSO against the hand reference.

## 4. Sources

* Modular RAG: https://arxiv.org/abs/2407.21059
* Masala-CHAI: https://arxiv.org/pdf/2411.14299
* NetlistBench: https://arxiv.org/pdf/2608.12197
* Op-amp netlist benchmark: https://arxiv.org/pdf/2508.19393v1.pdf
* HSPICE quick reference: https://www.synopsys.com/content/dam/synopsys/verification/hspice-quickrefcard-M-2017-03.pdf
* TI SPICE Universal Test Circuits: https://ti.com/lit/pdf/snoa475
* Berkeley EE105 lab: https://inst.eecs.berkeley.edu/~ee105/fa19/labs/Lab2.ee105.fa19.bx2.pdf
* Stanford HSPICE sample: https://web.stanford.edu/class/ee133/handouts/general/hspice_sample.pdf
