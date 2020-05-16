from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

from context import Context, mock_context
from errors.rt_error import RTError
from lang_types.lang_type import LangType
from lang_types.lang_variant_type import LangVariantType
from nodes.node import Node
from position import mock_position
from symbol_table import SymbolTable

if TYPE_CHECKING:
    from tokens.lang_string_token import StringToken


class LangNoMatchType(LangType):
    ...


# TODO add support for tuples
class MatchCaseNode(Node):
    def __init__(
        self,
        type_variant_name_token: StringToken,
        arg_tokens: List[StringToken],
        expr_node: Node,
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

    def visit(self, context: Context) -> LangType:
        assert self.var is not None
        every = self.type_variant_name_token.value == "_"

        if every:
            if self.arg_tokens:
                raise RTError(
                    self.pos_start, self.pos_end, "Unexpected arguments", context
                )

        elif not self.var.is_of_type(self.type_variant_name_token.value):
            return LangNoMatchType(
                "no-match", mock_position, mock_position, mock_context
            )
        if len(self.arg_tokens) != len(self.var.args) and not every:
            raise RTError(
                self.pos_start,
                self.pos_end,
                "Number of arguments doesn't match",
                context,
            )

        new_ctx = Context(
            f"Case {self.type_variant_name_token.value}",
            SymbolTable(),
            context,
            self.pos_start,
        )
        if not every:
            for i, arg_token in enumerate(self.arg_tokens):
                new_ctx.set(arg_token.value, self.var.args[i])

        return self.expr_node.visit(new_ctx)
