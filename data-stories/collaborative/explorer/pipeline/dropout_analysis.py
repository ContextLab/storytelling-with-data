"""Dropout / retention analysis for the RTU 2025–26 event series.

ECOLOGICAL CAVEAT
-----------------
The source workbooks contain *no* persistent participant identifier. Every
response in the bundle has ``linkage_key=None`` so we cannot follow individual
students across the five events (Kickoff → Event 2 → ... → Event 5). Every
analysis in this module is therefore *aggregate* / *ecological*: counts and
means are computed at the (school, event) cell, and any retention curve is
computed as a ratio of *response counts*, not of *students*. Apparent dips
could be driven by (a) genuine drop-out, (b) caregivers vs. students differing
in whether they fill out the form, (c) different students attending different
events, or (d) sampling noise.

Regression specification
------------------------
For each cell (school s, event ordinal k) we have:

    retention_{s,k} = n_responses_{s,k} / n_responses_{s,1}    (event 1 = Kickoff)

We fit two ordinary-least-squares (OLS) models with hand-rolled numpy
``lstsq`` (no scipy / statsmodels — only built-in numpy). Bootstrap CIs
(1000 resamples over respondents per school) are used to derive 95% CIs for
each coefficient.

Per-school OLS (one per school, retention vs. event ordinal + prior cell
mean sentiment + prior cell % agree safety):

    retention_{s,k} = β0_s + β1_s · k
                            + β2_s · prior_event_mean_sentiment_{s,k-1}
                            + β3_s · prior_event_pct_agree_safety_{s,k-1}
                            + ε

Pooled OLS (across schools, school as a one-hot fixed effect):

    retention_{s,k} = β0 + β1 · k
                          + β2 · prior_event_mean_sentiment_{s,k-1}
                          + β3 · prior_event_pct_agree_safety_{s,k-1}
                          + Σ_j γ_j · 1[school = j]
                          + ε

The ``school heterogeneity`` summary in the front-end forest plot collapses
the γ coefficients into a single (min, max) range so the figure stays legible.

Cells with fewer than 5 responses are treated as null (their retention,
sentiment, and safety values are not used as either an outcome or a
predictor). Bootstrap iterations skip resampled designs that go rank-deficient.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterable

import numpy as np

from . import ingest
from .responses import Response, FreeTextStub


MIN_CELL_N = 5
N_BOOTSTRAP = 1000
RANDOM_SEED = 20251201


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _is_agree(value: Any) -> bool:
    """Mirror of effectiveness._is_agree but local to keep modules decoupled."""
    if value is None:
        return False
    s = str(value).lower()
    return any(tok in s for tok in ("agree", "often", "always", "usually", "yes", "true"))


def _safety_columns(measures, col_to_measure) -> set[str]:
    """Return the set of column ids that map to the rtu_felt_safe measure."""
    out: set[str] = set()
    for cid, mid in col_to_measure.items():
        if mid == "rtu_felt_safe":
            out.add(cid)
    return out


def _build_event_index(sheets: list[ingest.SheetData]) -> dict[str, tuple[str, int]]:
    """sheet_id -> (event_id, ordinal) for RTU sheets only."""
    out: dict[str, tuple[str, int]] = {}
    for s in sheets:
        if s.workbook_id != "rtu_2025_26":
            continue
        meta = ingest.event_meta_for_sheet(s)
        if meta is None:
            continue
        out[s.sheet_id] = (meta[0], meta[1])
    return out


def _ols(y: np.ndarray, X: np.ndarray) -> np.ndarray | None:
    """Plain numpy OLS, returns coefficient vector or None if rank-deficient."""
    if len(y) < X.shape[1]:
        return None
    try:
        coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    except np.linalg.LinAlgError:
        return None
    if not np.all(np.isfinite(coef)):
        return None
    return coef


def _bootstrap_ci(
    fit_fn,
    rng: np.random.Generator,
    n_obs: int,
    n_iter: int = N_BOOTSTRAP,
    n_coef: int = 4,
) -> list[list[float | None]]:
    """Wrap a fit function (returns coef vector or None) in a bootstrap.

    Returns a list of [lo, hi] 95% CIs (one per coefficient) — None for
    coefficients that never converged.
    """
    if n_obs < 2:
        return [[None, None] for _ in range(n_coef)]
    sims: list[list[float]] = [[] for _ in range(n_coef)]
    for _ in range(n_iter):
        idx = rng.integers(0, n_obs, size=n_obs)
        coef = fit_fn(idx)
        if coef is None or len(coef) < n_coef:
            continue
        for j in range(n_coef):
            sims[j].append(float(coef[j]))
    out: list[list[float | None]] = []
    for vec in sims:
        if len(vec) < 25:  # too few successful resamples
            out.append([None, None])
            continue
        lo, hi = np.percentile(vec, [2.5, 97.5])
        out.append([float(lo), float(hi)])
    return out


# ---------------------------------------------------------------------------
# Cell statistics
# ---------------------------------------------------------------------------


def _cell_stats(
    responses: list[Response],
    freetext_items: list[FreeTextStub],
    sheets: list[ingest.SheetData],
    col_to_measure: dict[str, str],
    sentiment_scores: dict[str, float],
) -> dict[tuple[str, int], dict[str, Any]]:
    """For each (school_id, event_ordinal) cell, compute:

      n: number of responses
      mean_sentiment: mean of sentiment scores across all freetext items
                     submitted in that cell (None if < MIN_CELL_N or no text)
      pct_agree_safety: % of responses (in cell) that agreed felt safe
                       (None if < MIN_CELL_N or no measured items)
      grade_counts: dict[grade] -> n
    """
    sheet_event = _build_event_index(sheets)
    safety_cols = _safety_columns(None, col_to_measure)

    cells: dict[tuple[str, int], dict[str, Any]] = defaultdict(lambda: {
        "n": 0,
        "sent_vals": [],
        "safety_hits": 0,
        "safety_total": 0,
        "grade_counts": defaultdict(int),
    })

    resp_by_id: dict[str, Response] = {r.id: r for r in responses}

    # Walk responses
    for r in responses:
        ev = sheet_event.get(r.sheet_id)
        if ev is None:
            continue
        ev_id, ev_ord = ev
        key = (r.school, ev_ord)
        cell = cells[key]
        cell["n"] += 1
        cell["grade_counts"][r.grade_level or "unknown"] += 1
        # safety
        for cid in safety_cols:
            v = r.values.get(cid)
            if v is None:
                continue
            cell["safety_total"] += 1
            if _is_agree(v):
                cell["safety_hits"] += 1

    # Walk freetext for sentiment
    for ft in freetext_items:
        r = resp_by_id.get(ft.response_id)
        if r is None:
            continue
        ev = sheet_event.get(r.sheet_id)
        if ev is None:
            continue
        ev_id, ev_ord = ev
        s = sentiment_scores.get(ft.id)
        if s is None:
            continue
        cells[(r.school, ev_ord)]["sent_vals"].append(float(s))

    # Finalize
    out: dict[tuple[str, int], dict[str, Any]] = {}
    for key, cell in cells.items():
        n = cell["n"]
        if n < MIN_CELL_N:
            mean_sent = None
            pct_safe = None
        else:
            mean_sent = (
                float(np.mean(cell["sent_vals"])) if cell["sent_vals"] else None
            )
            pct_safe = (
                100.0 * cell["safety_hits"] / cell["safety_total"]
                if cell["safety_total"] > 0
                else None
            )
        out[key] = {
            "n": int(n),
            "mean_sentiment": mean_sent,
            "pct_agree_safety": pct_safe,
            "grade_counts": dict(cell["grade_counts"]),
        }
    return out


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def compute(
    responses: list[Response],
    sheets: list[ingest.SheetData],
    freetext_items: list[FreeTextStub],
    sentiment_scores: dict[str, float],
    effectiveness_indicators: list[dict[str, Any]],
    col_to_measure: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Compute the dropout_analysis bundle dict.

    Parameters
    ----------
    responses, sheets, freetext_items, sentiment_scores: see build.py.
    effectiveness_indicators: included for parity with the build pipeline
        signature; not currently used (the safety / sentiment statistics are
        recomputed at cell level here so we control the n thresholds).
    col_to_measure: dict mapping column_id → measure_id; required.
    """
    if col_to_measure is None:
        col_to_measure = {}

    rng = np.random.default_rng(RANDOM_SEED)

    sheet_event = _build_event_index(sheets)
    rtu_sheet_ids = set(sheet_event.keys())

    # All schools that appear in any RTU response (sorted for stability)
    schools_seen: list[str] = sorted({
        r.school for r in responses if r.sheet_id in rtu_sheet_ids
    })
    grades_seen: list[str] = sorted({
        (r.grade_level or "unknown") for r in responses if r.sheet_id in rtu_sheet_ids
    })
    events_sorted = sorted(
        {(eid, eord) for (eid, eord) in sheet_event.values()},
        key=lambda x: x[1],
    )
    event_ids = [eid for eid, _ in events_sorted]
    event_ords = [eord for _, eord in events_sorted]

    cells = _cell_stats(
        responses=responses,
        freetext_items=freetext_items,
        sheets=sheets,
        col_to_measure=col_to_measure,
        sentiment_scores=sentiment_scores,
    )

    # ---- 1: per-school per-event count matrix ----
    school_event_counts = {
        s: {eid: 0 for eid in event_ids} for s in schools_seen
    }
    for (s, eord), cell in cells.items():
        if s in school_event_counts:
            eid = event_ids[event_ords.index(eord)]
            school_event_counts[s][eid] = cell["n"]

    # ---- 2: per-grade per-event count matrix ----
    grade_event_counts = {
        g: {eid: 0 for eid in event_ids} for g in grades_seen
    }
    for r in responses:
        ev = sheet_event.get(r.sheet_id)
        if ev is None:
            continue
        ev_id, _ = ev
        g = r.grade_level or "unknown"
        if g in grade_event_counts:
            grade_event_counts[g][ev_id] += 1

    # Total per event (across schools + unknown), for the headline numbers
    total_per_event: dict[str, int] = {eid: 0 for eid in event_ids}
    for s in schools_seen:
        for eid in event_ids:
            total_per_event[eid] += school_event_counts[s][eid]

    # ---- 3: retention curves (% of kickoff) ----
    school_retention: dict[str, dict[str, float | None]] = {}
    for s in schools_seen:
        kickoff_n = school_event_counts[s].get(event_ids[0], 0)
        curve: dict[str, float | None] = {}
        for eid in event_ids:
            n = school_event_counts[s][eid]
            if kickoff_n == 0:
                curve[eid] = None
            elif n == 0:
                curve[eid] = None  # render gap, not zero
            else:
                curve[eid] = 100.0 * n / kickoff_n
        school_retention[s] = curve

    grade_retention: dict[str, dict[str, float | None]] = {}
    for g in grades_seen:
        kickoff_n = grade_event_counts[g].get(event_ids[0], 0)
        curve = {}
        for eid in event_ids:
            n = grade_event_counts[g][eid]
            if kickoff_n == 0:
                curve[eid] = None
            elif n == 0:
                curve[eid] = None
            else:
                curve[eid] = 100.0 * n / kickoff_n
        grade_retention[g] = curve

    # ---- 4 + 5: regression rows ----
    # Build the cell-level design table:
    #   row per (school, event_ordinal>=2 with valid retention + valid lag)
    rows: list[dict[str, Any]] = []
    for s in schools_seen:
        kickoff_n = school_event_counts[s].get(event_ids[0], 0)
        if kickoff_n < MIN_CELL_N:
            continue
        for idx, eid in enumerate(event_ids):
            eord = event_ords[idx]
            if eord == 1:
                continue  # event 1 retention = 1 by construction
            cell = cells.get((s, eord))
            if cell is None or cell["n"] < MIN_CELL_N:
                continue
            ret = 100.0 * cell["n"] / kickoff_n
            # prior-event predictors (event ord-1)
            prior_cell = cells.get((s, eord - 1))
            if prior_cell is None or prior_cell["n"] < MIN_CELL_N:
                continue
            prior_sent = prior_cell["mean_sentiment"]
            prior_safe = prior_cell["pct_agree_safety"]
            if prior_sent is None or prior_safe is None:
                continue
            rows.append({
                "school": s,
                "event_ord": int(eord),
                "retention": float(ret),
                "prior_sent": float(prior_sent),
                "prior_safe": float(prior_safe),
                "n_cell": int(cell["n"]),
            })

    # 4. Per-school OLS
    per_school_regression: dict[str, dict[str, Any]] = {}
    for s in schools_seen:
        sub = [r for r in rows if r["school"] == s]
        if len(sub) < 4:
            continue
        y = np.array([r["retention"] for r in sub], dtype=float)
        X = np.column_stack([
            np.ones(len(sub)),
            np.array([r["event_ord"] for r in sub], dtype=float),
            np.array([r["prior_sent"] for r in sub], dtype=float),
            np.array([r["prior_safe"] for r in sub], dtype=float),
        ])
        coef = _ols(y, X)
        if coef is None:
            continue

        def fit_fn(idx, _y=y, _X=X):
            return _ols(_y[idx], _X[idx, :])

        cis = _bootstrap_ci(fit_fn, rng, n_obs=len(sub), n_coef=4)
        per_school_regression[s] = {
            "n_cells": len(sub),
            "coefficients": {
                "intercept": {"beta": float(coef[0]), "ci95": cis[0]},
                "event_ordinal": {"beta": float(coef[1]), "ci95": cis[1]},
                "prior_mean_sentiment": {"beta": float(coef[2]), "ci95": cis[2]},
                "prior_pct_agree_safety": {"beta": float(coef[3]), "ci95": cis[3]},
            },
        }

    # 5. Pooled OLS with school fixed effects (one-hot, drop reference school)
    pooled_regression: dict[str, Any] | None = None
    if len(rows) >= 6 and len(set(r["school"] for r in rows)) >= 2:
        pooled_schools = sorted({r["school"] for r in rows})
        ref_school = pooled_schools[0]
        oh_schools = pooled_schools[1:]
        oh_index = {s: j for j, s in enumerate(oh_schools)}

        n = len(rows)
        ncoef_main = 4
        X = np.zeros((n, ncoef_main + len(oh_schools)), dtype=float)
        y = np.zeros(n, dtype=float)
        for i, r in enumerate(rows):
            X[i, 0] = 1.0
            X[i, 1] = float(r["event_ord"])
            X[i, 2] = float(r["prior_sent"])
            X[i, 3] = float(r["prior_safe"])
            if r["school"] in oh_index:
                X[i, ncoef_main + oh_index[r["school"]]] = 1.0
            y[i] = float(r["retention"])

        coef = _ols(y, X)
        if coef is not None:
            n_coef_total = X.shape[1]

            def fit_fn(idx, _y=y, _X=X):
                return _ols(_y[idx], _X[idx, :])

            cis = _bootstrap_ci(
                fit_fn, rng, n_obs=n, n_coef=n_coef_total
            )
            fe_betas = [float(coef[ncoef_main + j]) for j in range(len(oh_schools))]
            fe_range = [
                min(fe_betas + [0.0]),
                max(fe_betas + [0.0]),
            ] if fe_betas else [0.0, 0.0]
            pooled_regression = {
                "n_cells": int(n),
                "reference_school": ref_school,
                "coefficients": {
                    "intercept": {"beta": float(coef[0]), "ci95": cis[0]},
                    "event_ordinal": {"beta": float(coef[1]), "ci95": cis[1]},
                    "prior_mean_sentiment": {"beta": float(coef[2]), "ci95": cis[2]},
                    "prior_pct_agree_safety": {"beta": float(coef[3]), "ci95": cis[3]},
                },
                "school_fixed_effects": {
                    s: {
                        "beta": float(coef[ncoef_main + j]),
                        "ci95": cis[ncoef_main + j],
                    }
                    for j, s in enumerate(oh_schools)
                },
                "school_heterogeneity_range": fe_range,
            }

    # ---- 6: top-20 drop-off cohorts ----
    drop_offs: list[dict[str, Any]] = []
    for s in schools_seen:
        for i in range(len(event_ids) - 1):
            eid_a = event_ids[i]
            eid_b = event_ids[i + 1]
            n_a = school_event_counts[s][eid_a]
            n_b = school_event_counts[s][eid_b]
            if n_a < MIN_CELL_N:
                continue
            drop_pct = 100.0 * (n_a - n_b) / n_a
            drop_offs.append({
                "school": s,
                "from_event_id": eid_a,
                "to_event_id": eid_b,
                "transition_label": f"{_event_label(eid_a)} → {_event_label(eid_b)}",
                "n_before": int(n_a),
                "n_after": int(n_b),
                "drop_pct": float(drop_pct),
            })
    drop_offs.sort(key=lambda d: abs(d["drop_pct"]), reverse=True)
    top_drop_offs = drop_offs[:20]

    return {
        "caveat": (
            "Ecological / aggregate analysis only — the source data carry no "
            "participant identifier, so individual students cannot be tracked "
            "across events. All retention curves and regression coefficients "
            "describe response counts at each (school, event) cell, not "
            "individual survival."
        ),
        "min_cell_n": MIN_CELL_N,
        "n_bootstrap": N_BOOTSTRAP,
        "events": [
            {"id": eid, "ordinal": eord, "display_name": _event_label(eid)}
            for eid, eord in events_sorted
        ],
        "schools": schools_seen,
        "grades": grades_seen,
        "totals_per_event": total_per_event,
        "school_event_counts": school_event_counts,
        "grade_event_counts": grade_event_counts,
        "school_retention": school_retention,
        "grade_retention": grade_retention,
        "per_school_regression": per_school_regression,
        "pooled_regression": pooled_regression,
        "top_drop_offs": top_drop_offs,
        "regression_rows": rows,  # exposed for diagnostics in the front-end
    }


def _event_label(eid: str) -> str:
    return {
        "kickoff": "Kickoff",
        "event_2": "Event 2",
        "event_3": "Event 3",
        "event_4": "Event 4",
        "event_5": "Event 5",
    }.get(eid, eid)
