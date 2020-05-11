from __future__ import annotations

from position import Position
from tokens.lang_token import Token


class EmptyToken(Token[None]):
    def __init__(self, type_: str, pos_start: Position, pos_end: Position) -> None:
        super().__init__(type_, pos_start, pos_end, None)
