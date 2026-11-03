#!/usr/bin/env python3
"""Приблизительный подсчёт записей strace (включая -f и -yy)."""
import re
import sys
from collections import Counter
from pathlib import Path

PATTERN = re.compile(r'^\s*(?:\[pid\s+\d+\]\s*|\d+\s+)?([a-zA-Z_][\w]*)\(')

def analyze(filename, target):
    counters = Counter()
    own_reads = 0
    for line in Path(filename).read_text(errors='replace').splitlines():
        match = PATTERN.match(line)
        if match:
            syscall = match.group(1)
            counters[syscall] += 1
            # strace -yy добавляет путь к дескриптору: read(3</.../01.log>, ...)
            if syscall in ('read', 'pread64', 'readv') and re.search(r'\b(?:read|pread64|readv)\(\d+<[^>]*' + re.escape(Path(target).name) + r'>', line):
                own_reads += 1
    print(f'Файл трассы: {filename}')
    print(f'Всего строк с завершёнными вызовами: {sum(counters.values())}')
    print(f'Чтений именно {Path(target).name} (нужен strace -yy): {own_reads}')
    print('Частые вызовы:', counters.most_common(5))

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('Использование: python3 analyze_trace.py trace.txt data/01.log')
    analyze(sys.argv[1], sys.argv[2])
