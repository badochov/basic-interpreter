from __future__ import annotations

from typing import TYPE_CHECKING

from errors.rt_error import RTError
from interpreter.runtime_result import RuntimeResult
from lang_types.lang_variant_type import LangVariantType
from lang_types.type_def import LangVariantTypeDefinition
from nodes.node import Node

if TYPE_CHECKING:
    from context import Context
    from tokens.lang_string_token import StringToken


class VariableAccessNode(Node):
    def __init__(self, var_name_token: StringToken):
        pos_end = var_name_token.pos_end
        super().__init__(var_name_token.pos_start, pos_end)
        self.var_name_token = var_name_token

    def __repr__(self) -> str:
        return f"({self.var_name_token})"

    def visit(self, context: Context) -> RuntimeResult:
        res = RuntimeResult()
        var_name = self.var_name_token.value

        value = context.get(var_name)
        if not value:
            return res.failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f'"{var_name}" is not defined',
                    context,
                )
            )
        if isinstance(value, LangVariantTypeDefinition):
            if len(value.args) == 0:
                value = LangVariantType(
                    [], var_name, self.pos_start, self.pos_end, context
                )
            else:
                return res.failure(
                    RTError(
                        self.pos_start,
                        self.pos_end,
                        f'"{var_name}" excepts more arguments',
                        context,
                    )
                )
        else:
            value = value.copy().set_pos(self.pos_start, self.pos_end)
        return res.success(value)
