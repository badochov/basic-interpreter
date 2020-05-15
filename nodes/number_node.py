from __future__ import annotations

from typing import TYPE_CHECKING


from lang_types.lang_number import LangNumber
from nodes.node import Node

if TYPE_CHECKING:
    from context import Context
    from tokens.lang_number_token import NumberToken


class NumberNode(Node):
    def __init__(self, token: NumberToken):
        super().__init__(token.pos_start, token.pos_end)
        self.token = token

    def __repr__(self) -> str:
        return f"{self.token}"

    def visit(self, context: Context) -> LangNumber:
        return LangNumber(self.token.value, self.pos_start, self.pos_end, context)
