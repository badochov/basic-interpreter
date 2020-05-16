from __future__ import annotations

from typing import TYPE_CHECKING, Union

from keywords import *
from lang_types.lang_number import LangNumber
from lang_types.lang_type import LangType
from nodes.node import Node
from token_types import *

if TYPE_CHECKING:
    from context import Context
    from tokens.lang_empty_token import EmptyToken
    from tokens.lang_string_token import StringToken


class UnaryOperationNode(Node):
    def __init__(self, operation_token: Union[EmptyToken, StringToken], node: Node):
        super().__init__(operation_token.pos_start, node.pos_end)
        self.operation_token = operation_token
        self.node = node

    def __repr__(self) -> str:
        return f"({self.operation_token} {self.node})"

    def visit(self, context: Context) -> LangType:
        result = self.node.visit(context)
        if self.operation_token.type == TT_MINUS:
            result = result.multiplied_by(
                LangNumber(-1, self.pos_start, self.pos_end, context)
            )
        elif self.operation_token.matches(TT_KEYWORD, KEYWORDS["NOT"]):
            result = result.notted()

        return result.set_pos(self.pos_start, self.pos_end)
