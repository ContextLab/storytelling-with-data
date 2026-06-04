from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

import pandas as pd

from data_viz_mcp.models import Dataset, Plot, VizSpec

if TYPE_CHECKING:
    pass


class ResourceStore:
    def __init__(self) -> None:
        self._datasets: dict[str, Dataset] = {}
        self._dataset_frames: dict[str, pd.DataFrame] = {}
        self._vizspecs: dict[str, VizSpec] = {}
        self._plots: dict[str, Plot] = {}
        self._plot_png: dict[str, bytes] = {}
        self._plot_html: dict[str, str] = {}

    def new_id(self, prefix: str) -> str:
        return f"{prefix}_{uuid.uuid4().hex}"

    # --- Dataset ---

    def add_dataset(self, dataset: Dataset, df: pd.DataFrame) -> None:
        self._datasets[dataset.id] = dataset
        self._dataset_frames[dataset.id] = df

    def get_dataset(self, id: str) -> tuple[Dataset, pd.DataFrame] | None:
        ds = self._datasets.get(id)
        if ds is None:
            return None
        return ds, self._dataset_frames[id]

    def list_datasets(self) -> list[Dataset]:
        return list(self._datasets.values())

    # --- VizSpec ---

    def add_vizspec(self, spec: VizSpec) -> None:
        self._vizspecs[spec.id] = spec

    def get_vizspec(self, id: str) -> VizSpec | None:
        return self._vizspecs.get(id)

    def update_vizspec(self, id: str, **fields: object) -> VizSpec | None:
        spec = self._vizspecs.get(id)
        if spec is None:
            return None
        updated = spec.model_copy(update=fields)
        self._vizspecs[id] = updated
        return updated

    def list_vizspecs(self) -> list[VizSpec]:
        return list(self._vizspecs.values())

    # --- Plot ---

    def add_plot(self, plot: Plot, png_data: bytes, html_data: str | None) -> None:
        self._plots[plot.id] = plot
        self._plot_png[plot.id] = png_data
        if html_data is not None:
            self._plot_html[plot.id] = html_data

    def get_plot(self, id: str) -> tuple[Plot, bytes, str | None] | None:
        plot = self._plots.get(id)
        if plot is None:
            return None
        return plot, self._plot_png[id], self._plot_html.get(id)

    def list_plots(self) -> list[Plot]:
        return list(self._plots.values())
