from __future__ import annotations

import pandas as pd
import plotly.express as px

from data_viz_mcp.models import PlotType, VizSpec


def render_to_html(df: pd.DataFrame, spec: VizSpec) -> str:
    for col in ([spec.x_column] + ([spec.y_column] if spec.y_column else [])):
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in dataset data")

    color_seq = [spec.color] if spec.color else None
    kwargs: dict[str, object] = {
        "x": spec.x_column,
        "title": spec.title or "",
    }
    if color_seq:
        kwargs["color_discrete_sequence"] = color_seq

    if spec.plot_type == PlotType.LINE:
        fig = px.line(df, y=spec.y_column, **kwargs)  # type: ignore[arg-type]
    elif spec.plot_type == PlotType.BAR:
        fig = px.bar(df, y=spec.y_column, **kwargs)  # type: ignore[arg-type]
    elif spec.plot_type == PlotType.SCATTER:
        fig = px.scatter(df, y=spec.y_column, **kwargs)  # type: ignore[arg-type]
    elif spec.plot_type == PlotType.HISTOGRAM:
        fig = px.histogram(df, **kwargs)  # type: ignore[arg-type]
    else:
        raise ValueError(f"Unsupported plot type: {spec.plot_type}")

    if spec.x_label:
        fig.update_xaxes(title_text=spec.x_label)
    if spec.y_label:
        fig.update_yaxes(title_text=spec.y_label)

    return fig.to_html(full_html=True, include_plotlyjs=True)
