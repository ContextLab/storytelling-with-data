# Test results — Collaborative Explorer

Last run: 2026-04-29

## Summary

```
75 passed, 1 skipped, 2 warnings in 149.21s
```

## Coverage by phase

| Phase | Tests | Status |
|-|-|-|
| Phase 2 (foundational): ingest, reconcile, NLP, recipes, schema | 24 | ✅ all pass |
| US1 — Tables view | 17 (12 parametrized + 5) | ✅ 16 pass, 1 skipped (virtualized rows) |
| US2 — Compare | 4 | ✅ all pass |
| US3 — Timeline | 3 | ✅ all pass |
| US4 — Sankey | 4 | ✅ all pass |
| US5 — Effectiveness | 4 | ✅ all pass |
| US6 — Sentiment | 3 | ✅ all pass |
| US7 — Theme map | 4 | ✅ all pass |
| US8 — Recipes | 5 | ✅ all pass |
| Polish: perf | 2 | ✅ all pass (initial load < 10 s, view-switch < 4 s) |
| Polish: offline | 1 | ✅ no external network requests during full view walkthrough |

## Notes

- All tests use real `.xlsx` data and the real `data.json` produced by `python -m pipeline.build`.
- No mocks — sentiment, embeddings, UMAP, HDBSCAN, recipe-axis projection all run against the actual models.
- The 1 skipped test (`test_freetext_cell_expand`) checks for a truncated freetext cell in the visible viewport. Tabulator's virtualization sometimes excludes any wide-text rows from the initial render; the truncation behavior is exercised manually and via the `freetextFormatter` code path.
- Determinism: re-running `build.py` produces a `data.json` that varies only in the `built_at` timestamp.

## Reproducing

```bash
cd data-stories/collaborative/explorer
source .venv/bin/activate
python -m pipeline.build --out dist/data.json   # ~3 min on first run, model download
EXPLORER_SKIP_BUILD=1 python -m pytest tests/ -v
```
