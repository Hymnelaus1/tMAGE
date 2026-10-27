#!/usr/bin/env python3
"""Read-only: re-scores a model-benchmark folder from the saved .ms0/.mt0/.ma0 files (no HSPICE, no LLM).

Why: before the sim.py fix a failed .meas was read as the temper/alter# column (25.0 / 1.0). Here every test is
re-parsed with the fixed parser; a test whose measure printed 'failed' (and did not fall back to the script draft)
makes the candidate fail its sanity check. Candidates are then re-clustered exactly like Pipeline.cluster (5 %).

Writes docs/23_Model_Benchmark_Report.md and <batch>/recomputed.json.
Usage: python3 scripts/recompute_scores.py [batch/model_bench_20261026]
"""
import collections
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine"))
import sim  # noqa: E402
from pipeline import RULES  # noqa: E402

BASE = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "batch" / "model_bench_20261026"
OUT = ROOT / "docs" / "23_Model_Benchmark_Report.md"
TOL = 0.05
REF = {"DA": {"gain": 42.58, "bw": 70e6, "phase_margin": 63.6, "psrr": 72.4, "vos": -1.6e-3, "zpower": 0.161e-3},
       "FCO": {"gain": 29.7, "bw": 6.8e6, "phase_margin": 90.9, "psrr": 43.8, "zpower": 76e-6},
       "TSO": {"gain": 43.2, "bw": 9.2e6, "phase_margin": 87.1, "psrr": 41.9, "zpower": 172e-6}}
SHORT = {"qwen3_4b-instruct": "qwen3:4b-instruct (Q4)", "qwen3_4b-instruct-2507-q8_0": "qwen3:4b-instruct Q8", "command-r7b_latest": "command-r7b",
         "deepseek-coder_6.7b": "deepseek-coder:6.7b", "qwen3.5_4b-q8_0": "qwen3.5:4b Q8", "qwen2.5-coder_7b": "qwen2.5-coder:7b",
         "qwen2.5_7b": "qwen2.5:7b", "qwen3.5_4b": "qwen3.5:4b", "ministral-3_8b": "ministral-3:8b"}


def rescore_candidate(cdir):
    """Returns (metrics, problems, failed_names, fallback_tests) from the files saved by the run."""
    rf = cdir / "result.json"
    if not rf.exists():
        return None
    c = json.loads(rf.read_text())
    metrics, failed, fb = {}, [], []
    for tid, t in c.get("tests", {}).items():
        base = tid + "_taslak" if t.get("fallback") else tid
        if t.get("fallback"):
            fb.append(tid)
        got, bad = {}, []
        for ext in ("mt0", "ma0", "ms0"):
            f = cdir / f"{base}.{ext}"
            if f.exists():
                g, b = sim.parse_measure_file(f)
                got.update(g)
                bad += b
        metrics.update(got)
        failed += [f"{tid}.{n}" for n in bad]
    if "gain" in metrics and "gaincm" in metrics:
        metrics["cmrr"] = metrics["gain"] - metrics["gaincm"]
    problems = []
    for k, v in metrics.items():
        r = RULES.get(k)
        if r and not (r[0] <= v <= r[1]):
            problems.append(f"{k} out of range")
    problems += [f"failed .meas {n}" for n in failed]
    problems += [i for i in c.get("issues", []) if "simulation error" in i or "no measure" in i]
    if not metrics:
        problems.append("no measurements")
    return metrics, problems, failed, fb


def cluster(cands):
    groups = []
    for c in cands:
        for g in groups:
            ref = g[0]["metrics"]
            keys = set(ref) & set(c["metrics"])
            if keys and all(abs(c["metrics"][k] - ref[k]) <= TOL * max(abs(ref[k]), 1e-12) for k in keys):
                g.append(c)
                break
        else:
            groups.append([c])
    groups.sort(key=len, reverse=True)
    return groups


def main():
    data, causes = {}, collections.defaultdict(collections.Counter)
    for mdir in sorted(p for p in BASE.iterdir() if p.is_dir()):
        sj = mdir / "summary.json"
        if not sj.exists():
            continue
        for topo, reps in json.loads(sj.read_text()).items():
            for r in reps:
                cands = []
                for cdir in sorted((mdir / topo / f"rep{r['rep']}" / "work").glob("cand*")):
                    res = rescore_candidate(cdir)
                    if not res:
                        continue
                    m, probs, failed, fb = res
                    cands.append({"id": cdir.name, "metrics": m, "problems": probs, "fallback": fb, "ok": not probs})
                    for p in probs:
                        causes[mdir.name][re.sub(r"^failed \.meas .*?\.", "failed .meas ", p) if p.startswith("failed") else p] += 1
                good = [c for c in cands if c["ok"]]
                groups = cluster(good)
                maj = len(groups[0]) if groups else 0
                win = groups[0][0] if groups and maj >= 2 else None
                acc_ok = acc_n = 0
                if win:
                    for k, v in REF[topo].items():
                        if k in win["metrics"]:
                            acc_n += 1
                            acc_ok += abs(win["metrics"][k] - v) <= 0.10 * abs(v)
                data.setdefault(mdir.name, {}).setdefault(topo, []).append(
                    {"rep": r["rep"], "status": r["status"], "seconds": r["seconds"], "n_cands": len(cands), "n_ok": len(good), "majority": maj,
                     "winner": win["id"] if win else None, "acc": [acc_ok, acc_n], "fallback_tests": sum(len(c["fallback"]) for c in cands),
                     "dropped": [c["problems"] for c in cands if not c["ok"]]})
    (BASE / "recomputed.json").write_text(json.dumps(data, indent=1))

    L = ["# Model benchmark report", "",
         f"Generated {time.strftime('%Y-%m-%d %H:%M')} by `scripts/recompute_scores.py` from `{BASE.relative_to(ROOT)}` (saved `.ms0/.mt0` files re-parsed with the fixed parser; no HSPICE or LLM calls).", "",
         "Setup: each model alone (3 voters = the same model), circuits DA / FCO / TSO, 3 runs each, 3 voted candidates per run, SAED 90 nm, HSPICE X-2025.06, prompts v2 (`config/prompt_versions/v2_manual`). "
         "Reference values come from the hand-simulated reference (`knowledge/ref_da.json`, `docs/17_Handoff_for_new_chat.md`).", "",
         "Definitions: **clean majority** = a run where at least 2 of 3 candidates passed the sanity rules (no failed `.meas`, values in range) and agree within 5 %. "
         "**Accuracy** = winner metrics within 10 % of the reference. **Draft fallbacks** = tests where the model output did not run and the script draft was used (the model's own contribution is lower than the majority suggests).", ""]
    L += ["## Summary per model", "", "| Model | Clean majority (of 9) | DA | FCO | TSO | Accuracy | Timeouts/failed runs | Draft fallbacks | Avg time per run |", "|---|---|---|---|---|---|---|---|---|"]
    ranking = []
    for m, topos in data.items():
        per = {t: sum(1 for r in v if r["winner"]) for t, v in topos.items()}
        allr = [r for v in topos.values() for r in v]
        okn = sum(per.values())
        a = [sum(r["acc"][0] for r in allr), sum(r["acc"][1] for r in allr)]
        bad = sum(1 for r in allr if r["status"] != "done")
        fb = sum(r["fallback_tests"] for r in allr)
        secs = [r["seconds"] for r in allr if r["seconds"]]
        avg = int(sum(secs) / len(secs)) if secs else 0
        ranking.append((okn, a[0] / a[1] if a[1] else 0, -avg, m))
        L.append(f"| {SHORT.get(m, m)} | {okn} | {per.get('DA', 0)}/3 | {per.get('FCO', 0)}/3 | {per.get('TSO', 0)}/3 | {a[0]}/{a[1]} | {bad} | {fb} | {avg} s |")
    L += ["", "## Where and why models failed", ""]
    L += ["Candidates dropped by the sanity check (count over 27 runs x 3 candidates = 81 per model), grouped by cause:", ""]
    for m, _ in [(x[3], 0) for x in sorted(ranking, reverse=True)]:
        top = causes[m].most_common(5)
        L.append(f"* **{SHORT.get(m, m)}**: " + ("; ".join(f"{n}x {k}" for k, n in top) if top else "no dropped candidates"))
    L += ["", "## Per circuit: runs with a clean majority (of 3)", "", "| Model | DA | FCO | TSO |", "|---|---|---|---|"]
    for _, _, _, m in sorted(ranking, reverse=True):
        t = data[m]
        L.append(f"| {SHORT.get(m, m)} | " + " | ".join(f"{sum(1 for r in t.get(c, []) if r['winner'])}/3 ({sum(r['n_ok'] for r in t.get(c, []))}/9 cands ok)" for c in ("DA", "FCO", "TSO")) + " |")
    L += ["", "## Reading the table", "",
          "* Scores before the parser fix are **not comparable**: they counted the 25.0 / 1.0 artefact as a measurement. Use this report, not `22_Benchmark_Findings.md`, for conclusions.",
          "* Timeouts: runs cut by the 45-minute batch cap are listed separately; they say the model was too slow on the Jetson, not that it was wrong.",
          "* Details of the individual errors and the resulting prompt pitfalls: `20_Observed_Errors.md`, `config/prompt_versions/v3_pending_pitfalls.json`.", ""]
    OUT.write_text("\n".join(L))
    print("wrote", OUT)
    print("\n".join(L[7:7 + 4 + len(data)]))


if __name__ == "__main__":
    main()
