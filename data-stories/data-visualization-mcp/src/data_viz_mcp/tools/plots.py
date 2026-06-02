from __future__ import annotations

import base64
import json
from datetime import datetime, timezone

from mcp.types import ImageContent, TextContent

from data_viz_mcp.models import Plot
from data_viz_mcp.server import err, log_err, log_ok, mcp, store
from data_viz_mcp.viz.interactive import render_to_html
from data_viz_mcp.viz.renderer import render_to_png


@mcp.tool()
def generate_plot(spec_id: str, include_html: bool = False) -> list:
    op = "generate_plot"

    spec = store.get_vizspec(spec_id)
    if spec is None:
        log_err(op, [spec_id], f"VizSpec '{spec_id}' not found")
        return [TextContent(type="text", text=json.dumps(err(op, spec_id, f"VizSpec '{spec_id}' not found")))]

    ds_result = store.get_dataset(spec.dataset_id)
    if ds_result is None:
        log_err(op, [spec_id, spec.dataset_id], f"Dataset '{spec.dataset_id}' not found")
        return [TextContent(type="text", text=json.dumps(err(op, spec.dataset_id, f"Dataset '{spec.dataset_id}' not found")))]

    _, df = ds_result

    try:
        png_data = render_to_png(df, spec)
    except ValueError as exc:
        log_err(op, [spec_id], str(exc))
        return [TextContent(type="text", text=json.dumps(err(op, spec_id, str(exc))))]
    except Exception as exc:
        log_err(op, [spec_id], f"Rendering failed: {exc}")
        return [TextContent(type="text", text=json.dumps(err(op, spec_id, f"Rendering failed: {exc}")))]

    html_data: str | None = None
    if include_html:
        try:
            html_data = render_to_html(df, spec)
        except Exception as exc:
            log_err(op, [spec_id], f"HTML rendering failed: {exc}")

    plot_id = store.new_id("pl")
    plot = Plot(id=plot_id, spec_id=spec_id, has_html=html_data is not None, created_at=datetime.now(timezone.utc))
    store.add_plot(plot, png_data, html_data)
    log_ok(op, [spec_id, plot_id])

    return [
        TextContent(
            type="text",
            text=json.dumps({"id": plot_id, "spec_id": spec_id, "created_at": plot.created_at.isoformat(), "has_html": plot.has_html}),
        ),
        ImageContent(type="image", data=base64.b64encode(png_data).decode(), mimeType="image/png"),
    ]


@mcp.tool()
def get_plot(id: str, format: str = "png") -> list:
    op = "get_plot"

    result = store.get_plot(id)
    if result is None:
        log_err(op, [id], f"Plot '{id}' not found")
        return [TextContent(type="text", text=json.dumps(err(op, id, f"Plot '{id}' not found")))]

    plot, png_data, html_data = result

    if format == "html":
        if html_data is None:
            log_err(op, [id], "No HTML stored for this plot")
            return [TextContent(type="text", text=json.dumps(err(
                op, id, f"Plot '{id}' was generated without HTML; re-generate with include_html=true"
            )))]
        log_ok(op, [id])
        return [TextContent(type="text", text=html_data)]

    log_ok(op, [id])
    return [ImageContent(type="image", data=base64.b64encode(png_data).decode(), mimeType="image/png")]


@mcp.tool()
def list_plots() -> str:
    op = "list_plots"
    plots = store.list_plots()
    log_ok(op, [p.id for p in plots])
    return json.dumps(
        [{"id": p.id, "spec_id": p.spec_id, "has_html": p.has_html, "created_at": p.created_at.isoformat()} for p in plots]
    )


@mcp.tool()
def list_plot_types() -> str:
    op = "list_plot_types"
    log_ok(op, [])
    return json.dumps(["line", "bar", "scatter", "histogram"])
