from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, Iterable, Optional
from .parse import guess_level

TS_FORMATS = [
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M:%S",
    "%Y/%m/%d %H:%M:%S",
]


def _iter_lines(path: str, limit: int = 0) -> Iterable[str]:
    n = 0
    with open(path, "r", errors="ignore") as f:
        for line in f:
            if limit and n >= limit:
                break
            n += 1
            yield line.rstrip("\n")


def _parse_ts_prefix(line: str) -> Optional[datetime]:
    head = line[:19]
    for fmt in TS_FORMATS:
        try:
            return datetime.strptime(head, fmt)
        except Exception:
            continue
    return None


def scan_logs(path: str, pattern: Optional[str] = None, limit: int = 0) -> Dict[str, object]:
    total = 0
    matched = 0
    levels = Counter()
    top_msgs = Counter()

    for line in _iter_lines(path, limit=limit):
        total += 1
        if pattern and pattern not in line:
            continue
        matched += 1
        levels[guess_level(line)] += 1
        top_msgs[line[-160:]] += 1

    return {
        "total_lines": total,
        "matched_lines": matched,
        "levels": dict(levels),
        "top_messages": dict(top_msgs.most_common(10)),
    }


def summarize_buckets(path: str, bucket: str = "hour", limit: int = 0) -> Dict[str, object]:
    buckets = defaultdict(int)
    total_ts = 0
    for line in _iter_lines(path, limit=limit):
        ts = _parse_ts_prefix(line)
        if not ts:
            continue
        total_ts += 1
        if bucket == "minute":
            key = ts.strftime("%Y-%m-%d %H:%M")
        elif bucket == "day":
            key = ts.strftime("%Y-%m-%d")
        else:
            key = ts.strftime("%Y-%m-%d %H:00")
        buckets[key] += 1

    ordered = dict(sorted(buckets.items()))
    return {"bucket": bucket, "sampled_lines": total_ts, "counts": ordered}
