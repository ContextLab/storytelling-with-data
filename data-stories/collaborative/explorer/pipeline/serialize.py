"""T020: Assemble the final bundle dict and write data.json + data.json.gz.

Validates against contracts/data-bundle.schema.json before writing.
"""

from __future__ import annotations

import gzip
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import jsonschema


BUNDLE_SCHEMA_VERSION = "1.0.0"


# Dartmouth-green palette (research R-13)
PALETTE = {
    "categorical": [
        "#00351e", "#004f2d", "#00693e",
        "#3e8c66", "#74af8e", "#a6cdb9",
    ],
    "sequential": [
        "#f3f7f4", "#cfe1d6", "#74af8e", "#00693e", "#00351e",
    ],
    "diverging": [
        "#a86b6b", "#d6b8b8", "#f3f3f3", "#74af8e", "#00351e",
    ],
}


def assemble_bundle(
    *,
    workbooks: list[dict[str, Any]],
    sheets: list[dict[str, Any]],
    columns: list[dict[str, Any]],
    measures: list[dict[str, Any]],
    schools: list[dict[str, Any]],
    events: list[dict[str, Any]],
    responses: list[dict[str, Any]],
    freetext_items: list[dict[str, Any]],
    theme_clusters: list[dict[str, Any]],
    theme_maps: list[dict[str, Any]],
    effectiveness_indicators: list[dict[str, Any]],
    schema_drift: list[dict[str, Any]],
    recipe_axes: dict[str, Any],
    model_versions: dict[str, str],
    dropout_analysis: dict[str, Any] | None = None,
    curated_themes: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "version": BUNDLE_SCHEMA_VERSION,
        "built_at": datetime.now(timezone.utc).isoformat(),
        "model_versions": model_versions,
        "palette": PALETTE,
        "workbooks": workbooks,
        "sheets": sheets,
        "columns": columns,
        "measures": measures,
        "schools": schools,
        "events": events,
        "responses": responses,
        "freetext_items": freetext_items,
        "theme_clusters": theme_clusters,
        "theme_maps": theme_maps,
        "effectiveness_indicators": effectiveness_indicators,
        "schema_drift": schema_drift,
        "recipe_axes": recipe_axes,
        "dropout_analysis": dropout_analysis or {},
        "curated_themes": curated_themes or [],
    }


def validate(bundle: dict[str, Any], schema_path: Path) -> None:
    with open(schema_path, "r") as fh:
        schema = json.load(fh)
    jsonschema.validate(instance=bundle, schema=schema)


def write_bundle(bundle: dict[str, Any], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(bundle, separators=(",", ":"), default=_default)
    with open(out_path, "w") as fh:
        fh.write(text)
    gz_path = out_path.with_suffix(out_path.suffix + ".gz")
    with gzip.open(gz_path, "wb", compresslevel=9) as fh:
        fh.write(text.encode("utf-8"))


def _default(o):
    # Numpy scalars / arrays
    try:
        import numpy as np
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
    except ImportError:
        pass
    if hasattr(o, "isoformat"):
        return o.isoformat()
    raise TypeError(f"not JSON serializable: {type(o).__name__}")
