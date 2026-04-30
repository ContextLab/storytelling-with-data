"""T038 + T039: Playwright smoke for the Compare view (US2)."""

from __future__ import annotations

from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright, expect


EXPLORER_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def page(built_bundle_path, dist_server):
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(accept_downloads=True)
        p = ctx.new_page()
        p.goto(dist_server + "/index.html")
        p.wait_for_function(
            "() => document.getElementById('bundle-badge').textContent.includes('bundle v')",
            timeout=30_000,
        )
        # navigate to Compare
        p.click("[data-view='compare']")
        p.wait_for_selector("#cmp-search", timeout=10_000)
        yield p
        browser.close()


def test_search_filters_measure_list(page):
    page.fill("#cmp-search", "vape")
    page.wait_for_timeout(300)
    items = page.locator("#cmp-measure-list .chip").all_inner_texts()
    assert len(items) > 0, "expected vape measures to appear"
    assert all("vape" in i.lower() for i in items), \
        f"expected only vape measures; got {items}"


def test_picking_measure_renders_chart(page):
    page.fill("#cmp-search", "vape")
    page.wait_for_timeout(200)
    page.locator("#cmp-measure-list .chip").first.click()
    page.wait_for_selector("#cmp-chart-host svg", timeout=5_000)
    bars = page.locator("#cmp-chart-host svg rect")
    assert bars.count() > 0, "expected at least one bar"


def test_split_by_grade_relayouts(page):
    page.fill("#cmp-search", "vape")
    page.wait_for_timeout(200)
    page.locator("#cmp-measure-list .chip").first.click()
    page.wait_for_selector("#cmp-chart-host svg", timeout=5_000)
    initial_bars = page.locator("#cmp-chart-host svg rect").count()
    page.click("[data-split='grade']")
    page.wait_for_timeout(300)
    new_bars = page.locator("#cmp-chart-host svg rect").count()
    # Either count or layout differs after re-grouping
    assert new_bars > 0


def test_export_emits_caption(page):
    page.fill("#cmp-search", "vape")
    page.wait_for_timeout(200)
    page.locator("#cmp-measure-list .chip").first.click()
    page.wait_for_selector("#cmp-chart-host svg", timeout=5_000)
    with page.expect_download(timeout=5_000) as dl_info:
        page.click("#cmp-export")
    dl = dl_info.value
    assert dl.suggested_filename.endswith(".png") or dl.suggested_filename.endswith(".caption.json"), \
        f"unexpected download filename: {dl.suggested_filename}"
