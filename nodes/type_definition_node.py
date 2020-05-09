from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List

from errors.rt_error import RTError
from interpreter.runtime_result import RuntimeResult
from lang_types.lang_function import LangFunction
from lang_types.lang_type import LangType
from nodes.node import Node
from nodes.type_variant_node import TypeVariantNode

if TYPE_CHECKING:
    from context import Context
    from lang_token import Token


class TypeDefinitionNode(Node):
    def __init__(
        self, var_name_token: Token, variants: List[TypeVariantNode],
    ):
        pos_end = variants[-1].pos_end if variants else var_name_token.pos_end

        super().__init__(var_name_token.pos_start, pos_end)
        self.var_name_token = var_name_token
        self.variants = variants

    def __repr__(self) -> str:
        return f"({self.var_name_token}: {self.variants})"

    def visit(self, context: Context) -> RuntimeResult:
        res = RuntimeResult()
        return res
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
