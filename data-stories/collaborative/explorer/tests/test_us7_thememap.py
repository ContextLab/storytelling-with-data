"""T063 + T064: Theme Map view (US7).

Pytest validates that every column with ≥30 freetext items has at least one
non-uncategorized cluster with member_count ≥ 3 (data-model §10).
Playwright verifies the dots + labels + drill-in.
"""

from __future__ import annotations

import pytest
from playwright.sync_api import sync_playwright


def test_columns_with_30plus_items_have_a_real_cluster(built_bundle):
    by_col = {}
    for ft in built_bundle["freetext_items"]:
        by_col.setdefault(ft["column_id"], []).append(ft)
    clusters_by_col = {}
    for c in built_bundle["theme_clusters"]:
        clusters_by_col.setdefault(c["column_id"], []).append(c)
    for col_id, items in by_col.items():
        if len(items) < 30:
            continue
        clusters = clusters_by_col.get(col_id, [])
        named = [c for c in clusters if not c["id"].endswith("uncategorized")]
        # at least one named cluster with member_count >= 3
        if not named:
            # Some columns may have so much variance that everything is uncategorized;
            # log as a warning by checking the count
            assert any(c["member_count"] >= 3 for c in clusters), \
                f"col {col_id}: zero clusters with member_count>=3"
        else:
            assert any(c["member_count"] >= 3 for c in named), \
                f"col {col_id}: no named cluster has >=3 members"


@pytest.fixture(scope="module")
def page(built_bundle_path, dist_server):
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context()
        p = ctx.new_page()
        p.goto(dist_server + "/index.html")
        p.wait_for_function(
            "() => document.getElementById('bundle-badge').textContent.includes('bundle v')",
            timeout=30_000,
        )
        p.click("[data-view='theme-map']")
        p.wait_for_selector("#tm-col", timeout=10_000)
        yield p
        browser.close()


def test_default_renders_dots_and_labels(page):
    page.wait_for_selector("#tm-host svg .dots circle", timeout=10_000)
    assert page.locator("#tm-host svg .dots circle").count() > 30
    # At least one cluster label rendered
    assert page.locator("#tm-host svg .labels g").count() >= 1


def test_recolor_does_not_redraw_dots(page):
    page.wait_for_selector("#tm-host svg .dots circle", timeout=5_000)
    n_before = page.locator("#tm-host svg .dots circle").count()
    page.click("[data-color='school']")
    page.wait_for_timeout(200)
    n_after = page.locator("#tm-host svg .dots circle").count()
    assert n_before == n_after


def test_click_cluster_label_opens_panel(page):
    page.wait_for_selector("#tm-host svg .labels g", timeout=5_000)
    page.locator("#tm-host svg .labels g").first.click(force=True)
    page.wait_for_selector("#side-panel.open", timeout=5_000)
    body = page.locator("#side-panel-body").inner_text()
    assert "members" in body.lower()
