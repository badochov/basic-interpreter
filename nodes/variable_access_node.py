from __future__ import annotations

from typing import TYPE_CHECKING

from errors.rt_error import RTError
from lang_types.lang_function import LangFunction
from lang_types.lang_type import LangType
from lang_types.lang_variant_type import LangVariantType
from lang_types.type_def import LangVariantTypeDefinition
from nodes.node import Node

if TYPE_CHECKING:
    from context import Context
    from tokens.lang_string_token import StringToken


class VariableAccessNode(Node):
    __slots__ = ["var_name_token"]

    def __init__(self, var_name_token: StringToken):
        super().__init__(var_name_token.pos_start, var_name_token.pos_end)
        self.var_name_token = var_name_token

    def __repr__(self) -> str:
        return f"({self.var_name_token})"

    def visit(self, context: Context) -> LangType:
        var_name = self.var_name_token.value
        value = context.get(var_name)
        if not value:
            raise RTError(
                self.pos_start, self.pos_end, f'"{var_name}" is not defined', context,
            )

        if isinstance(value, LangVariantTypeDefinition):
            if len(value.args) == 0:
                return LangVariantType([], var_name)
            else:
                raise RTError(
                    self.pos_start,
                    self.pos_end,
                    f'"{var_name}" excepts more arguments',
                    context,
                )

        else:
            if isinstance(value, LangFunction):
                return value.copy().set_pos(self.pos_start)
            return value.copy()
