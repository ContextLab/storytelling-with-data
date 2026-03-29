#!/usr/bin/env bash
# Compile all cdl-slides markdown files to HTML.
# Usage: ./scripts/build-slides.sh [output_dir]
#
# Finds all .md files in slides/ with 'marp: true' frontmatter
# and compiles each via cdl-slides compile.

set -euo pipefail

SLIDES_DIR="$(cd "$(dirname "$0")/.." && pwd)/slides"
OUTPUT_DIR="${1:-$SLIDES_DIR}"

if ! command -v cdl-slides &>/dev/null; then
    echo "ERROR: cdl-slides not found. Install with: pip install cdl-slides"
    exit 1
fi

compiled=0
failed=0

for md_file in "$SLIDES_DIR"/*.md; do
    [ -f "$md_file" ] || continue

    # Check for marp frontmatter
    if ! head -5 "$md_file" | grep -q "marp: true"; then
        echo "SKIP: $(basename "$md_file") (no marp frontmatter)"
        continue
    fi

    echo "COMPILE: $(basename "$md_file")"
    out_file="$OUTPUT_DIR/$(basename "${md_file%.md}.html")"

    if cdl-slides compile "$md_file" --format html 2>&1; then
        compiled=$((compiled + 1))
        echo "  → $out_file"
    else
        failed=$((failed + 1))
        echo "  ERROR: Failed to compile $(basename "$md_file")"
    fi
done

echo ""
echo "Results: $compiled compiled, $failed failed"
[ "$failed" -eq 0 ] || exit 1
