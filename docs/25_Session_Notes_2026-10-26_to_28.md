# Session notes 2026-10-26 to 2026-10-28 (what was done, decided and planned)

Written so a new chat can continue without the old, very long conversation. Read this together with `17_Handoff_for_new_chat.md` (access, machines) and `18_Change_Log_Benchmark.md` (chronological log).

## 1. Rules from the user (keep them)

* **No model below 4B parameters.** Q4/Q8 of 4B+ models are fine. Ask before downloading a model.
* **Claude must never appear as a commit author, co-author or contributor** (no `Co-Authored-By`, no session link, no "Generated with" line in commits, tags or PRs). Mentions inside files are allowed. Before every push: `git log main --tags --format=%B | grep -iE 'claude|anthropic|co-authored'` must be empty and all authors must be `hym`. (Local `refs/original` still holds the pre-rewrite history; it is not pushed.)
* GitHub repo `Hymnelaus1/tMAGE` stays **private**. Never commit Synopsys tools/PDK/manual, the VPN helper, license server addresses, vendor process models, simulator outputs, `config/env.sh`, `config/jetson.env`.
* The HSPICE manual is used to improve prompts but is **not given to the models**.
* Keep old prompt versions (`config/prompt_versions/`) so a bad result can be rolled back; log every change in `18_Change_Log_Benchmark.md`.
* Big changes are backed up automatically: local snapshot in `/data/tmage_backups` and push to GitHub (`scripts/backup.sh`, post-commit hook, 2-hourly timer).
* The project language is English (docs are done; code comments, UI texts and `config/` labels are still partly Turkish).
* Do not use `pkill -f` with a pattern that matches your own command line.

## 2. What was done

| Date | Work | Where |
|---|---|---|
| 10-26 | Prompts moved to English; 8 measure rules from the HSPICE manual verified on X-2025.06 | `config/prompt_versions/v2_manual`, `21_HSPICE_Manual_Notes.md` |
| 10-26 | Model benchmark: 9 models, each alone, DA/FCO/TSO x 3 runs x 3 candidates (about 29 h) | `batch/model_bench_20261026`, `model_bench.sh` |
| 10-26 | Verilog-A toolchain smoke test (gain 20 dB); use case still open | `work/va_test` (local) |
| 10-27 | GitHub repo, README, ROADMAP, tags v0.1.0 to v0.3.1, figures instead of Mermaid | `README.md`, `docs/images/` |
| 10-27 | History rewrite (no Claude trailers), docs translated and renamed to English | `18_...` |
| 10-27 | `sim.py` failed-`.meas` bug fixed, scores recomputed offline, benchmark report | `070b21b`, `scripts/recompute_scores.py`, `23_Model_Benchmark_Report.md` |
| 10-27 | 10 benchmark pitfalls added to the prompts | `abccc68`, `config/prompt_versions/v3_pitfalls` |
| 10-27 | Mixed-model vote (qwen3:4b-instruct, command-r7b, deepseek-coder:6.7b), 3 h 15 min | `batch/mixed_vote_20261027` |
| 10-28 | All run logs consolidated with an errors-and-fixes table | `24_All_Runs_Log.md`, `docs/logs/all_runs_raw.log.gz`, `scripts/collect_logs.py` |

## 3. Results to remember

* Clean majority out of 9 runs: qwen3:4b-instruct Q4 **9**, command-r7b **8**, qwen3 Q8 8 (but 39 script-draft fallbacks), deepseek-coder:6.7b 4, qwen2.5-coder:7b 3, qwen2.5:7b 1, qwen3.5:4b 0, qwen3.5:4b Q8 0, ministral-3:8b 0. Winners match the hand reference (DA 42.58 dB / 70 MHz / 63.6 deg; FCO 29.7 dB / 6.8 MHz / 90.9 deg; TSO 43.2 dB / 9.2 MHz / 87.1 deg) within 10 %.
* Mixed vote: majority in 7 of 9 runs, but deepseek's candidate was dropped in 7 runs (measure stage did not give valid JSON), so the vote was effectively two models. DA runs 1 and 2 had no majority only because `zpower` differed by 7 % (tolerance 5 %). The winner was always candidate 0, and agreement partly comes from the shared script draft.
* The v3 pitfalls were activated after the model benchmark, so the mixed vote and the benchmark are not a one-variable comparison.

## 4. Open items (priority order)

1. **Clustering fixes** (items 21 and 22 in `24_All_Runs_Log.md`): per-metric tolerance or leave `zpower` out; require a minimum common metric set; then re-run DA.
2. **deepseek measure-stage failure**: read its raw outputs in `batch/mixed_vote_20261027/*/rep*/work` and `logs/`, decide to fix the prompt or replace it (qwen2.5-coder:7b or qwen3 Q8 are candidates).
3. **Model-contribution metric** per candidate in the report (how much came from the script draft).
4. Timeout as its own run state (ministral stayed `running`).
5. Translate remaining Turkish in code comments, `app/static/index.html`, `app/server.py`, `engine/*.py`, `config/catalog.json`, `config/stages.json` labels, `run.sh`.
6. Ablation: script-first, drafts, RAG, schema, prompt versions v1/v2/v3, English vs Turkish.
7. BGR and LNA drafts; COMP/OSC through a `.subckt` wrapper; PVT and Monte Carlo.
8. Verilog-A use case (ask the PhD assistant): ideal blocks in testbenches, behavioural vs transistor comparison, or spec checker.
9. Invite the project partner as a collaborator in GitHub settings; optional GitHub Releases per tag.
10. Before ever making the repo public: history scan, clean Tailscale IPs and machine names in `17_...`, add a `LICENSE`, advisor approval, HSPICE/PDK licensing check.

## 5. Idea under study: RAG over books and papers

* Worth trying, but as a **small curated knowledge base**, not raw PDFs: the 4B models have an 8192-token context, and most failures are HSPICE `.meas` syntax and test set-up, not circuit theory.
* **Modular RAG:** per-topology note sets (design equations, typical metric ranges, test recipes), separate indexes per agent (measure agent sees `.meas` recipes only, stimulus agent sees test set-ups), metadata filters (topology, metric, test).
* Expected value: sanity ranges, and circuits without a draft (BGR, LNA). Little gain on DA/FCO/TSO where drafts already exist.
* Measure it: same benchmark with and without RAG. Books and papers must not be committed (copyright); only our own notes.

## 6. How to continue

```bash
cd ~/tmage && source config/env.sh
git log --oneline | head                       # state of the repo
curl -s http://<jetson>:11434/api/tags         # Jetson reachable? (address in config/jetson.env)
python3 scripts/recompute_scores.py            # rebuild docs/23 from a batch folder
python3 scripts/collect_logs.py                # rebuild docs/24 and the raw log archive
scripts/mixed_vote.sh batch/<name> DA=a,b,c FCO=a,b,c TSO=a,b,c
```

The VPN must be up for HSPICE licenses (`17_...` section 2). Prompts are read on every call: do not edit `config/` or `engine/` while a batch is running.
