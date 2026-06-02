from __future__ import annotations

import io
import json
from datetime import datetime, timezone

import pandas as pd

from data_viz_mcp.models import ColumnInfo, Dataset
from data_viz_mcp.server import err, log_err, log_ok, mcp, store


@mcp.tool()
def upload_dataset(name: str, csv_data: str) -> str:
    op = "upload_dataset"
    if not name or not name.strip():
        log_err(op, [], "Dataset name must be non-empty")
        return json.dumps(err(op, None, "Dataset name must be non-empty"))
    try:
        df = pd.read_csv(io.StringIO(csv_data))
    except Exception as exc:
        log_err(op, [], str(exc))
        return json.dumps(err(op, None, f"CSV parsing failed: {exc}"))
    if df.empty and len(df.columns) == 0:
        log_err(op, [], "CSV must contain at least one column")
        return json.dumps(err(op, None, "CSV must contain at least one column"))

    ds_id = store.new_id("ds")
    columns = [ColumnInfo(name=col, dtype=str(df[col].dtype)) for col in df.columns]
    dataset = Dataset(
        id=ds_id,
        name=name.strip(),
        columns=columns,
        row_count=len(df),
        created_at=datetime.now(timezone.utc),
    )
    store.add_dataset(dataset, df)
    log_ok(op, [ds_id])
    return json.dumps(
        {"id": ds_id, "name": dataset.name, "columns": [c.model_dump() for c in columns], "row_count": dataset.row_count}
    )


@mcp.tool()
def list_datasets() -> str:
    op = "list_datasets"
    datasets = store.list_datasets()
    log_ok(op, [ds.id for ds in datasets])
    return json.dumps(
        [
            {"id": ds.id, "name": ds.name, "columns": [c.model_dump() for c in ds.columns], "row_count": ds.row_count}
            for ds in datasets
        ]
    )


@mcp.tool()
def get_dataset(id: str) -> str:
    op = "get_dataset"
    result = store.get_dataset(id)
    if result is None:
        log_err(op, [id], f"Dataset '{id}' not found")
        return json.dumps(err(op, id, f"Dataset '{id}' not found"))
    ds, df = result
    log_ok(op, [id])
    return json.dumps(
        {
            "id": ds.id,
            "name": ds.name,
            "columns": [c.model_dump() for c in ds.columns],
            "row_count": ds.row_count,
            "preview": df.head(5).to_csv(index=False),
        }
    )
