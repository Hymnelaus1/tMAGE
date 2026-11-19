"""Ollama (Jetson) chat call, plus local CLI backends (model names `cli:claude[:alias]`, `cli:codex[:model]`). Standard library only."""
import json
import re
import shutil
import subprocess
import tempfile
import time
import urllib.error
import urllib.request


def _cli_chat(model, messages, timeout, json_mode):
    """Runs the system-installed `claude` or `codex` CLI with the account already logged in there (no API key handled here).
    model: cli:claude, cli:claude:<alias>, cli:codex, cli:codex:<model>. Tools are disabled; the CLI only answers text."""
    kind, _, alias = model[4:].partition(":")
    exe = shutil.which(kind)
    if kind not in ("claude", "codex") or not exe:
        raise RuntimeError(f"CLI backend '{kind}' not found on PATH")
    system = "\n\n".join(m["content"] for m in messages if m["role"] == "system")
    user = "\n\n".join(m["content"] for m in messages if m["role"] != "system")
    if json_mode:
        user += "\n\nReply with a single JSON object only, no prose, no code fence."
    t0 = time.time()
    with tempfile.TemporaryDirectory() as cwd:           # empty cwd: the CLI sees no project files, no CLAUDE.md
        if kind == "claude":
            cmd = [exe, "-p", "--output-format", "json", "--tools", "", "--no-session-persistence", "--disable-slash-commands",
                   "--setting-sources", "", "--system-prompt", system or "You are a careful assistant."] + (["--model", alias] if alias else [])
            p = subprocess.run(cmd, input=user, cwd=cwd, capture_output=True, text=True, timeout=timeout)
            if p.returncode:
                raise RuntimeError("claude CLI failed: " + (p.stderr or p.stdout)[:300])
            d = json.loads(p.stdout)
            u = d.get("usage") or {}
            return {"text": d.get("result", ""), "ms": int((time.time() - t0) * 1000), "prompt_tokens": u.get("input_tokens"),
                    "output_tokens": u.get("output_tokens"), "model": model, "done_reason": None}
        cmd = [exe, "exec", "--skip-git-repo-check", "--sandbox", "read-only"] + (["-m", alias] if alias else []) + ["-"]
        p = subprocess.run(cmd, input=(system + "\n\n" + user) if system else user, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        if p.returncode:
            raise RuntimeError("codex CLI failed: " + (p.stderr or p.stdout)[:300])
        return {"text": p.stdout, "ms": int((time.time() - t0) * 1000), "prompt_tokens": None, "output_tokens": None, "model": model, "done_reason": None}


def chat(url, model, messages, temperature=0.2, timeout=600, json_mode=True, schema=None, num_predict=None):
    if str(model).startswith("cli:"):
        return _cli_chat(model, messages, timeout, json_mode)
    base = re.sub(r"/v1/?$", "", url.rstrip("/"))
    body = {"model": model, "messages": messages, "stream": False, "think": False,
            "options": {"temperature": temperature, "num_ctx": 8192}}
    if schema:
        body["format"] = schema  # yapılandırılmış çıktı: model şemaya uymak zorunda
    elif json_mode:
        body["format"] = "json"
    if num_predict:
        body["options"]["num_predict"] = num_predict
    body["options"]["stop"] = ["\\n\\n\\n\\n\\n\\n"]  # JSON içinde satır sonu döngüsü (\n\n\n...) başlarsa üretimi erken kes
    t0 = time.time()
    req = urllib.request.Request(base + "/api/chat", json.dumps(body).encode(), {"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        if e.code != 400:
            raise
        body.pop("think", None)  # bazı modeller "think" alanını desteklemez
        req = urllib.request.Request(base + "/api/chat", json.dumps(body).encode(), {"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.load(r)
    return {"text": d.get("message", {}).get("content", ""), "ms": int((time.time() - t0) * 1000),
            "prompt_tokens": d.get("prompt_eval_count"), "output_tokens": d.get("eval_count"), "model": model, "done_reason": d.get("done_reason")}


def parse_json(text):
    """Model çıktısından JSON nesnesini çıkarır (kod bloğu veya fazladan metin olsa da)."""
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t, flags=re.I)
    try:
        return json.loads(t, strict=False)
    except ValueError:
        m = re.search(r"\{.*\}", t, re.S)
        if m:
            return json.loads(m.group(0), strict=False)
        raise
