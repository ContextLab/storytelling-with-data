from __future__ import annotations

import sys

# Tool and resource registrations — must import before mcp.run()
import data_viz_mcp.tools.datasets  # noqa: F401
import data_viz_mcp.tools.specs  # noqa: F401
import data_viz_mcp.tools.plots  # noqa: F401

from data_viz_mcp.server import logger, mcp


def main() -> None:
    logger.info(
        "starting",
        extra={
            "tool": "startup",
            "resource_ids": [],
            "outcome": f"python={sys.version.split()[0]} transport=stdio",
        },
    )
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
