#!/usr/bin/env python3
"""Batch runner: for every topology netlist we have, REPS runs, each a vote over N candidates.

Çıktı klasörü (varsayılan ~/tmage/batch/<tarih>/):
  README.md, SUMMARY.md, summary.json   özet, kullanılan modeller ve ayarlar
  manifest.json                         model özetleri (digest), ayarlar, atlanan topolojiler ve nedenleri
  code_snapshot/                        koşu anındaki engine/ ve config/ kopyası
  batch.log                             toplu çalıştırıcı günlüğü
  <TOPOLOJI>/rep<k>/                    koşunun tamamı: job/context, orijinal+uyarlanmış netlist, üretilen testbench'ler,
                                        HSPICE çıktıları, logs/ (LLM yazışmaları dahil), stages/, report.md
Kullanım: python3 engine/batch.py [--reps 3] [--n 3] [--only DA,FCO]   (sunucu 127.0.0.1:8765'te çalışıyor olmalı)
"""
import argparse
import json
import os
import shutil
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine"))
from pipeline import license_reachable  # noqa: E402

API = "http://127.0.0.1:8765"
JETSON = "http://100.113.87.120:11434"
INPUTS = ROOT / "knowledge" / "inputs"
VOTERS = ["qwen3:4b-instruct", "qwen2.5:7b", "command-r7b:latest"]
STAGE_AGENT_MODEL = "qwen3:4b-instruct"
RUN_TIMEOUT = 45 * 60

# topoloji -> (netlist dosyası, analizler)
CORE = ["ac_loop", "cmrr", "psrr", "cl_gain", "offset", "tran_slew", "vos_temp", "power_area"]
TOPOS = {
    "DA": ("amp_llm.sp", CORE), "FCO": ("fcascode_llm.sp", CORE), "TSO": ("tso2_llm.sp", CORE),
    "BGR": ("bgr_llm.sp", ["temp_sweep", "supply_sweep", "psrr", "power_area"]),
    "LNA": ("lna.sp", ["rf_sparam", "power_area"]),
}
SKIPPED = {
    "COMP": "comparator.sp is a flat netlist (no .subckt). Pipeline v0 instantiates the circuit as a subcircuit; a .subckt wrapper is needed first.",
    "OSC": "cmos_osc.sp is a flat netlist (no .subckt) and uses harmonic-balance (HB) analysis, which v0 does not support.",
}


def api(path, data=None):
    req = urllib.request.Request(API + path, json.dumps(data).encode() if data is not None else None)
    return json.load(urllib.request.urlopen(req, timeout=120))


def say(logf, msg):
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    with open(logf, "a") as f:
        f.write(line + "\n")


def make_job(topo, fname, aids, name, n):
    cat = api("/api/config")
    text = (INPUTS / fname).read_text()
    parsed0 = api("/api/parse", {"text": text, "name": fname})
    ad = api("/api/adapt", {"text": text, "tech": "saed90", "corner": "TT"})
    if not ad.get("ok"):
        raise RuntimeError("adaptation failed: " + str(ad.get("error")))
    parsed = api("/api/parse", {"text": ad["text"], "name": fname})
    an = [x for x in cat["analyses"] if x["id"] in aids]
    job = {"name": name, "topology": topo,
           "technology": {"id": "saed90", "simulator": "hspice", "vdd": "1.2", "pdk": "/opt/synopsys/edk/SAED90nm_PDK_10222017", "temps": "27", "corners": ["TT"]},
           "circuit": {"path": str(INPUTS / fname), "name": fname, "parsed": parsed["parsed"]},
           "netlist_text": ad["text"], "netlist_original": text, "adaptation": {"tech": "saed90", "report": ad["report"]},
           "analyses": [{"id": x["id"], "label": x["label"], "spice": x["spice"], "metrics": x["metrics"],
                         "params": {p["k"]: str(p["d"]) for p in x["params"]}} for x in an],
           "verification": {"method": "voting", "n": n, "tolerance_pct": 5},
           "llm": {"backend": "ollama", "url": JETSON, "voters": VOTERS[:n],
                   "agents": {k: STAGE_AGENT_MODEL for k in ("spec", "scenario", "stimulus", "measure", "judge")}}}
    return job, parsed0["tech"]


def wait_done(run_dir, logf):
    sf = run_dir / "logs" / "status.json"
    t0 = time.time()
    while time.time() - t0 < RUN_TIMEOUT:
        time.sleep(10)
        if sf.exists():
            st = json.loads(sf.read_text())
            if st.get("state") in ("done", "failed"):
                return st
    say(logf, "  TIMEOUT: stopping the run")
    try:
        pid = json.loads(sf.read_text()).get("pid")
        if pid:
            os.kill(int(pid), 15)
    except Exception:
        pass
    return {"state": "timeout"}


def summarize_run(dst):
    """Bir koşu klasöründen özet satırı çıkarır."""
    s = {"status": None, "seconds": None, "winner": None, "clusters": None, "flags": [], "spec": [], "candidates": [], "winner_metrics": {}}
    sf = dst / "logs" / "status.json"
    if sf.exists():
        st = json.loads(sf.read_text())
        s["status"], s["seconds"] = st.get("state"), st.get("seconds")
        if st.get("error"):
            s["error"] = st["error"][:200]
    vf = dst / "stages" / "05_verify.json"
    if vf.exists():
        v = json.loads(vf.read_text())["data"]
        s.update({"winner": v.get("winner"), "clusters": v.get("clusters"), "flags": v.get("flags", []), "spec": v.get("spec", [])})
    for rf in sorted((dst / "work").glob("cand*/result.json")) if (dst / "work").exists() else []:
        c = json.loads(rf.read_text())
        s["candidates"].append({"candidate": c["candidate"], "model": c.get("model"), "rules_passed": c["rules_passed"], "attempts": c["attempts"],
                                "filled": c.get("filled", {}), "fallback_tests": [t for t, x in c.get("tests", {}).items() if x.get("fallback")],
                                "issues": c["issues"][:3], "metrics": c["metrics"]})
        if s["winner"] == c["candidate"]:
            s["winner_metrics"] = c["metrics"]
    return s


def write_summary(out, results, skipped, manifest):
    (out / "summary.json").write_text(json.dumps(results, ensure_ascii=False, indent=1))
    L = ["# Batch run summary", "", f"Date: {manifest['started']} · voting models: {', '.join(manifest['voters'])} · candidates N={manifest['n']} · tolerance 5%", "",
         "| Topology | Run | Status | Time | Clusters | Winner | Flags |", "|---|---|---|---|---|---|---|"]
    for t, reps in results.items():
        for r in reps:
            L.append(f"| {t} | {r['rep']} | {r['status']} | {r['seconds'] or '-'} s | {r['clusters']} | {r['winner']} | {'; '.join(r['flags'])[:80] or '-'} |")
    L += ["", "## Measurements of the winning candidates", ""]
    for t, reps in results.items():
        for r in reps:
            if r["winner_metrics"]:
                L.append(f"- **{t} / run {r['rep']}**: " + ", ".join(f"{k}={v:.4g}" for k, v in sorted(r["winner_metrics"].items())))
                for c in r["candidates"]:
                    f = c.get("filled", {})
                    if f or c.get("fallback_tests"):
                        L.append(f"  - candidate {c['candidate']} ({c.get('model')}): testbenches completed from script drafts={f.get('stimulus', [])}, measurements completed={f.get('measure', [])}, tests that fell back to the draft={c.get('fallback_tests', [])}")
            else:
                L.append(f"- **{t} / run {r['rep']}**: no winner. " + (r.get("error") or "; ".join(i for c in r["candidates"] for i in c["issues"])[:200]))
    L += ["", "## Specification checks", ""]
    for t, reps in results.items():
        for r in reps:
            for x in r["spec"]:
                L.append(f"- {t}/{r['rep']}: {'✓' if x['ok'] else '✗'} {x['name']}: {x['detail']}")
    if skipped:
        L += ["", "## Skipped topologies", ""] + [f"- **{k}**: {v}" for k, v in skipped.items()]
    (out / "SUMMARY.md").write_text("\n".join(L))


def write_readme(out):
    (out / "README.md").write_text(
        "# Batch run outputs\n\nRepeated runs per topology are under `<TOPOLOGY>/rep<k>/`. Suggested review order:\n"
        "1. `SUMMARY.md` overall table, `manifest.json` models and settings\n"
        "2. `<TOPOLOGY>/rep<k>/report.md` report of the run\n"
        "3. `.../work/cand<i>/*.sp` generated testbenches (candidate i; `result.json` has the model and measurements)\n"
        "4. `.../logs/run.log` log, `logs/llm/` full input/output of every LLM call, `logs/sim/` HSPICE output\n"
        "5. `circuit_original.sp` source netlist, `circuit.sp` adapted (SAED90) version\n")


def summarize_only(out):
    """Rebuild SUMMARY.md / README.md from the saved summary.json (no re-run)."""
    manifest = json.loads((out / "manifest.json").read_text())
    results = json.loads((out / "summary.json").read_text())
    write_summary(out, results, manifest.get("skipped", {}), manifest)
    write_readme(out)


def main():
    if ARGS.summarize:
        summarize_only(Path(ARGS.summarize))
        return 0
    out = Path(ARGS.out) if ARGS.out else ROOT / "batch" / time.strftime("%Y%m%d_%H%M%S")
    out.mkdir(parents=True, exist_ok=True)
    logf = out / "batch.log"
    say(logf, f"Batch started: {out}")
    if not license_reachable():
        say(logf, "ERROR: license server unreachable. Bring the VPN up.")
        return 2
    try:
        tags = json.load(urllib.request.urlopen(JETSON + "/api/tags", timeout=8))["models"]
    except Exception as e:
        say(logf, f"ERROR: Jetson unreachable: {e}")
        return 3
    digests = {m["name"]: {"digest": m["digest"][:16], "params": m["details"].get("parameter_size"), "quant": m["details"].get("quantization_level")} for m in tags}
    only = ARGS.only.split(",") if ARGS.only else list(TOPOS)
    manifest = {"started": time.strftime("%Y-%m-%d %H:%M:%S"), "reps": ARGS.reps, "n": ARGS.n, "voters": VOTERS[:ARGS.n],
                "agent_model": STAGE_AGENT_MODEL, "models": {m: digests.get(m) for m in set(VOTERS + [STAGE_AGENT_MODEL])},
                "technology": "SAED90nm TT_12, HSPICE X-2025.06-SP2, VDD 1.2 V", "mode": "improved (script-first, drafts, RAG, schema)",
                "topologies": {t: {"netlist": TOPOS[t][0], "analyses": TOPOS[t][1]} for t in only if t in TOPOS}, "skipped": SKIPPED}
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
    snap = out / "code_snapshot"
    shutil.copytree(ROOT / "engine", snap / "engine", ignore=shutil.ignore_patterns("__pycache__"), dirs_exist_ok=True)
    shutil.copytree(ROOT / "config", snap / "config", ignore=shutil.ignore_patterns("*.bak", "ui_state.json", "env.sh", "jetson.env"), dirs_exist_ok=True)
    results = {}
    for topo in only:
        if topo not in TOPOS:
            continue
        fname, aids = TOPOS[topo]
        results[topo] = []
        for rep in range(1, ARGS.reps + 1):
            name = f"batch_{topo}_r{rep}"
            say(logf, f"== {topo} run {rep}/{ARGS.reps}  ({fname}, {len(aids)} analyses)")
            dst = out / topo / f"rep{rep}"
            try:
                job, src_tech = make_job(topo, fname, aids, name, ARGS.n)
                r = api("/api/jobs", job)
                rid = Path(r["dir"]).name
                run_dir = ROOT / "runs" / rid
                if not api("/api/run/start", {"dir": rid}).get("ok"):
                    raise RuntimeError("could not start the run")
                st = wait_done(run_dir, logf)
                shutil.copytree(run_dir, dst, dirs_exist_ok=True)
                (dst / "circuit_original.sp").write_text(job["netlist_original"])
                (dst / "circuit_original_tech.txt").write_text(f"source technology: {src_tech}\ntarget: saed90\n")
                s = summarize_run(dst)
                say(logf, f"  finished: {s['status']} {s['seconds']} s, winner={s['winner']}, clusters={s['clusters']}, flags={s['flags']}")
            except Exception as e:
                s = {"status": "error", "seconds": None, "winner": None, "clusters": None, "flags": [], "spec": [], "candidates": [], "winner_metrics": {}, "error": str(e)[:200]}
                say(logf, f"  ERROR: {e}")
            s["rep"] = rep
            s["run_id"] = locals().get("rid")
            results[topo].append(s)
            write_summary(out, results, SKIPPED, manifest)
    write_readme(out)
    say(logf, "Batch finished. Summary: " + str(out / "SUMMARY.md"))
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--only", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--voters", default="", help="comma-separated voter models (default: the mixed-family set)")
    ap.add_argument("--agent", default="", help="model for spec/scenario/stimulus/measure agents")
    ap.add_argument("--summarize", default="", help="rebuild SUMMARY.md from an existing batch folder")
    ARGS = ap.parse_args()
    if ARGS.voters:
        VOTERS = [v for v in ARGS.voters.split(",") if v]
    if ARGS.agent:
        STAGE_AGENT_MODEL = ARGS.agent
    sys.exit(main())
