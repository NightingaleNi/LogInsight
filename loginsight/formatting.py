from __future__ import annotations

def kv_lines(d: dict) -> str:
    return "\n".join(f"{k}: {v}" for k, v in d.items())

