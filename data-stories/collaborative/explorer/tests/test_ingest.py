"""T024: ingest.py — assert source_row_count for every sheet matches data-model §2 within ±1."""

from __future__ import annotations

import pytest

from pipeline import ingest


EXPECTED = {
    ("rtu_2025_26", "Kickoff Follow Up"): 465,
    ("rtu_2025_26", "Event 2 Follow Up"): 491,
    ("rtu_2025_26", "Event 3 Follow Up"): 443,
    ("rtu_2025_26", "Event 4 Follow Up"): 294,
    ("rtu_2025_26", "Event 5 Follow up"): 157,
    ("hs_core", "2022"): 472,
    ("hs_core", "2023"): 229,
    ("hs_core", "2025"): 563,
    ("ms_core", "2022"): 417,
    ("ms_core", "2023"): 305,
    ("ms_core", "2024"): 419,
    ("ms_core", "2025"): 264,
}


def test_all_sheets_loaded(data_dir):
    sheets = ingest.read_workbooks(data_dir)
    seen = {(s.workbook_id, s.display_name): s.source_row_count for s in sheets}
    assert len(seen) == 12, f"expected 12 sheets, got {len(seen)}"


@pytest.mark.parametrize("key,expected", list(EXPECTED.items()))
def test_row_counts_match(data_dir, key, expected):
    sheets = ingest.read_workbooks(data_dir)
    by_key = {(s.workbook_id, s.display_name): s.source_row_count for s in sheets}
    observed = by_key.get(key)
    assert observed is not None, f"missing sheet {key}"
    assert abs(observed - expected) <= 1, f"{key}: observed {observed}, expected ~{expected}"


def test_inferred_types_present(data_dir):
    """Every column has a non-empty inferred_type and the set is the closed enum we expect."""
    sheets = ingest.read_workbooks(data_dir)
    allowed = {"categorical", "ordinal", "numeric", "freetext", "datetime", "empty"}
    for s in sheets:
        assert len(s.inferred_types) == len(s.headers)
        for t in s.inferred_types:
            assert t in allowed, f"unknown inferred_type {t!r} in {s.sheet_id}"
