#!/usr/bin/env python3
"""tMAGE boru hattı (v0): job -> ajanlar -> testbench -> HSPICE -> doğrulama -> rapor.

Kullanım: python3 engine/pipeline.py runs/<koşu klasörü>
Her adım logs/ altına kaydedilir (bkz. log.py).
"""
import json
import os
import re
import shutil
import sys
import time
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import socket  # noqa: E402
import handoff  # noqa: E402
import llm  # noqa: E402
import sim  # noqa: E402
from log import RunLogger  # noqa: E402

# Sağlamlık kuralları: bir ölçüm bu aralığın dışındaysa aday elenir (LLM gerekmez)
RULES = {"gain": (0, 140), "gainvv": (0, 140), "phase_margin": (0, 180), "cmrr": (0, 220), "psrr": (0, 220),
         "zpower": (1e-12, 1), "bw": (1, 1e12), "gbw": (1, 1e12), "bw_3db": (1, 1e12), "ppm": (0, 1e4), "slewrate": (0, 1e12)}
DEFAULT_URL = "http://100.113.87.120:11434"


def safe(name):
    return re.sub(r"[^\w\-]+", "_", str(name)).strip("_") or "t"


def extract_dut(text, subckt):
    """Netlistten yalnızca devreyi alır: .param, .inc ve .subckt ... .ends blokları."""
    keep, in_sub = [], False
    for ln in text.splitlines():
        low = ln.strip().lower()
        if low.startswith(".subckt"):
            in_sub = True
        if in_sub:
            keep.append(ln)
            if low.startswith(".ends"):
                in_sub = False
            continue
        if low.startswith(".param"):
            keep.append(ln)
        elif low.startswith((".inc", ".include")) and not re.search(r"130nm|nfet|pfet|pnp_", low):
            keep.append(ln)
    return "\n".join(keep)


def license_spec():
    """env.sh içindeki SNPSLMD_LICENSE_FILE='port@sunucu' değerinden 'sunucu:port' üretir."""
    lic = sim.hspice_env().get("SNPSLMD_LICENSE_FILE", "")
    m = re.match(r"(\d+)@(\S+)", lic)
    return f"{m.group(2)}:{m.group(1)}" if m else ""


def license_reachable(spec=None, timeout=4):
    spec = spec or license_spec()
    if not spec:
        return False
    host, port = spec.rsplit(":", 1)
    try:
        socket.create_connection((host, int(port)), timeout=timeout).close()
        return True
    except OSError:
        return False


class LicenseError(RuntimeError):
    pass


class Pipeline:
    def __init__(self, run_dir):
        self.run = Path(run_dir).resolve()
        self.lg = RunLogger(self.run)
        self.job = json.loads((self.run / "job.json").read_text())
        self.ctx = json.loads((self.run / "context.json").read_text())
        self.url = (self.ctx.get("llm") or {}).get("url") or DEFAULT_URL
        self.agents = (self.ctx.get("llm") or {}).get("agents") or {}
        self.circ = self.ctx["circuit"]
        self.tech = self.ctx["technology"]
        self.corner = (self.tech.get("corners") or ["TT"])[0]
        self.analyses = {a["id"]: a for a in self.ctx.get("analyses", [])}
        ver = self.ctx.get("verification") or {}
        self.n_cand = int(ver.get("n", 1))
        self.tol = float(ver.get("tolerance_pct", 5)) / 100.0

    # ---------- LLM ----------
    def model_for(self, stage):
        m = self.agents.get(stage) or next((v for v in self.agents.values() if v), "")
        if not m:
            raise RuntimeError(f"'{stage}' ajanı için model seçilmemiş.")
        return m

    def call_stage(self, stage, check, overrides=None, feedback=None, temperature=0.2, tag=""):
        msgs = handoff.build_messages(self.run, stage, overrides) + (feedback or [])
        model = self.model_for(stage)
        t_start, tok, ms_llm = time.time(), 0, 0
        self.last = {"attempts": 0, "ms_total": 0, "ms_llm": 0, "out_tokens": 0}
        for attempt in range(1, 4):
            self.lg.info(f"LLM çağrısı: {stage}{tag} model={model} deneme={attempt}", stage=stage, model=model, attempt=attempt)
            try:
                r = llm.chat(self.url, model, msgs, temperature=temperature, timeout=int(os.environ.get("TMAGE_LLM_TIMEOUT", "600")))
            except Exception as e:  # ağ/zaman aşımı
                self.lg.error(f"LLM çağrısı başarısız: {e}", stage=stage)
                time.sleep(3)
                continue
            errs, data = [], None
            try:
                data = llm.parse_json(r["text"])
                errs = handoff.validate(stage, data) + check(data)
            except ValueError as e:
                errs = [f"JSON okunamadı: {e}"]
            tok += r["output_tokens"] or 0
            ms_llm += r["ms"]
            self.last = {"attempts": attempt, "ms_total": int((time.time() - t_start) * 1000), "ms_llm": ms_llm, "out_tokens": tok}
            name = self.lg.llm_call(stage + tag, {"stage": stage, "model": model, "attempt": attempt, "ms": r["ms"], "prompt_tokens": r["prompt_tokens"],
                                                  "output_tokens": r["output_tokens"], "errors": errs, "messages": msgs, "response": r["text"]})
            self.lg.info(f"LLM yanıtı: {stage}{tag} {r['ms']} ms, {r['output_tokens']} çıktı tokeni, hata={len(errs)}  [{name}]",
                         stage=stage, ms=r["ms"], tokens=r["output_tokens"], errors=errs)
            if not errs:
                return data
            msgs = msgs + [{"role": "assistant", "content": r["text"]},
                           {"role": "user", "content": "Çıktında sorun var: " + "; ".join(errs) + ". Yalnızca düzeltilmiş tek JSON nesnesi ver."}]
        raise RuntimeError(f"'{stage}' aşaması 3 denemede geçerli çıktı üretemedi.")

    # ---------- aşamalar ----------
    def stage_spec(self):
        ports = self.circ["ports"]

        def check(d):
            pr = d.get("port_roles")
            if not isinstance(pr, dict):
                return ["port_roles bir nesne olmalı"]
            bad = [p for p in pr if p not in ports]
            return [f"bilinmeyen port: {', '.join(bad)}"] if bad else []
        data = self.call_stage("spec", check)
        handoff.save_stage(self.run, "spec", data, self.model_for("spec"))
        self.lg.info("spec tamam: " + json.dumps(data["port_roles"], ensure_ascii=False))
        return data

    def stage_scenario(self):
        ids = set(self.analyses)

        def check(d):
            t = d.get("tests")
            if not isinstance(t, list) or not t:
                return ["tests boş olamaz"]
            return [f"geçersiz analysis_id: {x.get('analysis_id')}" for x in t if x.get("analysis_id") not in ids]
        data = self.call_stage("scenario", check)
        handoff.save_stage(self.run, "scenario", data, self.model_for("scenario"))
        self.lg.info(f"scenario tamam: {len(data['tests'])} test: " + ", ".join(str(t.get("id")) for t in data["tests"]))
        return data

    def assemble(self, test_id, tb, meas):
        lib = self.tech["lib_lines"].get(self.corner, "")
        if self.tech["id"] != "saed90" or not lib:
            raise RuntimeError("v0 yalnızca SAED90 teknolojisini çalıştırır.")
        path, sec = lib.rsplit(" ", 1)
        src = (self.run / "circuit.sp").read_text()
        extra = f".lib '{path}' BJT_12\n" if self.corner.upper() != "TT" and re.search(r"\b[VL]PNP\b", src) else ""
        dut = extract_dut(src, self.circ["subckt"])
        tb = re.sub(r"(?im)^\s*\.(end|lib|inc|include|meas|measure)\b.*$", "", tb)
        return (f"* tMAGE test={test_id} köşe={self.corner}\n.lib '{path}' {sec}\n{extra}{dut}\n\n{tb}\n\n{meas}\n.end\n")

    def copy_includes(self, workdir):
        src_dir = Path(self.job.get("circuit", {}).get("path") or "").parent
        for inc in re.findall(r"(?im)^\s*\.inc(?:lude)?\s+['\"]?([^'\"\s]+)", (self.run / "circuit.sp").read_text()):
            f = src_dir / inc
            if f.exists():
                shutil.copy(f, workdir / Path(inc).name)
            elif not (workdir / inc).exists():
                self.lg.warn(f"include dosyası bulunamadı: {inc}")

    def run_tests(self, ci, stim, meas):
        if not license_reachable():
            raise LicenseError(f"Lisans sunucusuna ({license_spec() or 'SNPSLMD_LICENSE_FILE tanımsız'}) ulaşılamıyor. VPN bağlı mı? (sudo openvpn --config ~/vpn/gtu.ovpn)")
        wd = self.run / "work" / f"cand{ci}"
        wd.mkdir(parents=True, exist_ok=True)
        self.copy_includes(wd)
        by_test = {}
        for m in meas["measurements"]:
            by_test.setdefault(safe(m["test_id"]), []).append(m["statement"].replace("\\n", "\n"))
        metrics, issues, tests = {}, [], {}
        for tb in stim["testbenches"]:
            tid = safe(tb["test_id"])
            statements = by_test.get(tid)
            if not statements:
                issues.append(f"{tid}: ölçüm yok")
                continue
            text = self.assemble(tid, tb["netlist_text"], "\n".join(statements))
            (wd / f"{tid}.sp").write_text(text)
            r = sim.run_hspice(wd, f"{tid}.sp")
            self.lg.sim_output(f"cand{ci}_{tid}", r["stdout"])
            prob = sim.lis_problems(wd, tid)
            if "Unable to checkout" in r["stdout"] or "Unable to checkout" in (wd / f"{tid}.lis").read_text(errors="replace"):
                raise LicenseError("HSPICE lisansı alamadı (Unable to checkout). VPN bağlantısını kontrol et.")
            vals = sim.read_measures(wd, tid)
            self.lg.info(f"HSPICE {tid}: rc={r['rc']} {r['ms']} ms, ölçüm={len(vals)}, hata={len(prob['errors'])}  {prob['license']}",
                         test=tid, ms=r["ms"], measures=vals, errors=prob["errors"])
            for w in prob["warnings"][:3]:
                self.lg.warn(f"{tid}: {w}")
            if prob["errors"]:
                issues.append(f"{tid}: simülasyon hatası: " + " | ".join(prob["errors"][:3]))
            elif not vals:
                issues.append(f"{tid}: ölçüm üretilmedi (.meas ifadeleri sonuç vermedi)")
            metrics.update(vals)
            tests[tid] = {"measures": vals, "errors": prob["errors"]}
        return metrics, issues, tests

    def rules_check(self, metrics):
        bad = []
        for k, v in metrics.items():
            lo_hi = RULES.get(k)
            if lo_hi and not (lo_hi[0] <= v <= lo_hi[1]):
                bad.append(f"{k}={v:g} beklenen aralık {lo_hi} dışında")
        if not metrics:
            bad.append("hiç ölçüm yok")
        return bad

    def check_stimulus(self, d):
        tb = d.get("testbenches")
        if not isinstance(tb, list) or not tb:
            return ["testbenches boş olamaz"]
        errs = []
        for x in tb:
            t, n = x.get("test_id"), str(x.get("netlist_text", ""))
            if not n.strip():
                errs.append(f"{t}: netlist_text boş")
                continue
            if "{" in n or "context." in n:
                errs.append(f"{t}: yer tutucu ({{...}} veya 'context.') var; gerçek sayıları yaz")
            if not re.search(r"(?im)^\s*x\w*\s.*\b" + re.escape(self.circ["subckt"]) + r"\s*$", n):
                errs.append(f"{t}: DUT çağrısı yok (X0 ... {self.circ['subckt']})")
            if not re.search(r"(?im)^\s*v\w+\s", n):
                errs.append(f"{t}: gerilim kaynağı (V...) yok; besleme ve giriş kaynaklarını yaz")
            if not re.search(r"(?im)^\s*\.(ac|tran|dc|op|noise)\b", n):
                errs.append(f"{t}: analiz komutu (.ac/.tran/.dc/.op) yok")
        return errs

    def check_measure(self, d):
        ms = d.get("measurements")
        if not isinstance(ms, list) or not ms:
            return ["measurements boş olamaz"]
        errs = []
        for x in ms:
            st = str(x.get("statement", ""))
            if not re.match(r"\s*\.meas", st, re.I):
                errs.append(f"{x.get('test_id')}: statement '.meas' ile başlamalı")
            if "{" in st or "context." in st:
                errs.append(f"{x.get('test_id')}: yer tutucu var; gerçek sayı/düğüm adı yaz")
        return errs

    def candidate(self, ci):
        temp = 0.2 + 0.25 * ci
        fb_s = fb_m = None
        stim = meas = None
        for attempt in range(1, 4):
            chk_s, chk_m = self.check_stimulus, self.check_measure
            tag = f"_c{ci}_a{attempt}"
            if stim is None or fb_s:
                stim = self.call_stage("stimulus", chk_s, feedback=fb_s, temperature=temp, tag=tag)
            if meas is None or fb_m or fb_s:
                meas = self.call_stage("measure", chk_m, overrides={"stimulus": stim}, feedback=fb_m, temperature=temp, tag=tag)
            metrics, issues, tests = self.run_tests(ci, stim, meas)
            rule_bad = self.rules_check(metrics) if not issues else []
            if not issues and not rule_bad:
                return {"candidate": ci, "metrics": metrics, "rules_passed": True, "issues": [], "tests": tests, "attempts": attempt,
                        "stimulus": stim, "measure": meas}
            self.lg.warn(f"aday {ci} deneme {attempt} başarısız: " + "; ".join(issues + rule_bad))
            sim_err = any("simülasyon hatası" in i for i in issues)
            fb_s = ([{"role": "assistant", "content": json.dumps(stim, ensure_ascii=False)},
                     {"role": "user", "content": "Simülasyon şu hatayı verdi: " + "; ".join(issues) + ". Testbench'i düzelt."}] if sim_err else None)
            fb_m = ([{"role": "assistant", "content": json.dumps(meas, ensure_ascii=False)},
                     {"role": "user", "content": "Sorun: " + "; ".join(issues + rule_bad) + ". .meas ifadelerini düzelt."}] if not sim_err else None)
            if attempt == 3:
                return {"candidate": ci, "metrics": metrics, "rules_passed": False, "issues": issues + rule_bad, "tests": tests,
                        "attempts": attempt, "stimulus": stim, "measure": meas}

    def cluster(self, cands):
        ok = [c for c in cands if c["rules_passed"]]
        groups = []
        for c in ok:
            for g in groups:
                ref = g[0]["metrics"]
                keys = set(ref) & set(c["metrics"])
                if keys and all(abs(c["metrics"][k] - ref[k]) <= self.tol * max(abs(ref[k]), 1e-12) for k in keys):
                    g.append(c)
                    break
            else:
                groups.append([c])
        groups.sort(key=len, reverse=True)
        return groups

    def stage_verify(self, cands):
        groups = self.cluster(cands)
        flags = []
        if not groups:
            flags.append("Kurallardan geçen aday yok.")
        winner = groups[0][0]["candidate"] if groups else None
        if len(cands) == 1:
            flags.append("Tek aday: oylama yapılmadı (N=1). Güven düşük, kurallar dışında çapraz doğrulama yok.")
        elif groups and len(groups[0]) * 2 <= len(cands):
            flags.append(f"Çoğunluk yok: en büyük küme {len(groups[0])}/{len(cands)}.")
        data = {"runs": [{"candidate": c["candidate"], "metrics": c["metrics"], "rules_passed": c["rules_passed"], "issues": c["issues"]} for c in cands],
                "clusters": [[c["candidate"] for c in g] for g in groups], "winner": winner, "flags": flags}
        handoff.save_stage(self.run, "verify", data, "script")
        self.lg.info(f"verify: kazanan={winner}, kümeler={data['clusters']}, bayraklar={flags}")
        return data

    def stage_report(self, ver, cands):
        win = next((c for c in cands if c["candidate"] == ver["winner"]), None)
        L = [f"# tMAGE raporu: {self.job.get('name')}", "",
             f"- Topoloji: {self.ctx['topology'].get('label')}", f"- Teknoloji: {self.tech.get('label')} · köşe {self.corner} · {self.tech.get('simulator')}",
             f"- Devre: {self.circ.get('file')} · subckt `{self.circ.get('subckt')}`", f"- Aday sayısı: {len(cands)}, kazanan: {ver['winner']}", ""]
        if win:
            exp = {str(m.get("name", "")).lower(): m.get("expect") or {} for m in win["measure"]["measurements"]}
            L += ["## Ölçümler", "", "| Ölçüm | Değer | Beklenen |", "|---|---|---|"]
            for k, v in sorted(win["metrics"].items()):
                e = exp.get(k, {})
                L.append(f"| {k} | {v:.6g} | {e.get('min', '-')} … {e.get('max', '-')} {e.get('unit', '')} |")
            L.append("")
        if ver["flags"]:
            L += ["## Uyarılar", ""] + [f"- {f}" for f in ver["flags"]] + [""]
        bad = [c for c in cands if not c["rules_passed"]]
        if bad:
            L += ["## Elenen adaylar", ""] + [f"- aday {c['candidate']}: " + "; ".join(c["issues"]) for c in bad] + [""]
        L.append("_Bu rapor script ile üretildi; sayılar doğrudan HSPICE çıktısından alındı._")
        md = "\n".join(L)
        (self.run / "report.md").write_text(md)
        handoff.save_stage(self.run, "report", {"markdown": md}, "script")
        self.lg.info("rapor yazıldı: report.md")

    def go(self):
        t0 = time.time()
        self.lg.status("running", started=time.strftime("%Y-%m-%d %H:%M:%S"), stage="spec", pid=os.getpid())
        if not license_reachable():
            raise LicenseError(f"Koşu başlamadan önce lisans kontrolü başarısız: {license_spec()} ulaşılamıyor. VPN'i bağla ve yeniden başlat.")
        self.lg.info(f"Koşu başladı: {self.job.get('name')} · {self.ctx['topology'].get('id')} · {self.tech.get('id')} · köşe {self.corner} · N={self.n_cand}")
        try:
            self.lg.status("running", stage="spec")
            self.stage_spec()
            self.lg.status("running", stage="scenario")
            self.stage_scenario()
            cands = []
            for ci in range(self.n_cand):
                self.lg.status("running", stage=f"aday {ci + 1}/{self.n_cand}")
                c = self.candidate(ci)
                cands.append(c)
                if ci == 0:
                    handoff.save_stage(self.run, "stimulus", c["stimulus"], self.model_for("stimulus"))
                    handoff.save_stage(self.run, "measure", c["measure"], self.model_for("measure"))
                (self.run / "work" / f"cand{ci}" / "result.json").write_text(json.dumps(c, ensure_ascii=False, indent=1))
            self.lg.status("running", stage="verify")
            ver = self.stage_verify(cands)
            self.stage_report(ver, cands)
            ok = ver["winner"] is not None
            self.lg.status("done" if ok else "failed", stage="bitti", finished=time.strftime("%Y-%m-%d %H:%M:%S"), seconds=int(time.time() - t0))
            self.lg.info(f"Koşu bitti ({int(time.time() - t0)} sn): {'BAŞARILI' if ok else 'geçerli aday yok'}")
            return ok
        except Exception as e:
            self.lg.error(f"Koşu hatası: {e}\n{traceback.format_exc()}")
            self.lg.status("failed", error=str(e), finished=time.strftime("%Y-%m-%d %H:%M:%S"))
            return False


if __name__ == "__main__":
    sys.exit(0 if Pipeline(sys.argv[1]).go() else 1)
