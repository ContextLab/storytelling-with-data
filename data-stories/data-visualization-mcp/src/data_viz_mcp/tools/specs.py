from __future__ import annotations

import json
from datetime import datetime, timezone

from data_viz_mcp.models import PlotType, VizSpec
from data_viz_mcp.server import err, log_err, log_ok, mcp, store


def _spec_to_dict(spec: VizSpec) -> dict:
    return {
        "id": spec.id,
        "dataset_id": spec.dataset_id,
        "plot_type": spec.plot_type.value,
        "x_column": spec.x_column,
        "y_column": spec.y_column,
        "title": spec.title,
        "x_label": spec.x_label,
        "y_label": spec.y_label,
        "color": spec.color,
        "created_at": spec.created_at.isoformat(),
        "updated_at": spec.updated_at.isoformat(),
    }


@mcp.tool()
def create_vizspec(
    dataset_id: str,
    plot_type: str,
    x_column: str,
    y_column: str | None = None,
    title: str | None = None,
    x_label: str | None = None,
    y_label: str | None = None,
    color: str | None = None,
) -> str:
    op = "create_vizspec"

    ds_result = store.get_dataset(dataset_id)
    if ds_result is None:
        log_err(op, [dataset_id], f"Dataset '{dataset_id}' not found")
        return json.dumps(err(op, dataset_id, f"Dataset '{dataset_id}' not found"))

    try:
        pt = PlotType(plot_type)
    except ValueError:
        supported = ", ".join(v.value for v in PlotType)
        log_err(op, [dataset_id], f"Unsupported plot type '{plot_type}'")
        return json.dumps(err(op, dataset_id, f"Unsupported plot type '{plot_type}'. Supported: {supported}"))

    ds, _ = ds_result
    col_names = {c.name for c in ds.columns}

    if x_column not in col_names:
        log_err(op, [dataset_id], f"Column '{x_column}' not found")
        return json.dumps(err(op, dataset_id, f"Column '{x_column}' not found in dataset '{dataset_id}'"))

    if pt != PlotType.HISTOGRAM:
        if y_column is None:
            log_err(op, [dataset_id], f"y_column required for {plot_type}")
            return json.dumps(err(op, dataset_id, f"y_column is required for plot type '{plot_type}'"))
        if y_column not in col_names:
            log_err(op, [dataset_id], f"Column '{y_column}' not found")
            return json.dumps(err(op, dataset_id, f"Column '{y_column}' not found in dataset '{dataset_id}'"))

    now = datetime.now(timezone.utc)
    spec_id = store.new_id("vs")
    spec = VizSpec(
        id=spec_id,
        dataset_id=dataset_id,
        plot_type=pt,
        x_column=x_column,
        y_column=y_column,
        title=title,
        x_label=x_label,
        y_label=y_label,
        color=color,
        created_at=now,
        updated_at=now,
    )
    store.add_vizspec(spec)
    log_ok(op, [dataset_id, spec_id])
    return json.dumps(_spec_to_dict(spec))


@mcp.tool()
def get_vizspec(id: str) -> str:
    op = "get_vizspec"
    spec = store.get_vizspec(id)
    if spec is None:
        log_err(op, [id], f"VizSpec '{id}' not found")
        return json.dumps(err(op, id, f"VizSpec '{id}' not found"))
    log_ok(op, [id])
    return json.dumps(_spec_to_dict(spec))


@mcp.tool()
def update_vizspec(
    id: str,
    plot_type: str | None = None,
    x_column: str | None = None,
    y_column: str | None = None,
    title: str | None = None,
    x_label: str | None = None,
    y_label: str | None = None,
    color: str | None = None,
) -> str:
    op = "update_vizspec"

    spec = store.get_vizspec(id)
    if spec is None:
        log_err(op, [id], f"VizSpec '{id}' not found")
        return json.dumps(err(op, id, f"VizSpec '{id}' not found"))

    fields: dict[str, object] = {}

    if plot_type is not None:
        try:
            fields["plot_type"] = PlotType(plot_type)
        except ValueError:
            supported = ", ".join(v.value for v in PlotType)
            return json.dumps(err(op, id, f"Unsupported plot type '{plot_type}'. Supported: {supported}"))

    ds_result = store.get_dataset(spec.dataset_id)
    if ds_result is None:
        return json.dumps(err(op, id, f"Referenced dataset '{spec.dataset_id}' no longer available"))
    ds, _ = ds_result
    col_names = {c.name for c in ds.columns}

    if x_column is not None:
        if x_column not in col_names:
            return json.dumps(err(op, id, f"Column '{x_column}' not found in dataset '{spec.dataset_id}'"))
        fields["x_column"] = x_column

    if y_column is not None:
        if y_column not in col_names:
            return json.dumps(err(op, id, f"Column '{y_column}' not found in dataset '{spec.dataset_id}'"))
        fields["y_column"] = y_column

    for key, val in [("title", title), ("x_label", x_label), ("y_label", y_label), ("color", color)]:
        if val is not None:
            fields[key] = val

    if not fields:
        return json.dumps(err(op, id, "At least one field must be provided for update"))

    fields["updated_at"] = datetime.now(timezone.utc)
    updated = store.update_vizspec(id, **fields)
    log_ok(op, [id])
    return json.dumps(_spec_to_dict(updated))  # type: ignore[arg-type]


@mcp.tool()
def list_vizspecs() -> str:
    op = "list_vizspecs"
    specs = store.list_vizspecs()
    log_ok(op, [s.id for s in specs])
    return json.dumps(
        [{"id": s.id, "dataset_id": s.dataset_id, "plot_type": s.plot_type.value, "created_at": s.created_at.isoformat()}
         for s in specs]
    )
