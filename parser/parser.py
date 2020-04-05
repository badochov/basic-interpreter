from __future__ import annotations

from typing import List, Callable, TYPE_CHECKING, Union, Tuple

from errors.invalid_syntax_error import InvalidSyntaxError
from keywords import KEYWORDS
from nodes.binary_operation_node import BinaryOperationNode
from nodes.if_node import IfNode
from nodes.number_node import NumberNode
from nodes.unary_operation_node import UnaryOperationNode
from nodes.variable_access_node import VariableAccessNode
from nodes.variable_assignment_node import VariableAssignmentNode
from parser.parse_result import ParseResult
from token_types import *

if TYPE_CHECKING:
    from lang_token import Token


class Parser:
    def __init__(self, tokens: List[Token]):
        # TODO handle if token list is empty
        self.tokens = tokens
        self.token_index = 0
        self.current_token: Token = tokens[0]

    def parse(self) -> ParseResult:
        res = self.expression()
        if not res.error and self.current_token.type != TT_EOF:
            res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected '+', '-', '*' or '/'",
                )
            )
        return res

    def advance(self) -> Token:
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def binary_operation(
        self,
        function: Callable[[], ParseResult],
        operands: Union[List[str], List[Tuple[str, str]]],
        function2: Callable[[], ParseResult] = None,
    ) -> ParseResult:
        if function2 is None:
            function2 = function

        res = ParseResult()
        left = res.register(function())
        if res.error or left is None:
            return res
        while (
            self.current_token.type in operands
            or (self.current_token.type, self.current_token.value) in operands
        ):
            op_token = self.current_token
            res.register_advancement(self.advance())
            right = res.register(function2())
            if res.error or right is None:
                return res
            left = BinaryOperationNode(left, op_token, right)

        return res.success(left)

    def power(self) -> ParseResult:
        return self.binary_operation(self.atom, [TT_POW], self.factor)

    def expression(self) -> ParseResult:
        res = ParseResult()
        if self.current_token.matches(TT_KEYWORD, KEYWORDS["VARIABLE_DECLARATION"]):
            res.register_advancement(self.advance())

            if self.current_token.type != TT_IDENTIFIER:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "Expected identifier",
                    )
                )

            var_name = self.current_token

            res.register_advancement(self.advance())

            if self.current_token.type != TT_EQUALS:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        "Expected '='",
                    )
                )
            res.register_advancement(self.advance())
            expr = res.register(self.expression())
            if res.error or expr is None:
                return res
            return res.success(VariableAssignmentNode(var_name, expr))
        node = res.register(
            self.binary_operation(
                self.logic_expression,
                [(TT_KEYWORD, KEYWORDS["AND"]), (TT_KEYWORD, KEYWORDS["OR"])],
            )
        )
        if res.error or node is None:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f'Expected "{KEYWORDS["VARIABLE_DECLARATION"]}", int, float, +, - or (',
                )
            )
        return res.success(node)

    def logic_expression(self) -> ParseResult:
        res = ParseResult()

        if self.current_token.matches(TT_KEYWORD, KEYWORDS["NOT"]):
            token = self.current_token
            res.register_advancement(self.advance())

            node = res.register(self.logic_expression())
            if res.error or node is None:
                return res
            return res.success(UnaryOperationNode(token, node))

        node = res.register(
            self.binary_operation(
                self.arithmetic_expression,
                [TT_EE, TT_GT, TT_NE, TT_LT, TT_LTE, TT_GTE],
            )
        )
        if res.error or node is None:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f'Expected "{KEYWORDS["NOT"]}", int, float, +, - or (',
                )
            )
        return res.success(node)

    def arithmetic_expression(self) -> ParseResult:
        return self.binary_operation(self.term, [TT_PLUS, TT_MINUS])

    def term(self) -> ParseResult:
        return self.binary_operation(self.factor, [TT_DIV, TT_MUL])

    def factor(self) -> ParseResult:
        res = ParseResult()

        token = self.current_token
        if token is None:
            raise Exception

        if token.type in (TT_PLUS, TT_MINUS):
            res.register_advancement(self.advance())
            factor = res.register(self.factor())
            if res.error or factor is None:
                return res
            return res.success(UnaryOperationNode(token, factor))

        return self.power()

    def atom(self) -> ParseResult:
        res = ParseResult()

        token = self.current_token
        if token is None:
            raise Exception

        if token.type in (TT_FLOAT, TT_INT):
            res.register_advancement(self.advance())
            return res.success(NumberNode(token))
        elif token.type in (TT_IDENTIFIER,):
            res.register_advancement(self.advance())
            return res.success(VariableAccessNode(token))
        elif token.type in (TT_LPAREN,):
            res.register_advancement(self.advance())
            expr = res.register(self.expression())
            if res.error or expr is None:
                return res
            if self.current_token and self.current_token.type == TT_RPAREN:
                res.register_advancement(self.advance())
                return res.success(expr)
            return res.failure(
                InvalidSyntaxError(token.pos_start, token.pos_end, "Expected ')'")
            )
        elif token.matches(TT_KEYWORD, KEYWORDS["IF"]):
            if_expr = res.register(self.if_expression())
            if res.error or if_expr is None:
                return res
            return res.success(if_expr)

        return res.failure(
            InvalidSyntaxError(
                token.pos_start, token.pos_end, "Expected int, float, +, - or ("
            )
        )

    def if_expression(self, keyword_type: str = "IF") -> ParseResult:
        pos_start = self.current_token.pos_start.copy()
        res = ParseResult()
        if not self.current_token.matches(TT_KEYWORD, KEYWORDS[keyword_type]):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected {KEYWORDS[keyword_type]}",
                )
            )

        res.register_advancement(self.advance())
        condition = res.register(self.expression())
        if res.error or condition is None:
            return res

        if not self.current_token.matches(TT_KEYWORD, KEYWORDS["THEN"]):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f'Expected {KEYWORDS["THEN"]}',
                )
            )

        res.register_advancement(self.advance())

        expr = res.register(self.expression())
        if res.error or expr is None:
            return res
        if self.current_token.matches(TT_KEYWORD, KEYWORDS["ELIF"]):
            node = res.register(self.if_expression("ELIF"))
            if res.error or node is None:
                return res
            return res.success(IfNode(condition, expr, node))
        elif self.current_token.matches(TT_KEYWORD, KEYWORDS["ELSE"]):
            res.register_advancement(self.advance())
            node = res.register(self.expression())
            if res.error or node is None:
                return res
            return res.success(IfNode(condition, expr, node))

        return res.failure(
            InvalidSyntaxError(
                self.current_token.pos_start,
                self.current_token.pos_end,
                f'Expected {KEYWORDS["ELIF"]} or {KEYWORDS["ELSE"]}',
            )
        )
