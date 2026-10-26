#!/usr/bin/env python3
"""Jetson'daki tüm modelleri her ajan için ayrı ayrı sınar ve ajan başına en uygun modeli önerir.

Adil karşılaştırma için her ajan, diğer aşamaların *referans* çıktısıyla denenir:
  spec      -> port rolleri referansla karşılaştırılır
  scenario  -> referans spec ile; seçilen analizlerin kapsanması
  stimulus  -> modelin testbench'i + referans .meas satırları ile HSPICE; ölçümler referansla karşılaştırılır
  measure   -> referans testbench + modelin .meas satırları ile HSPICE; ölçümler referansla karşılaştırılır

Kullanım: python3 engine/bench.py [--models a,b,c] [--timeout 420]
Çıktı: ~/tmage/bench/<tarih>/{report.md,results.json,bench.log} ve modele göre alt klasörler (tam log).
"""
import argparse
import json
import os
import shutil
import sys
import time
import traceback
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine"))
import handoff  # noqa: E402
import sim  # noqa: E402
from pipeline import Pipeline, license_reachable  # noqa: E402

URL = "http://100.113.87.120:11434"
TOL = 0.10  # ölçümler referansın %10'u içinde olmalı

EXPECT_ROLES = {"vinp": "input_pos", "vinn": "input_neg", "vout": "output", "vdd": "supply_pos", "vss": "supply_neg"}

REF_SPEC = {"port_roles": EXPECT_ROLES, "circuit_summary": "Aktif yüklü PMOS girişli fark yükselteci.", "assumptions": [], "open_questions": []}
REF_SCENARIO = {"tests": [
    {"id": "ac_loop", "analysis_id": "ac_loop", "purpose": "kazanç, bant genişliği, faz payı", "connections": {}, "sweep": {}, "metrics": ["gain", "bw", "phase_margin"]},
    {"id": "power_area", "analysis_id": "power_area", "purpose": "statik güç", "connections": {}, "sweep": {}, "metrics": ["zpower"]}],
    "order": ["ac_loop", "power_area"]}
TB_AC = ("Vdd vdd 0 1.2\nVss vss 0 0\nVcm cm 0 0.6\nVin vinp cm DC 0 AC 0.5\nVinn vinn cm DC 0 AC -0.5\n"
         "X0 vinp vinn vout vdd vss da\nCl vout 0 0.5p\n.ac dec 20 1 1e9")
TB_PW = "Vdd vdd 0 1.2\nVss vss 0 0\nVcm cm 0 0.6\nVin vinp cm DC 0\nVinn vinn cm DC 0\nX0 vinp vinn vout vdd vss da\nCl vout 0 0.5p\n.tran 10n 1u"
REF_STIM = {"testbenches": [{"test_id": "ac_loop", "file": "ac_loop.sp", "netlist_text": TB_AC},
                            {"test_id": "power_area", "file": "power_area.sp", "netlist_text": TB_PW}]}
REF_MEAS = {"measurements": [
    {"test_id": "ac_loop", "name": "gain", "statement": ".meas ac gain find par('db(v(vout))') at=1000", "expect": {"min": 20, "max": 80, "unit": "dB"}},
    {"test_id": "ac_loop", "name": "bw", "statement": ".meas ac bw when par('db(v(vout))')=0", "expect": {"min": 1e6, "max": 1e10, "unit": "Hz"}},
    {"test_id": "ac_loop", "name": "phase_margin", "statement": ".meas ac phase_margin find par('180+vp(vout)') at=bw", "expect": {"min": 45, "max": 90, "unit": "deg"}},
    {"test_id": "power_area", "name": "zpower", "statement": ".meas tran zpower avg power", "expect": {"min": 1e-6, "max": 1e-2, "unit": "W"}}]}


def say(path, msg):
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    with open(path, "a") as f:
        f.write(line + "\n")


def _params_b(txt):
    t = (txt or "").strip().upper()
    try:
        return float(t[:-1]) / (1000 if t.endswith("M") else 1)
    except ValueError:
        return 0.0


def jetson_models(min_b=3.9):
    """4B ve üzeri modeller, küçükten büyüğe: [(ad, parametre, kuantizasyon, GB)]."""
    with urllib.request.urlopen(URL + "/api/tags", timeout=8) as r:
        ms = json.load(r)["models"]
    out = [(m["name"], m["details"].get("parameter_size", "?"), m["details"].get("quantization_level", "?"), round(m["size"] / 1e9, 1))
           for m in sorted(ms, key=lambda m: m["size"]) if _params_b(m["details"].get("parameter_size")) >= min_b]
    return out


def make_run(base, dest, model):
    dest.mkdir(parents=True, exist_ok=True)
    for f in ("job.json", "circuit.sp"):
        shutil.copy(base / f, dest / f)
    ctx = json.loads((base / "context.json").read_text())
    ctx["llm"] = {"backend": "ollama", "url": URL, "agents": {k: model for k in ("spec", "scenario", "stimulus", "measure", "judge")}}
    ctx["verification"] = {"method": "voting", "n": 1, "tolerance_pct": 5}
    (dest / "stages").mkdir(exist_ok=True)
    (dest / "context.json").write_text(json.dumps(ctx, ensure_ascii=False, indent=2))
    return dest


def score_metrics(got, ref):
    if not ref:
        return 0.0
    ok = sum(1 for k, v in ref.items() if k in got and abs(got[k] - v) <= TOL * max(abs(v), 1e-12))
    return ok / len(ref)


def stage_record(p, ok, score, extra=None):
    last = getattr(p, "last", {}) or {}
    secs = last.get("ms_total", 0) / 1000
    tps = (last.get("out_tokens", 0) / (last["ms_llm"] / 1000)) if last.get("ms_llm") else 0
    return {"ok": ok, "score": round(score, 2), "attempts": last.get("attempts", 0), "seconds": round(secs, 1), "tok_per_s": round(tps, 1), **(extra or {})}


def bench_model(model, base, out, ref_metrics, logf):
    run = make_run(base, out / model.replace(":", "_").replace("/", "_"), model)
    p = Pipeline(run)
    os.environ["TMAGE_LLM_TIMEOUT"] = str(ARGS.timeout)
    res = {}

    def guard(name, fn):
        try:
            res[name] = fn()
        except Exception as e:
            res[name] = stage_record(p, False, 0.0, {"error": str(e)[:160]})
            say(logf, f"  {name}: HATA {str(e)[:120]}")
        say(logf, f"  {name}: {json.dumps(res[name], ensure_ascii=False)}")

    def t_spec():
        d = p.stage_spec()
        got = d["port_roles"]
        sc = sum(1 for k, v in EXPECT_ROLES.items() if got.get(k) == v) / len(EXPECT_ROLES)
        return stage_record(p, sc == 1.0, sc)

    def t_scenario():
        handoff.save_stage(run, "spec", REF_SPEC, "ref")
        d = p.stage_scenario()
        have = {t.get("analysis_id") for t in d["tests"]}
        sc = len(have & set(p.analyses)) / len(p.analyses)
        return stage_record(p, sc == 1.0, sc)

    def t_stimulus():
        handoff.save_stage(run, "scenario", REF_SCENARIO, "ref")
        d = p.call_stage("stimulus", p.check_stimulus)
        st = stage_record(p, True, 0.0)
        metrics, issues, _ = p.run_tests(0, d, REF_MEAS)
        sc = score_metrics(metrics, ref_metrics)
        return {**st, "score": round(sc, 2), "ok": sc == 1.0 and not issues, "issues": issues[:2]}

    def t_measure():
        handoff.save_stage(run, "stimulus", REF_STIM, "ref")
        d = p.call_stage("measure", p.check_measure, overrides={"stimulus": REF_STIM})
        st = stage_record(p, True, 0.0)
        metrics, issues, _ = p.run_tests(1, REF_STIM, d)
        sc = score_metrics(metrics, ref_metrics)
        return {**st, "score": round(sc, 2), "ok": sc == 1.0 and not issues, "issues": issues[:2]}

    for name, fn in (("spec", t_spec), ("scenario", t_scenario), ("stimulus", t_stimulus), ("measure", t_measure)):
        guard(name, fn)
    return res


def report(results, out, meta=None, mode=""):
    agents = ["spec", "scenario", "stimulus", "measure"]
    L = ["# Jetson LLM karşılaştırması", "", f"Tarih: {time.strftime('%Y-%m-%d %H:%M')} · {len(results)} model · tolerans %{int(TOL * 100)}", "",
         "Hücre: `puan (süre sn, deneme sayısı)`. Puan 1.0 = hedef davranış tam. Süre toplam LLM+deneme süresi.", "",
         f"Mod: **{mode or 'TEMEL'}**", "",
         "| Model | Param · Kuant. | " + " | ".join(agents) + " |", "|---|---|" + "---|" * len(agents)]
    for m, r in results.items():
        cells = []
        for a in agents:
            x = r.get(a, {})
            cells.append("—" if not x else f"{'✓' if x.get('ok') else '✗'} {x.get('score', 0):.2f} ({x.get('seconds', 0):.0f}s, {x.get('attempts', 0)}x)")
        pm = (meta or {}).get(m)
        L.append(f"| {m} | {pm[0] + ' · ' + pm[1] if pm else '?'} | " + " | ".join(cells) + " |")
    L += ["", "## Ajan başına öneri", ""]
    for a in agents:
        rows = [(m, r[a]) for m, r in results.items() if a in r]
        if not rows:
            continue
        rows.sort(key=lambda t: (-t[1].get("score", 0), t[1].get("attempts", 9), t[1].get("seconds", 1e9)))
        best = rows[0]
        if best[1].get("score", 0) == 0:
            L.append(f"- **{a}**: hiçbir model geçemedi.")
        else:
            alt = [m for m, x in rows[1:3] if x.get("score", 0) >= best[1]["score"] - 0.01]
            L.append(f"- **{a}**: `{best[0]}` (puan {best[1]['score']:.2f}, {best[1].get('seconds', 0):.0f} sn)" + (f"; eşdeğer: {', '.join(alt)}" if alt else ""))
    L += ["", "Not: Tek koşuya dayanır; LLM çıktısı koşudan koşuya değişir. Önemli kararlar için tekrarla."]
    (out / "report.md").write_text("\n".join(L))
    (out / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=1))


def main():
    out = ROOT / "bench" / time.strftime("%Y%m%d_%H%M%S")
    out.mkdir(parents=True)
    logf = out / "bench.log"
    say(logf, f"Bench başladı: {out}")
    if not license_reachable():
        say(logf, "HATA: lisans sunucusuna ulaşılamıyor. VPN'i bağla.")
        return 2
    base = ROOT / "bench" / "base"
    if not (base / "context.json").exists():
        src = Path(ARGS.base)
        base.mkdir(parents=True, exist_ok=True)
        for f in ("job.json", "circuit.sp", "context.json"):
            shutil.copy(src / f, base / f)
    # Referans koşu: elle yazılmış testbench + ölçümler -> beklenen değerler
    ref_run = make_run(base, out / "_referans", "referans")
    pr = Pipeline(ref_run)
    metrics, issues, _ = pr.run_tests(0, REF_STIM, REF_MEAS)
    say(logf, f"Referans ölçümleri: {metrics} sorunlar={issues}")
    if issues or len(metrics) < 4:
        say(logf, "HATA: referans testbench çalışmadı; bench durduruldu.")
        return 3
    (out / "ref_metrics.json").write_text(json.dumps(metrics, indent=1))
    meta = {n: (p, q, g) for n, p, q, g in jetson_models(0)}
    models = ARGS.models.split(",") if ARGS.models else [m[0] for m in jetson_models(ARGS.min_b)]
    mode = "İYİLEŞTİRİLMİŞ (şema+örnek+RAG+taslak)" if os.environ.get("TMAGE_IMPROVED") == "1" else "TEMEL"
    say(logf, f"Mod: {mode}. Modeller (>= {ARGS.min_b}B, küçükten büyüğe): " + ", ".join(f"{m} [{meta.get(m, ('?', '?', 0))[0]} {meta.get(m, ('?', '?', 0))[1]}]" for m in models))
    results = {}
    for m in models:
        say(logf, f"== {m}")
        t0 = time.time()
        try:
            results[m] = bench_model(m, base, out, metrics, logf)
        except Exception:
            say(logf, f"  model atlandı: {traceback.format_exc()[-300:]}")
            results[m] = {}
        say(logf, f"  süre: {int(time.time() - t0)} sn")
        report(results, out, meta, mode)
    say(logf, "Bench bitti. Rapor: " + str(out / "report.md"))
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="")
    ap.add_argument("--timeout", type=int, default=420)
    ap.add_argument("--min-b", type=float, default=3.9, help="en küçük model boyutu (milyar parametre)")
    ap.add_argument("--improved", action="store_true", help="şema+örnek+RAG+taslak modu")
    ap.add_argument("--base", default=str(sorted((ROOT / "runs").glob("*_da_test1"))[-1]) if list((ROOT / "runs").glob("*_da_test1")) else "")
    ARGS = ap.parse_args()
    if ARGS.improved:
        os.environ["TMAGE_IMPROVED"] = "1"
    sys.exit(main())
