#!/usr/bin/env bash
set -euo pipefail

# Directory containing the input .txt files (default: input/)
INDIR="${1:-input}"

# Output directory for cleaned files
OUTDIR="${2:-cleaned_no_quran}"

mkdir -p "$OUTDIR"

cd "$INDIR"

for file in *.txt; do
    # Prevent literal glob when no files exist
    [ -e "$file" ] || { echo "No .txt files found in $INDIR"; exit 0; }

    # Construct output filename *inside* OUTDIR
    outfile="../${OUTDIR}/${file}"

    # Replace every { ... } segment with <QQ>
    sed -E 's/\{[^}]*\}/<QQ>/g' "$file" > "$outfile"

    echo "Processed: $file -> $outfile"
done
