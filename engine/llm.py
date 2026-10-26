"""Ollama (Jetson) sohbet çağrısı. Yalnızca standart kütüphane."""
import json
import re
import time
import urllib.error
import urllib.request


def chat(url, model, messages, temperature=0.2, timeout=600, json_mode=True, schema=None, num_predict=None):
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
