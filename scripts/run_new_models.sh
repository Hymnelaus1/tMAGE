#!/bin/bash
# Chain: wait for the model pull -> benchmark of the new models -> report -> random 3-model votes.
# Usage: scripts/run_new_models.sh <pull_pid> <bench_dir> <triples_dir> "<model> <model> ..."
cd "$(dirname "$0")/.."
source config/env.sh
PID=$1; BENCH=$2; TRI=$3; MODELS=$4
while kill -0 "$PID" 2>/dev/null; do sleep 30; done
echo "$(date +%T) pull finished, start benchmark" >> "$BENCH.log"
scripts/model_bench.sh "$BENCH" $MODELS
python3 scripts/recompute_scores.py "$BENCH" docs/27_New_Models_Benchmark_Report.md >> "$BENCH.log" 2>&1
python3 scripts/random_triples.py "$TRI" 4 20261028 4 batch/model_bench_20261026/recomputed.json "$BENCH/recomputed.json" >> "$TRI.log" 2>&1
echo "$(date +%T) all done" >> "$TRI.log"
