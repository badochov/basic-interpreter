from __future__ import annotations

from typing import TYPE_CHECKING

from errors.rt_error import RTError
from interpreter.runtime_result import RuntimeResult
from nodes.node import Node
from token_types import *

if TYPE_CHECKING:
    from context import Context
    from token import Token


class BinaryOperationNode(Node):
    def __init__(self, left_node: Node, operation_token: Token, right_node: Node):
        super().__init__(left_node.pos_start, right_node.pos_end)
        self.left_node = left_node
        self.operation_token = operation_token
        self.right_node = right_node

    def __repr__(self) -> str:
        return f"({self.left_node}, {self.operation_token}, {self.right_node})"

    def visit(self, context: Context) -> RuntimeResult:
        res = RuntimeResult()
        left = res.register(self.left_node.visit(context))
        if res.error or left is None:
            return res
        right = res.register(self.right_node.visit(context))
        if res.error or right is None:
            return res

        result = None

        if self.operation_token.type == TT_PLUS:
            result, error = left.added_to(right)
        elif self.operation_token.type == TT_MINUS:
            result, error = left.subtracted_by(right)
        elif self.operation_token.type == TT_MUL:
            result, error = left.multiplied_by(right)
        elif self.operation_token.type == TT_DIV:
            result, error = left.divided_by(right)
        elif self.operation_token.type == TT_POW:
            result, error = left.raised_to_power_by(right)
        else:
            error = RTError(
                self.pos_start,
                self.pos_end,
                f"Operation not found {self.operation_token.type}",
                context,
            )

        if error or result is None:
            return res.failure(error)
        return res.success(result.set_pos(self.pos_start, self.pos_end))
