#!/usr/bin/env python3
"""Открыть и прочитать файл, вывести размер содержимого в байтах."""
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('file', type=Path)
args = parser.parse_args()
with args.file.open('rb') as f:
    data = f.read()
print(f'Прочитано {len(data)} байт из {args.file}')
