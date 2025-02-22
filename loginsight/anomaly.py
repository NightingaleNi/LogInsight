from __future__ import annotations

from statistics import mean, pstdev
from typing import Dict, List, Tuple


def detect_spikes(counts: Dict[str, int], window: int = 5, z: float = 2.5) -> List[Tuple[str, int, float]]:
    keys = sorted(counts.keys())
    vals = [counts[k] for k in keys]
    out = []
    for i, v in enumerate(vals):
        left = max(0, i - window)
        base = vals[left:i] + vals[i + 1 : min(len(vals), i + window + 1)]
        if len(base) < 2:
            continue
        m = mean(base)
        s = pstdev(base)
        if s == 0:
            continue
        score = (v - m) / s
        if score >= z:
            out.append((keys[i], v, round(score, 2)))
    return out

