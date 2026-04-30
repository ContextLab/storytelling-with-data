"""T014: Canonical school resolution.

The RTU sheets list 10–11 schools spanning Vermont/NH region. The Core
Measures workbooks don't carry a school column (each workbook is one
HS or one MS), so the school is implied by the workbook.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class School:
    id: str
    display_name: str
    aliases: list[str]
    level: str  # 'middle' | 'high' | 'unknown'


# Canonical school table. Levels reflect typical Vermont K-12 mapping.
SCHOOLS: list[School] = [
    School(
        id="arlington_memorial",
        display_name="Arlington Memorial",
        aliases=["Arlington Memorial", "Arlington Memorial High School"],
        level="high",
    ),
    School(
        id="bba",
        display_name="BBA (Burr & Burton Academy)",
        aliases=["BBA", "Burr and Burton Academy", "Burr & Burton Academy"],
        level="high",
    ),
    School(
        id="bba_intl",
        display_name="BBA International Student",
        aliases=["BBA International Student"],
        level="high",
    ),
    School(
        id="dorset",
        display_name="Dorset School",
        aliases=["Dorset School"],
        level="middle",
    ),
    School(
        id="flood_brook",
        display_name="Flood Brook School",
        aliases=["Flood Brook School", "Flood Brook"],
        level="middle",
    ),
    School(
        id="homeschool",
        display_name="Homeschool",
        aliases=["Homeschool", "Home school", "Home School"],
        level="unknown",
    ),
    School(
        id="leland_gray",
        display_name="Leland & Gray",
        aliases=["Leland & Gray", "Leland and Gray"],
        level="high",
    ),
    School(
        id="long_trail",
        display_name="Long Trail School",
        aliases=["Long Trail School", "Long Trail"],
        level="high",
    ),
    School(
        id="mems",
        display_name="MEMS (Manchester Elementary/Middle)",
        aliases=["MEMS", "Manchester Elementary/Middle School"],
        level="middle",
    ),
    School(
        id="maple_street",
        display_name="Maple Street School",
        aliases=["Maple Street School"],
        level="middle",
    ),
    School(
        id="stratton_mountain",
        display_name="Stratton Mountain School",
        aliases=["Stratton Mountain School"],
        level="high",
    ),
    School(
        id="hs_aggregate",
        display_name="High School (aggregate)",
        aliases=["__hs_core__"],
        level="high",
    ),
    School(
        id="ms_aggregate",
        display_name="Middle School (aggregate)",
        aliases=["__ms_core__"],
        level="middle",
    ),
    School(
        id="unknown_school",
        display_name="Unknown",
        aliases=[],
        level="unknown",
    ),
]


def _build_alias_index() -> dict[str, str]:
    idx: dict[str, str] = {}
    for s in SCHOOLS:
        for a in s.aliases:
            idx[a.strip().lower()] = s.id
    return idx


_ALIAS_INDEX = _build_alias_index()


def resolve_school(raw: str | None, workbook_id: str | None = None) -> str:
    """Map a raw school string (or None) to a canonical school id.

    For Core Measures workbooks (which lack a school column), the
    workbook_id determines the aggregate school.
    """
    if raw is None or (isinstance(raw, str) and not raw.strip()):
        if workbook_id == "hs_core":
            return "hs_aggregate"
        if workbook_id == "ms_core":
            return "ms_aggregate"
        return "unknown_school"
    key = str(raw).strip().lower()
    return _ALIAS_INDEX.get(key, "unknown_school")


def school_records() -> list[dict]:
    """Return the school table as plain dicts for the bundle."""
    return [
        {
            "id": s.id,
            "display_name": s.display_name,
            "aliases": s.aliases,
            "level": s.level,
        }
        for s in SCHOOLS
    ]


def normalize_grade(raw) -> str | None:
    """Normalize grade-level strings to one of {'6'..'12', 'unknown', None}."""
    if raw is None:
        return None
    s = str(raw).strip().lower()
    if not s:
        return None
    # patterns like '6th', '7th', '12th', or just '7'
    digits = "".join(c for c in s if c.isdigit())
    if digits:
        try:
            n = int(digits)
            if 6 <= n <= 12:
                return str(n)
        except ValueError:
            pass
    return "unknown"
