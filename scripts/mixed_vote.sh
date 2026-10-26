#!/bin/bash
# Mixed-model voting: for each topology run 3 reps with 3 DIFFERENT voter models (one per candidate).
# Usage: scripts/mixed_vote.sh <outdir> DA=modelA,modelB,modelC FCO=... TSO=...   (first model also runs spec/scenario/stimulus/measure agents)
cd "$(dirname "$0")/.."
source config/env.sh
OUT=$1; shift
for spec in "$@"; do
  topo=${spec%%=*}; voters=${spec#*=}; agent=${voters%%,*}
  echo "$(date +%T) start mixed $topo voters=$voters" >> "$OUT.log"
  python3 engine/batch.py --only "$topo" --reps 3 --n 3 --voters "$voters" --agent "$agent" --out "$OUT/$topo" >> "$OUT.log" 2>&1
  echo "$(date +%T) done mixed $topo" >> "$OUT.log"
done
