from __future__ import annotations

import glob
from typing import Iterable, List


def expand_inputs(path_or_glob: str) -> List[str]:
    matched = sorted(glob.glob(path_or_glob))
    return matched if matched else [path_or_glob]

