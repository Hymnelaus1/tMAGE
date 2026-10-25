#!/usr/bin/env python3
"""tMAGE arayüz sunucusu: yalnızca standart kütüphane, kurulum gerektirmez."""
import ipaddress
import json
import os
import re
import shutil
import socket
import time
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine"))
import handoff  # noqa: E402
from log import glog  # noqa: E402
import subprocess  # noqa: E402
STATIC = Path(__file__).resolve().parent / "static"
CONFIG = ROOT / "config"
RUNS = ROOT / "runs"
STATE = CONFIG / "ui_state.json"
HOST = os.environ.get("TMAGE_HOST", "127.0.0.1")
PORT = int(os.environ.get("TMAGE_PORT", "8765"))

# Dosya tarayıcısının görebileceği kökler
FS_ROOTS = [Path.home(), Path("/run/media"), Path("/data"), Path("/opt/synopsys")]
TEXT_EXT = {".sp", ".cir", ".spice", ".scs", ".net", ".txt", ".inc", ".lib", ".md", ".json", ".py"}
MAX_FILE = 2 * 1024 * 1024


def read_env_file():
    env = {}
    f = CONFIG / "jetson.env"
    if f.exists():
        for line in f.read_text().splitlines():
            m = re.match(r'\s*export\s+(\w+)=(.*)', line)
            if m:
                env[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return env


def allowed(path: Path) -> bool:
    p = path.resolve()
    return any(p == r or r in p.parents for r in FS_ROOTS)


def host_is_private(url: str) -> bool:
    """Model listesi proxy'si yalnızca yerel/özel ağ/Tailscale adreslerine gider."""
    u = urllib.parse.urlparse(url)
    if u.scheme not in ("http", "https") or not u.hostname:
        return False
    try:
        for info in socket.getaddrinfo(u.hostname, None):
            ip = ipaddress.ip_address(info[4][0])
            if not (ip.is_private or ip.is_loopback or ip in ipaddress.ip_network("100.64.0.0/10")):
                return False
        return True
    except OSError:
        return False


def parse_netlist(text: str):
    """.subckt, .param, .inc ve mevcut analiz satırlarını çıkarır (+ devam satırları birleşik)."""
    lines = []
    for raw in text.splitlines():
        if raw.startswith("+") and lines:
            lines[-1] += " " + raw[1:].strip()
        else:
            lines.append(raw.rstrip())
    subckts, params, incs, analyses = [], [], [], []
    for ln in lines:
        s = ln.strip()
        low = s.lower()
        m = re.match(r"\.subckt\s+(\S+)\s*(.*)", s, re.I)
        if m:
            ports = [t for t in m.group(2).split() if "=" not in t]
            subckts.append({"name": m.group(1), "ports": ports})
        elif low.startswith(".param"):
            for k, v in re.findall(r"([A-Za-z_]\w*)\s*=\s*(\S+)", s):
                params.append({"name": k, "value": v})
        elif low.startswith((".inc", ".include", ".lib")):
            incs.append(s)
        elif re.match(r"\.(ac|dc|tran|noise|op|temp|tf|pz)\b", low):
            analyses.append(s.split()[0].lower())
    return {"subckts": subckts, "params": params, "includes": incs,
            "analyses": sorted(set(analyses)), "lines": len(lines)}


def guess_topology(text: str, name: str = ""):
    """Önce dosya adı ve subckt adlarına, bulunamazsa netlist metnine bakar."""
    rules = [("BGR", ["bandgap", "bgr", "vref"]), ("FCO", ["foldedcascode", "fcascode", "fco", "folded"]),
             ("TSO", ["twostage", "two-stage", "miller", "tso"]), ("DA", ["diffamp", "diff_amp", "diff amp", "amp", "da"])]
    subs = " ".join(s["name"] for s in parse_netlist(text)["subckts"])
    for hay in ((name + " " + subs).lower(), text[:4000].lower()):
        tokens = set(re.split(r"[^a-z0-9]+", hay))
        for topo, keys in rules:
            if any(k in hay if len(k) > 3 else k in tokens for k in keys):
                return topo
    return None


def load_catalog():
    return json.loads((CONFIG / "catalog.json").read_text())


def detect_tech(text: str):
    low = text.lower()
    if "sky130_fd_pr__" in low:
        return "sky130"
    if re.search(r"\b(nfet|pfet)\b", low) or "130nm" in low:
        return "gtu130"
    if re.search(r"\b(n12|p12|n12_lvt|p12_lvt|n12_hvt|p12_hvt)\b", low) or "saed90" in low:
        return "saed90"
    return None


def adapt_netlist(text: str, dst_id: str, pdk: str = "", corner: str = "TT"):
    """Netlisti kaynak teknolojiden hedef teknolojiye çevirir. Yaptığı ve yapamadığı şeyleri raporlar."""
    techs = {t["id"]: t for t in load_catalog()["technologies"]}
    src_id, dst = detect_tech(text), techs[dst_id]
    if src_id is None:
        return {"ok": False, "error": "Kaynak teknoloji anlaşılamadı (model adı bulunamadı)."}
    if src_id == dst_id:
        return {"ok": True, "text": text, "source": src_id, "report": ["Netlist zaten bu teknolojide."], "changed": 0}
    src, report, changed, xfix = techs[src_id], [], 0, 0
    pairs = []
    sd, dd = src.get("devices", {}), dst.get("devices", {})
    for role in ("nmos", "pmos", "pnp"):
        if role in sd and role in dd:
            pairs.append((sd[role], dd[role]))
    out = []
    for ln in text.splitlines():
        s_ = ln.strip().lower()
        if s_.startswith(("*", ".model")):
            out.append(ln)
            continue
        new, hit = ln, 0
        for a, b in pairs:
            new, n = re.subn(r"(?<![\w.])" + re.escape(a) + r"(?![\w])", b, new, flags=re.I)
            changed += n
            hit += n
        if hit and src_id == "sky130":
            # SKY130 modelleri alt devredir (XM...); SAED90 HSPICE modelleri doğrudan MOSFET'tir (M...)
            fixed = re.sub(r"^(\s*)X(M\w*)", r"\1\2", new, flags=re.I)
            xfix += fixed != new
            new = fixed
        out.append(new)
    res = "\n".join(out)
    # Eski model include satırlarını tek bir .lib ile değiştir
    inc_re = re.compile(r"^\s*\.(inc|include)\s+[\"']?([^\"'\s]*(nfet|pfet|pnp|130nm)[^\"'\s]*)[\"']?.*$", re.I | re.M)
    removed = inc_re.findall(res)
    res = inc_re.sub("", res)
    if dst_id == "saed90":
        lib = (pdk or dst["pdk"]).rstrip("/") + "/" + dst["lib_file"]
        sec = dst["lib_section"].format(corner=corner.upper())
        header = f"* tMAGE: {src_id} -> saed90 uyarlaması\n.lib '{lib}' {sec}\n"
        if corner.upper() != "TT" and re.search(r"(?im)^\s*q\w*\s", res):
            header += f".lib '{lib}' BJT_12\n"
            report.append("Köşe TT değil ve BJT var: BJT_12 ayrıca eklendi (yalnızca TT_12 içinde hazır gelir).")
        res = header + res
        report.append(f"Model kütüphanesi: .lib '{lib}' {sec}")
    else:
        res = f"* tMAGE: {src_id} -> {dst_id} uyarlaması (model dosyasını elle ekle)\n" + res
        report.append("Hedef teknolojinin model dosyası otomatik eklenmedi.")
    report.insert(0, f"{changed} model adı değişti: " + ", ".join(f"{a} → {b}" for a, b in pairs))
    if removed:
        report.append(f"{len(removed)} eski .inc satırı kaldırıldı.")
    if xfix:
        report.append(f"{xfix} transistör satırı XM... → M... olarak düzeltildi (SKY130 alt devre, SAED90 doğrudan model).")
    ssup, dsup = src.get("supply", {}), dst.get("supply", {})
    if ssup.get("mode") != dsup.get("mode") or ssup.get("vss") != dsup.get("vss"):
        report.append(f"UYARI: besleme düzeni farklı ({ssup.get('mode')} VSS={ssup.get('vss')} → {dsup.get('mode')} VSS={dsup.get('vss')}). "
                      "pVSS/pVDD .param ve kaynak satırlarını gözden geçir.")
    if re.search(r"(?i)\.param\s+lcm\w*\s*=", res):
        report.append(f"UYARI: .param Lcmd/Lcm değeri {src.get('lmin')} civarı; hedef Lmin {dst.get('lmin')}. Boyutlar yeniden ayarlanmalı.")
    report.append("UYARI: W/L ve .param boyut dosyaları (param_*.cir) eski teknolojiye göre; testbench ölçümleri çalışır, değerler yeniden boyutlandırılmalı.")
    return {"ok": True, "text": res, "source": src_id, "report": report, "changed": changed}


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):  # sessiz
        pass

    def _json(self, obj, code=200):
        data = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _body(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n > 8 * 1024 * 1024:
            raise ValueError("istek çok büyük")
        return json.loads(self.rfile.read(n) or b"{}")

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        try:
            if u.path in ("/", "/index.html"):
                data = (STATIC / "index.html").read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            elif u.path == "/api/config":
                cat = load_catalog()
                env = read_env_file()
                base = env.get("OLLAMA_URL", "http://100.113.87.120:11434/v1")
                cat["env"] = {"ollama_url": re.sub(r"/v1/?$", "", base), "ollama_model": env.get("OLLAMA_MODEL", ""),
                              "ollama_models": env.get("OLLAMA_MODELS", "").split()}
                cat["roots"] = [str(r) for r in FS_ROOTS if r.exists()]
                cat["usb_tb"] = next((str(p) for p in Path("/run/media").glob("*/*/*/tb")), "")
                cat["home"] = str(Path.home())
                self._json(cat)
            elif u.path == "/api/state":
                self._json(json.loads(STATE.read_text()) if STATE.exists() else {})
            elif u.path == "/api/fs":
                p = Path(q.get("path", [str(Path.home())])[0]).expanduser()
                if not allowed(p) or not p.is_dir():
                    return self._json({"error": "Klasör erişilemez"}, 403)
                items = []
                for e in sorted(p.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
                    if e.name.startswith("."):
                        continue
                    try:
                        isdir = e.is_dir()
                        items.append({"name": e.name, "dir": isdir, "size": 0 if isdir else e.stat().st_size})
                    except OSError:
                        pass
                self._json({"path": str(p.resolve()), "parent": str(p.resolve().parent), "items": items[:800]})
            elif u.path == "/api/file":
                p = Path(q.get("path", [""])[0]).expanduser()
                if not allowed(p) or not p.is_file() or p.suffix.lower() not in TEXT_EXT:
                    return self._json({"error": "Dosya okunamaz"}, 403)
                if p.stat().st_size > MAX_FILE:
                    return self._json({"error": "Dosya 2 MB'tan büyük"}, 413)
                text = p.read_text(errors="replace")
                self._json({"path": str(p.resolve()), "name": p.name, "text": text, "tech": detect_tech(text),
                            "parsed": parse_netlist(text), "guess": guess_topology(text, p.name)})
            elif u.path == "/api/models":
                url = q.get("url", [""])[0].rstrip("/")
                url = re.sub(r"/v1$", "", url)
                if not host_is_private(url):
                    return self._json({"ok": False, "error": "Yalnızca yerel/özel ağ/Tailscale adresleri"}, 400)
                t0 = time.time()
                try:
                    with urllib.request.urlopen(url + "/api/tags", timeout=5) as r:
                        d = json.load(r)
                    models = [{"name": m["name"], "size_gb": round(m.get("size", 0) / 1e9, 1),
                               "params": m.get("details", {}).get("parameter_size", "")} for m in d.get("models", [])]
                    self._json({"ok": True, "ms": int((time.time() - t0) * 1000), "models": models})
                except Exception as e:
                    self._json({"ok": False, "error": f"Bağlanılamadı: {e}"})
            elif u.path == "/api/run/log":
                d = RUNS / Path(q.get("dir", [""])[0]).name
                logf = d / "logs" / "run.log"
                lines = logf.read_text(errors="replace").splitlines() if logf.exists() else []
                since = int(q.get("since", ["0"])[0])
                sf = d / "logs" / "status.json"
                self._json({"lines": lines[since:], "total": len(lines), "status": json.loads(sf.read_text()) if sf.exists() else {"state": "hazir"},
                            "stages": handoff.status(d) if (d / "context.json").exists() else [],
                            "report": (d / "report.md").read_text() if (d / "report.md").exists() else ""})
            elif u.path == "/api/run":
                d = RUNS / Path(q.get("dir", [""])[0]).name
                if not (d / "context.json").exists():
                    return self._json({"error": "koşu bulunamadı"}, 404)
                self._json({"dir": d.name, "context": json.loads((d / "context.json").read_text()), "stages": handoff.status(d)})
            elif u.path == "/api/jobs":
                jobs = []
                for d in sorted(RUNS.glob("*/job.json"), reverse=True)[:30]:
                    try:
                        j = json.loads(d.read_text())
                        jobs.append({"dir": d.parent.name, "name": j.get("name"), "topology": j.get("topology"),
                                     "created": j.get("created"), "analyses": len(j.get("analyses", []))})
                    except Exception:
                        pass
                self._json({"jobs": jobs})
            else:
                self._json({"error": "bulunamadı"}, 404)
        except Exception as e:
            self._json({"error": str(e)}, 500)

    def do_POST(self):
        u = urllib.parse.urlparse(self.path)
        try:
            body = self._body()
            if u.path == "/api/run/start":
                d = RUNS / Path(body.get("dir", "")).name
                if not (d / "context.json").exists():
                    return self._json({"ok": False, "error": "koşu bulunamadı"}, 404)
                sf = d / "logs" / "status.json"
                if sf.exists():
                    st = json.loads(sf.read_text())
                    alive = False
                    if st.get("state") == "running" and st.get("pid"):
                        try:
                            os.kill(int(st["pid"]), 0)
                            alive = True
                        except OSError:
                            pass
                    if alive:
                        return self._json({"ok": False, "error": "zaten çalışıyor"})
                for old in ("logs", "stages", "work", "report.md"):  # temiz başlangıç
                    t = d / old
                    if t.is_dir():
                        shutil.rmtree(t)
                    elif t.exists():
                        t.unlink()
                handoff.init_run(d, json.loads((d / "job.json").read_text()), load_catalog())
                subprocess.Popen([sys.executable, str(ROOT / "engine" / "pipeline.py"), str(d)], start_new_session=True,
                                 stdout=subprocess.DEVNULL, stderr=open(d / "pipeline.err", "w"))
                glog(f"koşu başlatıldı: {d.name}")
                self._json({"ok": True})
            elif u.path == "/api/parse":
                text = body.get("text", "")
                self._json({"parsed": parse_netlist(text), "tech": detect_tech(text),
                            "guess": guess_topology(text, body.get("name", ""))})
            elif u.path == "/api/adapt":
                r = adapt_netlist(body.get("text", ""), body.get("tech", "saed90"), body.get("pdk", ""), body.get("corner", "TT"))
                r["parsed"] = parse_netlist(r["text"]) if r.get("ok") else None
                self._json(r)
            elif u.path == "/api/state":
                STATE.write_text(json.dumps(body, ensure_ascii=False, indent=1))
                self._json({"ok": True})
            elif u.path == "/api/jobs":
                name = re.sub(r"[^\w\-]+", "_", body.get("name") or "devre").strip("_") or "devre"
                stamp = time.strftime("%Y%m%d_%H%M%S")
                d = RUNS / f"{stamp}_{name}"
                d.mkdir(parents=True, exist_ok=True)
                body["created"] = time.strftime("%Y-%m-%d %H:%M:%S")
                body["status"] = "hazir"
                (d / "job.json").write_text(json.dumps(body, ensure_ascii=False, indent=2))
                # Devre netliste kopyalanır, böylece iş tek başına yeniden üretilebilir
                if body.get("netlist_text"):
                    (d / "circuit.sp").write_text(body["netlist_text"])
                handoff.init_run(d, body, load_catalog())
                glog(f"iş kaydedildi: {d.name} ({body.get('topology')}, {len(body.get('analyses', []))} analiz)")
                self._json({"ok": True, "dir": str(d), "stages": handoff.status(d)})
            else:
                self._json({"error": "bulunamadı"}, 404)
        except Exception as e:
            self._json({"error": str(e)}, 500)


if __name__ == "__main__":
    RUNS.mkdir(exist_ok=True)
    srv = ThreadingHTTPServer((HOST, PORT), H)
    print(f"tMAGE arayüzü: http://{HOST}:{PORT}  (durdurmak için Ctrl+C)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
