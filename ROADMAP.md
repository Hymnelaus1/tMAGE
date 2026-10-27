# Roadmap

Status: `done`, `running`, `next`, `later`. Order inside a section is priority.

## Checklist

- [x] Web UI, pipeline, logging, docs (`v0.1.0`)
- [x] Script-first spec/scenario, drafts, RAG, batch runner (`v0.2.0`)
- [x] English prompts, HSPICE-manual rules, benchmark and findings tooling (`v0.3.0`)
- [x] Verilog-A toolchain smoke test
- [x] Documents translated to English, files renamed
- [ ] UI texts, code comments and `config/` labels translated to English (after the benchmark, the running benchmark executes those files)
- [x] GitHub repository, tags, automatic local and GitHub backup
- [x] Model benchmark finished (9 models, 81 runs, `docs/23_Model_Benchmark_Report.md`)
- [x] `sim.py` failed-`.meas` bug fixed, scores recomputed
- [x] Pitfalls from `config/prompt_versions/v3_pending_pitfalls.json` activated (`v3_pitfalls`)
- [ ] Mixed-model voting: command-r7b + qwen3:4b-instruct + deepseek-coder:6.7b (running next)
- [ ] RAG over books and papers (modular RAG, see below)
- [ ] Model-contribution metric in the report
- [ ] Ablation of the improvements, English vs Turkish prompts
- [ ] BGR and LNA drafts and RAG examples
- [ ] COMP and OSC through a `.subckt` wrapper
- [ ] Corners x temperature x supply (PVT) and Monte Carlo
- [ ] Verilog-A use case chosen and wired into the pipeline
- [ ] Optional LLM explanation in the report
- [ ] Per-agent model defaults in the UI, VPN on/off button
- [ ] SKY130 / ngspice fallback plan
- [ ] Final report and presentation

## Done: model benchmark

* `done` 9 models x DA/FCO/TSO x 3 runs x 3 candidates, each model alone (`scripts/model_bench.sh`). Findings are scanned automatically into `docs/22_Benchmark_Findings.md`.
* `done` `sim.py` fixed (failed `.meas` no longer becomes 25.0/1.0); all scores recomputed offline by `scripts/recompute_scores.py` into `docs/23_Model_Benchmark_Report.md`.
* `done` Benchmark pitfalls activated (`config/prompt_versions/v3_pitfalls`; v2 stays for comparison).

## Next: decide the models

* `next` Rank models per circuit (`scripts/rank_models.py`) from the corrected scores.
* `next` **Mixed-model voting**: per circuit, the top 3 models of *different base models* vote (`scripts/mixed_vote.sh`). Question: does a diverse vote beat same-model voting?
* `next` Report the model's own contribution (share of testbenches/measures the model wrote vs. script draft fallbacks).

## Knowledge base (RAG)

* `next` Study modular RAG over analog-design books and FCO/TSO papers (design equations, typical metric ranges, test recipes). Start small: a curated, per-topology note set with metadata (topology, metric, test) instead of raw PDFs; evaluate with the benchmark (same circuits, with/without RAG).

## Evidence for the thesis

* `next` Ablation on the best model: script-first, drafts, RAG, JSON schema, prompt version (v1 vs v2 vs v3), English vs Turkish prompts. Today these were measured only as one bundle.
* `later` More than one run per cell for every claim; report variance.

## Coverage

* `next` Script drafts and RAG examples for BGR (temperature and supply sweeps, start-up) and LNA (S-parameters).
* `later` COMP and OSC through a `.subckt` wrapper step; OSC needs harmonic balance.
* `later` Per-test LLM calls instead of one large stimulus call (shorter outputs, less degeneration).

## Verilog-A

* `done` Toolchain works (`gcc` + `glibc-devel`, HSPICE `.hdl` smoke test: gain 20 dB for A=10).
* `next` Choose the use case with the PhD assistant: (1) ideal behavioural blocks inside testbenches (recommended first), (2) behavioural model vs transistor-level comparison as a second verification source, (3) spec checker in Verilog-A.
* `later` Wire the chosen use case into the pipeline and the UI; rules are in `docs/21_HSPICE_Manual_Notes.md`.

## Product

* `later` UI: voting diversity warning, per-agent model defaults taken from the benchmark, benchmark view.
* `later` Q8/Q4 and model choice per agent as a saved profile.
* `later` Re-size at least one circuit for 90 nm so results describe a real design (sizing itself stays out of scope).

## Delivery

* `next` Result tables generated automatically for the report and the presentation.
* `later` Final report, presentation, README polish, release tag.

## Done

* `done` v0.1.0 UI, pipeline, logging, docs
* `done` v0.2.0 improved mode (script-first, drafts, RAG), batch runner
* `done` v0.3.0 English prompts, HSPICE-manual rules, benchmark and findings tooling
