from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from errors.rt_error import RTError
from interpreter.runtime_result import RuntimeResult
from lang_token import Token
from lang_types.lang_variant_type import LangVariantType
from nodes.node import Node
from symbol_table import SymbolTable

from context import Context


class MatchCaseNode(Node):
    def __init__(
        self, type_variant_name_token: Token, arg_tokens: List[Token], expr_node: Node
    ):
        super().__init__(type_variant_name_token.pos_start, expr_node.pos_end)
        self.type_variant_name_token = type_variant_name_token
        self.arg_tokens = arg_tokens
        self.expr_node = expr_node
        self.var: Optional[LangVariantType] = None

    def __repr__(self) -> str:
        res = "(" + f"{self.expr_node}("
        for case_node in self.arg_tokens:
            res += f"{case_node},"

        return ")" + res + ")"

    def set_matched_variable(self, var: LangVariantType) -> None:
        self.var = var

    def visit(self, context: Context) -> RuntimeResult:
        res = RuntimeResult()
        if self.var is None:
            return res.failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "set_matched_variable should be called before visiting MatchCaseNode",
                    context,
                )
            )

        if not self.var.is_of_type(str(self.type_variant_name_token.value)):
            return res
        if len(self.arg_tokens) != len(self.var.args):
            return res.failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "Number of arguments doesn't match",
                    context,
                )
            )
        new_ctx = Context(
            f"Case {self.type_variant_name_token.value}",
            SymbolTable(),
            context,
            self.pos_start,
        )
        for i, arg_token in enumerate(self.arg_tokens):
            if not isinstance(arg_token.value, str):
                return res.failure(
                    RTError(self.pos_start, self.pos_end, "Expected string", context,)
                )
            new_ctx.symbol_table.set(arg_token.value, self.var.args[i])

        value = res.register(self.expr_node.visit(new_ctx))
        if value is None or res.error:
            return res
        return res.success(value)
