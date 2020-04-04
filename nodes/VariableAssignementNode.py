from __future__ import annotations

from typing import TYPE_CHECKING

from interpreter.RuntimeResult import RuntimeResult
from nodes.Node import Node

if TYPE_CHECKING:
    from Context import Context
    from Token import Token


class VariableAssignmentNode(Node):
    def __init__(self, var_name_token: Token, value_node: Node):
        super().__init__(var_name_token.pos_start, var_name_token.pos_end)
        self.var_name_token = var_name_token
        self.value_node = value_node

        self.pos_start = var_name_token.pos_start
        self.pos_end = var_name_token.pos_end

    def visit(self, context: Context) -> RuntimeResult:
        res = RuntimeResult()
        var_name = self.var_name_token.value

        value = res.register(self.value_node.visit(context))
        if res.error or value is None:
            return res

        if isinstance(var_name, str):
            context.symbol_table.set(var_name, value)

        return res.success(value)
