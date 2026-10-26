#!/usr/bin/env python3
"""Read-only: ranks models per topology from a model-benchmark folder and prints the top 3.

Score per (model, topology), 3 runs each:
  clean_majority = runs with a majority cluster (>=2 candidates agree) whose WINNER has no failed-measure artefacts
  accuracy       = winner metrics within 10% of the hand reference (where a reference exists)
  score = clean_majority/3 * 0.6 + accuracy * 0.3 + speed * 0.1   (speed = 1 - mean_seconds/2700, floor 0)
A measure that HSPICE printed as 'failed' makes the candidate's values unreliable (sim.py read_measures bug),
so those runs do not count as clean. Usage: python3 scripts/rank_models.py [batch/model_bench_20261026]
"""
import glob
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "batch" / "model_bench_20261026"
REF = {"DA": {"gain": 42.58, "bw": 70e6, "phase_margin": 63.6, "psrr": 72.4, "vos": -1.6e-3, "zpower": 0.161e-3},
       "FCO": {"gain": 29.7, "bw": 6.8e6, "phase_margin": 90.9, "psrr": 43.8, "zpower": 76e-6},
       "TSO": {"gain": 43.2, "bw": 9.2e6, "phase_margin": 87.1, "psrr": 41.9, "zpower": 172e-6}}


def has_failed(cand):
    for f in glob.glob(str(Path(cand) / "*.m[sat]0")):
        if "failed" in Path(f).read_text(errors="replace"):
            return True
    return False


def main():
    rows = {}
    for mdir in sorted(p for p in BASE.iterdir() if p.is_dir()):
        sj = mdir / "summary.json"
        if not sj.exists():
            continue
        for topo, reps in json.loads(sj.read_text()).items():
            if len(reps) < 3:
                continue
            clean = acc_ok = acc_n = 0
            secs = []
            for r in reps:
                if r["seconds"]:
                    secs.append(r["seconds"])
                maj = max((len(c) for c in (r["clusters"] or [])), default=0) >= 2
                w = r["winner"]
                if not maj or w is None:
                    continue
                cand = mdir / topo / f"rep{r['rep']}" / "work" / f"cand{w}"
                if has_failed(cand):
                    continue
                clean += 1
                mt = r["winner_metrics"]
                for k, v in REF[topo].items():
                    if k in mt:
                        acc_n += 1
                        acc_ok += abs(mt[k] - v) <= 0.10 * abs(v)
            acc = acc_ok / acc_n if acc_n else 0
            speed = max(0, 1 - (sum(secs) / max(1, len(secs))) / 2700)
            rows.setdefault(topo, []).append((0.6 * clean / 3 + 0.3 * acc + 0.1 * speed, mdir.name, clean, acc, int(sum(secs) / max(1, len(secs)))))
    for topo, lst in rows.items():
        print(f"\n== {topo}")
        for i, (s, m, c, a, t) in enumerate(sorted(lst, reverse=True), 1):
            print(f"{i}. {m:30} score={s:.2f} clean_majority={c}/3 accuracy={a:.2f} avg={t}s")


if __name__ == "__main__":
    main()
