from __future__ import annotations

from typing import TYPE_CHECKING

from interpreter.runtime_result import RuntimeResult
from nodes.node import Node
from types_.number import Number

if TYPE_CHECKING:
    from context import Context
    from token import Token


class NumberNode(Node):
    def __init__(self, token: Token):
        super().__init__(token.pos_start, token.pos_end)
        self.token = token

    def __repr__(self) -> str:
        return f"{self.token}"

    def visit(self, context: Context) -> RuntimeResult:
        return RuntimeResult().success(
            Number(self.token.value, self.pos_start, self.pos_end, context)
        )
