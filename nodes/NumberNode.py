from __future__ import annotations

from typing import TYPE_CHECKING

from interpreter.RuntimeResult import RuntimeResult
from nodes.Node import Node
from types_.Number import Number

if TYPE_CHECKING:
    from Context import Context
    from Token import Token


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
