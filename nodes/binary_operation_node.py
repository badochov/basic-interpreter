from __future__ import annotations

from typing import TYPE_CHECKING

from errors.type_errors import RTTypeError
from keywords import KEYWORDS
from lang_types.lang_function import LangFunction
from lang_types.lang_type import LangType
from nodes.node import Node
from token_types import *

if TYPE_CHECKING:
    from context import Context
    from tokens.lang_token import Token


class BinaryOperationNode(Node):
    __slots__ = ["left_node", "operation_token", "right_node"]

    def __init__(self, left_node: Node, operation_token: Token, right_node: Node):
        super().__init__(left_node.pos_start, right_node.pos_end)
        self.left_node = left_node
        self.operation_token = operation_token
        self.right_node = right_node

    def __repr__(self) -> str:
        return f"({self.left_node}, {self.operation_token}, {self.right_node})"

    def visit(self, context: Context) -> LangType:
        left = self.left_node.visit(context)
        right = self.right_node.visit(context)
        try:
            if self.operation_token.type == TT_PLUS:
                result = left.added_to(right)
            elif self.operation_token.type == TT_MINUS:
                result = left.subtracted_by(right)
            elif self.operation_token.type == TT_MUL:
                result = left.multiplied_by(right)
            elif self.operation_token.type == TT_DIV:
                result = left.divided_by(right)
            elif self.operation_token.type == TT_POW:
                result = left.raised_to_power_by(right)
            elif self.operation_token.type == TT_EE:
                result = left.get_comparison_eq(right)
            elif self.operation_token.type == TT_NE:
                result = left.get_comparison_ne(right)
            elif self.operation_token.type == TT_LT:
                result = left.get_comparison_lt(right)
            elif self.operation_token.type == TT_GT:
                result = left.get_comparison_gt(right)
            elif self.operation_token.type == TT_LTE:
                result = left.get_comparison_lte(right)
            elif self.operation_token.type == TT_GTE:
                result = left.get_comparison_gte(right)
            elif self.operation_token.matches(TT_KEYWORD, KEYWORDS["AND"]):
                result = left.anded_by(right)
            elif self.operation_token.matches(TT_KEYWORD, KEYWORDS["OR"]):
                result = left.ored_by(right)
            elif self.operation_token.matches(TT_KEYWORD, KEYWORDS["IN"]):
                result = right
            else:
                return self._fail_with(
                    f"Operation not found {self.operation_token.type}", context
                )
        except RTTypeError as e:
            return self._fail_with(e.message, context)

        if isinstance(result, LangFunction):
            result.set_pos(self.pos_start)
        return result
