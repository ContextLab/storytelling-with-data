from __future__ import annotations

import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from data_viz_mcp.models import PlotType, VizSpec


def render_to_png(df: pd.DataFrame, spec: VizSpec) -> bytes:
    for col in ([spec.x_column] + ([spec.y_column] if spec.y_column else [])):
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in dataset data")

    fig, ax = plt.subplots()
    x = df[spec.x_column]
    color = spec.color or None

    if spec.plot_type == PlotType.LINE:
        ax.plot(x, df[spec.y_column], color=color)  # type: ignore[index]
    elif spec.plot_type == PlotType.BAR:
        ax.bar(x, df[spec.y_column], color=color)  # type: ignore[index]
    elif spec.plot_type == PlotType.SCATTER:
        ax.scatter(x, df[spec.y_column], color=color)  # type: ignore[index]
    elif spec.plot_type == PlotType.HISTOGRAM:
        ax.hist(x, color=color)

    if spec.title:
        ax.set_title(spec.title)
    ax.set_xlabel(spec.x_label or spec.x_column)
    if spec.y_column:
        ax.set_ylabel(spec.y_label or spec.y_column)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf.read()
