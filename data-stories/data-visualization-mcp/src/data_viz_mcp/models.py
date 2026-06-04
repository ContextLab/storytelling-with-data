from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class PlotType(str, Enum):
    LINE = "line"
    BAR = "bar"
    SCATTER = "scatter"
    HISTOGRAM = "histogram"


class ColumnInfo(BaseModel):
    name: str
    dtype: str


class Dataset(BaseModel):
    id: str
    name: str
    columns: list[ColumnInfo]
    row_count: int
    created_at: datetime


class VizSpec(BaseModel):
    id: str
    dataset_id: str
    plot_type: PlotType
    x_column: str
    y_column: str | None = None
    title: str | None = None
    x_label: str | None = None
    y_label: str | None = None
    color: str | None = None
    created_at: datetime
    updated_at: datetime


class Plot(BaseModel):
    id: str
    spec_id: str
    has_html: bool
    created_at: datetime
