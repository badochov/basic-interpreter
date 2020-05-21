from __future__ import annotations

from typing import cast

from tokens.lang_token import Token


class StringToken(Token[str]):
    def is_asterix_token(self) -> bool:
        return False

    def is_string_token(self) -> bool:
        return True

    def is_empty_token(self) -> bool:
        return False

    def is_number_token(self) -> bool:
        return False

    @staticmethod
    def as_string_token(token: Token) -> StringToken:
        return cast(StringToken, token)
