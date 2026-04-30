"""T043 + T044: Playwright smoke for the Timeline view (US3)."""

from __future__ import annotations

from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright, expect


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
        p.click("[data-view='timeline']")
        p.wait_for_selector("#tl-measures", timeout=10_000)
        yield p
        browser.close()


def test_picks_three_harm_measures_overlay(page):
    # Click first three harm-* measure chips
    chips = page.locator("#tl-measures .chip")
    count = chips.count()
    assert count > 0, "no measures listed"
    picked = 0
    for i in range(count):
        text = chips.nth(i).inner_text()
        if "harm" in text.lower() and picked < 3:
            chips.nth(i).click()
            picked += 1
            page.wait_for_timeout(120)
    assert picked >= 1, "no harm measures available"
    page.wait_for_selector("#tl-chart-host svg", timeout=5_000)
    paths = page.locator("#tl-chart-host svg path")
    assert paths.count() >= picked, "expected at least one line per measure"


def test_small_multiples_toggle(page):
    page.click("[data-layout='small-multiples']")
    page.wait_for_timeout(300)
    # In small-multiples mode each measure gets its own SVG
    svgs = page.locator("#tl-chart-host svg")
    assert svgs.count() >= 1


def test_event_axis_for_rtu_measure(page):
    page.click("[data-axis='event']")
    page.wait_for_timeout(300)
    # The picker should now show RTU measures
    chips = page.locator("#tl-measures .chip")
    assert chips.count() > 0, "no RTU measures listed for event axis"
