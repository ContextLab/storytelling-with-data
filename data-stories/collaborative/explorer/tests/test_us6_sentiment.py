"""T058 + T059: Playwright smoke for the Sentiment view (US6)."""

from __future__ import annotations

import pytest
from playwright.sync_api import sync_playwright


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
        p.click("[data-view='sentiment']")
        p.wait_for_selector("#sn-col", timeout=10_000)
        yield p
        browser.close()


def test_default_column_renders_chart(page):
    page.wait_for_selector("#sn-chart-host svg", timeout=5_000)
    bars = page.locator("#sn-chart-host svg rect")
    assert bars.count() > 0


def test_drill_into_bar_shows_three_responses(page):
    page.wait_for_selector("#sn-chart-host svg rect", timeout=5_000)
    page.locator("#sn-chart-host svg rect").first.click()
    panel_text = page.locator("#side-panel-body").inner_text()
    # Should mention at least the three labels
    for label in ("Most positive", "Median", "Most negative"):
        assert label in panel_text, f"missing '{label}' in drill panel"


def test_changing_group_redraws(page):
    page.click("[data-grp='school']")
    page.wait_for_timeout(300)
    bars = page.locator("#sn-chart-host svg rect")
    assert bars.count() > 0
