"""Bilgi tabanı (RAG) ve script taslakları.

1) retrieve(): kitteki gerçek testbench'lerden ve .meas ifadelerinden, topoloji/analiz/metriğe göre en ilgili örnekleri seçer
   (anahtar sözcük + metaveri puanlaması; gömme modeli gerektirmez, Jetson'a ek yük bindirmez).
2) drafts(): standart testler için scriptin yazdığı taslak testbench ve .meas satırları. LLM bunları temel alıp düzeltir.
"""
import re
from pathlib import Path

KB = Path(__file__).resolve().parent.parent / "knowledge"
TOPO_BY_FILE = {"amp_llm.sp": "DA", "fcascode_llm.sp": "FCO", "tso2_llm.sp": "TSO", "bgr_llm.sp": "BGR", "bandgap_banba.sp": "BGR",
                "comparator.sp": "COMP", "cmos_osc.sp": "OSC", "lna.sp": "LNA"}
# Metrik adı -> kitte geçebilen ad(lar)
ALIAS = {"gain": ["gain", "gainvv"], "bw": ["bw", "bw_3db"], "bw_3db": ["bw", "bw_3db"], "gbw": ["bw"], "phase_margin": ["phase_margin"],
         "cmrr": ["cmrr", "gaincm"], "psrr": ["psrr", "gainpsrr"], "slewrate": ["slewrate", "tdlay2", "perc"], "zpower": ["zpower", "rpower"],
         "ppm": ["ppm"], "tot_noise": ["tot_noise", "noise"], "noise": ["noise", "tot_noise"], "tdlay": ["tdlay"], "offset": ["offset"],
         "s11": ["s11"], "s21": ["s21"], "s12": ["s12"], "nf": ["nf"], "phasenoise": ["phasenoise"]}

NOTE = ("These examples come from an older technology (130 nm, dual supply). Take the structure and the .meas syntax; change model names, "
        "supply values and node names to match this circuit's context.")


def _files():
    return sorted((KB / "examples").glob("*.sp")) if (KB / "examples").exists() else []


def _split(text):
    """Netlisti (devre dışı kalan testbench kısmı, .meas satırları) olarak ayırır."""
    tb, meas, in_sub = [], [], False
    for ln in text.splitlines():
        low = ln.strip().lower()
        if low.startswith(".subckt"):
            in_sub = True
            continue
        if in_sub:
            if low.startswith(".ends"):
                in_sub = False
            continue
        if low.startswith((".meas", ".measure")):
            meas.append(ln.strip())
        elif low and not low.startswith(("*", ".inc", ".include", ".option", ".end")):
            tb.append(ln.rstrip())
    return "\n".join(tb), meas


def _meas_name(stmt):
    m = re.match(r"\.meas(?:ure)?\s+(?:ac|tran|dc|noise)?\s*(\w+)", stmt, re.I)
    return m.group(1).lower() if m else ""


def retrieve(topology, metrics, k_tb=1, k_meas=2, max_tb_chars=1500):
    tb_ex, meas_ex = [], {}
    for f in _files():
        topo = TOPO_BY_FILE.get(f.name, "")
        tb, meas = _split(f.read_text(errors="replace"))
        if topo == topology and tb and len(tb_ex) < k_tb:
            tb_ex.append({"source": f.name, "topology": topo, "testbench": tb[:max_tb_chars]})
        for mt in metrics:
            names = ALIAS.get(mt.lower(), [mt.lower()])
            for st in meas:
                if _meas_name(st) in names:
                    lst = meas_ex.setdefault(mt, [])
                    if st not in lst and len(lst) < k_meas:
                        lst.append(st if topo == topology else st)
    return {"not": NOTE, "testbench_examples": tb_ex, "meas_examples": meas_ex}


# ---------- script taslakları (SAED90 tek besleme, doğrulanmış sözdizimi) ----------
def _role(roles, name):
    return next((p for p, r in roles.items() if r == name), None)


def _f(x, d):
    try:
        return float(x)
    except (TypeError, ValueError):
        return d


def draft_testbench(analysis_id, ctx, roles, params):
    c, t = ctx["circuit"], ctx["technology"]
    inp, inn, out = _role(roles, "input_pos"), _role(roles, "input_neg"), _role(roles, "output")
    vp, vn = _role(roles, "supply_pos"), _role(roles, "supply_neg")
    if not (inp and inn and out and vp and vn):
        return None
    vdd = _f(t.get("vdd"), 1.2)
    hint = c.get("supply_hint")  # devre içinde toprağa bağlı bias varsa simetrik besleme
    vhi, vlo, vmid = (hint["vpos"], hint["vneg"], hint["vcm"]) if hint else (vdd, 0.0, vdd / 2)
    nets = {p: p for p in c["ports"]}
    cl = params.get("cl", "0.5")
    vcm = vmid if hint else _f(params.get("vcm"), vdd / 2)
    sup = f"Vdd {vp} 0 {vhi:g}\nVss {vn} 0 {vlo:g}\n"
    fs, fe, pts = params.get("fstart", "1"), params.get("fstop", "1e9"), params.get("pts", "20")
    extra = ""
    if analysis_id == "ac_loop":
        body = sup + f"Vcm cm 0 {vmid:g}\nVin {inp} cm DC 0 AC 0.5\nVinn {inn} cm DC 0 AC -0.5\n"
        an = f".ac dec {pts} {fs} {fe}"
    elif analysis_id == "cmrr":
        body = sup + f"Vcm cm 0 {vmid:g}\nVin {inp} cm DC 0 AC 0.5\nVinn {inn} cm DC 0 AC 0.5\n"
        an = f".ac dec {pts} {fs} {fe}"
    elif analysis_id == "psrr":
        nets[inn] = out  # birim kazançlı tampon
        body = f"Vdd {vp} 0 {vhi:g} AC 1\nVss {vn} 0 {vlo:g}\nVin {inp} 0 DC {vmid:g}\n"
        an = f".ac dec {pts} {fs} {fe}"
    elif analysis_id == "power_area":
        body = sup + f"Vcm cm 0 {vmid:g}\nVin {inp} cm DC 0\nVinn {inn} cm DC 0\n"
        an = ".tran 10n 1u"
    elif analysis_id == "cl_gain":
        g = _f(params.get("gain_ideal"), 1.0)
        body = sup + f"Vin {inp} 0 DC {vcm} AC 1\n"
        if g <= 1.0001:
            nets[inn] = out
        else:  # eviren olmayan: Rf/Rg bölücüsü, kazanç = 1 + Rf/Rg
            nets[inn] = "fb"
            extra = f"Rf {out} fb {(g - 1) * 10}k\nRg fb 0 10k\n"
        an = f".ac dec {pts} {fs} {fe}"
    elif analysis_id == "offset":
        nets[inn] = out
        body = sup + f"Vin {inp} 0 DC {vcm}\n"
        an = f".dc Vin {vcm - 0.05:g} {vcm + 0.05:g} 0.05"
    elif analysis_id == "tran_slew":
        step, tstop = _f(params.get("step"), 0.2), _f(params.get("tstop"), 6)
        v0, v1 = vcm - step / 2, vcm + step / 2
        nets[inn] = out
        body = sup + f"Vin {inp} 0 PULSE({v0:g} {v1:g} 1u 1n 1n {tstop:g}u {2 * tstop:g}u)\n"
        an = f".tran 1n {tstop:g}u"
    elif analysis_id == "vos_temp":
        nets[inn] = out
        body = sup + f"Vin {inp} 0 DC {vcm}\n"
        an = f".dc temp {params.get('tmin', '-40')} {params.get('tmax', '125')} {params.get('tstep', '5')}"
    else:
        return None
    inst = "X0 " + " ".join(nets[p] for p in c["ports"]) + " " + c["subckt"]
    return f"{body}{extra}{inst}\nCl {out} 0 {cl}p\n{an}"


def draft_measures(analysis_id, out, params=None, vdd=1.2, inp="vinp", sym=False):
    params = params or {}
    v = f"par('db(v({out}))')"
    vcm = 0.0 if sym else _f(params.get("vcm"), vdd / 2)
    step, tstop = _f(params.get("step"), 0.2), _f(params.get("tstop"), 6)
    tol = _f(params.get("tol_pct"), 1) / 100.0
    v0 = vcm - step / 2
    g = _f(params.get("gain_ideal"), 1.0)
    import math
    ideal_db = 20 * math.log10(g) if g > 0 else 0.0
    tmin, tmax = _f(params.get("tmin"), -40), _f(params.get("tmax"), 125)
    return {"ac_loop": [("gain", f".meas ac gain find {v} at=1000"), ("bw", f".meas ac bw when {v}=0"),
                        ("phase_margin", f".meas ac phase_margin find par('180+vp({out})') at=bw")],
            "cmrr": [("gaincm", f".meas ac gaincm find {v} at=1000")],
            "psrr": [("gainpsrr", f".meas ac gainpsrr find {v} at=1000"), ("psrr", ".meas ac psrr param='-1*(gainpsrr)'")],
            "power_area": [("zpower", ".meas tran zpower avg power")],
            "cl_gain": [("cl_gain", f".meas ac cl_gain find {v} at=1000"),
                        ("cl_gain_err", f".meas ac cl_gain_err param='abs(cl_gain-({ideal_db:.4f}))'"),
                        ("cl_bw", f".meas ac cl_bw when {v}='cl_gain-3'")],
            "offset": [("vos", f".meas dc vos find par('v({out})-v({inp})') at={vcm:g}")],
            "tran_slew": [("vfin", f".meas tran vfin find v({out}) at={tstop:g}u"),
                          ("t20", f".meas tran t20 when v({out})={v0 + 0.2 * step:g} rise=1"),
                          ("t80", f".meas tran t80 when v({out})={v0 + 0.8 * step:g} rise=1"),
                          ("slewrate", f".meas tran slewrate param='{0.6 * step:g}/(t80-t20)'"),
                          ("tsettle_abs", f".meas tran tsettle_abs when v({out})='vfin-{tol * step:g}' rise=last"),
                          ("tsettle", ".meas tran tsettle param='tsettle_abs-1u'")],
            "vos_temp": [("vos_max", f".meas dc vos_max max par('v({out})-v({inp})')"),
                         ("vos_min", f".meas dc vos_min min par('v({out})-v({inp})')"),
                         ("vos_drift", f".meas dc vos_drift param='(vos_max-vos_min)/({tmax:g}-({tmin:g}))*1e6'")]}.get(analysis_id)


def drafts(ctx, spec, scenario):
    """Senaryodaki her test için taslak testbench + taslak .meas."""
    roles = (spec or {}).get("port_roles", {})
    an = {a["id"]: a for a in ctx.get("analyses", [])}
    out_p = _role(roles, "output") or "vout"
    tbs, ms = [], []
    for t in (scenario or {}).get("tests", []):
        aid = t.get("analysis_id")
        text = draft_testbench(aid, ctx, roles, (an.get(aid) or {}).get("params", {}))
        if text:
            tbs.append({"test_id": t.get("id"), "file": f"{t.get('id')}.sp", "netlist_text": text})
        inp_p = _role(roles, "input_pos") or "vinp"
        for name, st in draft_measures(aid, out_p, (an.get(aid) or {}).get("params", {}), _f(ctx["technology"].get("vdd"), 1.2), inp_p, bool(ctx["circuit"].get("supply_hint"))) or []:
            ms.append({"test_id": t.get("id"), "name": name, "statement": st})
    return {"draft_testbenches": tbs, "draft_measurements": ms}
