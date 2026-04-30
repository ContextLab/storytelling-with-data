"""T019 + T051: Effectiveness indicators per data-model.md §9.

Builds an EffectivenessIndicator table for the four families:
- survey_direct (e.g. share agreeing 'felt safe and comfortable')
- sentiment_derived (e.g. mean sentiment of 'what did you learn')
- behavioral_intent (share of 'how will you apply' responses with concrete intent)
- retention_derived (share returning to next event)
"""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Any, Iterable

from . import ingest, schools as schools_mod
from .reconcile import MeasureRecord
from .responses import Response, FreeTextStub


# Likert-5 agree scales: anything containing 'agree' or 'often' is positive.
AGREE_TOKENS = re.compile(r"agree|often|always|usually|yes\b|true\b", re.I)

# Concrete behavioral intent: response contains an action verb + object cue.
ACTION_VERBS = re.compile(
    r"\b(i\s+(will|am going to|plan to|intend to|am gonna|gonna)|let me|i'll|i ll|i'm going)\b",
    re.I,
)


def _is_agree(value: Any) -> bool:
    if value is None:
        return False
    return bool(AGREE_TOKENS.search(str(value)))


def _has_concrete_intent(text: str) -> bool:
    if not text:
        return False
    if not ACTION_VERBS.search(text):
        return False
    # at least 4 distinct words to count as concrete
    words = re.findall(r"\w+", text.lower())
    return len(set(words)) >= 4


def _filter_key(
    response: Response,
    sheet_by_id: dict[str, ingest.SheetData],
) -> dict[str, Any]:
    sheet = sheet_by_id[response.sheet_id]
    event_meta = ingest.event_meta_for_sheet(sheet)
    year = sheet.period if isinstance(sheet.period, int) else None
    return {
        "event_id": event_meta[0] if event_meta else None,
        "school_id": response.school,
        "grade": response.grade_level,
        "year": year,
    }


def _aggregate(
    items: Iterable[tuple[dict[str, Any], float]],
) -> list[dict[str, Any]]:
    """Group (filter_key, value) pairs by all combinations of the filters."""
    bucket: dict[tuple, list[float]] = defaultdict(list)
    for filt, val in items:
        # keep only the four canonical filter keys
        key = (
            filt.get("event_id"),
            filt.get("school_id"),
            filt.get("grade"),
            filt.get("year"),
        )
        bucket[key].append(val)
    out: list[dict[str, Any]] = []
    for (event_id, school_id, grade, year), vals in bucket.items():
        if not vals:
            continue
        mean = sum(vals) / len(vals)
        out.append({
            "filters": {
                "event_id": event_id,
                "school_id": school_id,
                "grade": grade,
                "year": year,
            },
            "value": float(mean),
            "n": len(vals),
            "ci": None,  # CI computation skipped for now
        })
    return out


def compute_indicators(
    responses: list[Response],
    freetext_items: list[FreeTextStub],
    sheets: list[ingest.SheetData],
    measures: list[MeasureRecord],
    col_to_measure: dict[str, str],
    sentiment_scores: dict[str, float],
) -> list[dict[str, Any]]:
    """Produce all indicator records per data-model.md §9."""
    sheet_by_id = {s.sheet_id: s for s in sheets}
    measure_by_id = {m.id: m for m in measures}

    indicators: list[dict[str, Any]] = []

    # ---- Survey-direct: % agree on "felt safe and comfortable" ----
    if "rtu_felt_safe" in measure_by_id:
        m = measure_by_id["rtu_felt_safe"]
        col_ids = [a["column_id"] for a in m.aliases]
        items: list[tuple[dict, float]] = []
        for resp in responses:
            for cid in col_ids:
                v = resp.values.get(cid)
                if v is not None:
                    items.append((_filter_key(resp, sheet_by_id), 100.0 if _is_agree(v) else 0.0))
        indicators.append({
            "id": "pct_agree_safety",
            "display_name": "% agree felt safe and comfortable",
            "family": "survey_direct",
            "description": "Share of respondents who agreed they felt safe and comfortable at the event.",
            "inputs": [{"kind": "measure", "ref": "rtu_felt_safe"}],
            "value_scale": "pct_in_0_100",
            "computed_values": _aggregate(items),
        })

    # ---- Survey-direct: mean of developmental-asset items (Event 5) ----
    da_ids = [
        "da_support", "da_empowerment", "da_boundaries", "da_constructive_time",
        "da_commitment_learning", "da_positive_values", "da_social_competencies",
        "da_positive_identity",
    ]
    for da_id in da_ids:
        if da_id not in measure_by_id:
            continue
        m = measure_by_id[da_id]
        col_ids = [a["column_id"] for a in m.aliases]
        items = []
        for resp in responses:
            for cid in col_ids:
                v = resp.values.get(cid)
                if v is not None:
                    items.append((_filter_key(resp, sheet_by_id), 100.0 if _is_agree(v) else 0.0))
        if items:
            indicators.append({
                "id": f"pct_agree_{da_id}",
                "display_name": f"% agree {m.display_name.replace('Developmental asset: ', '')}",
                "family": "survey_direct",
                "description": m.description,
                "inputs": [{"kind": "measure", "ref": da_id}],
                "value_scale": "pct_in_0_100",
                "computed_values": _aggregate(items),
            })

    # ---- Sentiment-derived: mean sentiment of "what did you learn" ----
    learn_cols = _find_columns_for_measure(measure_by_id.get("rtu_what_learned"))
    if learn_cols:
        items = []
        for ft in freetext_items:
            if ft.column_id in learn_cols:
                s = sentiment_scores.get(ft.id)
                if s is None:
                    continue
                resp = _resp_lookup(responses, ft.response_id)
                if resp is None:
                    continue
                items.append((_filter_key(resp, sheet_by_id), float(s)))
        indicators.append({
            "id": "mean_sentiment_learning",
            "display_name": "Mean sentiment — 'What did you learn'",
            "family": "sentiment_derived",
            "description": "Mean of model-scored sentiment for 'What did you learn' free-text responses.",
            "inputs": [{"kind": "freetext_column", "ref": "rtu_what_learned"}],
            "value_scale": "mean_in_neg1_pos1",
            "computed_values": _aggregate(items),
        })

    # ---- Behavioral-intent: share of "how will you apply" with concrete intent ----
    apply_cols = _find_columns_for_measure(measure_by_id.get("rtu_apply_learned"))
    if apply_cols:
        items = []
        for ft in freetext_items:
            if ft.column_id in apply_cols:
                resp = _resp_lookup(responses, ft.response_id)
                if resp is None:
                    continue
                val = 100.0 if _has_concrete_intent(ft.text) else 0.0
                items.append((_filter_key(resp, sheet_by_id), val))
        indicators.append({
            "id": "pct_concrete_intent",
            "display_name": "% with concrete behavioral intent",
            "family": "behavioral_intent",
            "description": "Share of 'How will you apply what you learned' responses that contain a concrete future-intent phrase.",
            "inputs": [{"kind": "freetext_column", "ref": "rtu_apply_learned"}],
            "value_scale": "pct_in_0_100",
            "computed_values": _aggregate(items),
        })

    # ---- Retention-derived: share of prior-event respondents who returned ----
    retention = _retention_indicator(responses, sheets)
    if retention:
        indicators.append(retention)

    return indicators


def _find_columns_for_measure(m: MeasureRecord | None) -> set[str]:
    if m is None:
        return set()
    return {a["column_id"] for a in m.aliases}


def _resp_lookup(responses: list[Response], rid: str) -> Response | None:
    # responses is small (~4k); a dict speedup helps but linear is fine for one call set
    if not hasattr(_resp_lookup, "_cache") or _resp_lookup._cache_id != id(responses):
        _resp_lookup._cache = {r.id: r for r in responses}
        _resp_lookup._cache_id = id(responses)
    return _resp_lookup._cache.get(rid)


def _retention_indicator(
    responses: list[Response],
    sheets: list[ingest.SheetData],
) -> dict[str, Any] | None:
    """Aggregate funnel: count per (event, school) and emit retention as
    pct of prior event total. No individual linking (linkage_key is null)."""
    rtu_sheets = [s for s in sheets if s.workbook_id == "rtu_2025_26"]
    if not rtu_sheets:
        return None
    # Order by event ordinal
    rtu_sheets.sort(key=lambda s: ingest.RTU_EVENT_META.get(s.display_name, ("", 99, ""))[1])

    # Counts keyed by (event_id, school_id)
    counts_by_school: dict[tuple[str, str], int] = defaultdict(int)
    for r in responses:
        # only count rows that are in an rtu_2025_26 sheet
        sheet = next((s for s in rtu_sheets if s.sheet_id == r.sheet_id), None)
        if sheet is None:
            continue
        meta = ingest.event_meta_for_sheet(sheet)
        if meta is None:
            continue
        counts_by_school[(meta[0], r.school)] += 1

    # Build computed_values: for each (event, school), retention = count / count_at_kickoff
    cv: list[dict[str, Any]] = []
    for (event_id, school_id), n in counts_by_school.items():
        # Use kickoff as the baseline for this school
        baseline = counts_by_school.get(("kickoff", school_id), 0)
        if baseline == 0:
            continue
        ratio = n / baseline
        cv.append({
            "filters": {
                "event_id": event_id,
                "school_id": school_id,
                "grade": None,
                "year": 2025,
            },
            "value": float(ratio),
            "n": int(n),
            "ci": None,
        })

    return {
        "id": "retention_vs_kickoff",
        "display_name": "Retention vs Kickoff (per school)",
        "family": "retention_derived",
        "description": "Aggregate ratio of respondents at each event to that school's Kickoff response count. Note: not an individual-level retention because no participant linking is available.",
        "inputs": [{"kind": "retention_edge", "ref": "kickoff -> later events"}],
        "value_scale": "ratio_in_0_1",
        "computed_values": cv,
    }
