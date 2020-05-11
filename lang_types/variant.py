from __future__ import annotations

from dataclasses import dataclass
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from tokens.lang_token import Token


@dataclass
class Variant:
    name: str
    args: List[Token]
