"""Collaborative Explorer build pipeline.

T010: importing this module on the wrong Python version errors out fast.
"""

import sys

if sys.version_info[:2] != (3, 11):
    raise RuntimeError(
        f"Collaborative Explorer build requires Python 3.11 (found {sys.version_info.major}.{sys.version_info.minor}). "
        "Create a venv with python3.11 -m venv .venv and re-run."
    )
