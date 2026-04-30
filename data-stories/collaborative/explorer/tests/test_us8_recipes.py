"""T068 + T069: Recipes view (US8) — Playwright smoke + axis-calibration unit."""

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
        p.click("[data-view='recipes']")
        p.wait_for_selector("#rc-host", timeout=10_000)
        yield p
        browser.close()


def test_default_renders_recipe_dots(page):
    page.wait_for_selector("#rc-host svg circle", timeout=5_000)
    n = page.locator("#rc-host svg circle").count()
    assert n > 10, f"expected many recipe dots; got {n}"


def test_filter_by_school_reduces_count(page):
    page.wait_for_selector("#rc-host svg circle", timeout=5_000)
    n_all = page.locator("#rc-host svg circle").count()
    # Pick the second option (first non-"All")
    options = page.locator("#rc-school option").all_text_contents()
    if len(options) < 2:
        pytest.skip("only one school in recipe data")
    page.select_option("#rc-school", index=1)
    page.wait_for_timeout(200)
    n_filtered = page.locator("#rc-host svg circle").count()
    assert n_filtered <= n_all


def test_click_recipe_opens_side_panel(page):
    page.wait_for_selector("#rc-host svg circle", timeout=5_000)
    page.locator("#rc-host svg circle").first.click(force=True)
    page.wait_for_selector("#side-panel.open", timeout=5_000)
    body = page.locator("#side-panel-body").inner_text()
    assert "savory" in body.lower() or "complex" in body.lower()


def test_swap_axis_relayouts(page):
    page.wait_for_selector("#rc-host svg circle", timeout=5_000)
    page.select_option("#rc-x", "complexity")
    page.wait_for_timeout(200)
    assert page.locator("#rc-host svg circle").count() > 0


def test_filtered_out_count_visible(page):
    text = page.locator("#rc-footer").inner_text()
    assert "excluded" in text.lower() and "confidence" in text.lower()
