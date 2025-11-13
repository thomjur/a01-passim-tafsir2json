#!/usr/bin/env bash
# statsgen.sh — word & character stats for .txt files, sorted by character count
# Usage: ./statsgen.sh [FOLDER] [OUTPUT_FILE]
# Example: ./statsgen.sh ./input summary.txt

set -euo pipefail

DIR="${1:-.}"
OUT="${2:-summary.txt}"
DEBUG="${DEBUG:-0}"   # set to 1 for debug lines (to stderr)

TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

have_any=0

# Plain glob over *.txt (quoted) — no process substitution, no arrays
for f in "$DIR"/*.txt; do
  [[ -f "$f" ]] || continue
  ((have_any=1))

  base="$(basename "$f")"

  # Try UTF-8 chars first; fall back to C; then to bytes (-c)
  out=""
  status=0
  out=$(LC_ALL=C.UTF-8 wc -w -m -- "$f" 2>/dev/null) || status=$?
  if (( status != 0 )); then
    status=0
    out=$(LC_ALL=C wc -w -m -- "$f" 2>/dev/null) || status=$?
  fi
  if (( status != 0 )); then
    # bytes instead of multibyte chars; still good for sorting by size
    out=$(wc -w -c -- "$f" 2>/dev/null) || out=""
  fi

  # Example wc output (GNU/BSD): "   123   456 filename with spaces.txt"
  # Extract first two numbers robustly:
  words=$(awk '{print $1+0}' <<<"$out")
  chars=$(awk '{print $2+0}' <<<"$out")

  if [[ "$DEBUG" == "1" ]]; then
    >&2 echo "[DBG] file='$base' raw='$out' | words=$words chars=$chars"
  fi

  printf "%d\t%d\t%s\n" "$words" "$chars" "$base" >> "$TMP"
done

if (( have_any == 0 )); then
  echo "No .txt files found in '$DIR'." >&2
  exit 1
fi

# Sort by Chars (2nd column) descending
sort -nrk2,2 "$TMP" -o "$TMP"

# Aggregates
total=$(wc -l < "$TMP")
sum_words=$(awk '{w+=$1} END{print w+0}' "$TMP")
sum_chars=$(awk '{c+=$2} END{print c+0}' "$TMP")
avg_words=$(awk -v s="$sum_words" -v n="$total" 'BEGIN{printf "%.2f", (n?s/n:0)}')
avg_chars=$(awk -v s="$sum_chars" -v n="$total" 'BEGIN{printf "%.2f", (n?s/n:0)}')

read -r max_words max_chars max_file < <(head -n1 "$TMP")
read -r min_words min_chars min_file < <(tail -n1 "$TMP")

# Report
{
  echo "# Statistics for .txt files in: $DIR"
  echo "# Generated on: $(date '+%Y-%m-%d %H:%M:%S')"
  echo
  printf "%-8s\t%-8s\t%s\n" "Words" "Chars" "File"
  echo "------------------------------------------------------------"
  awk '{printf "%-8d\t%-8d\t%s\n", $1, $2, $3}' "$TMP"
  echo
  echo "== Summary =="
  echo "Total files: $total"
  printf "Words  : Sum=%d | Avg=%s | Min=%d (%s) | Max=%d (%s)\n" \
    "$sum_words" "$avg_words" "$min_words" "$min_file" "$max_words" "$max_file"
  printf "Chars  : Sum=%d | Avg=%s | Min=%d (%s) | Max=%d (%s)\n" \
    "$sum_chars" "$avg_chars" "$min_chars" "$min_file" "$max_chars" "$max_file"
} > "$OUT"

echo "Done. Sorted statistics written to: $OUT"

