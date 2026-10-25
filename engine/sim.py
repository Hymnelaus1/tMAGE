"""HSPICE koşusu ve çıktı okuma."""
import os
import re
import subprocess
import time
from pathlib import Path

ENV_SH = Path(__file__).resolve().parent.parent / "config" / "env.sh"


def hspice_env():
    env = dict(os.environ)
    for line in ENV_SH.read_text().splitlines():
        m = re.match(r"\s*export\s+(\w+)=(.*)", line)
        if m:
            val = m.group(2).strip().strip('"')
            val = re.sub(r"\$(\w+)|\$\{(\w+)\}", lambda x: env.get(x.group(1) or x.group(2), ""), val)
            env[m.group(1)] = val
    return env


def run_hspice(workdir, netlist, timeout=300):
    t0 = time.time()
    base = Path(netlist).stem
    try:
        p = subprocess.run(["hspice", "-i", netlist, "-o", base], cwd=workdir, env=hspice_env(), capture_output=True, text=True, timeout=timeout)
        out, rc = (p.stdout or "") + (p.stderr or ""), p.returncode
    except subprocess.TimeoutExpired:
        out, rc = f"ZAMAN AŞIMI ({timeout} sn)", -1
    except FileNotFoundError:
        out, rc = "hspice komutu bulunamadı (env.sh / kurulum)", -2
    return {"rc": rc, "stdout": out, "ms": int((time.time() - t0) * 1000), "base": base}


def read_measures(workdir, base):
    """.mt0/.ma0/.ms0 dosyalarından ölçümleri {ad: değer} olarak okur."""
    res = {}
    for ext in ("mt0", "ma0", "ms0"):
        f = Path(workdir) / f"{base}.{ext}"
        if not f.exists():
            continue
        toks = []
        for ln in f.read_text(errors="replace").splitlines():
            if ln.startswith(("$", ".")):
                continue
            toks += ln.split()
        names, vals = [], []
        for t in toks:
            try:
                vals.append(float(t))
            except ValueError:
                if vals:
                    break
                names.append(t.lower())
        for n, v in zip(names, vals):
            if n not in ("temper", "alter#"):
                res[n] = v
    return res


def lis_problems(workdir, base):
    f = Path(workdir) / f"{base}.lis"
    if not f.exists():
        return {"errors": ["çıktı (.lis) oluşmadı"], "warnings": [], "license": ""}
    txt = f.read_text(errors="replace")
    errs = [l.strip() for l in txt.splitlines() if "**error**" in l.lower() or "fatal" in l.lower()][:12]
    warns = [l.strip() for l in txt.splitlines() if "**warning**" in l.lower()][:8]
    lic = next((l.strip() for l in txt.splitlines() if "FLOATING license" in l), "")
    return {"errors": errs, "warnings": warns, "license": lic}
