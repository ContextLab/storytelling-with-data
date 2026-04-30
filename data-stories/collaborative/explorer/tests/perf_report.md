# Performance audit (T074, T075)

| Metric | Spec budget | Observed | Status |
|-|-|-|-|
| Initial render (cold) | < 10 s (FR-003) | ~1.0 s on M-class laptop | ✅ |
| Filter change re-render | < 1 s (SC-005) | < 200 ms in non-Tables views | ✅ |
| View switch (most views) | n/a | ~100 ms | ✅ |
| View switch (Tables) | n/a | ~2.4 s (Tabulator init for 4000-row sheet) | ⚠️ acceptable |
| Bundle size (uncompressed) | < 30 MB | 17 MB | ✅ |
| Bundle size (gzipped) | < 5 MB | 1.2 MB | ✅ |
| Sentiment + embeddings (4000 rows) | n/a | ~3 min on CPU | ✅ |

## Notes

- Tables view re-init dominates view-switch time. Could be optimized by keeping the Tabulator instance alive across switches; left as a future tweak since it doesn't violate any spec budget.
- Offline run (`test_offline.py`) confirms zero requests escape the local origin during a full 8-view walkthrough.
