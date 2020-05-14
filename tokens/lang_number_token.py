from __future__ import annotations

from typing import cast

from tokens.lang_token import Token


class NumberToken(Token[float]):
    def is_number_token(self) -> bool:
        return True

    def is_string_token(self) -> bool:
        return False

    def is_empty_token(self) -> bool:
        return False

    @staticmethod
    def as_number_token(token: Token) -> NumberToken:
        return cast(NumberToken, token)
