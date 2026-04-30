"""T013: Reconcile schemas across years using header_map.yaml.

Produces:
- the Measure table per data-model.md §4 (with `scale_mixed` flag)
- the SchemaDriftRecord table per data-model.md §14
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from . import ingest


@dataclass
class MeasureRecord:
    id: str
    display_name: str
    description: str
    value_scale_canonical: str
    aliases: list[dict[str, Any]] = field(default_factory=list)
    coverage_years: list[int] = field(default_factory=list)
    coverage_workbooks: list[str] = field(default_factory=list)
    scale_mixed: bool = False


@dataclass
class SchemaDriftRecord:
    workbook_id: str
    added: list[dict[str, str]] = field(default_factory=list)
    removed: list[dict[str, str]] = field(default_factory=list)
    scale_changes: list[dict[str, str]] = field(default_factory=list)


def load_header_map(path: Path) -> list[dict[str, Any]]:
    with open(path, "r") as fh:
        doc = yaml.safe_load(fh)
    return list(doc.get("measures", []))


def build_measures(
    sheets: list[ingest.SheetData],
    header_map: list[dict[str, Any]],
) -> tuple[list[MeasureRecord], dict[str, str]]:
    """Build the Measure table and a column_id→measure_id back-reference index."""
    by_sheet: dict[str, ingest.SheetData] = {s.sheet_id: s for s in sheets}
    by_wb: dict[str, list[ingest.SheetData]] = {}
    for s in sheets:
        by_wb.setdefault(s.workbook_id, []).append(s)

    measures: list[MeasureRecord] = []
    col_to_measure: dict[str, str] = {}

    for entry in header_map:
        m = MeasureRecord(
            id=entry["id"],
            display_name=entry["display_name"],
            description=entry["description"],
            value_scale_canonical=entry["value_scale_canonical"],
        )
        seen_workbooks: set[str] = set()
        seen_years: set[int] = set()
        scales_seen: set[str] = set()

        for alias in entry.get("aliases", []):
            wb_id = alias["workbook_id"]
            sheet_re = re.compile(alias["sheet_pattern"])
            header_pat = alias["header_pattern"].lower()
            transform = alias.get("transform", "identity")

            for s in by_wb.get(wb_id, []):
                # Match by either display_name (e.g. '2023', 'Event 5 Follow up')
                # OR by the period_label, OR by the underlying sheet name.
                if not (
                    sheet_re.search(s.display_name)
                    or sheet_re.search(s.period_label)
                ):
                    continue

                # Find the first column whose original header contains the pattern
                col_pos = _find_header(s.headers, header_pat)
                if col_pos is None:
                    continue

                col_id = s.column_ids[col_pos]
                m.aliases.append({
                    "column_id": col_id,
                    "raw_scale": s.inferred_types[col_pos],
                    "transform": transform,
                })
                col_to_measure[col_id] = m.id

                seen_workbooks.add(wb_id)
                if isinstance(s.period, int):
                    seen_years.add(s.period)
                scales_seen.add(s.inferred_types[col_pos])

        m.coverage_workbooks = sorted(seen_workbooks)
        m.coverage_years = sorted(seen_years)
        m.scale_mixed = len(scales_seen) > 1
        if m.aliases:
            measures.append(m)

    return measures, col_to_measure


def build_schema_drift(sheets: list[ingest.SheetData]) -> list[SchemaDriftRecord]:
    """Compare consecutive sheets within each workbook to surface header drift."""
    records: list[SchemaDriftRecord] = []
    by_wb: dict[str, list[ingest.SheetData]] = {}
    for s in sheets:
        by_wb.setdefault(s.workbook_id, []).append(s)

    for wb_id, ws in by_wb.items():
        # Sort by period (year ints; for RTU use the event ordinal via period)
        ws_sorted = sorted(
            ws,
            key=lambda s: (
                s.period if isinstance(s.period, int) else 999
            ),
        )
        rec = SchemaDriftRecord(workbook_id=wb_id)
        for i in range(1, len(ws_sorted)):
            prev = ws_sorted[i - 1]
            curr = ws_sorted[i]
            prev_set = {
                _norm(h): (idx, h) for idx, h in enumerate(prev.headers) if not h.startswith("<empty")
            }
            curr_set = {
                _norm(h): (idx, h) for idx, h in enumerate(curr.headers) if not h.startswith("<empty")
            }
            for k, (idx, h) in curr_set.items():
                if k not in prev_set:
                    rec.added.append({
                        "sheet_id": curr.sheet_id,
                        "column_id": curr.column_ids[idx],
                        "original_header": h,
                    })
            for k, (idx, h) in prev_set.items():
                if k not in curr_set:
                    rec.removed.append({
                        "sheet_id": prev.sheet_id,
                        "column_id": prev.column_ids[idx],
                        "original_header": h,
                    })
        records.append(rec)
    return records


def _find_header(headers: list[str], pattern_lower: str) -> int | None:
    for i, h in enumerate(headers):
        if pattern_lower in str(h).lower():
            return i
    return None


def _norm(h: str) -> str:
    """Normalize header for drift comparison: strip whitespace, lowercase, trim trailing dedup suffixes."""
    s = str(h).strip().lower()
    # Strip trailing ' 2', ' 3', etc. that the source uses to disambiguate duplicates.
    s = re.sub(r"\s+\d+$", "", s)
    s = re.sub(r"\s+", " ", s)
    return s
