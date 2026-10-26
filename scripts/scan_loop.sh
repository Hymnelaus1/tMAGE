#!/bin/bash
# Read-only: refreshes docs/22_Benchmark_Bulgulari.md every 30 min until the benchmark has finished.
cd "$(dirname "$0")/.."
LOG=batch/model_bench_20261026.log
while true; do
  python3 scripts/scan_findings.py >/dev/null 2>&1
  grep -q "done deepseek-coder:6.7b" "$LOG" && { python3 scripts/scan_findings.py >/dev/null 2>&1; echo "$(date +%T) benchmark finished, final scan written" >> batch/scan_loop.log; break; }
  sleep 1800
done
