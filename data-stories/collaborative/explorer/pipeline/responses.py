"""T015: Build the Response table per data-model.md §5.

Iterates rows in every Sheet and produces:
- one Response per non-empty row
- one FreeTextItem stub per non-empty freetext cell (NLP fields filled in nlp.py)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pandas as pd

from . import ingest
from . import schools


@dataclass
class FreeTextStub:
    id: str
    response_id: str
    column_id: str
    text: str
    text_length: int
    is_recipe_candidate: bool = False


@dataclass
class Response:
    id: str
    sheet_id: str
    school: str  # canonical school id
    grade_level: str | None
    submitted_at: str | None
    event_ordinal: int | None
    linkage_key: str | None
    values: dict[str, Any]
    freetext_item_ids: list[str] = field(default_factory=list)


def build_responses(
    sheets: list[ingest.SheetData],
) -> tuple[list[Response], list[FreeTextStub]]:
    out_resp: list[Response] = []
    out_ft: list[FreeTextStub] = []

    for sheet in sheets:
        # Find positional indices of school/grade/timestamp columns by name
        school_idx = _find_col(sheet.headers, ("School",))
        grade_idx = _find_col(sheet.headers, ("Grade Level", "What grade are you in?"))
        time_idx = _find_col(sheet.headers, ("Timestamp", "Submission Date"))
        recipe_idx = _find_col(sheet.headers, ("RTU cookbook",))

        event_meta = ingest.event_meta_for_sheet(sheet)
        event_ordinal = event_meta[1] if event_meta else None

        for row_idx, row in enumerate(sheet.df.itertuples(index=False, name=None)):
            # Skip rows that are entirely blank
            if all(_is_blank(v) for v in row):
                continue

            raw_school = row[school_idx] if school_idx is not None else None
            raw_grade = row[grade_idx] if grade_idx is not None else None
            raw_time = row[time_idx] if time_idx is not None else None

            resp_id = f"{sheet.sheet_id}.r{row_idx:04d}"
            response = Response(
                id=resp_id,
                sheet_id=sheet.sheet_id,
                school=schools.resolve_school(raw_school, sheet.workbook_id),
                grade_level=schools.normalize_grade(raw_grade),
                submitted_at=_to_iso(raw_time),
                event_ordinal=event_ordinal,
                linkage_key=None,
                values={},
            )

            # Build values + freetext stubs
            for col_pos, val in enumerate(row):
                if _is_blank(val):
                    continue
                col_id = sheet.column_ids[col_pos]
                col_type = sheet.inferred_types[col_pos]
                response.values[col_id] = _jsonable(val)
                if col_type == "freetext":
                    text = str(val).strip()
                    if not text:
                        continue
                    ft = FreeTextStub(
                        id=f"{resp_id}::{col_id}",
                        response_id=resp_id,
                        column_id=col_id,
                        text=text,
                        text_length=len(text),
                        is_recipe_candidate=(recipe_idx is not None and col_pos == recipe_idx),
                    )
                    response.freetext_item_ids.append(ft.id)
                    out_ft.append(ft)

            out_resp.append(response)

    return out_resp, out_ft


def _find_col(headers: list[str], needles: tuple[str, ...]) -> int | None:
    for i, h in enumerate(headers):
        for n in needles:
            if n.lower() in str(h).lower():
                return i
    return None


def _is_blank(v: Any) -> bool:
    if v is None:
        return True
    if isinstance(v, float):
        try:
            import math
            return math.isnan(v)
        except Exception:
            return False
    if isinstance(v, str) and not v.strip():
        return True
    return False


def _to_iso(v: Any) -> str | None:
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        try:
            return v.isoformat()
        except Exception:
            return str(v)
    if isinstance(v, str) and v.strip():
        return v
    return None


def _jsonable(v: Any) -> Any:
    if v is None:
        return None
    if isinstance(v, (str, int, bool)):
        return v
    if isinstance(v, float):
        import math
        if math.isnan(v) or math.isinf(v):
            return None
        return v
    if hasattr(v, "isoformat"):
        try:
            return v.isoformat()
        except Exception:
            return str(v)
    return str(v)
