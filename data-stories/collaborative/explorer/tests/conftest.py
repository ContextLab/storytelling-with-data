"""T009: Shared pytest fixtures for the Collaborative Explorer test suite.

Tests use the real source `.xlsx` files and the real `data.json` produced
by `build.py` — no mocks (per repo CLAUDE.md and project constitution).
"""

from __future__ import annotations

import http.server
import json
import os
import socket
import socketserver
import subprocess
import sys
import threading
from contextlib import closing
from pathlib import Path

import pytest

EXPLORER_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = EXPLORER_DIR.parent  # data-stories/collaborative/
BUILD_DIR = EXPLORER_DIR / "pipeline"
DIST_DIR = EXPLORER_DIR / "dist"


@pytest.fixture(scope="session")
def explorer_dir() -> Path:
    return EXPLORER_DIR


@pytest.fixture(scope="session")
def data_dir() -> Path:
    """The folder holding the three source .xlsx files."""
    return DATA_DIR


@pytest.fixture(scope="session")
def source_xlsx_paths(data_dir: Path) -> dict[str, Path]:
    paths = {
        "rtu_2025_26": data_dir / "2025-2026 All RTU Data .xlsx",
        "hs_core": data_dir / "High School Core Measures 2022-2025.xlsx",
        "ms_core": data_dir / "Middle School Core Measures Data 2022 - 2025.xlsx",
    }
    for k, p in paths.items():
        assert p.exists(), f"missing source workbook for {k}: {p}"
    return paths


@pytest.fixture(scope="session")
def built_bundle_path(explorer_dir: Path) -> Path:
    """Run `build.py` once per session and return the path to the bundle.

    If `EXPLORER_SKIP_BUILD=1` is set and a bundle already exists, reuse it
    (useful while iterating on UI tests). Otherwise always rebuild.
    """
    out_path = DIST_DIR / "data.json"
    skip = os.environ.get("EXPLORER_SKIP_BUILD") == "1"
    if skip and out_path.exists():
        return out_path

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, "-m", "pipeline.build", "--out", str(out_path)]
    subprocess.run(cmd, check=True, cwd=str(explorer_dir))
    assert out_path.exists(), "build.py did not produce data.json"
    return out_path


@pytest.fixture(scope="session")
def built_bundle(built_bundle_path: Path) -> dict:
    with open(built_bundle_path, "r") as fh:
        return json.load(fh)


@pytest.fixture(scope="session")
def dist_server(built_bundle_path):
    """Local HTTP server rooted at dist/ — required because Chromium blocks
    ES-module imports from file:// URLs.

    Yields the base URL (e.g. http://127.0.0.1:54321).
    """
    dist = DIST_DIR
    handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(*a, directory=str(dist), **kw)
    # Find a free port
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    server = socketserver.TCPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{port}"
    try:
        yield base
    finally:
        server.shutdown()
        server.server_close()


@pytest.fixture(scope="session")
def bundle_schema() -> dict:
    schema_path = (
        EXPLORER_DIR.parent.parent.parent
        / "specs"
        / "004-collab-data-explorer"
        / "contracts"
        / "data-bundle.schema.json"
    )
    with open(schema_path, "r") as fh:
        return json.load(fh)
