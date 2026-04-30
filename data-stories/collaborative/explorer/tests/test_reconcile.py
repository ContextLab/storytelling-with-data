"""T025: reconcile.py — assert every measure resolves to ≥1 column per declared coverage year."""

from __future__ import annotations

from pathlib import Path

from pipeline import ingest, reconcile


def _measures():
    here = Path(__file__).resolve().parent.parent / "pipeline"
    return reconcile.load_header_map(here / "header_map.yaml")


def test_header_map_loads():
    m = _measures()
    assert len(m) > 5
    for entry in m:
        for key in ("id", "display_name", "description", "value_scale_canonical", "aliases"):
            assert key in entry, f"measure {entry.get('id')} missing key {key}"
        assert len(entry["aliases"]) > 0, f"measure {entry['id']} has no aliases"


def test_every_measure_has_at_least_one_resolved_column(data_dir):
    sheets = ingest.read_workbooks(data_dir)
    measures, col_to_measure = reconcile.build_measures(sheets, _measures())
    for m in measures:
        assert len(m.aliases) > 0, f"measure {m.id} resolved to zero columns"


def test_no_two_measures_share_a_column(data_dir):
    sheets = ingest.read_workbooks(data_dir)
    measures, col_to_measure = reconcile.build_measures(sheets, _measures())
    seen: dict[str, str] = {}
    for m in measures:
        for a in m.aliases:
            cid = a["column_id"]
            if cid in seen and seen[cid] != m.id:
                raise AssertionError(
                    f"column {cid} mapped to both {seen[cid]} and {m.id}"
                )
            seen[cid] = m.id


def test_schema_drift_records_built(data_dir):
    sheets = ingest.read_workbooks(data_dir)
    drift = reconcile.build_schema_drift(sheets)
    assert len(drift) == 3
    wb_ids = {d.workbook_id for d in drift}
    assert wb_ids == {"rtu_2025_26", "hs_core", "ms_core"}
