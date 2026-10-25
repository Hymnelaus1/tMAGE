"""Ajanlar arası veri aktarımı.

Her koşu (runs/<id>/) şu yapıyı taşır:
  job.json        kullanıcının seçimleri (değişmez)
  context.json    LLM'lere verilen standart özet (değişmez, job.json'dan üretilir)
  stages/NN_ad.json   her aşamanın çıktısı (sırayla yazılır)
  trace.jsonl     kim, ne zaman, hangi modelle yazdı
Bir ajan yalnızca context.json ile kendi "needs" listesindeki önceki aşamaların çıktısını görür.
"""
import json
import re
import time
from pathlib import Path

CONFIG = Path(__file__).resolve().parent.parent / "config"
STAGES = json.loads((CONFIG / "stages.json").read_text())
ORDER = STAGES["order"]

PORT_HINTS = [(r"^(vinp|inp|ip|in\+|vin\+|in)$", "giris_pozitif"), (r"^(vinn|inn|in_n|in-|vin-)$", "giris_negatif"),
              (r"^(vout|out|output|ou|vo)$", "cikis"), (r"^(vref)$", "referans"),
              (r"^(vdd|avdd|vcc|vd)$", "besleme_pozitif"), (r"^(vss|gnd|avss|vs)$", "besleme_negatif")]


def port_hints(ports):
    out = {}
    for p in ports:
        for rx, role in PORT_HINTS:
            if re.match(rx, p, re.I):
                out[p] = role
                break
        else:
            out[p] = "bilinmiyor"
    return out


def lib_line(tech: dict, corner: str):
    if tech.get("id") == "saed90":
        return f"{tech['pdk'].rstrip('/')}/{tech['lib_file']} {tech['lib_section'].format(corner=corner.upper())}"
    if tech.get("inc"):
        return tech["inc"]
    return ""


def build_context(job: dict, catalog: dict) -> dict:
    tech = next((t for t in catalog["technologies"] if t["id"] == job["technology"]["id"]), {})
    topo = next((t for t in catalog["topologies"] if t["id"] == job.get("topology")), {})
    jt = job["technology"]
    corners = jt.get("corners") or ["TT"]
    circ = job.get("circuit") or {}
    parsed = circ.get("parsed") or {}
    sub = (parsed.get("subckts") or [{}])[0]
    ports = sub.get("ports", [])
    return {
        "job_id": job.get("name"), "created": job.get("created"),
        "technology": {"id": tech.get("id"), "label": tech.get("label"), "simulator": jt.get("simulator"), "vdd": jt.get("vdd"),
                       "supply_mode": tech.get("supply", {}).get("mode"), "vss": tech.get("supply", {}).get("vss"),
                       "pdk": jt.get("pdk"), "corners": corners, "temps": jt.get("temps"),
                       "lib_lines": {c: lib_line({**tech, "pdk": jt.get("pdk") or tech.get("pdk", "")}, c) for c in corners},
                       "devices": tech.get("devices", {}), "notes": tech.get("notes", [])},
        "circuit": {"file": circ.get("name"), "netlist_file": "circuit.sp", "subckt": sub.get("name"), "ports": ports,
                    "port_hints": port_hints(ports), "params": [p["name"] for p in parsed.get("params", [])],
                    "adapted": bool(job.get("adaptation"))},
        "topology": {"id": topo.get("id"), "label": topo.get("label"), "desc": topo.get("desc")},
        "analyses": job.get("analyses", []),
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
    return ["eksik alan: " + k for k in missing]


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
            raise RuntimeError(f"'{stage}' için önce '{need}' aşaması bitmeli.")
        prev[need] = d
    system = (f"Sen tMAGE'in '{spec['label']}' ajanısın. Analog devre testbench üretim hattında çalışıyorsun.\n"
              f"Görev: {spec['goal']}\nKurallar: Yalnızca verilen context'teki bilgiyi kullan, bilmediğini uydurma, "
              "belirsizse open_questions/assumptions alanına yaz. Çıktın tek bir JSON nesnesi olsun, başka metin yazma.\n"
              "Beklenen JSON alanları:\n" + json.dumps(spec["output"], ensure_ascii=False, indent=1))
    user = {"context": ctx, "previous_stages": prev}
    if stage in ("stimulus", "spec"):
        user["circuit_netlist"] = (run_dir / "circuit.sp").read_text() if (run_dir / "circuit.sp").exists() else ""
    return [{"role": "system", "content": system}, {"role": "user", "content": json.dumps(user, ensure_ascii=False)}]
