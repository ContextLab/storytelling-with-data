"""Unit tests for matplotlib and Plotly renderers."""
from datetime import datetime, timezone

import pandas as pd
import pytest

from data_viz_mcp.models import PlotType, VizSpec
from data_viz_mcp.viz.renderer import render_to_png
from data_viz_mcp.viz.interactive import render_to_html


def _spec(plot_type: PlotType, y_column: str | None = "y") -> VizSpec:
    now = datetime.now(timezone.utc)
    return VizSpec(
        id="vs_test",
        dataset_id="ds_test",
        plot_type=plot_type,
        x_column="x",
        y_column=y_column,
        created_at=now,
        updated_at=now,
    )


DF = pd.DataFrame({"x": [1, 2, 3], "y": [10, 20, 30]})


@pytest.mark.parametrize("plot_type", [PlotType.LINE, PlotType.BAR, PlotType.SCATTER])
def test_render_to_png_xy_types(plot_type):
    png = render_to_png(DF, _spec(plot_type))
    assert isinstance(png, bytes)
    assert len(png) > 0
    assert png[:4] == b"\x89PNG"


def test_render_to_png_histogram():
    png = render_to_png(DF, _spec(PlotType.HISTOGRAM, y_column=None))
    assert isinstance(png, bytes)
    assert png[:4] == b"\x89PNG"


def test_render_to_png_missing_column():
    spec = _spec(PlotType.LINE)
    bad_df = pd.DataFrame({"a": [1, 2]})
    with pytest.raises(ValueError, match="not found"):
        render_to_png(bad_df, spec)


@pytest.mark.parametrize("plot_type", [PlotType.LINE, PlotType.BAR, PlotType.SCATTER])
def test_render_to_html_xy_types(plot_type):
    html = render_to_html(DF, _spec(plot_type))
    assert isinstance(html, str)
    assert "<html" in html.lower()
    assert "plotly" in html.lower()


def test_render_to_html_histogram():
    html = render_to_html(DF, _spec(PlotType.HISTOGRAM, y_column=None))
    assert "<html" in html.lower()
    assert "plotly" in html.lower()


def test_render_to_html_self_contained():
    html = render_to_html(DF, _spec(PlotType.LINE))
    # Must not load Plotly from an external script tag (self-contained requirement)
    assert '<script src="https://cdn.plot.ly' not in html
    assert '<script src="http' not in html
