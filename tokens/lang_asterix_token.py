from __future__ import annotations

from typing import cast, TYPE_CHECKING

from token_types import TT_ASTERIX
from tokens.lang_token import Token

if TYPE_CHECKING:
    from tokens.lang_string_token import StringToken
    from position import Position


class AsterixToken(Token[str]):
    def is_string_token(self) -> bool:
        return False

    def is_empty_token(self) -> bool:
        return False

    def is_number_token(self) -> bool:
        return False

    def is_asterix_token(self) -> bool:
        return False

    @staticmethod
    def as_asterix_token(token: Token) -> AsterixToken:
        return cast(AsterixToken, token)

    def __init__(self, pos_start: Position, pos_end: Position, name: str) -> None:
        super().__init__(TT_ASTERIX, pos_start, pos_end, name)

    @staticmethod
    def from_string_token(token: StringToken) -> AsterixToken:
        return AsterixToken(token.pos_start, token.pos_end, token.value)
