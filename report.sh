#!/usr/bin/env bash
set -euo pipefail
usage() { echo 'Использование: ./report.sh КАТАЛОГ ERROR|WARN [--top N]' >&2; }
if (( $# != 2 && $# != 4 )); then usage; exit 1; fi
dir=$1
level=$2
top=0
if [[ ! -d "$dir" ]]; then echo "Каталог не найден: $dir" >&2; exit 2; fi
if [[ "$level" != ERROR && "$level" != WARN ]]; then usage; exit 1; fi
if (( $# == 4 )); then
    if [[ $3 != '--top' || ! $4 =~ ^[1-9][0-9]*$ ]]; then usage; exit 1; fi
    top=$4
fi
# Модуль извлекается из поля module=... только в записях заданного уровня.
# Обход файлов через -print0 работает и с пробелами в имени.
tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT
while IFS= read -r -d '' file; do
    awk -v target="$level" '
        $3 == target {
            for (i = 4; i <= NF; i++)
                if ($i ~ /^module=/) {
                    sub(/^module=/, "", $i)
                    print $i
                    break
                }
        }
    ' "$file" >> "$tmp"
done < <(find "$dir" -type f -name '*.log' -print0)
printf '%-20s %s\n' 'Модуль' 'Количество'
if [[ ! -s "$tmp" ]]; then echo 'Нет записей'; exit 0; fi
if (( top == 0 )); then
    sort "$tmp" | uniq -c | sort -k1,1nr -k2,2 | awk '{printf "%-20s %d\n", $2, $1}'
else
    # awk ограничивает печать без SIGPIPE в pipefail.
    sort "$tmp" | uniq -c | sort -k1,1nr -k2,2 | awk -v n="$top" 'NR<=n {printf "%-20s %d\n", $2, $1}'
fi
