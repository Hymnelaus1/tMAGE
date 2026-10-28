#!/usr/bin/env python3
"""Random 3-model majority votes from the models that did well in the benchmarks.

Pool = every model with at least MIN_CLEAN clean majorities (of 9 runs) in any given recomputed.json
(written by scripts/recompute_scores.py). Triples are drawn at random (fixed seed, written to PLAN.md);
each triple runs scripts/mixed_vote.sh on DA, FCO and TSO (3 runs x 3 candidates, one model per candidate;
the first model of the triple also runs the spec/scenario/stimulus/measure agents).

Usage: python3 scripts/random_triples.py <outdir> <K triples> <seed> <min_clean> <recomputed.json> [...]
"""
import itertools
import json
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def pool(files, min_clean):
    best = {}
    for f in files:
        base = Path(f).parent
        data = json.loads(Path(f).read_text())
        for mdir, topos in data.items():
            clean = sum(1 for reps in topos.values() for r in reps if r["winner"])
            sj = base / mdir / "summary.json"
            name = next(c["model"] for t in json.loads(sj.read_text()).values() for r in t for c in r["candidates"])
            if clean >= min_clean:
                best[name] = max(best.get(name, 0), clean)
    return best


def main():
    out, k, seed, min_clean, files = Path(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5:]
    models = pool(files, min_clean)
    if len(models) < 3:
        sys.exit(f"pool too small: {models}")
    combos = list(itertools.combinations(sorted(models), 3))
    rnd = random.Random(seed)
    rnd.shuffle(combos)
    picked = [rnd.sample(c, 3) for c in combos[:k]]
    out.mkdir(parents=True, exist_ok=True)
    plan = [f"# Random triples (seed {seed}, min clean majorities {min_clean})", "", "Pool: " + ", ".join(f"{m} ({n}/9)" for m, n in sorted(models.items())), "",
            f"{len(combos)} possible triples, {len(picked)} drawn.", ""] + [f"{i}. {', '.join(t)}" for i, t in enumerate(picked, 1)]
    (out / "PLAN.md").write_text("\n".join(plan) + "\n")
    print("\n".join(plan), flush=True)
    for i, t in enumerate(picked, 1):
        v = ",".join(t)
        subprocess.run([str(ROOT / "scripts" / "mixed_vote.sh"), str(out / f"T{i}"), f"DA={v}", f"FCO={v}", f"TSO={v}"], check=False)


if __name__ == "__main__":
    main()
