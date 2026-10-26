# tMAGE: handoff for a new chat

Paste this file at the start of a new conversation. It captures the state of the project as of **2026-10-26 ~00:00 (+03)**: what exists, how to reach the Jetson, what the LLM tests showed, and what is still open. Language: the user writes Turkish or English; **everything an LLM sees (prompts, context, logs, reports) is in English** because small models work better that way. The web UI is Turkish.

---

## 1. What the project is

**tMAGE** (testbench Multi-Agent Generation Engine) is a GTU ELM491 graduation project (students: Orhan Haluk Tascioglu, Nisa Bekci; advisor: Prof. Dr. Engin Afacan). The user gives an analog circuit netlist and picks a topology and analyses; LLM agents generate HSPICE testbenches, the system simulates them, verifies by **majority voting plus sanity rules**, and writes a report. Sizing/optimisation is out of scope.

Target circuits: DA (diff amp), FCO (folded-cascode OTA), TSO (two-stage op-amp), BGR (bandgap). Kit also has COMP (comparator), OSC (oscillator), LNA. Main technology: **SAED 90 nm (HSPICE)**. Reference kit netlists were written for 130 nm / SKY130.

Presentation (Canva): "tMAGE Proje Onerisi". The original plan said "LLM-as-judge"; it was **replaced by voting + rule checks** (decision recorded in `docs/10_Verification_Voting.md`).

---

## 2. Machines and access

| Name | Role | Tailscale IP | Notes |
|---|---|---|---|
| `msi` | Main machine. Rocky Linux 9.8, GNOME, HSPICE, tMAGE | 100.73.38.99 | user `hym` (lowercase!), RDP via xrdp |
| `hym` | Windows PC (RDP client) | 100.105.14.59 | `mstsc` to `100.73.38.99` |
| `jetson-orin` | NVIDIA Jetson Orin Nano (8 GB), Ollama | 100.113.87.120 | Ollama on port 11434 |

- **Remote desktop:** xrdp + xorgxrdp, GNOME session via `~/.xsession` (`exec gnome-session`). Username must be lowercase. Close the physical GNOME session if RDP shows a black screen.
- **Power:** auto-suspend disabled via gsettings; battery may sit at `pending-charge` ~93% (battery-care limit, not a fault).
- **Disks:** `/` 108 GB; `/opt/synopsys` 250 GB (tools, ~72 GB used); `/data` 650 GB (installers/tmp).
- **Synopsys:** installed in `/opt/synopsys/tools` (CustomCompiler, FineSim, HSPICE, IC Validator, StarRC, X-2025.06-SP2); SAED90nm PDK in `/opt/synopsys/edk/SAED90nm_PDK_10222017`. Environment: `source ~/tmage/config/env.sh` (sets all tool paths + license; `~/.bashrc` was NOT modified, the user can append the source line). Custom Compiler launches with `cd ~ && custom_compiler &`.
- **License:** floating server on port 27200 (address in `config/env.sh`), reachable only through the university VPN.
- **VPN (always-on):** systemd service `openvpn-client@gtu` created by `sudo bash ~/tmage/scripts/vpn.sh kur` (credentials stored root-only in `/etc/openvpn/client/gtu.auth`). Split tunnel: only the license host goes through `tun0`; general internet does not. Check with `bash ~/tmage/scripts/vpn.sh durum` (service active, `tun0` present, license port reachable, public IP unchanged). If the VPN drops, HSPICE waits ~120 s then reports `Unable to checkout`; the pipeline pre-checks the license port.
- **Verilog-A:** HSPICE compiles Verilog-A to C; this machine lacks gcc/glibc headers (`stdio.h` missing). Fix needs `sudo dnf install -y gcc glibc-devel` (not done yet). HSPICE syntax: `.hdl file.va` and instantiate with an `X` prefix.

### Jetson / Ollama
```bash
curl -s http://100.113.87.120:11434/api/tags      # list models
curl -s http://100.113.87.120:11434/api/ps        # loaded model
```
- Native chat API used by the engine: `POST /api/chat` with `format` (JSON schema or "json"), `options.num_ctx=8192`, `think:false`.
- Throughput is low: **~4-13 tokens/s** (4B models ~7-13, 7-8B models ~4-9). Run time is dominated by output length.
- Only one model fits at a time; switching models reloads (tens of seconds).
- **`gpt-oss:20b` (13.8 GB) crashes Ollama on this device** (`Connection refused`, HTTP 500). Excluded.
- User rules: **never use models below 4B**; Q4/Q8 quantisations preferred. All installed models are Q4_K_M (gpt-oss MXFP4). Q8 variants of the 4B models would fit (~4.5 GB) but **downloading them is awaiting the user's approval**. 7-8B Q8 would not fit.

Installed models used (>=4B): `qwen3:4b-instruct` (4.0B), `qwen3.5:4b` (4.2B), `mistral:latest` (7.2B), `qwen2.5:7b` (7.6B), `command-r7b:latest` (8.0B), `ministral-3:8b` (8.9B). Excluded: `qwen2.5:0.5b`, `llama3.2:1b` (below 4B), `gpt-oss:20b` (crashes).

---

## 3. Code layout (`~/tmage`, local git repo, ONE commit; ~21 uncommitted changes)

| Path | What |
|---|---|
| `app/server.py`, `app/static/index.html` | Local web UI (stdlib only), `http://127.0.0.1:8765`, start with `~/tmage/run.sh`. Palette from the presentation. 5 sections: circuit, topology, technology, analyses, LLM (+ voting-model selection) |
| `config/catalog.json` | topologies (DA, FCO, TSO, BGR, COMP, OSC, LNA, custom), technologies (saed90, sky130, gtu130), 20 analyses (English `label_en`/`desc_en` for LLMs), agents, backends |
| `config/stages.json` | stage order + output schemas: spec, scenario, stimulus, measure, verify, report |
| `config/agent_prompts.json` | **English per-agent prompts with "known errors and fixes"** |
| `engine/pipeline.py` | the pipeline (see below) |
| `engine/handoff.py` | builds `context.json`, stage validation, system prompts, JSON schemas |
| `engine/rag.py` | knowledge-base retrieval + script **drafts** (testbench + `.meas`) |
| `engine/llm.py`, `sim.py`, `log.py` | Ollama client, HSPICE runner/parsers, logging |
| `engine/bench.py` | per-agent model benchmark |
| `engine/batch.py` | batch runner (N topologies x reps, voted) |
| `knowledge/inputs/` (65 files), `knowledge/examples/` | copies of the USB kit inputs (kit netlists, 130 nm models); git-ignored |
| `scripts/vpn.sh` | always-on VPN service installer/status |
| `docs/` | Obsidian vault (16 notes + this file) |
| `runs/`, `bench/`, `batch/` | outputs (git-ignored) |

Kit source on USB: `/run/media/hym/USB_STRELEC/USB_STRELEC/{SYNOPSYS_KURULUM,tb}`. Originals were **copied, not moved**.

---

## 4. Pipeline design (v0, SAED90 only)

```
job.json -> context.json -> spec -> scenario -> [DUT precheck] -> N candidates{stimulus -> measure -> HSPICE} -> verify (rules + vote) -> report
```
- Run folder `runs/<id>/`: `job.json`, `circuit.sp`, `context.json`, `stages/NN_*.json`, `work/cand*/` (testbenches, HSPICE output, `result.json`), `logs/` (`run.log`, `events.jsonl`, `llm/*.json` full prompts+replies, `sim/*.txt`, `status.json`), `report.md`.
- **Improved mode (`TMAGE_IMPROVED=1`, default when started from the UI):**
  1. spec and scenario are done by **script** (port-name hints, one test per selected analysis), no LLM call.
  2. Script **drafts** of testbench and `.meas` (verified syntax) are given to the model, which refines them.
  3. **RAG**: matching real testbench/`.meas` examples from the kit.
  4. JSON schema (first attempt only), token caps, truncation detection, format example.
  5. English prompts with known errors and fixes (see section 7).
  6. Output repair (`post()`): double-escaped `\\n`, missing `test_id`, and **missing tests completed from script drafts** (logged and counted as "model contribution").
  7. If a model testbench fails in HSPICE, the script draft for that test is used (flagged).
  8. A candidate crash drops that candidate only; voting continues.
  9. **DUT precheck**: script runs the draft AC test first; non-positive gain stops the run with a diagnosis (saves LLM time on broken circuits).
- **Verification:** sanity ranges (`RULES` in `pipeline.py`), candidates clustered by metric tolerance (default 5%), majority wins; derived CMRR = gain - gaincm; spec checks from user limits (offset max, closed-loop gain error, slew min, settling max, drift max).
- **Voting:** `n` candidates, each generated by a different "voter" model (UI block "Hakem: oylama"). Default voters: `qwen3:4b-instruct`, `qwen2.5:7b`, `command-r7b:latest` (different families on purpose).
- **Circuit-aware supply:** `context.circuit.supply_hint` is set when the subcircuit has voltage sources referenced to ground (FCO has `Vcm1/Vcm2` to GND). Then testbenches use symmetric supplies (+/-VDD/2, common mode 0) instead of VSS=0.

Analyses available (catalog ids): `op, ac_loop, cmrr, psrr, noise, tran_slew, cl_gain, offset, vos_temp, tran_start, comp_tran, osc_pn, rf_sparam, dc_transfer, temp_sweep, supply_sweep, power_area, corners, montecarlo, verilog_a`. **Script drafts exist only for:** `ac_loop, cmrr, psrr, power_area, cl_gain, offset, tran_slew, vos_temp` (op-amp-like circuits with ports inp/inn/out/vdd/vss).

---

## 5. LLM test results

Task: SAED90 DA, `ac_loop` + `power_area` (benchmark). Score = fraction of measurements within 10% of a hand-written reference. Single run per cell.

### 5.1 Baseline vs improved mode (total time)

| Model | Baseline | Improved |
|---|---|---|
| qwen3:4b-instruct | stimulus 0.00, measure 0.00 (319 s) | **1.00 / 1.00 (78 s)** |
| qwen3.5:4b | 0.75 / 0.00 (150 s) | **1.00 / 1.00 (91 s)** |
| qwen2.5:7b | 0.25 / 0.00 (252 s) | **1.00 / 1.00 (91 s)** |

Baseline LLM-written spec/scenario took 63-81 s and 19-33 s; improved mode does them by script in 0 s.

### 5.2 All models, improved mode

| Model | stimulus | measure | Notes |
|---|---|---|---|
| qwen3:4b-instruct | 1.00 (47 s) | 1.00 (27 s) | fastest, reliable |
| qwen3.5:4b | 1.00 (46 s) | 1.00 (41 s) | reliable |
| qwen2.5:7b | 1.00 (52 s) | 1.00 (35 s) | reliable in benchmark; **dissents in full batch (see 6)** |
| command-r7b | 1.00 (66 s) | 1.00 (65 s) | HTTP 500 with JSON-schema; works without schema |
| mistral | 0.00 | 1.00 (33-40 s) | writes netlists as code (`"Vdd " + context.x + ...`) -> invalid JSON; usable for measure only |
| ministral-3:8b | 0.75 (119 s) | 0.25 (90 s) | `.meas` syntax errors; unreliable |
| gpt-oss:20b | - | - | crashes Ollama |
| qwen2.5:0.5b | - | - | cannot produce valid JSON (spec failed 3x) |

### 5.3 Per-agent recommendation (current)
- spec, scenario: **script**; LLM fallback only for unknown ports / custom topology (`qwen2.5:7b` / `qwen3:4b-instruct`).
- stimulus: `qwen3:4b-instruct`, `qwen3.5:4b`, `qwen2.5:7b` (46-52 s); backup `command-r7b`.
- measure: `qwen3:4b-instruct` (27 s); backup `mistral`.
- voting: diverse families (`qwen3:4b-instruct`, `qwen2.5:7b`, `command-r7b`).

### 5.4 Caveats
- Improvements were measured **as a bundle** (script-first + drafts + RAG + schema + English prompts); no ablation. The effect of English vs Turkish prompts was **not measured separately**.
- One run per cell; LLM output varies run to run.
- In the full 8-analysis runs the model often writes only part of the testbenches (e.g. 1 of 8); the rest is completed from script drafts. Reports now show "Model contribution".

---

## 6. Reference numbers and batch results

**Hand/script reference (SAED90 TT, drafts, no LLM):**
- DA (single supply): gain 42.58 dB, BW 70 MHz, PM 63.6 deg, CMRR 67.8 dB, PSRR 72.4 dB, closed-loop gain error 0.057 dB (BW 63.9 MHz), Vos -1.6 mV, slew 24.6 V/us, settling 10 ns, Vos drift 3.37 uV/degC, power 0.161 mW.
- FCO (symmetric +/-0.6 V): gain 29.7 dB, BW 6.8 MHz, PM 90.9 deg, CMRR 51.6, PSRR 43.8, Vos -7.9 mV, slew 3.4 V/us, settling 100 ns, drift 25 uV/degC, power 76 uW. (With VSS=0 it shows -7 dB because of ground-referenced bias; that was the root cause of the first FCO failure.)
- TSO (single supply): gain 43.2 dB, BW 9.2 MHz, PM 87.1 deg, CMRR 43.1, PSRR 41.9, slew 5.5 V/us, settling 85 ns, drift 11.6 uV/degC, power 172 uW.
- Device sizes are still the old 130 nm values (sizing is out of scope); HSPICE gives a harmless BSIM4 geometry warning.

**Batch plan:** DA, FCO, TSO, BGR, LNA x 3 runs x 3 voted candidates. COMP and OSC are skipped (flat netlists without `.subckt`; OSC also needs harmonic balance).
- **Batch v1** (`batch/20261025_204154`, earlier code/prompts): DA run 1 and 3 done (cluster [[0,2],[1]]), DA run 2 failed (one candidate crashed the run; now fixed), FCO run 1 failed (all candidates gain -7 dB: supply problem; now fixed). Kept for comparison.
- **Batch v2** (`batch/20261025_220928_v2`, consistent final code): DA run 1 (793 s) and 2 (929 s) cluster [[0,2],[1]]; DA run 3 (1338 s) clusters [[0],[1]] with flag "No majority: largest cluster 1/3". **The batch process died when the previous session ended, right after FCO run 1 started. FCO, TSO, BGR, LNA have NOT been run in v2.** To resume: `cd ~/tmage && python3 engine/batch.py --only FCO,TSO,BGR,LNA --out batch/<new folder>`; rebuild a summary with `python3 engine/batch.py --summarize <folder>`.
- **Unexamined anomaly:** in DA the `qwen2.5:7b` candidate repeatedly disagreed (v1 run 1: CMRR 17.6 dB, PSRR 1.0 dB vs 67.8 / 72.4 for the others). Probably a wiring mistake in its CMRR/PSRR testbench; nobody has opened `DA/rep*/work/cand1/{cmrr,psrr}.sp` yet. Voting caught it (it is the outlier), sanity rules did not.

---

## 7. Intuition and lessons for small LLMs on this task

**What works**
- Do everything deterministic by **script**; use the LLM only for judgement or creativity. Spec and scenario by script removed 2-3 minutes and all failures there.
- Give the model a **verified draft and ask it to refine it**. This is the single biggest reliability gain; free-form generation of whole testbenches by 4B models is fragile.
- Short, rule-based English prompts with an explicit "known errors and fixes" list; a concrete example of the output format.
- Sanity rules on measured values catch wrong testbenches (e.g. PSRR 560 dB when the AC source was missing on the supply). **Diverse-family voting** catches wiring errors that still pass sanity ranges.
- Put the repair/validation **before** the expensive step: static checks on the netlist (placeholders, CUT instance, sources, analysis card, AC source) are far cheaper than an HSPICE round trip plus an LLM retry (~2 min).
- Per-test/per-candidate isolation: one failure must not abort the vote; fall back to the draft and flag it.

**Failure patterns seen (these are baked into `config/agent_prompts.json`)**
- Unresolved template placeholders (`{context.analyses[0]...}`) and **string concatenation in JSON** (mistral).
- Missing sources, missing CUT instance, missing analysis card; `.ac` with no AC source; PSRR with the AC on the input instead of the supply.
- Dual supply copied from old 130 nm examples; ground-referenced bias circuits (FCO) mis-biased with VSS=0.
- `.meas` mistakes: `v(out)(12u)` syntax, `when ... fall=last` for settling (use `vfin` then `when v(out)='vfin-tol' rise=last`), `when` for min/max (use `max`/`min`), measuring `area`, cross-testbench references (CMRR must be derived by the system).
- Output **degeneration** (endless `\n\n\n...` inside a JSON string) hit the token cap; stop sequence and retries without schema help. **Double-escaped `\\n`** when the prompt talks about escaping.
- JSON-schema constrained output breaks some models (HTTP 500 on command-r7b, truncated strings on mistral): use the schema on the first attempt only.
- A "keep it short / hardware is slow" sentence in the prompt made the model **skip tests**; do not push brevity, demand completeness instead.
- Models differ more by family than by size: a 4B Qwen beat 7-9B Mistral-family models on this structured task.

**Practical numbers:** ~1.4k tokens of system prompt + ~3k tokens of user data per call fits the 8192 context; 8 stimulus tests ~1.1-2k output tokens (60-180 s); a 3-candidate, 8-analysis run takes 13-22 min.

---

## 8. Known issues / pitfalls

| Issue | State |
|---|---|
| BGR and LNA: no script drafts, model writes everything alone | expected weak; BGR netlist is SKY130 adapted to SAED90 (BJT lib only auto-included in TT) |
| COMP, OSC: flat netlists | skipped; would need a `.subckt` wrapper step |
| Verilog-A | blocked on `gcc`/`glibc-devel`; catalog entry exists, not wired into runs |
| Sizes from 130 nm | not re-sized; results validate the flow, not a real 90 nm design |
| `pkill -f` on a pattern that appears in your own command line kills your shell | use `pgrep -f '^python3 ...'` or `[x]` tricks |
| Zombie `pipeline.py` made a finished run look "running" | fixed (reaper thread + pid check) |
| `.bashrc` edit and persistence | the sandbox blocked auto-editing `~/.bashrc`; user can run the one-line `echo ... >> ~/.bashrc` |
| Git | 21 uncommitted changes; no remote; use a **private** repo if pushed; no secrets are tracked |

---

## 9. Open items / next steps
1. Resume the batch for FCO, TSO, BGR, LNA (3 runs each), then add one DA run; rebuild `SUMMARY.md` (English) and review outputs in the batch folder (the user intends to review testbenches and results by hand).
2. Inspect the `qwen2.5:7b` CMRR/PSRR dissent in DA; decide whether to change voters or prompt.
3. Ablation of the improvements (script-first, drafts, RAG, schema, English) and a Turkish-vs-English prompt comparison.
4. Script drafts and RAG examples for BGR (temperature/supply sweep, startup), LNA (S-parameters), then COMP/OSC with `.subckt` wrappers.
5. Per-test LLM calls instead of one big stimulus call (shorter outputs, less degeneration).
6. Voting settings in the UI beyond N/tolerance/voter models (e.g. diversity warnings, per-agent model defaults from the benchmark).
7. Pending user approval: Q8 downloads for the 4B models; installing `gcc glibc-devel` for Verilog-A; `.bashrc` line; git commit/push; the original "which Verilog-A use" question (ideal behavioural blocks in testbenches, behavioural model comparison, or a Verilog-A spec checker) is unanswered.
8. Project requests mentioned by the user: closed-loop gain check, offset suitability, slew/settling, DC temperature sweep, Verilog-A (all but Verilog-A are implemented as analyses).

---

## 10. Quick commands
```bash
source ~/tmage/config/env.sh                       # tools + license
bash ~/tmage/scripts/vpn.sh durum                  # VPN / license health
~/tmage/run.sh                                     # UI at http://127.0.0.1:8765
cd ~/tmage && TMAGE_IMPROVED=1 python3 engine/bench.py --improved --models qwen3:4b-instruct
cd ~/tmage && python3 engine/batch.py --only FCO,TSO,BGR,LNA --reps 3 --n 3
tail -f ~/tmage/runs/<id>/logs/run.log             # live run log
```

## 11. Suggested opening message for the new chat
> Context: tMAGE project (analog testbench generation with small LLMs on a Jetson Orin Nano + HSPICE/SAED90 on a Rocky Linux machine). Read `~/tmage/docs/17_Handoff_for_new_chat.md` first. Then: check VPN and Jetson, resume the batch for FCO/TSO/BGR/LNA, and help me review the outputs. Rules: no LLM below 4B, prefer Q4/Q8, prompts/logs/reports in English, UI in Turkish, ask before downloading models or pushing to GitHub.
