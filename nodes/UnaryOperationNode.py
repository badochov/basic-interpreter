from __future__ import annotations

from typing import TYPE_CHECKING

from interpreter.RuntimeResult import RuntimeResult
from nodes.Node import Node
from types_.Number import Number

if TYPE_CHECKING:
    from Context import Context
    from Token import Token
    from token_types import *


class UnaryOperationNode(Node):
    def __init__(self, operation_token: Token, node: Node):
        super().__init__(operation_token.pos_start, node.pos_end)
        self.operation_token = operation_token
        self.node = node

    def __repr__(self) -> str:
        return f"({self.operation_token} {self.node})"

    def visit(self, context: Context) -> RuntimeResult:
        res = RuntimeResult()
        result = res.register(self.node.visit(context))
        if res.error or result is None:
            return res

        error = None
        if self.operation_token.type == TT_MINUS:
            result, error = result.multiplied_by(
                Number(-1, self.pos_start, self.pos_end, context)
            )
        if error:
            return res.failure(error)
        if result is None:
            return res
        return res.success(result.set_pos(self.pos_start, self.pos_end))
