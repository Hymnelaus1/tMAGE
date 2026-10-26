"""Ajanlar arası veri aktarımı.

Her koşu (runs/<id>/) şu yapıyı taşır:
  job.json        kullanıcının seçimleri (değişmez)
  context.json    LLM'lere verilen standart özet (değişmez, job.json'dan üretilir)
  stages/NN_ad.json   her aşamanın çıktısı (sırayla yazılır)
  trace.jsonl     kim, ne zaman, hangi modelle yazdı
Bir ajan yalnızca context.json ile kendi "needs" listesindeki önceki aşamaların çıktısını görür.
"""
import json
import os
import re
import time
from pathlib import Path

CONFIG = Path(__file__).resolve().parent.parent / "config"
STAGES = json.loads((CONFIG / "stages.json").read_text())
ORDER = STAGES["order"]

PORT_HINTS = [(r"^(vinp|inp|ip|in\+|vin\+|in)$", "input_pos"), (r"^(vinn|inn|in_n|in-|vin-)$", "input_neg"),
              (r"^(vout|out|output|ou|vo)$", "output"), (r"^(vref)$", "reference"),
              (r"^(vdd|avdd|vcc|vd)$", "supply_pos"), (r"^(vss|gnd|avss|vs)$", "supply_neg")]


def port_hints(ports):
    out = {}
    for p in ports:
        for rx, role in PORT_HINTS:
            if re.match(rx, p, re.I):
                out[p] = role
                break
        else:
            out[p] = "unknown"
    return out


def lib_line(tech: dict, corner: str):
    if tech.get("id") == "saed90":
        return f"{tech['pdk'].rstrip('/')}/{tech['lib_file']} {tech['lib_section'].format(corner=corner.upper())}"
    if tech.get("inc"):
        return tech["inc"]
    return ""


def ground_referenced_sources(text, subckt):
    """Alt devre içinde toprağa (GND/0) bağlı gerilim kaynağı var mı? (iç bias toprağa göre ayarlıdır)"""
    found, inside = [], False
    for ln in (text or "").splitlines():
        low = ln.strip().lower()
        if low.startswith(".subckt"):
            inside = subckt is None or low.split()[1] == str(subckt).lower()
            continue
        if low.startswith(".ends"):
            inside = False
        if inside and re.match(r"v\w*\s+\S+\s+\S+", low):
            nodes = low.split()[1:3]
            if any(n in ("gnd", "0") for n in nodes):
                found.append(ln.strip()[:50])
    return found


def build_context(job: dict, catalog: dict) -> dict:
    tech = next((t for t in catalog["technologies"] if t["id"] == job["technology"]["id"]), {})
    topo = next((t for t in catalog["topologies"] if t["id"] == job.get("topology")), {})
    an_cat = {a["id"]: a for a in catalog.get("analyses", [])}
    tech_en = {"saed90": "SAED 90 nm", "sky130": "SKY130", "gtu130": "130 nm (reference kit)"}
    jt = job["technology"]
    corners = jt.get("corners") or ["TT"]
    circ = job.get("circuit") or {}
    parsed = circ.get("parsed") or {}
    sub = (parsed.get("subckts") or [{}])[0]
    ports = sub.get("ports", [])
    vdd_f = float(jt.get("vdd") or 1.2)
    gref = ground_referenced_sources(job.get("netlist_text", ""), sub.get("name"))
    supply_hint = ({"mode": "symmetric", "vpos": round(vdd_f / 2, 4), "vneg": -round(vdd_f / 2, 4), "vcm": 0.0,
                    "reason": "The subcircuit contains voltage sources referenced to ground (" + "; ".join(gref[:2]) + "): its internal bias is centred on ground, "
                              "so use symmetric supplies (positive supply = +vpos, negative supply = vneg) and an input common mode of vcm instead of VSS=0."}
                   if gref else None)
    return {
        "job_id": job.get("name"), "created": job.get("created"),
        "technology": {"id": tech.get("id"), "label": tech_en.get(tech.get("id"), tech.get("label")), "simulator": jt.get("simulator"), "vdd": jt.get("vdd"),
                       "supply_mode": tech.get("supply", {}).get("mode"), "vss": tech.get("supply", {}).get("vss"),
                       "pdk": jt.get("pdk"), "corners": corners, "temps": jt.get("temps"),
                       "lib_lines": {c: lib_line({**tech, "pdk": jt.get("pdk") or tech.get("pdk", "")}, c) for c in corners},
                       "devices": tech.get("devices", {}), "notes": tech.get("notes_en") or tech.get("notes", [])},
        "circuit": {"file": circ.get("name"), "netlist_file": "circuit.sp", "subckt": sub.get("name"), "ports": ports,
                    "port_hints": port_hints(ports), "params": [p["name"] for p in parsed.get("params", [])],
                    "adapted": bool(job.get("adaptation")), "supply_hint": supply_hint},
        "topology": {"id": topo.get("id"), "label": topo.get("label_en") or topo.get("label"), "desc": topo.get("desc_en") or topo.get("desc")},
        "analyses": [{**a, "label": (an_cat.get(a["id"]) or {}).get("label_en", a.get("label")), "description": (an_cat.get(a["id"]) or {}).get("desc_en", "")}
                     for a in job.get("analyses", [])],
        "verification": job.get("verification", {"method": "voting", "n": 3, "tolerance_pct": 5}),
        "llm": job.get("llm", {}),
    }


def init_run(run_dir: Path, job: dict, catalog: dict):
    (run_dir / "stages").mkdir(exist_ok=True)
    (run_dir / "context.json").write_text(json.dumps(build_context(job, catalog), ensure_ascii=False, indent=2))


def stage_file(run_dir: Path, stage: str) -> Path:
    return run_dir / "stages" / f"{ORDER.index(stage) + 1:02d}_{stage}.json"


def status(run_dir: Path):
    return [{"stage": s, "label": STAGES["stages"][s]["label"], "done": stage_file(run_dir, s).exists()} for s in ORDER]


def load_stage(run_dir: Path, stage: str):
    f = stage_file(run_dir, stage)
    return json.loads(f.read_text())["data"] if f.exists() else None


def validate(stage: str, data: dict):
    missing = [k for k in STAGES["stages"][stage]["output"] if k not in data]
    return ["missing field: " + k for k in missing]


def save_stage(run_dir: Path, stage: str, data: dict, model: str = ""):
    errs = validate(stage, data)
    if errs:
        raise ValueError(f"{stage}: " + ", ".join(errs))
    stage_file(run_dir, stage).write_text(json.dumps({"stage": stage, "model": model, "at": time.strftime("%Y-%m-%d %H:%M:%S"), "data": data},
                                                     ensure_ascii=False, indent=2))
    with open(run_dir / "trace.jsonl", "a") as f:
        f.write(json.dumps({"stage": stage, "model": model, "at": time.strftime("%H:%M:%S")}, ensure_ascii=False) + "\n")


def build_messages(run_dir: Path, stage: str, overrides=None):
    """OpenAI uyumlu mesaj listesi: ajanın rolü + context + önceki aşamaların çıktıları + beklenen çıktı biçimi."""
    spec = STAGES["stages"][stage]
    ctx = json.loads((run_dir / "context.json").read_text())
    prev = {}
    for need in spec["needs"]:
        d = (overrides or {}).get(need) or load_stage(run_dir, need)
        if d is None:
            raise RuntimeError(f"Stage '{need}' must finish before '{stage}'.")
        prev[need] = d
    system = (f"Sen tMAGE'in '{spec['label']}' ajanısın. Analog devre testbench üretim hattında çalışıyorsun.\n"
              f"Görev: {spec['goal']}\nKurallar: Yalnızca verilen context'teki bilgiyi kullan, bilmediğini uydurma, "
              "belirsizse open_questions/assumptions alanına yaz. Çıktın tek bir JSON nesnesi olsun, başka metin yazma.\n"
              "Beklenen JSON alanları:\n" + json.dumps(spec["output"], ensure_ascii=False, indent=1))
    user = {"context": ctx, "previous_stages": prev}
    if improved():
        sys_add, user_add = extras(stage, ctx, prev)
        system = (system_prompt(stage) or system) + sys_add
        user.update(user_add)
    if stage in ("stimulus", "spec"):
        user["circuit_netlist"] = (run_dir / "circuit.sp").read_text() if (run_dir / "circuit.sp").exists() else ""
    return [{"role": "system", "content": system}, {"role": "user", "content": json.dumps(user, ensure_ascii=False)}]


# ---------------- İyileştirilmiş mod (TMAGE_IMPROVED=1): şema + örnek + RAG + taslak ----------------
ROLES = ["input_pos", "input_neg", "output", "supply_pos", "supply_neg", "reference", "other", "unknown"]
MAX_TOKENS = {"spec": 500, "scenario": 800, "stimulus": 2000, "measure": 1500}


def system_prompt(stage):
    """İyileştirilmiş modda ajanın sistem istemi: ortak kurallar + rol + kurallar + bilinen hatalar ve çözümleri (İngilizce)."""
    f = Path(__file__).resolve().parent.parent / "config" / "agent_prompts.json"
    P = json.loads(f.read_text())
    st = P["stages"].get(stage)
    if not st:
        return None
    L = [P["common"], "", f"ROLE: {st['role']}", f"GOAL: {st['goal']}", "", "RULES:"] + [f"- {r}" for r in st["rules"]]
    L += ["", "KNOWN ERRORS AND FIXES (observed in earlier runs; do not repeat them):"] + [f"- ERROR: {x['error']} FIX: {x['fix']}" for x in st["pitfalls"]]
    L += ["", "OUTPUT: return exactly one JSON object with these fields (descriptions in Turkish are only hints about the value format):",
          json.dumps(STAGES["stages"][stage]["output"], ensure_ascii=False)]
    return "\n".join(L)


def improved():
    return os.environ.get("TMAGE_IMPROVED") == "1"


def schema_for(stage, ctx):
    """Ollama 'format' için JSON şeması (model bu şemaya uymak zorunda)."""
    S, A = {"type": "string"}, lambda i: {"type": "array", "items": i}
    if stage == "spec":
        return {"type": "object", "properties": {"port_roles": {"type": "object", "additionalProperties": {"type": "string", "enum": ROLES}},
                                                 "circuit_summary": S, "assumptions": A(S), "open_questions": A(S)},
                "required": ["port_roles", "circuit_summary", "assumptions", "open_questions"]}
    if stage == "scenario":
        ids = [a["id"] for a in ctx.get("analyses", [])]
        t = {"type": "object", "properties": {"id": S, "analysis_id": {"type": "string", "enum": ids}, "purpose": S,
                                              "connections": {"type": "object"}, "sweep": {"type": "object"}, "metrics": A(S)},
             "required": ["id", "analysis_id", "purpose", "metrics"]}
        return {"type": "object", "properties": {"tests": A(t), "order": A(S)}, "required": ["tests", "order"]}
    if stage == "stimulus":
        t = {"type": "object", "properties": {"test_id": S, "file": S, "netlist_text": S}, "required": ["test_id", "file", "netlist_text"]}
        return {"type": "object", "properties": {"testbenches": A(t)}, "required": ["testbenches"]}
    if stage == "measure":
        e = {"type": "object", "properties": {"min": {"type": "number"}, "max": {"type": "number"}, "unit": S}, "required": ["min", "max", "unit"]}
        m = {"type": "object", "properties": {"test_id": S, "name": S, "statement": S, "expect": e}, "required": ["test_id", "name", "statement", "expect"]}
        return {"type": "object", "properties": {"measurements": A(m)}, "required": ["measurements"]}
    return None


def _example(stage):
    f = Path(__file__).resolve().parent.parent / "knowledge" / "ref_da.json"
    return json.loads(f.read_text()).get(stage) if f.exists() else None


def extras(stage, ctx, prev):
    """build_messages'a eklenen iyileştirmeler: (sistem metni eki, kullanıcı alanları)."""
    sys_add, user_add = "", {}
    ex = _example(stage)
    if ex:
        sys_add += ("\n\nFORMAT EXAMPLE (a different diff-amp circuit; copy only the structure, never the values or names):\n" + json.dumps(ex, ensure_ascii=False))
    if stage in ("stimulus", "measure"):
        import rag
        metrics = sorted({m for a in ctx.get("analyses", []) for m in a.get("metrics", [])})
        user_add["reference_examples"] = rag.retrieve(ctx["topology"]["id"], metrics)
        d = rag.drafts(ctx, prev.get("spec"), prev.get("scenario"))
        key = "draft_testbenches" if stage == "stimulus" else "draft_measurements"
        if d[key]:
            user_add[key] = d[key]
            sys_add += (f"\n\n'{key}' contains drafts prepared by a script, with syntax verified in HSPICE. Use them as the basis and change them only "
                        "if they do not fit this circuit or analysis. Add missing tests yourself.")
    return sys_add, user_add
