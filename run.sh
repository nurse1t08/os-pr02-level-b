#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 gen_logs.py
./report.sh data ERROR --top 5
./report.sh data WARN
python3 hello.py data/01.log
if command -v strace >/dev/null 2>&1; then
  strace -f -yy -o trace_python.txt python3 hello.py data/01.log
  strace -f -yy -o trace_cat.txt cat data/01.log >/dev/null
  python3 analyze_trace.py trace_python.txt data/01.log
  python3 analyze_trace.py trace_cat.txt data/01.log
else
  echo 'strace не найден. На Ubuntu: sudo apt install strace'
fi
