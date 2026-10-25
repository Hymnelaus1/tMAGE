#!/bin/bash
# tMAGE arayüzünü başlatır. Tarayıcıda http://127.0.0.1:8765 açılır.
# Tailscale üzerinden başka PC'den açmak için: TMAGE_HOST=0.0.0.0 ./run.sh
cd "$(dirname "$0")"
[ -f config/jetson.env ] && source config/jetson.env
URL="http://${TMAGE_HOST:-127.0.0.1}:${TMAGE_PORT:-8765}"
if ! curl -s -m 1 "$URL/api/state" >/dev/null 2>&1; then
  nohup python3 app/server.py > runs/server.log 2>&1 &
  sleep 1
fi
[ "${1:-}" = "--no-browser" ] || { command -v xdg-open >/dev/null && xdg-open "$URL" >/dev/null 2>&1 & }
echo "tMAGE: $URL"
