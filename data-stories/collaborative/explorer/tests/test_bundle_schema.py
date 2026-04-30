"""T028: validate the produced data.json against the JSON schema."""

from __future__ import annotations

import json

import jsonschema


def test_bundle_schema_valid(built_bundle, bundle_schema):
    jsonschema.validate(instance=built_bundle, schema=bundle_schema)


def test_bundle_has_expected_top_level_keys(built_bundle):
    expected = {
        "version", "built_at", "model_versions", "palette",
        "workbooks", "sheets", "columns", "measures", "schools",
        "events", "responses", "freetext_items", "theme_clusters",
        "theme_maps", "effectiveness_indicators", "schema_drift",
        "recipe_axes",
    }
    assert expected.issubset(built_bundle.keys())


def test_workbook_count_and_kinds(built_bundle):
    wbs = built_bundle["workbooks"]
    assert len(wbs) == 3
    ids = {w["id"] for w in wbs}
    assert ids == {"rtu_2025_26", "hs_core", "ms_core"}


def test_events_table_has_5_ordinals(built_bundle):
    events = built_bundle["events"]
    assert len(events) == 5
    assert sorted(e["ordinal"] for e in events) == [1, 2, 3, 4, 5]


def test_freetext_items_have_sentiment_and_cluster(built_bundle):
    """SC-006: 100% of free-text items are scored + clustered."""
    fts = built_bundle["freetext_items"]
    assert len(fts) > 0, "no free-text items in bundle"
    for ft in fts:
        assert ft["sentiment_label"] in {"negative", "neutral", "positive"}
        assert -1.0 <= ft["sentiment_score"] <= 1.0
        assert ft["cluster_id"], f"missing cluster_id on {ft['id']}"
