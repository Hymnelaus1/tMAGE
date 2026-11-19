#!/usr/bin/env python3
"""Read-only: report over every LLM call of every run (runs/*/logs/llm/*.json and run.log).

Writes docs/28_LLM_Run_Report.md: calls and failure causes per model and agent, which tests the models skip or break, what is measured.
Usage: python3 scripts/llm_run_report.py
"""
import collections
import glob
import json
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "28_LLM_Run_Report.md"
CATS = [("output cut off at the token limit", r"cut off at the token limit"),
        ("invalid JSON (other)", r"JSON could not be parsed"),
        ("missing CUT instance (testbench does not instantiate the circuit)", r"missing CUT instance"),
        ("AC source missing / PSRR supply without AC 1", r"AC <magnitude>|'AC 1'|AC <genlik>"),
        ("`.meas` statement malformed (does not start with .meas)", r"must start with '\.meas'"),
        ("no analysis card (.ac/.tran/.dc/.op)", r"no analysis card|analysis card"),
        ("value outside the plausible range (sanity rule)", r"plausible range|outside")]


def cat(e):
    for name, rx in CATS:
        if re.search(rx, str(e)):
            return name
    return "other"


def main():
    calls = collections.defaultdict(list)           # (model, stage) -> [(ms, out_tokens, failed, [cats])]
    for f in glob.glob(str(ROOT / "runs/*/logs/llm/*.json")):
        try:
            j = json.loads(Path(f).read_text())
        except Exception:
            continue
        e = j.get("errors")
        if isinstance(e, str):
            try:
                e = json.loads(e)
            except Exception:
                e = [e]
        e = e or []
        calls[(j.get("model"), j.get("stage"))].append((j.get("ms") or 0, j.get("output_tokens") or 0, bool(e), sorted({cat(x) for x in e})))
    skip = collections.defaultdict(collections.Counter)   # model -> kind:test -> n
    runs = 0
    for lf in glob.glob(str(ROOT / "runs/*/logs/run.log")):
        runs += 1
        model = "?"
        for line in Path(lf).read_text(errors="replace").splitlines():
            m = re.search(r"Candidate \d+/\d+: model=([\w.:\-]+)", line)
            if m:
                model = m.group(1)
                continue
            m = re.search(r"stimulus: testbench '(\w+)' was missing", line)
            if m:
                skip[model]["stimulus missing:" + m.group(1)] += 1
            m = re.search(r"measure: model wrote no measurements for '(\w+)'", line)
            if m:
                skip[model]["measure missing:" + m.group(1)] += 1
            m = re.search(r"(\w+): model output failed \((.*?)\); script draft used", line)
            if m:
                skip[model]["failed in HSPICE:" + m.group(1)] += 1
    models = sorted({k[0] for k in calls if k[0]}, key=lambda m: -sum(len(v) for k, v in calls.items() if k[0] == m))
    L = ["# LLM run report (all runs)", "",
         f"Generated {time.strftime('%Y-%m-%d %H:%M')} by `scripts/llm_run_report.py` from {runs} runs in `runs/` and {sum(len(v) for v in calls.values())} saved LLM calls (`logs/llm/*.json`). "
         "Includes runs of every prompt version (v1, v2, v3) and every phase; for the corrected per-model score use `23_Model_Benchmark_Report.md` and `27_New_Models_Benchmark_Report.md`.", "",
         "## 1. How a testbench is produced", "",
         "```",
         "job.json -> context.json -> spec (script) -> scenario (script: which tests) -> DUT precheck (script draft simulated, no LLM)",
         "   -> N candidates, each:  stimulus agent (LLM)  : writes one testbench per test, refining the script draft, with RAG examples",
         "                           measure agent  (LLM)  : writes the .meas statements per test, refining the script draft",
         "                           static checks (CUT instance, AC source, .meas form, analysis card)  -> retry up to 3 times",
         "                           HSPICE per test  -> .ms0/.mt0/.ma0 values",
         "   -> verify: sanity rules + cluster vote (5 %) -> report",
         "```", "",
         "* The **script draft** (deterministic, from the circuit topology and the catalog) is the basis: it fixes the ports, the supply (`supply_hint`), the test list and a working testbench for every test.",
         "* The **LLM only refines**: it must return JSON (`testbenches[]`, `measurements[]`). Anything it leaves out or breaks falls back to the script draft and is **flagged**, so a candidate can look healthy while most of it is the script's work.",
         "* The model sees: the system prompt with the pitfalls (`config/agent_prompts.json`), the circuit/context JSON, the script draft and retrieved examples. The HSPICE manual is not given to it.", "",
         "## 2. What is tested and measured", "",
         "| Test (analysis) | Setup | Measured names |", "|---|---|---|",
         "| `ac_loop` | open loop, differential AC | gain, bw, phase_margin |", "| `cmrr` | common-mode AC | gaincm (CMRR = gain - gaincm, computed by the system) |",
         "| `psrr` | AC 1 on the supply | gainpsrr, psrr |", "| `tran_slew` | pulse on the buffer | slewrate, tsettle |",
         "| `cl_gain` | closed loop (unity feedback) | cl_gain, cl_gain_err, cl_bw |", "| `offset` | DC sweep | vos |",
         "| `vos_temp` | DC temperature sweep | vos_max, vos_min, vos_drift |", "| `power_area` | quiescent transient | zpower |", "",
         "Hand reference (DA): 42.58 dB, 70 MHz, 63.6 deg, PSRR 72.4 dB, Vos -1.6 mV, 0.161 mW.", "",
         "## 3. LLM calls per model and agent", "",
         "A call is *failed* when the static checker rejected the reply (the stage then retries, up to 3 attempts).", "",
         "| Model | Agent | Calls | Failed calls | Cut off at token limit | Avg time | Avg output tokens |", "|---|---|---|---|---|---|---|"]
    for m in models:
        for stage in ("stimulus", "measure"):
            v = calls.get((m, stage))
            if not v:
                continue
            n = len(v)
            fail = sum(1 for x in v if x[2])
            cut = sum(1 for x in v if CATS[0][0] in x[3])
            L.append(f"| {m} | {stage} | {n} | {fail} ({100 * fail // n} %) | {cut} | {sum(x[0] for x in v) // n // 1000} s | {sum(x[1] for x in v) // n} |")
    L += ["", "## 4. Why calls fail (checker errors)", "", "A call can carry several errors, so rows add up to more than the failed calls.", "",
          "| Model | " + " | ".join(c[0].split(" (")[0] for c in CATS) + " | other |", "|---|" + "---|" * (len(CATS) + 1)]
    for m in models:
        cnt = collections.Counter()
        for (mm, _), v in calls.items():
            if mm == m:
                for x in v:
                    cnt.update(x[3])
        L.append(f"| {m} | " + " | ".join(str(cnt[c[0]]) for c in CATS) + f" | {cnt['other']} |")
    L += ["", "Cause key: " + "; ".join(f"**{c[0].split(' (')[0]}** = {c[0]}" for c in CATS), "",
          "## 5. What the models skip or break (script-draft fallbacks)", "",
          "Counted from the run logs, attributed to the model of the candidate that was running. *stimulus missing* = the testbench is absent from the model's JSON; *measure missing* = no `.meas` for the test; "
          "*failed in HSPICE* = the model's testbench or `.meas` did not simulate (no value or HSPICE error), the draft replaced it.", "",
          "| Model | Fallbacks | Most affected tests (count) |", "|---|---|---|"]
    for m in sorted(skip, key=lambda k: -sum(skip[k].values())):
        L.append(f"| {m} | {sum(skip[m].values())} | " + ", ".join(f"{k} ({n})" for k, n in skip[m].most_common(5)) + " |")
    tot = collections.Counter()
    for c in skip.values():
        for k, n in c.items():
            tot[k.split(":")[1]] += n
    L += ["", "Fallbacks per test over all models: " + ", ".join(f"`{k}` {n}" for k, n in tot.most_common()) + ".", ""]
    OUT.write_text("\n".join(L))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
