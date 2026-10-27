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
        out, rc = f"TIMEOUT ({timeout} s)", -1
    except FileNotFoundError:
        out, rc = "hspice command not found (check env.sh / installation)", -2
    return {"rc": rc, "stdout": out, "ms": int((time.time() - t0) * 1000), "base": base}


def parse_measure_file(path):
    """Parses one .mt0/.ma0/.ms0 file into ({name: value}, [failed names]).

    Layout: a header of measure names, then one row of values. A failed measure prints the token 'failed'
    in its own column, so values are matched to names by position (never by zipping the leading floats).
    """
    toks = []
    for ln in Path(path).read_text(errors="replace").splitlines():
        if ln.startswith(("$", ".")):
            continue
        toks += ln.split()

    def is_value(t):
        if t.lower() == "failed":
            return True
        try:
            float(t)
            return True
        except ValueError:
            return False

    k = 0
    while k < len(toks) and not is_value(toks[k]):
        k += 1
    names, vals = [t.lower() for t in toks[:k]], toks[k:k + k]
    good, bad = {}, []
    for n, v in zip(names, vals):
        if n in ("temper", "alter#"):
            continue
        if v.lower() == "failed":
            bad.append(n)
        else:
            good[n] = float(v)
    return good, bad


def read_measures(workdir, base, with_failed=False):
    """Reads measures from .mt0/.ma0/.ms0 as {name: value}. Failed measures are left out (never a fake number);
    with_failed=True also returns the list of failed measure names."""
    res, failed = {}, []
    for ext in ("mt0", "ma0", "ms0"):
        f = Path(workdir) / f"{base}.{ext}"
        if f.exists():
            g, b = parse_measure_file(f)
            res.update(g)
            failed += b
    return (res, failed) if with_failed else res


def lis_problems(workdir, base):
    f = Path(workdir) / f"{base}.lis"
    if not f.exists():
        return {"errors": ["output (.lis) was not created"], "warnings": [], "license": ""}
    txt = f.read_text(errors="replace")
    errs = [l.strip() for l in txt.splitlines() if "**error**" in l.lower() or "fatal" in l.lower()][:12]
    warns = [l.strip() for l in txt.splitlines() if "**warning**" in l.lower()][:8]
    lic = next((l.strip() for l in txt.splitlines() if "FLOATING license" in l), "")
    return {"errors": errs, "warnings": warns, "license": lic}
