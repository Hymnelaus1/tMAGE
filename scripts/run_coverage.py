#!/usr/bin/env python3
"""Read-only: which model x circuit x prompt-version runs exist and which are missing. Writes docs/30_Run_Coverage.md."""
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "30_Run_Coverage.md"
TOPOS = ("DA", "FCO", "TSO")
SETS = [("model_bench_20261026", "v2"), ("model_bench_new_20261028", "v3")]


def runs(sj):
    d = json.loads(sj.read_text())
    return {t: [(r["rep"], r["status"]) for r in reps] for t, reps in d.items()}


def main():
    cov = {}                                   # model -> {prompt: {topo: [status..]}}
    for batch, ver in SETS:
        for mdir in sorted((ROOT / "batch" / batch).glob("*/")):
            sj = mdir / "summary.json"
            if sj.exists():
                m = json.loads(sj.read_text())
                name = None
                for reps in m.values():
                    for r in reps:
                        for c in r.get("candidates", []):
                            name = name or c.get("model")
                cov.setdefault(name or mdir.name, {})[ver] = runs(sj)
    L = ["# Run coverage", "", f"Generated {time.strftime('%Y-%m-%d %H:%M')} by `scripts/run_coverage.py`. Cell = runs finished `done` / runs planned (3 per circuit); the status `failed` or a timeout counts as not done.", "",
         "## 1. Single-model benchmark (each model alone, 3 candidates, 3 runs per circuit)", "",
         "| Model | Prompts v2 (DA / FCO / TSO) | Prompts v3 (DA / FCO / TSO) |", "|---|---|---|"]
    for m in sorted(cov):
        row = []
        for v in ("v2", "v3"):
            c = cov[m].get(v)
            row.append(" / ".join(f"{sum(1 for _, s in c.get(t, []) if s == 'done')}/{len(c.get(t, []))}" for t in TOPOS) if c else "**missing**")
        L.append(f"| {m} | {row[0]} | {row[1]} |")
    mv = ROOT / "batch" / "mixed_vote_20261027"
    L += ["", "## 2. Mixed votes (different model per candidate)", "", "| Batch | Voters | DA | FCO | TSO | Prompts |", "|---|---|---|---|---|---|"]
    row = []
    for t in TOPOS:
        sj = mv / t / "summary.json"
        row.append(str(sum(1 for r in json.loads(sj.read_text())[t] if r["status"] == "done")) + "/3" if sj.exists() else "**missing**")
    L.append("| mixed_vote_20261027 | qwen3:4b-instruct, command-r7b, deepseek-coder:6.7b | " + " | ".join(row) + " | v3 |")
    plan = ROOT / "batch" / "random_triples_20261028" / "PLAN.md"
    trip = [l.split(". ", 1)[1] for l in plan.read_text().splitlines() if l[:2] in ("1.", "2.", "3.", "4.")] if plan.exists() else []
    for i, v in enumerate(trip, 1):
        row = []
        for t in TOPOS:
            sj = ROOT / "batch" / "random_triples_20261028" / f"T{i}" / t / "summary.json"
            row.append(str(len(json.loads(sj.read_text())[t])) + "/3" if sj.exists() else "**missing**")
        L.append(f"| random_triples T{i} | {v} | " + " | ".join(row) + " | v3 |")
    L += ["", "The random triples were interrupted by a reboot on 2026-11-09 (T1 FCO stopped at run 3 of 3 started; TSO and T2-T4 never ran).", "",
          "## 3. What is missing", "",
          "1. **Prompt versions are not comparable between model groups:** the four earlier models (qwen3:4b-instruct Q4/Q8, command-r7b, deepseek-coder:6.7b) were measured alone only with prompts v2, the six new models only with v3. A fair ranking needs both groups on the same prompts.",
          "2. **Random 3-model votes:** T1 incomplete, T2, T3, T4 not run (see section 2).",
          "3. **Models taken offline** (qwen3.5:4b, qwen3.5:4b Q8, qwen2.5:7b, qwen2.5-coder:7b, ministral-3:8b) have v2 data only, by decision.",
          "4. **Circuits never run:** BGR, LNA (script drafts missing), COMP and OSC (flat netlists need a `.subckt` wrapper).",
          "5. **No ablation runs** yet (no RAG / no pitfalls / no sanity rules / single candidate vs vote).",
          "6. **No CLI-model runs** (`cli:claude`, `cli:codex`) yet; the backend exists since 2026-11-20, `codex` is not installed on this machine.", ""]
    OUT.write_text("\n".join(L))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
