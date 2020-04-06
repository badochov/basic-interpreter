from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from errors.rt_error import RTError
from interpreter.runtime_result import RuntimeResult
from lang_types.lang_function import LangFunction
from lang_types.lang_type import LangType
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
        if self.arg_token:
            if not isinstance(self.arg_token.value, str):
                return res.failure(
                    RTError(
                        self.pos_start, self.pos_end, "Expected identifier", context
                    )
                )

            value: LangType = LangFunction(
                self.var_name_token,
                self.arg_token.value,
                self.body_node,
                self.pos_start,
                self.pos_end,
                context,
            )
        else:
            val = res.register(self.body_node.visit(context))
            if val is None or res.error:
                return res
            value = val

        if self.var_name_token:
            if not isinstance(self.var_name_token.value, str):
                return res.failure(
                    RTError(
                        self.pos_start, self.pos_end, "Expected identifier", context
                    )
                )
            context.symbol_table.set(self.var_name_token.value, value)
        return res.success(value)
