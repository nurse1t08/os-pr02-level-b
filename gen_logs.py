#!/usr/bin/env python3
"""Создать учебные логи для PR02: 50 файлов, фиксированный seed."""
from pathlib import Path
import argparse
import random


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--dir', default='data')
    p.add_argument('--files', type=int, default=50)
    p.add_argument('--lines', type=int, default=200)
    args = p.parse_args()
    rng = random.Random(42)
    dest = Path(args.dir)
    dest.mkdir(parents=True, exist_ok=True)
    for i in range(1, args.files + 1):
        with (dest / f'{i:02d}.log').open('w', encoding='utf-8') as f:
            for j in range(args.lines):
                level = rng.choices(['INFO', 'WARN', 'ERROR'], [60, 25, 15])[0]
                module = rng.choice(['net', 'db', 'auth', 'ui', 'cache'])
                f.write(f'2026-02-14 10:{j // 60:02d}:{j % 60:02d} '
                        f'{level} module={module} msg=sample_{j}\n')
    print(f'Создано {args.files} файлов в {dest}')


if __name__ == '__main__':
    main()
