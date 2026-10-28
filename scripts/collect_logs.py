#!/usr/bin/env python3
"""Read-only: collects every run log of the project in one place.

Output
  docs/24_All_Runs_Log.md          index of all runs, aggregated errors/warnings, errors and fixes
  docs/logs/all_runs_raw.log.gz    every run.log concatenated (duplicates removed, license server and home path scrubbed)

Sources: runs/*/logs/run.log (UI and early runs) and batch/**/logs/run.log (benchmarks, mixed vote).
Early logs (2026-10-25) are Turkish; they are kept as recorded.
Usage: python3 scripts/collect_logs.py
"""
import collections
import gzip
import hashlib
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_MD = ROOT / "docs" / "24_All_Runs_Log.md"
OUT_GZ = ROOT / "docs" / "logs" / "all_runs_raw.log.gz"


def scrub(s):
    s = re.sub(r"(\d+@)?\b(?:\d{1,3}\.){3}\d{1,3}(:\d+)?", "<ip>", s)
    return s.replace("/home/hym", "~")


def norm(msg):
    msg = re.sub(r"\x1b\[[0-9;]*m", "", msg)
    msg = re.sub(r"candidate \d+ attempt \d+ failed", "candidate N attempt N failed", msg)
    msg = re.sub(r"'[^']{0,60}'", "'..'", msg)
    msg = re.sub(r"[-+]?\d[\d.]*(e[-+]?\d+)?", "#", msg)
    return msg.strip()[:150]


def label(p):
    parts = p.relative_to(ROOT).parts
    if parts[0] == "runs":
        return "runs", parts[1]
    b = parts[1]
    return "batch/" + b, "/".join(parts[2:-2])


def main():
    seen, runs = set(), []
    for p in sorted(list((ROOT / "runs").glob("*/logs/run.log")) + list((ROOT / "batch").glob("**/logs/run.log"))):
        txt = p.read_text(errors="replace")
        h = hashlib.md5(txt.encode()).hexdigest()
        if not txt.strip() or h in seen:
            continue
        seen.add(h)
        group, name = label(p)
        lines = txt.splitlines()
        lv = collections.Counter(re.match(r"\S+ \S+ \[(\w+)\]", l).group(1) for l in lines if re.match(r"\S+ \S+ \[(\w+)\]", l))
        models = sorted(set(re.findall(r"model=([\w.:\-]+)", txt)))
        ver = next((l for l in reversed(lines) if "verify:" in l), "")
        w = re.search(r"winner=(\w+), clusters=(\[.*?\]\]|\[\])", ver)
        start = re.match(r"(\S+ \S+)", lines[0]).group(1) if lines else ""
        job = re.search(r"(?:Run started|Koşu başladı):\s*([^·]+)·\s*(\w+)", txt)
        runs.append({"group": group, "name": name, "start": start, "job": job.group(1).strip() if job else "", "topo": job.group(2) if job else "",
                     "models": models, "err": lv["ERROR"], "warn": lv["WARN"], "winner": w.group(1) if w else "-", "clusters": w.group(2) if w else "-", "lines": lines})
    runs.sort(key=lambda r: (r["start"], r["name"]))

    OUT_GZ.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(OUT_GZ, "wt", encoding="utf-8") as g:
        for r in runs:
            g.write(f"\n##### RUN {r['group']} :: {r['name']} :: start {r['start']}\n")
            g.write("\n".join(scrub(l) for l in r["lines"]) + "\n")

    err, warn = collections.Counter(), collections.Counter()
    for r in runs:
        for l in r["lines"]:
            m = re.match(r"\S+ \S+ \[(ERROR|WARN)\]\s*(.*)", l)
            if m:
                (err if m.group(1) == "ERROR" else warn)[norm(scrub(m.group(2)))] += 1

    by_group = collections.defaultdict(list)
    for r in runs:
        by_group[r["group"]].append(r)

    L = ["# All runs: consolidated log", "",
         f"Generated {time.strftime('%Y-%m-%d %H:%M')} by `scripts/collect_logs.py`. {len(runs)} distinct runs from `runs/` and `batch/`; "
         f"{sum(len(r['lines']) for r in runs)} log lines; {sum(r['err'] for r in runs)} errors; {sum(r['warn'] for r in runs)} warnings.", "",
         "* Full text of every run: `docs/logs/all_runs_raw.log.gz` (`zcat docs/logs/all_runs_raw.log.gz | less`). License server and home path are scrubbed.",
         "* Logs of the first two days (2026-10-25) are Turkish, later ones English; they are kept as recorded.",
         "* Per-model results of the benchmark: `23_Model_Benchmark_Report.md`. Aggregated problems per run: `22_Benchmark_Findings.md`.", "",
         "## 1. Overview by group", "", "| Group | Runs | Errors | Warnings | Runs with a winner |", "|---|---|---|---|---|"]
    for g, rs in by_group.items():
        L.append(f"| {g} | {len(rs)} | {sum(r['err'] for r in rs)} | {sum(r['warn'] for r in rs)} | {sum(1 for r in rs if r['winner'] != '-')}/{len(rs)} |")
    L += ["", "## 2. Index of all runs", "", "| # | Start | Group | Run | Circuit | Models | Err | Warn | Winner | Clusters |", "|---|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(runs, 1):
        ms = ", ".join(r["models"][:3]) + (" …" if len(r["models"]) > 3 else "")
        L.append(f"| {i} | {r['start']} | {r['group']} | {r['name']} | {r['topo']} | {ms} | {r['err']} | {r['warn']} | {r['winner']} | {r['clusters']} |")
    L += ["", "## 3. Most frequent errors and warnings (all runs)", "", "Numbers are normalised (digits → `#`).", "", "### Errors", ""]
    L += [f"* {n}x `{k}`" for k, n in err.most_common(25)] or ["* none"]
    L += ["", "### Warnings", ""] + [f"* {n}x `{k}`" for k, n in warn.most_common(30)]
    L += ["", FIXES, ""]
    OUT_MD.write_text("\n".join(L))
    print("wrote", OUT_MD, "and", OUT_GZ, f"({OUT_GZ.stat().st_size // 1024} KB, {len(runs)} runs)")


FIXES = """## 4. Errors and fixes (all phases)

Status: **fixed** = in code or prompts, **pitfall** = told to the model in `config/agent_prompts.json`, **open** = still to do.

| # | Phase | Error seen in the logs | Cause | Fix | Status |
|---|---|---|---|---|---|
| 1 | early | `{context.analyses[0]...}` placeholders left in netlist or `.meas` | model copied the template | static check (`check_stimulus`, `check_measure`) + pitfall | fixed, pitfall |
| 2 | early | invalid JSON: string concatenation, double-escaped `\\\\n`, `\\n\\n\\n...` degeneration | small models | repair in `post()`, stop sequence, retry without schema | fixed |
| 3 | early | HTTP 500 with a JSON schema (command-r7b), truncated strings (mistral) | schema + long output | schema only on the first attempt | fixed |
| 4 | early | tests missing from the stimulus (e.g. 1 of 8) | "keep it short" wording; model skips tests | ask for completeness; missing tests come from the script draft and are reported | fixed, pitfall |
| 5 | early | AC source on the input for PSRR (PSRR 560 dB) | wrong test setup | prompt rule + sanity range | fixed |
| 6 | early | `.meas` written as `v(out)(12u)`, `when` for min/max, `fall=last` for settling | invalid HSPICE forms | `find ... at=`, `max/min`, `vfin` + `when ... rise=last` | pitfall |
| 7 | early | CMRR referenced across testbenches (`Undefined parameter gainvv`) | each testbench runs alone | CMRR = gain − gaincm computed by the system | fixed, pitfall |
| 8 | early | dual supply copied from 130 nm examples; FCO −7 dB with VSS = 0 | no circuit-aware supply | `supply_hint` (symmetric ±VDD/2) | fixed |
| 9 | early | a candidate crash dropped the whole run; zombie `pipeline.py` shown as "running" | no isolation | only the candidate is dropped; reaper thread + pid check | fixed |
| 10 | infra | HSPICE waits ~120 s, `Unable to checkout` when the VPN is down | license unreachable | license port pre-check before each run | fixed |
| 11 | infra | `gpt-oss:20b` crashes Ollama on 8 GB | memory | excluded | fixed |
| 12 | infra | Verilog-A compile: no `stdio.h` | missing C headers | `gcc glibc-devel` installed, smoke test passed | fixed |
| 13 | benchmark | fake `vos=25`, `gaincm=25`, `psrr=1`, `vfin=25` (26+ candidates); old "qwen2.5:7b PSRR 1.0 dB" dissent | `sim.py read_measures()` read the `temper`/`alter#` column when a `.meas` printed `failed` | `parse_measure_file()` matches values to names by position and drops `failed`; the test falls back to the script draft (commit `070b21b`) | fixed |
| 14 | benchmark | `Measurement time value specified exceeds analysis limit` (offset `at=0.6` with `.dc -0.05..0.05`; `vfin` after `.tran` end) | `at=` outside the sweep | pitfalls in measure and stimulus agent (v3_pitfalls) | pitfall |
| 15 | benchmark | `Invalid keyword td in .MEASURE Equation Evaluation` (qwen2.5:7b, 12x) | `td=` inside `param=` | pitfall | pitfall |
| 16 | benchmark | `Unable to find referenced node vout#` (qwen2.5:7b, 25x) | invented node names | pitfall: copy node names letter for letter | pitfall |
| 17 | benchmark | `Value of resistance rf ... limited to RESMIN`, `cl_gain = −560 dB` (qwen3.5:4b) | feedback resistor written as 0 | pitfall: Rf, Rg ≥ 1k | pitfall |
| 18 | benchmark | `pulse vin period too small, reset` (qwen3.5:4b) | pulse period < rise + width + fall | pitfall | pitfall |
| 19 | benchmark | `Stage 'measure' did not produce valid output in 3 attempts` (deepseek-coder 10x, qwen2.5-coder 11x) | non-JSON or over-long output | pitfall "compact JSON only"; **deepseek still fails 7 of 9 mixed-vote runs** | open |
| 20 | benchmark | ministral-3:8b runs hit the 45 min cap (3 timeouts); status stayed `running` | too slow on the Jetson | batch cap kept; timeouts reported separately in `23_Model_Benchmark_Report.md` | open (state name) |
| 21 | mixed vote | DA runs 1 and 2 without majority although all metrics agree | `zpower` differs by 7 % (1.726e-4 vs 1.614e-4), tolerance is 5 % | proposal: per-metric tolerance or leave `zpower` out of the clustering | open |
| 22 | mixed vote | cluster compares only the metrics both candidates have (command-r7b has no `phase_margin`) | `cluster()` uses the key intersection | proposal: require a minimum common set | open |
| 23 | mixed vote | winner is always candidate 0; agreement partly comes from the shared script draft | drafts fill missing tests for every candidate | proposal: report the model's own contribution per candidate | open |
| 24 | infra | `LLM call failed: Connection refused` (4x), `Remote end closed connection` (4x) | Ollama restarted / model swap on the Jetson | the stage retries (3 attempts) and the candidate is dropped only after that; the vote goes on | fixed |
| 25 | git | commits carried a co-author trailer and a session link | default attribution | history rewritten, rule saved; commits have no attribution | fixed |
"""

if __name__ == "__main__":
    main()
