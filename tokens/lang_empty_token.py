from __future__ import annotations

from typing import cast, Type

from position import Position
from tokens.lang_token import Token


class EmptyToken(Token[bool]):
    def is_asterix_token(self) -> bool:
        return False

    def is_number_token(self) -> bool:
        return False

    def is_string_token(self) -> bool:
        return False

    def is_empty_token(self) -> bool:
        return True

    @staticmethod
    def as_empty_token(token: Token) -> EmptyToken:
        return cast(EmptyToken, token)

    def __init__(self, type_: str, pos_start: Position, pos_end: Position) -> None:
        super().__init__(type_, pos_start, pos_end, False)
