from __future__ import annotations

from typing import TYPE_CHECKING, cast

from errors.type_errors import RTTypeError
from keywords import KEYWORDS
from lang_types.lang_function import LangFunction
from lang_types.lang_type import (
    LangType,
    add,
    subtract,
    multiply,
    divide,
    raise_to_power,
    get_comparison_eq,
    get_comparison_ne,
    get_comparison_lt,
    get_comparison_gt,
    get_comparison_lte,
    get_comparison_gte,
    anded,
    ored,
    NotImplementedOperationType,
    not_implemented,
)
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
                result = add(left, right)
            elif self.operation_token.type == TT_MINUS:
                result = subtract(left, right)
            elif self.operation_token.type == TT_MUL:
                result = multiply(left, right)
            elif self.operation_token.type == TT_DIV:
                result = divide(left, right)
            elif self.operation_token.type == TT_POW:
                result = raise_to_power(left, right)
            elif self.operation_token.type == TT_EE:
                result = get_comparison_eq(left, right)
            elif self.operation_token.type == TT_NE:
                result = get_comparison_ne(left, right)
            elif self.operation_token.type == TT_LT:
                result = get_comparison_lt(left, right)
            elif self.operation_token.type == TT_GT:
                result = get_comparison_gt(left, right)
            elif self.operation_token.type == TT_LTE:
                result = get_comparison_lte(left, right)
            elif self.operation_token.type == TT_GTE:
                result = get_comparison_gte(left, right)
            elif self.operation_token.matches(TT_KEYWORD, KEYWORDS["AND"]):
                result = anded(left, right)
            elif self.operation_token.matches(TT_KEYWORD, KEYWORDS["OR"]):
                result = ored(left, right)
            elif self.operation_token.matches(TT_KEYWORD, KEYWORDS["IN"]):
                result = right
            else:
                return self._fail_with(
                    f"Operation not found {self.operation_token.type}", context
                )
        except RTTypeError as e:
            return self._fail_with(e.message, context)
        if not_implemented(result):
            return self._fail_with(
                cast(NotImplementedOperationType, result).msg, context
            )

        if isinstance(result, LangFunction):
            result.set_pos(self.pos_start)
        return result
