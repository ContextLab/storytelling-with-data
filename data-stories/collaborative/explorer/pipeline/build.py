"""T021: Build entry point.

Reads the three source `.xlsx` files, runs the entire NLP + reconciliation
pipeline, validates the bundle against the JSON schema, writes it to
`dist/data.json` (+ gzip).
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

import numpy as np

from . import (
    cluster_namer,
    effectiveness,
    ingest,
    nlp,
    recipes,
    reconcile,
    responses as responses_mod,
    schools as schools_mod,
    serialize,
)


REPO_ROOT = Path(__file__).resolve().parents[4]
EXPLORER_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = EXPLORER_DIR.parent  # data-stories/collaborative/
SPECS_DIR = REPO_ROOT / "specs" / "004-collab-data-explorer"
SCHEMA_PATH = SPECS_DIR / "contracts" / "data-bundle.schema.json"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=EXPLORER_DIR / "dist" / "data.json")
    parser.add_argument("--only-recipes", action="store_true",
                        help="Recompute only the recipe-axis scores; reuse the rest of an existing bundle.")
    parser.add_argument("--rename-clusters", action="store_true",
                        help="Force re-naming all clusters (clears the name cache).")
    args = parser.parse_args(argv)

    if args.rename_clusters:
        cache = cluster_namer.CACHE_FILE
        if cache.exists():
            cache.unlink()
            print(f"[build] cleared cluster name cache at {cache}")

    t0 = time.perf_counter()

    # ---- Phase A: ingest ----
    print(f"[build] reading source workbooks from {DATA_DIR}…")
    sheets = ingest.read_workbooks(DATA_DIR)
    print(f"[build]   {len(sheets)} sheets loaded.")

    # ---- Phase B: reconcile + schools ----
    header_map = reconcile.load_header_map(EXPLORER_DIR / "pipeline" / "header_map.yaml")
    measures, col_to_measure = reconcile.build_measures(sheets, header_map)
    drift = reconcile.build_schema_drift(sheets)
    print(f"[build]   {len(measures)} measures from header_map ({sum(len(m.aliases) for m in measures)} aliases).")

    # ---- Phase C: responses + freetext stubs ----
    resp_records, ft_stubs = responses_mod.build_responses(sheets)
    print(f"[build]   {len(resp_records)} responses, {len(ft_stubs)} free-text items.")

    # ---- Phase D: NLP — sentiment + embedding ----
    texts = [ft.text for ft in ft_stubs]
    print(f"[build]   computing sentiment for {len(texts)} items…")
    sent_scores, sent_labels = nlp.score_sentiment(texts)
    print(f"[build]   computing embeddings for {len(texts)} items…")
    embeddings = nlp.embed(texts)

    # ---- Phase E: per-column theme map (UMAP + HDBSCAN + cluster naming) ----
    theme_maps: list[dict[str, Any]] = []
    theme_clusters: list[dict[str, Any]] = []
    coords_by_ft_id: dict[str, np.ndarray] = {}
    cluster_id_by_ft_id: dict[str, str] = {}

    by_col: dict[str, list[int]] = {}
    for i, ft in enumerate(ft_stubs):
        by_col.setdefault(ft.column_id, []).append(i)

    for col_id, idxs in by_col.items():
        sub = embeddings[idxs]
        coords = nlp.project_2d(sub.astype(np.float32))
        labels = nlp.cluster(coords)
        for j, i in enumerate(idxs):
            coords_by_ft_id[ft_stubs[i].id] = coords[j]
        # Cluster records
        clusters_this: list[str] = []
        for label_id in sorted(set(labels.tolist())):
            members_local = [j for j, lab in enumerate(labels) if lab == label_id]
            members_ft = [ft_stubs[idxs[j]] for j in members_local]
            if label_id == -1:
                cid = f"{col_id}.uncategorized"
                for ft in members_ft:
                    cluster_id_by_ft_id[ft.id] = cid
                if members_ft:
                    theme_clusters.append({
                        "id": cid,
                        "column_id": col_id,
                        "member_count": len(members_ft),
                        "centroid_2d": [float(np.mean([coords[j][0] for j in members_local])),
                                        float(np.mean([coords[j][1] for j in members_local]))],
                        "label": "Uncategorized",
                        "description": "Responses that did not fit a dense theme cluster.",
                        "representative_item_ids": [ft.id for ft in members_ft[:8]],
                        "naming_method": "tfidf_fallback",
                    })
                    clusters_this.append(cid)
                continue
            cid = f"{col_id}.cluster_{int(label_id):02d}"
            # Pick representatives: the 8 members nearest the cluster centroid in 2-D
            cluster_coords = coords[members_local]
            centroid = cluster_coords.mean(axis=0)
            dists = np.linalg.norm(cluster_coords - centroid, axis=1)
            order = np.argsort(dists)
            rep_ft = [members_ft[k] for k in order[:8]]
            label, desc, method = cluster_namer.name_cluster([ft.text for ft in rep_ft])
            for ft in members_ft:
                cluster_id_by_ft_id[ft.id] = cid
            theme_clusters.append({
                "id": cid,
                "column_id": col_id,
                "member_count": len(members_ft),
                "centroid_2d": [float(centroid[0]), float(centroid[1])],
                "label": label,
                "description": desc,
                "representative_item_ids": [ft.id for ft in rep_ft],
                "naming_method": method,
            })
            clusters_this.append(cid)
        theme_maps.append({
            "column_id": col_id,
            "umap_params": {
                "n_neighbors": 15,
                "min_dist": 0.05,
                "metric": "cosine",
                "random_state": nlp.SEED,
            },
            "cluster_ids": clusters_this,
            "axis_labels": None,
        })

    print(f"[build]   {len(theme_clusters)} theme clusters across {len(by_col)} free-text columns.")

    # ---- Phase F: recipes ----
    recipe_idx = [i for i, ft in enumerate(ft_stubs) if ft.is_recipe_candidate]
    recipe_axes_per_ft: dict[str, dict[str, float]] = {}
    if recipe_idx:
        recipe_emb = embeddings[recipe_idx]
        axes = recipes.compute_recipe_axes(recipe_emb.astype(np.float32), nlp.embed)
        for j, i in enumerate(recipe_idx):
            recipe_axes_per_ft[ft_stubs[i].id] = {
                "savory_sweet": float(axes["savory_sweet"][j]),
                "complexity": float(axes["complexity"][j]),
                "recipe_confidence": float(axes["recipe_confidence"][j]),
            }
        print(f"[build]   recipe axes computed for {len(recipe_idx)} items.")

    # ---- Phase G: assemble ----
    sentiment_score_by_ft_id = {ft.id: float(sent_scores[i]) for i, ft in enumerate(ft_stubs)}

    workbooks_table = []
    for wb_id, fname in ingest.WORKBOOK_FILES.items():
        wb_sheets = [s.sheet_id for s in sheets if s.workbook_id == wb_id]
        workbooks_table.append({
            "id": wb_id,
            "title": ingest.WORKBOOK_TITLES[wb_id],
            "source_path": str(DATA_DIR / fname),
            "kind": ingest.WORKBOOK_KIND[wb_id],
            "sheet_ids": wb_sheets,
        })

    sheets_table = [
        {
            "id": s.sheet_id,
            "workbook_id": s.workbook_id,
            "display_name": s.display_name,
            "period": s.period,
            "period_label": s.period_label,
            "source_row_count": s.source_row_count,
            "usable_row_count": s.usable_row_count,
            "column_ids": s.column_ids,
        }
        for s in sheets
    ]

    columns_table = []
    for s in sheets:
        for pos, (h, cid, t, mp, tv, rs, rr, ri) in enumerate(zip(
            s.headers, s.column_ids, s.inferred_types, s.missing_pct, s.top_values,
            s.rtu_session, s.rtu_role, s.rtu_instance,
        )):
            # Decorate the display header for repeated RTU questions
            display = _short_header(h)
            if rs is not None and rr is not None:
                role_short = "stu" if rr == "student" else "care"
                session_short = {"gerety": "ger", "community_building": "cb", "makeup": "mk"}.get(rs, rs[:3])
                display = f"[{session_short}/{role_short}] {display}"
            columns_table.append({
                "id": cid,
                "sheet_id": s.sheet_id,
                "position": pos,
                "display_header": display,
                "original_header": h,
                "inferred_type": t,
                "value_scale": None,
                "missing_pct": float(mp),
                "top_values": tv,
                "measure_id": col_to_measure.get(cid),
                "rtu_session": rs,
                "rtu_role": rr,
                "rtu_instance": ri,
            })

    measures_table = [
        {
            "id": m.id,
            "display_name": m.display_name,
            "description": m.description,
            "value_scale_canonical": m.value_scale_canonical,
            "scale_mixed": m.scale_mixed,
            "aliases": m.aliases,
            "coverage_years": m.coverage_years,
            "coverage_workbooks": m.coverage_workbooks,
        }
        for m in measures
    ]

    schools_table = schools_mod.school_records()

    events_table = []
    for sheet in sheets:
        if sheet.workbook_id != "rtu_2025_26":
            continue
        meta = ingest.event_meta_for_sheet(sheet)
        if meta is None:
            continue
        events_table.append({
            "id": meta[0],
            "ordinal": meta[1],
            "display_name": meta[2],
            "sheet_id": sheet.sheet_id,
        })
    events_table.sort(key=lambda e: e["ordinal"])

    responses_payload = []
    for r in resp_records:
        responses_payload.append({
            "id": r.id,
            "sheet_id": r.sheet_id,
            "school": r.school,
            "grade_level": r.grade_level,
            "submitted_at": r.submitted_at,
            "event_ordinal": r.event_ordinal,
            "linkage_key": r.linkage_key,
            "values": r.values,
            "freetext_item_ids": r.freetext_item_ids,
        })

    freetext_payload = []
    for i, ft in enumerate(ft_stubs):
        coords = coords_by_ft_id.get(ft.id)
        coord_pair = [float(coords[0]), float(coords[1])] if coords is not None else None
        freetext_payload.append({
            "id": ft.id,
            "response_id": ft.response_id,
            "column_id": ft.column_id,
            "text": ft.text,
            "text_length": ft.text_length,
            "sentiment_score": float(sent_scores[i]),
            "sentiment_label": sent_labels[i],
            "coords_2d": coord_pair,
            "cluster_id": cluster_id_by_ft_id.get(ft.id, "uncategorized"),
            "is_recipe_candidate": bool(ft.is_recipe_candidate),
            "recipe_axes": recipe_axes_per_ft.get(ft.id),
        })

    drift_payload = [
        {
            "workbook_id": d.workbook_id,
            "added": d.added,
            "removed": d.removed,
            "scale_changes": d.scale_changes,
        }
        for d in drift
    ]

    indicators = effectiveness.compute_indicators(
        responses=resp_records,
        freetext_items=ft_stubs,
        sheets=sheets,
        measures=measures,
        col_to_measure=col_to_measure,
        sentiment_scores=sentiment_score_by_ft_id,
    )

    model_versions = nlp.model_versions()
    model_versions["cluster_namer"] = cluster_namer.cluster_namer_id()

    bundle = serialize.assemble_bundle(
        workbooks=workbooks_table,
        sheets=sheets_table,
        columns=columns_table,
        measures=measures_table,
        schools=schools_table,
        events=events_table,
        responses=responses_payload,
        freetext_items=freetext_payload,
        theme_clusters=theme_clusters,
        theme_maps=theme_maps,
        effectiveness_indicators=indicators,
        schema_drift=drift_payload,
        recipe_axes=recipes.axis_definitions(),
        model_versions=model_versions,
    )

    # ---- Phase H: validate + write ----
    print(f"[build] validating against {SCHEMA_PATH}…")
    serialize.validate(bundle, SCHEMA_PATH)
    print(f"[build] writing {args.out} (+ .gz)…")
    serialize.write_bundle(bundle, args.out)

    elapsed = time.perf_counter() - t0
    print(f"[build] done in {elapsed:.1f}s")
    print(f"[build]   responses: {len(responses_payload)}")
    print(f"[build]   freetext_items: {len(freetext_payload)}")
    print(f"[build]   theme_clusters: {len(theme_clusters)}")
    print(f"[build]   indicators: {len(indicators)}")
    return 0


def _short_header(h: str, max_len: int = 38) -> str:
    if len(h) <= max_len:
        return h
    return h[: max_len - 1].rstrip() + "…"


if __name__ == "__main__":
    raise SystemExit(main())
