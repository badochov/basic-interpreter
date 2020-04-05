from __future__ import annotations

from typing import TYPE_CHECKING

from interpreter.runtime_result import RuntimeResult
from nodes.node import Node
from lang_types.lang_number import LangNumber
from errors.rt_error import RTError

if TYPE_CHECKING:
    from context import Context
    from lang_token import Token


class NumberNode(Node):
    def __init__(self, token: Token):
        super().__init__(token.pos_start, token.pos_end)
        self.token = token

    def __repr__(self) -> str:
        return f"{self.token}"

    def visit(self, context: Context) -> RuntimeResult:
        if isinstance(self.token.value, float):
            return RuntimeResult().success(
                LangNumber(self.token.value, self.pos_start, self.pos_end, context)
            )
        return RuntimeResult().failure(
            RTError(self.pos_start, self.pos_end, "Expected float or int", context)
        )
