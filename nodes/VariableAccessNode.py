from __future__ import annotations

from typing import TYPE_CHECKING

from errors.RTError import RTError
from interpreter.RuntimeResult import RuntimeResult
from nodes.Node import Node

if TYPE_CHECKING:
    from Context import Context
    from Token import Token


class VariableAccessNode(Node):
    def __init__(self, var_name_token: Token):
        super().__init__(var_name_token.pos_start, var_name_token.pos_end)
        self.var_name_token = var_name_token

        self.pos_start = var_name_token.pos_start
        self.pos_end = var_name_token.pos_end

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
