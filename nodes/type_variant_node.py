from __future__ import annotations

from typing import TYPE_CHECKING, List

from interpreter.runtime_result import RuntimeResult
from lang_types.type_def import LangVariantTypeDefinition
from nodes.node import Node

if TYPE_CHECKING:
    from context import Context
    from tokens.lang_string_token import StringToken


class TypeVariantNode(Node):
    def __init__(
        self, var_name_token: StringToken, args_tokens: List[StringToken],
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

        variant_def = LangVariantTypeDefinition(
            var_name,
            list(map(lambda token: token.value, self.args_token)),
            self.pos_start,
            self.pos_end,
            context,
        )
        context.set(var_name, variant_def)

        return res.success(variant_def)
