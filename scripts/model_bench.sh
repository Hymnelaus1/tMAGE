#!/bin/bash
# Per-model benchmark: each model alone (agents + all N candidates), DA/FCO/TSO, REPS runs each.
# Usage: scripts/model_bench.sh <outdir> model1 model2 ...
cd "$(dirname "$0")/.."
source config/env.sh
OUT=$1; shift
for m in "$@"; do
  d="$OUT/$(echo "$m" | tr ':/' '__')"
  curl -s -m 5 http://100.113.87.120:11434/api/tags | grep -q "\"$m\"" || { echo "skip $m (not installed)" >> "$OUT.log"; continue; }
  echo "$(date +%T) start $m" >> "$OUT.log"
  python3 engine/batch.py --only DA,FCO,TSO --reps 3 --n 3 --voters "$m,$m,$m" --agent "$m" --out "$d" >> "$OUT.log" 2>&1
  echo "$(date +%T) done $m" >> "$OUT.log"
done
