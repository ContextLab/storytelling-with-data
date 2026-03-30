#!/usr/bin/env bash
# Compile cdl-slides markdown files to HTML and PDF.
#
# Usage:
#   ./scripts/build-slides.sh              # compile ALL marp slides
#   ./scripts/build-slides.sh slides/foo.md  # compile one file
#
# Output lands next to each .md file (slides/foo.html, slides/foo.pdf).

set -euo pipefail

SLIDES_DIR="$(cd "$(dirname "$0")/.." && pwd)/slides"

if ! command -v cdl-slides &>/dev/null; then
    echo "ERROR: cdl-slides not found. Install with: pip install cdl-slides"
    exit 1
fi

compile_one() {
    local md_file="$1"

    if ! head -5 "$md_file" | grep -q "marp: true"; then
        echo "SKIP  $(basename "$md_file") (no marp frontmatter)"
        return 0
    fi

    local out_dir
    out_dir="$(dirname "$md_file")"
    local base
    base="$(basename "${md_file%.md}")"

    echo "BUILD $(basename "$md_file")"
    if cdl-slides compile "$md_file" --format both -o "$out_dir" 2>&1 | sed 's/^/  /'; then
        echo "  → ${base}.html + ${base}.pdf"
        return 0
    else
        echo "  ERROR: $(basename "$md_file") failed"
        return 1
    fi
}

compiled=0
failed=0

if [ $# -ge 1 ]; then
    # Single-file mode
    md_file="$1"
    if [ ! -f "$md_file" ]; then
        echo "ERROR: File not found: $md_file"
        exit 1
    fi
    if compile_one "$md_file"; then
        compiled=1
    else
        failed=1
    fi
else
    # All-files mode
    for md_file in "$SLIDES_DIR"/*.md; do
        [ -f "$md_file" ] || continue
        if compile_one "$md_file"; then
            compiled=$((compiled + 1))
        else
            failed=$((failed + 1))
        fi
    done
fi

echo ""
echo "Results: $compiled compiled, $failed failed"
[ "$failed" -eq 0 ] || exit 1
