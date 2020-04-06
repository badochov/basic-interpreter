from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List

from interpreter.runtime_result import RuntimeResult
from nodes.node import Node

if TYPE_CHECKING:
    from context import Context
    from lang_token import Token


class FunctionDefinitionNode(Node):
    def __init__(
        self,
        var_name_token: Optional[Token],
        arg_token: Optional[Token],
        body_node: Node,
    ):
        if var_name_token:
            pos_start = var_name_token.pos_start
        elif arg_token:
            pos_start = arg_token.pos_start
        else:
            pos_start = body_node.pos_start

        super().__init__(pos_start, body_node.pos_end)
        self.var_name_token = var_name_token
        self.arg_token = arg_token
        self.body_node = body_node

    def visit(self, context: Context) -> RuntimeResult:
        res = RuntimeResult()
        var_name = self.var_name_token.value
        value = res.register(self.value_node.visit(context))
        if res.error or value is None:
            return res

        if isinstance(var_name, str):
            context.symbol_table.set(var_name, value)

        return res.success(value)
