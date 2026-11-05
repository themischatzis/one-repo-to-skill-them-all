#!/bin/sh
# Usage: log.sh <logfile> <phase> <decision> <why> <evidence> <result>
set -eu
[ "$#" -eq 6 ] || { echo "usage: $0 <logfile> <phase> <decision> <why> <evidence> <result>" >&2; exit 2; }
file=$1; shift
[ -s "$file" ] || printf 'ts\tphase\tdecision\twhy\tevidence\tresult\n' > "$file"
row=$(date -u +%Y-%m-%dT%H:%M:%SZ)
for cell in "$@"; do
  # single line, no tabs, and neutralise spreadsheet formula prefixes
  clean=$(printf '%s' "$cell" | tr '\t\n\r' '   ')
  case $clean in [=+@-]*) clean="'$clean" ;; esac
  row="$row	$clean"
done
printf '%s\n' "$row" >> "$file"
