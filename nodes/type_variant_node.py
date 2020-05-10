from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List

from errors.rt_error import RTError
from interpreter.runtime_result import RuntimeResult
from lang_types.lang_function import LangFunction
from lang_types.lang_type import LangType
from lang_types.lang_variant_type import LangVariantType
from lang_types.type_def import LangVariantTypeDefinition
from nodes.node import Node

if TYPE_CHECKING:
    from context import Context
    from lang_token import Token


class TypeVariantNode(Node):
    def __init__(
        self, var_name_token: Token, args_tokens: List[Token],
    ):
        pos_end = args_tokens[-1].pos_end if args_tokens else var_name_token.pos_end

        super().__init__(var_name_token.pos_start, pos_end)
        self.var_name_token = var_name_token
        self.args_token = args_tokens

    def __repr__(self) -> str:
        return f"({self.var_name_token} of {self.args_token})"

    def visit(self, context: Context) -> RuntimeResult:
        res = RuntimeResult()
        var_name = self.var_name_token.value

        assert isinstance(var_name, str)
        variant_def = LangVariantTypeDefinition(
            var_name,
            list(map(lambda token: str(token.type), self.args_token)),
            self.pos_start,
            self.pos_end,
            context,
        )
        context.symbol_table.set(var_name, variant_def)

        return res.success(variant_def)
