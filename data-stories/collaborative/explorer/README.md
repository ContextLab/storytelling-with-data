# Collaborative Dataset Interactive Explorer

A self-contained, offline-capable HTML explorer for the
`data-stories/collaborative/` dataset (RTU 2025–26 event follow-ups, plus
longitudinal Middle and High School Core Measures, 2022–2025).

> **Privacy note**: the explorer's bundled `data.json` contains raw free-text
> survey responses that may include identifying information. It is for
> internal team use only. `dist/data.json` is `.gitignore`d. Do **not**
> publish this artifact until a redaction pipeline is in place (a future
> spec).

## Quick start

```bash
# 1) Set up Python (3.11)
cd data-stories/collaborative/explorer
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium    # for the smoke tests

# 2) Optional: install local LLM for high-quality cluster naming
pip install llama-cpp-python==0.3.5

# 3) Build the data bundle
python pipeline/build.py --out dist/data.json

# 4) Open the explorer
open dist/index.html            # macOS
xdg-open dist/index.html        # Linux
```

That's it — no server, no network at runtime.

## What the explorer does

Eight views, all offline, Dartmouth-green palette, serif body / monospace numbers:

1. **Tables** — every sheet of every workbook; full-question tooltips on column headers; per-column missingness + top values; schema-diff view for Core Measures.
2. **Compare** — pick a measure, pick schools, split by grade or year.
3. **Timeline** — multi-measure overlay or small-multiples across years/events; gaps for missing periods.
4. **Sankey** — 5-event response funnel with stratification by school/grade.
5. **Effectiveness** — survey-direct, sentiment-derived, behavioral-intent, and retention-derived indicators.
6. **Sentiment** — aggregate free-text sentiment with drill-down to representative responses.
7. **Theme Map** — UMAP projection of free-text embeddings with auto-named HDBSCAN clusters.
8. **Recipes** — Event-4 recipe responses positioned on savory↔sweet × complexity axes.

## Architecture

Two-stage:

- **Build (Python)**: `pipeline/build.py` reads the three `.xlsx` files, normalizes schemas, computes sentiment/embeddings/clusters/cluster-names/recipe-axes, validates against the bundle schema, writes `dist/data.json` (and `dist/data.json.gz`).
- **Runtime (browser)**: `dist/index.html` + `dist/assets/app.js` + `dist/assets/views/*.js` consume the bundle. No network calls.

See:

- [`../../specs/004-collab-data-explorer/spec.md`](../../specs/004-collab-data-explorer/spec.md) — what the explorer must do
- [`../../specs/004-collab-data-explorer/plan.md`](../../specs/004-collab-data-explorer/plan.md) — how it's built
- [`../../specs/004-collab-data-explorer/contracts/data-bundle.schema.json`](../../specs/004-collab-data-explorer/contracts/data-bundle.schema.json) — the JSON contract
- `pipeline/MODEL_VERSIONS.md` — pinned model hashes for reproducibility

## Tests

```bash
pytest tests/                 # build-pipeline unit + integration
pytest tests/test_runtime_smoke.py   # Playwright against dist/index.html
```

All tests use real `.xlsx` files and the real `data.json` produced by
`build.py` — no mocks, per repo `CLAUDE.md`.

## Rebuilding

| Change | What to rerun |
|-|-|
| Updated source `.xlsx` | `python pipeline/build.py` |
| Edited `header_map.yaml` | `python pipeline/build.py` |
| Adjusted recipe anchors | `python pipeline/build.py --only-recipes` |
| Tweaked CSS / JS only | refresh the browser |
| Changed cluster-naming model | `python pipeline/build.py --rename-clusters` |
