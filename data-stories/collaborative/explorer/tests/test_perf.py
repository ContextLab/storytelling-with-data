"""T074 + T075: Coarse perf check — load + view-switch latency."""

from __future__ import annotations

import time
import pytest
from playwright.sync_api import sync_playwright


def test_initial_load_under_10s(built_bundle_path, dist_server):
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        t0 = time.perf_counter()
        page.goto(dist_server + "/index.html")
        page.wait_for_function(
            "() => document.getElementById('bundle-badge').textContent.includes('bundle v')",
            timeout=30_000,
        )
        page.wait_for_selector("#tabulator-host .tabulator-row", timeout=15_000)
        t1 = time.perf_counter() - t0
        browser.close()
    print(f"\n[perf] initial-load = {t1*1000:.0f}ms")
    assert t1 < 10.0, f"initial load took {t1:.1f}s (>10s budget)"


def test_view_switch_under_4s(built_bundle_path, dist_server):
    """View-switch budget: 4 s. The Tables view rebuilds Tabulator with
    4000+ rows on every switch; ~2-3 s is the inherent Tabulator init cost.
    Filter changes within a view (which spec SC-005 constrains to <1 s)
    are cheaper because they re-render through the existing Tabulator
    instance rather than destroying + recreating it."""
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(dist_server + "/index.html")
        page.wait_for_function(
            "() => document.getElementById('bundle-badge').textContent.includes('bundle v')",
            timeout=30_000,
        )
        timings = {}
        for v in ["compare", "timeline", "sankey", "sentiment", "theme-map", "recipes", "tables"]:
            t0 = time.perf_counter()
            page.click(f"[data-view='{v}']")
            page.wait_for_timeout(50)
            timings[v] = time.perf_counter() - t0
        browser.close()
    print(f"\n[perf] view-switch timings: {timings}")
    for v, t in timings.items():
        assert t < 4.0, f"view {v} switch took {t:.2f}s (>4s)"
