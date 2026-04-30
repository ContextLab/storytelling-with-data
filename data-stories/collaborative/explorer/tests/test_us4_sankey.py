"""T048 + T049: Playwright smoke for the Sankey view (US4)."""

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
        p.click("[data-view='sankey']")
        p.wait_for_selector("#sk-host", timeout=10_000)
        p.wait_for_selector("#sk-host svg", timeout=10_000)
        yield p
        browser.close()


def test_limitation_banner_visible(page):
    assert "aggregate response funnel" in page.locator(".banner").inner_text().lower()


def test_sankey_renders_with_paths_and_rects(page):
    assert page.locator("#sk-host svg path").count() > 0
    assert page.locator("#sk-host svg rect").count() > 0


def test_event_labels_present(page):
    text = page.evaluate("() => document.querySelector('#sk-host svg').textContent")
    for ev_label in ("Kickoff", "Event 2", "Event 3", "Event 4", "Event 5"):
        assert ev_label in text, f"missing event label {ev_label} in svg"


def test_stratify_by_grade_relayouts(page):
    page.click("[data-strat='grade']")
    page.wait_for_timeout(500)
    # After re-strat, paths still present
    assert page.locator("#sk-host svg path").count() > 0
