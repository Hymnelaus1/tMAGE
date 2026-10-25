"""tMAGE loglama. Her koşunun klasöründe:
  logs/run.log        insan okuyabilir günlük (zaman, seviye, mesaj)
  logs/events.jsonl   aynı olaylar, makine okuyabilir (süre, model, token vb. alanlarla)
  logs/llm/*.json     her LLM çağrısının tam istek/yanıtı
  logs/sim/*.txt      her HSPICE koşusunun ekran çıktısı
  logs/status.json    koşunun durumu (running/done/failed)
Genel olaylar (sunucu, iş kaydı) ~/tmage/logs/tmage.log dosyasına gider.
"""
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _ts():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def glog(msg, level="INFO"):
    d = ROOT / "logs"
    d.mkdir(exist_ok=True)
    with open(d / "tmage.log", "a") as f:
        f.write(f"{_ts()} [{level}] {msg}\n")


class RunLogger:
    def __init__(self, run_dir):
        self.run = Path(run_dir)
        self.dir = self.run / "logs"
        (self.dir / "llm").mkdir(parents=True, exist_ok=True)
        (self.dir / "sim").mkdir(exist_ok=True)
        self.n_llm = 0

    def log(self, level, msg, **kw):
        line = f"{_ts()} [{level}] {msg}"
        with open(self.dir / "run.log", "a") as f:
            f.write(line + "\n")
        with open(self.dir / "events.jsonl", "a") as f:
            f.write(json.dumps({"t": _ts(), "level": level, "msg": msg, **kw}, ensure_ascii=False) + "\n")

    def info(self, msg, **kw):
        self.log("INFO", msg, **kw)

    def warn(self, msg, **kw):
        self.log("WARN", msg, **kw)

    def error(self, msg, **kw):
        self.log("ERROR", msg, **kw)

    def llm_call(self, stage, record):
        self.n_llm += 1
        name = f"{self.n_llm:03d}_{stage}.json"
        (self.dir / "llm" / name).write_text(json.dumps(record, ensure_ascii=False, indent=1))
        return name

    def sim_output(self, name, text):
        (self.dir / "sim" / f"{name}.txt").write_text(text)

    def status(self, state, **kw):
        f = self.dir / "status.json"
        cur = json.loads(f.read_text()) if f.exists() else {}
        cur.update({"state": state, "updated": _ts(), **kw})
        f.write_text(json.dumps(cur, ensure_ascii=False))
