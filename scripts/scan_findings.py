#!/usr/bin/env python3
"""Read-only scanner for a model-benchmark folder. Writes docs/22_Benchmark_Bulgulari.md.

Never touches config/ or engine/ and never starts runs. Safe to run while a benchmark is in progress.
Usage: python3 scripts/scan_findings.py [batch/model_bench_20261026]
"""
import collections
import glob
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "batch" / "model_bench_20261026"
OUT = ROOT / "docs" / "22_Benchmark_Bulgulari.md"
SUSPECT = (25.0, 1.0)  # temper / alter# column values that leak when a measure fails (sim.py read_measures bug)


def failed_measures(cand):
    """Names of measures HSPICE printed as 'failed' in the .ms0/.mt0/.ma0 files of a candidate folder."""
    out = []
    for f in glob.glob(str(cand / "*.m[sat]0")):
        lines = [l for l in Path(f).read_text(errors="replace").splitlines() if not l.startswith(("$", "."))]
        toks = " ".join(lines).split()
        if "failed" in toks:
            names = []
            for t in toks:
                try:
                    float(t)
                    break
                except ValueError:
                    if t == "failed":
                        break
                    names.append(t.lower())
            out.append((Path(f).stem, [n for n in names if n not in ("temper", "alter#")]))
    return out


def warn_kinds(cand):
    kinds = collections.Counter()
    for f in glob.glob(str(cand / "*.lis")):
        for l in Path(f).read_text(errors="replace").splitlines():
            if "measure" in l.lower() and ("warning" in l.lower() or "failed" in l.lower()) and "never reached" in l.lower() or "exceeds analysis limit" in l.lower():
                kinds[re.sub(r"\(.*?\)|\d[\d.e+-]*", "", l.strip())[:90]] += 1
    return kinds


def main():
    L = [f"# Benchmark bulguları (otomatik)", "", f"Üretildi: {time.strftime('%Y-%m-%d %H:%M:%S')} · kaynak: `{BASE.relative_to(ROOT)}` · salt okunur tarama (`scripts/scan_findings.py`)", "",
         "Sahte değer kuralı: ölçüm `failed` iken `vos/gaincm/gainpsrr/psrr/vfin/cl_gain` = 25.0 veya 1.0 ise bu sıcaklık/alter# sütunudur, gerçek ölçüm değildir (bkz. `20_Gorulen_Hatalar.md` A).", ""]
    for mdir in sorted(p for p in BASE.iterdir() if p.is_dir()) if BASE.exists() else []:
        sf = mdir / "summary.json"
        if not sf.exists():
            continue
        res = json.loads(sf.read_text())
        L += [f"## {mdir.name}", "", "| Devre | Koşu | Durum | Süre | Kümeler | Çoğunluk | Sahte değer | Başarısız .meas | Taslağa düşen test |", "|---|---|---|---|---|---|---|---|---|"]
        issues, kinds = collections.Counter(), collections.Counter()
        for topo, reps in res.items():
            for r in reps:
                rd = mdir / topo / f"rep{r['rep']}"
                sus, fm, fb = 0, 0, 0
                for cand in glob.glob(str(rd / "work" / "cand*")):
                    cand = Path(cand)
                    rf = cand / "result.json"
                    if not rf.exists():
                        continue
                    c = json.loads(rf.read_text())
                    fl = failed_measures(cand)
                    fm += sum(len(n) or 1 for _, n in fl)
                    if fl:
                        sus += sum(1 for k, v in c["metrics"].items() if v in SUSPECT)
                    fb += len([t for t, x in c.get("tests", {}).items() if x.get("fallback")])
                    for i in c.get("issues", [])[:3]:
                        issues[re.sub(r"[-\d.e+]+", "#", i)[:100]] += 1
                    kinds.update(warn_kinds(cand))
                maj = max((len(x) for x in (r["clusters"] or [])), default=0)
                L.append(f"| {topo} | {r['rep']} | {r['status']} | {r['seconds'] or '-'} s | {r['clusters']} | {'evet' if maj >= 2 else 'hayır'} | {sus} | {fm} | {fb} |")
        if issues:
            L += ["", "En sık aday sorunları:", ""] + [f"- {n}x {k}" for k, n in issues.most_common(6)]
        if kinds:
            L += ["", "HSPICE ölçüm uyarıları:", ""] + [f"- {n}x {k}" for k, n in kinds.most_common(6)]
        L.append("")
    OUT.write_text("\n".join(L))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
