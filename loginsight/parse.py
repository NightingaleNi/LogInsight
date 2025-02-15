from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class LogLine:
    ts: Optional[datetime]
    level: str
    text: str


def guess_level(text: str) -> str:
    up = text.upper()
    if " ERROR" in up or up.startswith("ERROR"):
        return "error"
    if " WARN" in up or " WARNING" in up or up.startswith("WARN"):
        return "warn"
    if " INFO" in up or up.startswith("INFO"):
        return "info"
    return "other"

