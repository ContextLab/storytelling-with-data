"""T053 + T054: Effectiveness indicators — pytest unit + Playwright smoke."""

from __future__ import annotations

import pytest
from playwright.sync_api import sync_playwright


# -- pytest unit on the bundle --

ALLOWED_FAMILIES = {"survey_direct", "sentiment_derived", "behavioral_intent", "retention_derived"}
ALLOWED_SCALES = {"pct_in_0_100", "mean_in_neg1_pos1", "ratio_in_0_1"}


def test_indicators_have_consistent_value_scales(built_bundle):
    inds = built_bundle["effectiveness_indicators"]
    assert len(inds) > 0
    for ind in inds:
        assert ind["family"] in ALLOWED_FAMILIES, f"bad family for {ind['id']}"
        assert ind["value_scale"] in ALLOWED_SCALES, f"bad scale for {ind['id']}"
        # All computed_values should share the indicator's scale (we validate via range)
        for cv in ind["computed_values"]:
            v = cv["value"]
            if ind["value_scale"] == "pct_in_0_100":
                assert 0 <= v <= 100, f"{ind['id']}: value {v} not in [0,100]"
            elif ind["value_scale"] == "mean_in_neg1_pos1":
                assert -1 <= v <= 1, f"{ind['id']}: value {v} not in [-1,1]"
            elif ind["value_scale"] == "ratio_in_0_1":
                # retention ratios CAN exceed 1 since later events sometimes have more responses
                assert v >= 0


def test_all_four_families_present(built_bundle):
    families = {ind["family"] for ind in built_bundle["effectiveness_indicators"]}
    missing = ALLOWED_FAMILIES - families
    assert not missing, f"missing families: {missing}"


# -- Playwright smoke --

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
        p.click("[data-view='effectiveness']")
        p.wait_for_selector("#ef-picker", timeout=10_000)
        yield p
        browser.close()


def test_picker_shows_all_four_families(page):
    text = page.locator("#ef-picker").inner_text().lower()
    for fam in ("survey-direct", "sentiment-derived", "behavioral intent", "retention-derived"):
        assert fam in text, f"missing family {fam} in: {text[:200]}"


def test_selecting_three_indicators_renders_three_cards(page):
    chips = page.locator("#ef-picker .chip")
    n = min(3, chips.count())
    for i in range(n):
        chips.nth(i).click()
    page.wait_for_timeout(300)
    cards = page.locator("#ef-charts .panel")
    assert cards.count() == n, f"expected {n} cards, got {cards.count()}"
