from __future__ import annotations

from typing import TYPE_CHECKING, List

from errors.rt_error import RTError
from interpreter.runtime_result import RuntimeResult
from nodes.node import Node

if TYPE_CHECKING:
    from context import Context
    from lang_token import Token


class VariableAccessNode(Node):
    def __init__(self, var_name_token: Token, arg_nodes: List[Token]):
        pos_end = arg_nodes[-1].pos_end if arg_nodes else var_name_token.pos_end
        super().__init__(var_name_token.pos_start, pos_end)
        self.var_name_token = var_name_token
        self.arg_nodes = List[Token]

    def visit(self, context: Context) -> RuntimeResult:
        res = RuntimeResult()
        var_name = self.var_name_token.value

        value = None
        if isinstance(var_name, str):
            value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f'"{var_name}" is not defined',
                    context,
                )
            )

        value = value.copy().set_pos(self.pos_start, self.pos_end)
        return res.success(value)
