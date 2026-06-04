from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP

from data_viz_mcp.store import ResourceStore


class _JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "tool": getattr(record, "tool", record.name),
            "resource_ids": getattr(record, "resource_ids", []),
            "outcome": getattr(record, "outcome", ""),
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload)


def _setup_logging() -> logging.Logger:
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(_JsonFormatter())
    root = logging.getLogger("data_viz_mcp")
    root.setLevel(logging.INFO)
    root.addHandler(handler)
    return root


logger = _setup_logging()
mcp = FastMCP("data-viz-mcp")
store = ResourceStore()


def _log(tool: str, resource_ids: list[str], outcome: str, msg: str = "") -> None:
    logger.info(
        msg or f"{tool} {outcome}",
        extra={"tool": tool, "resource_ids": resource_ids, "outcome": outcome},
    )


def log_ok(tool: str, resource_ids: list[str]) -> None:
    _log(tool, resource_ids, "success")


def log_err(tool: str, resource_ids: list[str], reason: str) -> None:
    _log(tool, resource_ids, "error", reason)


def err(operation: str, resource_id: str | None, reason: str) -> dict:
    return {"error": True, "operation": operation, "resource_id": resource_id, "reason": reason}


# --- MCP Resources ---

@mcp.resource("dataset://{id}")
def dataset_resource(id: str) -> str:
    result = store.get_dataset(id)
    if result is None:
        raise ValueError(f"Dataset '{id}' not found")
    ds, _ = result
    return ds.model_dump_json()


@mcp.resource("vizspec://{id}")
def vizspec_resource(id: str) -> str:
    spec = store.get_vizspec(id)
    if spec is None:
        raise ValueError(f"VizSpec '{id}' not found")
    return spec.model_dump_json()


@mcp.resource("plot://{id}")
def plot_resource(id: str) -> bytes:
    result = store.get_plot(id)
    if result is None:
        raise ValueError(f"Plot '{id}' not found")
    _, png_data, _ = result
    return png_data


# Tools are registered by importing tool modules in __main__.py.
