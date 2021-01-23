from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar


@dataclass
class C:
    mu: ClassVar[float] = 2.0
    x: list[str]
