"""T076: Verify the explorer is fully offline-capable.

Launches Chromium with network access disabled (route abort for any
non-local request) and exercises all 8 views. Asserts:
- bundle loads (from data.json.gz on the local server)
- no requests escape the loopback origin
- every view module loads and renders without errors
"""

from __future__ import annotations

import pytest
from playwright.sync_api import sync_playwright


VIEWS = [
    "tables", "compare", "timeline", "sankey",
    "effectiveness", "sentiment", "theme-map", "recipes",
]


def test_no_external_network_at_runtime(built_bundle_path, dist_server):
    external_attempts = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context()
        page = ctx.new_page()

        # Block ANY request whose URL doesn't start with our local server.
        def route_handler(route):
            url = route.request.url
            if url.startswith(dist_server) or url.startswith("data:"):
                route.continue_()
            else:
                external_attempts.append(url)
                route.abort()

        page.route("**/*", route_handler)

        page.goto(dist_server + "/index.html")
        page.wait_for_function(
            "() => document.getElementById('bundle-badge').textContent.includes('bundle v')",
            timeout=30_000,
        )
        # Visit every view
        page_errors = []
        page.on("pageerror", lambda err: page_errors.append(str(err)))

        for v in VIEWS:
            page.click(f"[data-view='{v}']")
            page.wait_for_timeout(800)

        browser.close()

    assert not external_attempts, f"unexpected external network attempts: {external_attempts}"
    assert not page_errors, f"page errors during offline run: {page_errors}"
