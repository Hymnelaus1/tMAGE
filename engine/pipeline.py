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
import rag  # noqa: E402
import sim  # noqa: E402
from log import RunLogger  # noqa: E402

# Sağlamlık kuralları: bir ölçüm bu aralığın dışındaysa aday elenir (LLM gerekmez)
RULES = {"gain": (0, 140), "gainvv": (0, 140), "phase_margin": (0, 180), "cmrr": (0, 220), "psrr": (0, 220),
         "zpower": (1e-12, 1), "bw": (1, 1e12), "gbw": (1, 1e12), "bw_3db": (1, 1e12), "ppm": (0, 1e4), "slewrate": (0, 1e12),
         "cl_gain": (-60, 60), "cl_gain_err": (0, 30), "cl_bw": (1, 1e12), "vos": (-0.3, 0.3), "vos_max": (-0.3, 0.3),
         "vos_min": (-0.3, 0.3), "vos_drift": (0, 1e5), "tsettle": (0, 1e-3)}
DEFAULT_URL = "http://100.113.87.120:11434"


def _fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


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


class PrecheckError(RuntimeError):
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
        self.voters = [v for v in ((self.ctx.get("llm") or {}).get("voters") or []) if v]
        self.cand_model = None
        self.filled = {}
        self.tol = float(ver.get("tolerance_pct", 5)) / 100.0

    # ---------- LLM ----------
    def model_for(self, stage):
        if stage in ("stimulus", "measure") and getattr(self, "cand_model", None):
            return self.cand_model  # oylamada her aday kendi modeliyle üretilir
        m = self.agents.get(stage) or next((v for v in self.agents.values() if v), "")
        if not m:
            raise RuntimeError(f"No model selected for the '{stage}' agent.")
        return m

    def call_stage(self, stage, check, overrides=None, feedback=None, temperature=0.2, tag=""):
        msgs = handoff.build_messages(self.run, stage, overrides) + (feedback or [])
        model = self.model_for(stage)
        t_start, tok, ms_llm = time.time(), 0, 0
        self.last = {"attempts": 0, "ms_total": 0, "ms_llm": 0, "out_tokens": 0}
        for attempt in range(1, 4):
            self.lg.info(f"LLM call: {stage}{tag} model={model} attempt={attempt}", stage=stage, model=model, attempt=attempt)
            try:
                kw = {}
                if handoff.improved():
                    # Şema zorlaması yalnızca ilk denemede; bazı modellerde (HTTP 500 / yarıda kesilen dize) sorun çıkarıyor
                    kw = {"schema": handoff.schema_for(stage, self.ctx) if attempt == 1 else None, "num_predict": handoff.MAX_TOKENS.get(stage)}
                # 2. denemeden itibaren biçim kısıtı yok: bazı modeller (örn. mistral) kısıt altında satır sonlu dizeyi yarıda kesiyor
                free = handoff.improved() and attempt >= 2
                r = llm.chat(self.url, model, msgs, temperature=temperature, timeout=int(os.environ.get("TMAGE_LLM_TIMEOUT", "600")),
                             json_mode=not free, **kw)
            except Exception as e:  # ağ/zaman aşımı
                self.lg.error(f"LLM call failed: {e}", stage=stage)
                time.sleep(3)
                continue
            errs, data = [], None
            try:
                if r.get("done_reason") == "length":
                    raise ValueError("output was cut off at the token limit; answer with shorter, compact single-line JSON")
                data = self.post(stage, llm.parse_json(r["text"]))
                errs = handoff.validate(stage, data) + check(data)
            except ValueError as e:
                errs = [f"JSON could not be parsed: {e}"]
            tok += r["output_tokens"] or 0
            ms_llm += r["ms"]
            self.last = {"attempts": attempt, "ms_total": int((time.time() - t_start) * 1000), "ms_llm": ms_llm, "out_tokens": tok}
            name = self.lg.llm_call(stage + tag, {"stage": stage, "model": model, "attempt": attempt, "ms": r["ms"], "prompt_tokens": r["prompt_tokens"],
                                                  "output_tokens": r["output_tokens"], "errors": errs, "messages": msgs, "response": r["text"]})
            self.lg.info(f"LLM reply: {stage}{tag} {r['ms']} ms, {r['output_tokens']} output tokens, errors={len(errs)}  [{name}]",
                         stage=stage, ms=r["ms"], tokens=r["output_tokens"], errors=errs)
            if not errs:
                return data
            msgs = msgs + [{"role": "assistant", "content": r["text"]},
                           {"role": "user", "content": "Your output has problems: " + "; ".join(errs) + ". Reply with ONE corrected compact JSON object only."}]
        raise RuntimeError(f"Stage '{stage}' did not produce valid output in 3 attempts.")

    # ---------- aşamalar ----------
    def stage_spec(self):
        ports = self.circ["ports"]
        hints = self.circ.get("port_hints", {})
        if handoff.improved() and ports and all(hints.get(p, "unknown") != "unknown" for p in ports):
            data = {"port_roles": {p: hints[p] for p in ports},
                    "circuit_summary": f"{self.ctx['topology'].get('label')} ({self.circ.get('subckt')}), {len(ports)} ports.",
                    "assumptions": ["Port roles were derived from port names by a script (no LLM call needed)."], "open_questions": []}
            handoff.save_stage(self.run, "spec", data, "script")
            self.lg.info("spec (script): " + json.dumps(data["port_roles"], ensure_ascii=False))
            return data

        def check(d):
            pr = d.get("port_roles")
            if not isinstance(pr, dict):
                return ["port_roles must be an object"]
            bad = [p for p in pr if p not in ports]
            return [f"unknown port: {', '.join(bad)}"] if bad else []
        data = self.call_stage("spec", check)
        handoff.save_stage(self.run, "spec", data, self.model_for("spec"))
        self.lg.info("spec done: " + json.dumps(data["port_roles"], ensure_ascii=False))
        return data

    def stage_scenario(self):
        ids = set(self.analyses)
        if handoff.improved() and self.analyses:
            data = {"tests": [{"id": a["id"], "analysis_id": a["id"], "purpose": a.get("label", a["id"]), "connections": {}, "sweep": a.get("params", {}),
                               "metrics": a.get("metrics", [])} for a in self.analyses.values()], "order": list(self.analyses)}
            handoff.save_stage(self.run, "scenario", data, "script")
            self.lg.info(f"scenario (script): {len(data['tests'])} tests: " + ", ".join(self.analyses))
            return data

        def check(d):
            t = d.get("tests")
            if not isinstance(t, list) or not t:
                return ["tests must not be empty"]
            return [f"invalid analysis_id: {x.get('analysis_id')}" for x in t if x.get("analysis_id") not in ids]
        data = self.call_stage("scenario", check)
        handoff.save_stage(self.run, "scenario", data, self.model_for("scenario"))
        self.lg.info(f"scenario done: {len(data['tests'])} tests: " + ", ".join(str(t.get("id")) for t in data["tests"]))
        return data

    def assemble(self, test_id, tb, meas):
        lib = self.tech["lib_lines"].get(self.corner, "")
        if self.tech["id"] != "saed90" or not lib:
            raise RuntimeError("v0 runs SAED90 only.")
        path, sec = lib.rsplit(" ", 1)
        src = (self.run / "circuit.sp").read_text()
        extra = f".lib '{path}' BJT_12\n" if self.corner.upper() != "TT" and re.search(r"\b[VL]PNP\b", src) else ""
        dut = extract_dut(src, self.circ["subckt"])
        tb = re.sub(r"(?im)^\s*\.(end|lib|inc|include|meas|measure)\b.*$", "", tb)
        return (f"* tMAGE test={test_id} corner={self.corner}\n.lib '{path}' {sec}\n{extra}{dut}\n\n{tb}\n\n{meas}\n.end\n")

    def copy_includes(self, workdir):
        src_dir = Path(self.job.get("circuit", {}).get("path") or "").parent
        for inc in re.findall(r"(?im)^\s*\.inc(?:lude)?\s+['\"]?([^'\"\s]+)", (self.run / "circuit.sp").read_text()):
            f = src_dir / inc
            if f.exists():
                shutil.copy(f, workdir / Path(inc).name)
            elif not (workdir / inc).exists():
                self.lg.warn(f"include file not found: {inc}")

    def drafts(self):
        if not hasattr(self, "_dr"):
            self._dr = rag.drafts(self.ctx, handoff.load_stage(self.run, "spec"), handoff.load_stage(self.run, "scenario"))
        return self._dr

    def post(self, stage, d):
        """Model çıktısını onarır: çift kaçışlı \\n, eksik test_id, eksik testlerin script taslağıyla tamamlanması (loga işaretlenir)."""
        if not isinstance(d, dict) or not handoff.improved():
            return d
        if stage == "stimulus" and isinstance(d.get("testbenches"), list):
            tbs = [x for x in d["testbenches"] if isinstance(x, dict)]
            for x in tbs:
                if not x.get("test_id") and x.get("file"):
                    x["test_id"] = Path(str(x["file"])).stem
                n = x.get("netlist_text")
                if isinstance(n, str) and "\n" not in n and "\\n" in n:
                    x["netlist_text"] = n.replace("\\n", "\n")
            have = {x.get("test_id") for x in tbs}
            for t in self.drafts()["draft_testbenches"]:
                if t["test_id"] not in have:
                    tbs.append(dict(t))
                    self.filled.setdefault("stimulus", []).append(t["test_id"])
                    self.lg.warn(f"stimulus: testbench '{t['test_id']}' was missing from the model output; completed from the script draft")
            d["testbenches"] = tbs
        if stage == "measure" and isinstance(d.get("measurements"), list):
            ms = [x for x in d["measurements"] if isinstance(x, dict)]
            have = {x.get("test_id") for x in ms}
            for t in (getattr(self, "cur_stim", None) or {}).get("testbenches", []):
                tid = t.get("test_id")
                if tid not in have:
                    drs = [m for m in self.drafts()["draft_measurements"] if m["test_id"] == tid]
                    for m in drs:
                        ms.append({**m, "expect": {"min": -1e12, "max": 1e12, "unit": ""}})
                    if drs:
                        self.filled.setdefault("measure", []).append(tid)
                        self.lg.warn(f"measure: model wrote no measurements for '{tid}'; completed from the script draft")
            d["measurements"] = ms
        return d

    def fallback(self, wd, tid):
        """Model çıktısı çalışmadıysa scriptin doğrulanmış taslağını dener. Başarılıysa (değerler, lis sorunları) döner."""
        tb = next((x for x in self.drafts()["draft_testbenches"] if safe(x["test_id"]) == tid), None)
        ms = [m["statement"] for m in self.drafts()["draft_measurements"] if safe(m["test_id"]) == tid]
        if not tb or not ms:
            return None
        name = tid + "_taslak"
        (wd / f"{name}.sp").write_text(self.assemble(tid, tb["netlist_text"], "\n".join(ms)))
        r = sim.run_hspice(wd, f"{name}.sp")
        self.lg.sim_output(f"{wd.name}_{name}", r["stdout"])
        prob, vals = sim.lis_problems(wd, name), sim.read_measures(wd, name)
        return (vals, prob) if vals and not prob["errors"] else None

    def precheck(self):
        """Script taslağıyla devrenin çalışıp çalışmadığına bakar (LLM yok). Bozuk devre için LLM denemeleri boşa gider."""
        sc = handoff.load_stage(self.run, "scenario") or {}
        t = next((x for x in sc.get("tests", []) if x.get("analysis_id") == "ac_loop"), None)
        if not t:
            return
        tid = safe(t["id"])
        tb = next((x for x in self.drafts()["draft_testbenches"] if safe(x["test_id"]) == tid), None)
        ms = [m["statement"] for m in self.drafts()["draft_measurements"] if safe(m["test_id"]) == tid]
        if not tb or not ms:
            return
        wd = self.run / "work" / "precheck"
        wd.mkdir(parents=True, exist_ok=True)
        self.copy_includes(wd)
        (wd / "precheck.sp").write_text(self.assemble(tid, tb["netlist_text"], "\n".join(ms)))
        r = sim.run_hspice(wd, "precheck.sp")
        self.lg.sim_output("precheck", r["stdout"])
        prob, vals = sim.lis_problems(wd, "precheck"), sim.read_measures(wd, "precheck")
        gain = vals.get("gain")
        self.lg.info(f"DUT precheck (script draft, no LLM): gain={gain} dB, errors={len(prob['errors'])}  supply_hint={bool(self.circ.get('supply_hint'))}")
        if prob["errors"] or gain is None or gain <= 0:
            raise PrecheckError(f"DUT sanity precheck failed: the script's reference testbench gives open-loop gain {gain} dB "
                                f"(HSPICE errors: {prob['errors'][:1]}). The circuit itself is probably not biased correctly in this technology/supply, "
                                "so LLM retries would not help. Check bias sources, supplies and transistor sizes.")

    def run_tests(self, ci, stim, meas):
        if not license_reachable():
            raise LicenseError(f"License server ({license_spec() or 'SNPSLMD_LICENSE_FILE undefined'}) unreachable. Is the VPN up? (sudo openvpn --config ~/vpn/gtu.ovpn)")
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
                issues.append(f"{tid}: no measurement statements")
                continue
            text = self.assemble(tid, tb["netlist_text"], "\n".join(statements))
            (wd / f"{tid}.sp").write_text(text)
            r = sim.run_hspice(wd, f"{tid}.sp")
            self.lg.sim_output(f"cand{ci}_{tid}", r["stdout"])
            prob = sim.lis_problems(wd, tid)
            if "Unable to checkout" in r["stdout"] or "Unable to checkout" in (wd / f"{tid}.lis").read_text(errors="replace"):
                raise LicenseError("HSPICE could not get a license (Unable to checkout). Check the VPN connection.")
            vals = sim.read_measures(wd, tid)
            self.lg.info(f"HSPICE {tid}: rc={r['rc']} {r['ms']} ms, measures={len(vals)}, errors={len(prob['errors'])}  {prob['license']}",
                         test=tid, ms=r["ms"], measures=vals, errors=prob["errors"])
            used_fallback = False
            if (prob["errors"] or not vals) and handoff.improved():
                fb = self.fallback(wd, tid)
                if fb:
                    self.lg.warn(f"{tid}: model output failed ({(prob['errors'] or ['no measures'])[0][:90]}); script draft used")
                    vals, prob, used_fallback = fb[0], fb[1], True
            for w in prob["warnings"][:3]:
                self.lg.warn(f"{tid}: {w}")
            if prob["errors"]:
                issues.append(f"{tid}: simulation error: " + " | ".join(prob["errors"][:3]))
            elif not vals:
                issues.append(f"{tid}: no measurement produced (.meas statements gave no result)")
            metrics.update(vals)
            tests[tid] = {"measures": vals, "errors": prob["errors"], "fallback": used_fallback}
        if "gain" in metrics and "gaincm" in metrics:  # CMRR iki testten türetilir
            metrics["cmrr"] = metrics["gain"] - metrics["gaincm"]
        return metrics, issues, tests

    def rules_check(self, metrics):
        bad = []
        for k, v in metrics.items():
            lo_hi = RULES.get(k)
            if lo_hi and not (lo_hi[0] <= v <= lo_hi[1]):
                bad.append(f"{k}={v:g} is outside the plausible range {lo_hi}")
        if not metrics:
            bad.append("no measurements at all")
        return bad

    def check_stimulus(self, d):
        tb = d.get("testbenches")
        if not isinstance(tb, list) or not tb:
            return ["testbenches must not be empty"]
        errs = []
        for x in tb:
            t, n = x.get("test_id"), str(x.get("netlist_text", ""))
            if not n.strip():
                errs.append(f"{t}: netlist_text is empty")
                continue
            if "{" in n or "context." in n:
                errs.append(f"{t}: placeholder ({{...}} or 'context.') found; write literal numbers")
            if not re.search(r"(?im)^\s*x\w*\s.*\b" + re.escape(self.circ["subckt"]) + r"\s*$", n):
                errs.append(f"{t}: missing CUT instance (X0 ... {self.circ['subckt']})")
            if not re.search(r"(?im)^\s*v\w+\s", n):
                errs.append(f"{t}: no voltage source (V...); write supply and input sources")
            if not re.search(r"(?im)^\s*\.(ac|tran|dc|op|noise)\b", n):
                errs.append(f"{t}: no analysis card (.ac/.tran/.dc/.op)")
            if re.search(r"(?im)^\s*\.ac\b", n) and not re.search(r"(?im)^\s*v\w+\s.*\bac\b", n):
                errs.append(f"{t}: .ac analysis but no source has 'AC <magnitude>'")
            if "psrr" in str(t).lower():
                vp = next((p for p, r in self.circ.get("port_hints", {}).items() if r == "supply_pos"), None)
                if vp and not re.search(r"(?im)^\s*v\w+\s+" + re.escape(vp) + r"\s+\S+\s.*\bac\b", n):
                    errs.append(f"{t}: for PSRR the supply source needs 'AC 1' (e.g. Vdd {vp} 0 1.2 AC 1)")
        return errs

    def check_measure(self, d):
        ms = d.get("measurements")
        if not isinstance(ms, list) or not ms:
            return ["measurements must not be empty"]
        errs = []
        for x in ms:
            st = str(x.get("statement", ""))
            if not re.match(r"\s*\.meas", st, re.I):
                errs.append(f"{x.get('test_id')}: statement must start with '.meas'")
            if "{" in st or "context." in st:
                errs.append(f"{x.get('test_id')}: placeholder found; write literal numbers/node names")
        return errs

    def candidate(self, ci):
        self.filled = {}
        temp = 0.2 + 0.25 * ci
        fb_s = fb_m = None
        stim = meas = None
        for attempt in range(1, 4):
            chk_s, chk_m = self.check_stimulus, self.check_measure
            tag = f"_c{ci}_a{attempt}"
            if stim is None or fb_s:
                stim = self.call_stage("stimulus", chk_s, feedback=fb_s, temperature=temp, tag=tag)
                self.cur_stim = stim
            if meas is None or fb_m or fb_s:
                meas = self.call_stage("measure", chk_m, overrides={"stimulus": stim}, feedback=fb_m, temperature=temp, tag=tag)
            metrics, issues, tests = self.run_tests(ci, stim, meas)
            rule_bad = self.rules_check(metrics) if not issues else []
            if not issues and not rule_bad:
                return {"candidate": ci, "metrics": metrics, "rules_passed": True, "issues": [], "tests": tests, "attempts": attempt, "filled": dict(self.filled),
                        "stimulus": stim, "measure": meas}
            self.lg.warn(f"candidate {ci} attempt {attempt} failed: " + "; ".join(issues + rule_bad))
            sim_err = any("simulation error" in i for i in issues)
            fb_s = ([{"role": "assistant", "content": json.dumps(stim, ensure_ascii=False)},
                     {"role": "user", "content": "HSPICE reported: " + "; ".join(issues) + ". Fix the testbench."}] if sim_err else None)
            fb_m = ([{"role": "assistant", "content": json.dumps(meas, ensure_ascii=False)},
                     {"role": "user", "content": "Problem: " + "; ".join(issues + rule_bad) + ". Fix the .meas statements."}] if not sim_err else None)
            if rule_bad and not sim_err:  # ölçüm mantıksız: kaynak testbench'te de olabilir (örn. eksik AC kaynağı)
                fb_s = [{"role": "assistant", "content": json.dumps(stim, ensure_ascii=False)},
                        {"role": "user", "content": "The measured result is not plausible: " + "; ".join(rule_bad) + ". The testbench may have a source/connection error (missing AC source? for PSRR the AC source belongs on the supply). Fix the testbench."}]
            if attempt == 3:
                return {"candidate": ci, "metrics": metrics, "rules_passed": False, "issues": issues + rule_bad, "tests": tests, "filled": dict(self.filled),
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

    def spec_checks(self, m):
        """Kullanıcının girdiği spesifikasyon sınırlarına göre kontrol (0 = sınır yok). Testbench hatası değil, tasarım değerlendirmesi."""
        out = []
        P = lambda aid, k: _fnum((self.analyses.get(aid) or {}).get("params", {}).get(k))
        lim = P("offset", "vos_max")
        if lim and "vos" in m:
            out.append({"name": "Input offset", "ok": abs(m["vos"]) <= lim * 1e-3, "detail": f"|vos| = {abs(m['vos']) * 1e3:.3g} mV (limit {lim:g} mV)"})
        lim = P("cl_gain", "tol_db")
        if lim and "cl_gain_err" in m:
            out.append({"name": "Closed-loop gain error", "ok": m["cl_gain_err"] <= lim, "detail": f"{m['cl_gain_err']:.3g} dB (limit {lim:g} dB)"})
        lim = P("tran_slew", "slew_min")
        if lim and "slewrate" in m:
            out.append({"name": "Slew rate", "ok": m["slewrate"] >= lim * 1e6, "detail": f"{m['slewrate'] / 1e6:.3g} V/µs (min {lim:g})"})
        lim = P("tran_slew", "ts_max")
        if lim and "tsettle" in m:
            out.append({"name": "Settling time", "ok": m["tsettle"] <= lim * 1e-6, "detail": f"{m['tsettle'] * 1e6:.3g} µs (max {lim:g})"})
        lim = P("vos_temp", "drift_max")
        if lim and "vos_drift" in m:
            out.append({"name": "Offset temperature drift", "ok": m["vos_drift"] <= lim, "detail": f"{m['vos_drift']:.3g} µV/°C (max {lim:g})"})
        return out

    def stage_verify(self, cands):
        groups = self.cluster(cands)
        flags = []
        if not groups:
            flags.append("No candidate passed the sanity rules.")
        winner = groups[0][0]["candidate"] if groups else None
        if len(cands) == 1:
            flags.append("Single candidate: no voting (N=1). Low confidence, no cross-check beyond the sanity rules.")
        elif groups and len(groups[0]) * 2 <= len(cands):
            flags.append(f"No majority: largest cluster {len(groups[0])}/{len(cands)}.")
        data = {"runs": [{"candidate": c["candidate"], "metrics": c["metrics"], "rules_passed": c["rules_passed"], "issues": c["issues"]} for c in cands],
                "clusters": [[c["candidate"] for c in g] for g in groups], "winner": winner, "flags": flags,
                "spec": self.spec_checks(next((c["metrics"] for c in cands if c["candidate"] == winner), {}))}
        handoff.save_stage(self.run, "verify", data, "script")
        self.lg.info(f"verify: winner={winner}, clusters={data['clusters']}, flags={flags}")
        return data

    def stage_report(self, ver, cands):
        win = next((c for c in cands if c["candidate"] == ver["winner"]), None)
        L = [f"# tMAGE report: {self.job.get('name')}", "",
             f"- Topology: {self.ctx['topology'].get('label')}", f"- Technology: {self.tech.get('label')} · corner {self.corner} · {self.tech.get('simulator')}",
             f"- Circuit: {self.circ.get('file')} · subckt `{self.circ.get('subckt')}`", f"- Candidates: {len(cands)}, winner: {ver['winner']}", ""]
        if win:
            L += ["## Measurements", "", "| Measurement | Value | Sanity range |", "|---|---|---|"]
            for k, v in sorted(win["metrics"].items()):
                rng = RULES.get(k)
                chk = "-" if not rng else (f"{rng[0]:g} … {rng[1]:g} " + ("✓" if rng[0] <= v <= rng[1] else "✗"))
                L.append(f"| {k} | {v:.6g} | {chk} |")
            L.append("")
        if ver["flags"]:
            L += ["## Warnings", ""] + [f"- {f}" for f in ver["flags"]] + [""]
        if ver.get("spec"):
            L += ["## Specification check", ""] + [f"- {'✓' if x['ok'] else '✗'} {x['name']}: {x['detail']}" for x in ver["spec"]] + [""]
        if win:
            n_tb = len(win["stimulus"]["testbenches"])
            fs, fm = win.get("filled", {}).get("stimulus", []), win.get("filled", {}).get("measure", [])
            L += ["## Model contribution", "", f"- Testbenches: {n_tb - len(fs)}/{n_tb} written by the model" + (f"; completed from the script draft: {', '.join(fs)}" if fs else ""),
                  f"- Measurements: the model wrote measurements for {n_tb - len(fm)}/{n_tb} tests" + (f"; completed from the script draft: {', '.join(fm)}" if fm else ""), ""]
            fbt = [t for t, x in win["tests"].items() if x.get("fallback")]
            if fbt:
                L += ["## Tests that used the script draft", "", "The model output did not run in HSPICE, so the verified script draft was used for: " + ", ".join(fbt), ""]
        bad = [c for c in cands if not c["rules_passed"]]
        if bad:
            L += ["## Dropped candidates", ""] + [f"- candidate {c['candidate']}: " + "; ".join(c["issues"]) for c in bad] + [""]
        L.append("_This report was generated by a script; the numbers are taken directly from the HSPICE output._")
        md = "\n".join(L)
        (self.run / "report.md").write_text(md)
        handoff.save_stage(self.run, "report", {"markdown": md}, "script")
        self.lg.info("report written: report.md")

    def go(self):
        t0 = time.time()
        self.lg.status("running", started=time.strftime("%Y-%m-%d %H:%M:%S"), stage="spec", pid=os.getpid())
        if not license_reachable():
            raise LicenseError(f"Pre-run license check failed: {license_spec()} unreachable. Bring the VPN up and restart.")
        self.lg.info(f"Run started: {self.job.get('name')} · {self.ctx['topology'].get('id')} · {self.tech.get('id')} · corner {self.corner} · N={self.n_cand}")
        try:
            self.lg.status("running", stage="spec")
            self.stage_spec()
            self.lg.status("running", stage="scenario")
            self.stage_scenario()
            if handoff.improved():
                self.precheck()
            cands = []
            for ci in range(self.n_cand):
                self.cand_model = self.voters[ci % len(self.voters)] if self.voters else None
                self.lg.status("running", stage=f"candidate {ci + 1}/{self.n_cand}")
                self.lg.info(f"Candidate {ci + 1}/{self.n_cand}: model={self.cand_model or 'agent default'}")
                try:
                    c = self.candidate(ci)
                except LicenseError:
                    raise
                except Exception as e:  # tek adayın çökmesi oylamayı iptal etmez; aday elenmiş sayılır
                    self.lg.error(f"Candidate {ci + 1} could not be produced and was dropped: {e}")
                    c = {"candidate": ci, "metrics": {}, "rules_passed": False, "issues": [f"candidate failed: {e}"], "tests": {}, "attempts": 3,
                         "filled": dict(self.filled), "stimulus": {"testbenches": []}, "measure": {"measurements": []}}
                cands.append(c)
                if ci == 0 and c["stimulus"].get("testbenches"):
                    handoff.save_stage(self.run, "stimulus", c["stimulus"], self.model_for("stimulus"))
                    handoff.save_stage(self.run, "measure", c["measure"], self.model_for("measure"))
                c["model"] = self.cand_model
                (self.run / "work" / f"cand{ci}").mkdir(parents=True, exist_ok=True)
                (self.run / "work" / f"cand{ci}" / "result.json").write_text(json.dumps(c, ensure_ascii=False, indent=1))
                self.cand_model = None
            self.lg.status("running", stage="verify")
            ver = self.stage_verify(cands)
            self.stage_report(ver, cands)
            ok = ver["winner"] is not None
            self.lg.status("done" if ok else "failed", stage="finished", finished=time.strftime("%Y-%m-%d %H:%M:%S"), seconds=int(time.time() - t0))
            self.lg.info(f"Run finished ({int(time.time() - t0)} s): {'SUCCESS' if ok else 'no valid candidate'}")
            return ok
        except PrecheckError as e:
            self.lg.error(str(e))
            (self.run / "report.md").write_text(f"# tMAGE report: {self.job.get('name')}\n\n## Run stopped by the DUT precheck\n\n{e}\n")
            self.lg.status("failed", error=str(e)[:300], finished=time.strftime("%Y-%m-%d %H:%M:%S"))
            return False
        except Exception as e:
            self.lg.error(f"Run error: {e}\n{traceback.format_exc()}")
            self.lg.status("failed", error=str(e), finished=time.strftime("%Y-%m-%d %H:%M:%S"))
            return False


if __name__ == "__main__":
    sys.exit(0 if Pipeline(sys.argv[1]).go() else 1)
