from __future__ import annotations

from typing import List, Callable, TYPE_CHECKING

from errors.InvalidSyntaxError import InvalidSyntaxError
from keywords import VARIABLE_DECLARATION_KEYWORD
from nodes.BinaryOperationNode import BinaryOperationNode
from nodes.NumberNode import NumberNode
from nodes.UnaryOperationNode import UnaryOperationNode
from nodes.VariableAccessNode import VariableAccessNode
from nodes.VariableAssignementNode import VariableAssignmentNode
from parser.ParseResult import ParseResult
from token_types import *

if TYPE_CHECKING:
    from Token import Token


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
        operands: List[str],
        function2: Callable[[], ParseResult] = None,
    ) -> ParseResult:
        if function2 is None:
            function2 = function

        res = ParseResult()
        left = res.register(function())
        if res.error or left is None:
            return res
        while self.current_token and self.current_token.type in operands:
            op_token = self.current_token
            res.register_advancement(self.advance())
            right = res.register(function2())
            if res.error or right is None:
                return res
            left = BinaryOperationNode(left, op_token, right)

        return res.success(left)

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

        return res.failure(
            InvalidSyntaxError(
                token.pos_start, token.pos_end, "Expected int, float, +, - or ("
            )
        )

    def power(self) -> ParseResult:
        return self.binary_operation(self.atom, [TT_POW], self.factor)

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

    def term(self) -> ParseResult:
        return self.binary_operation(self.factor, [TT_DIV, TT_MUL])

    def expression(self) -> ParseResult:
        res = ParseResult()
        if self.current_token.matches(TT_KEYWORD, VARIABLE_DECLARATION_KEYWORD):
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
        node = res.register(self.binary_operation(self.term, [TT_PLUS, TT_MINUS]))
        if res.error or node is None:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f'Expected "{VARIABLE_DECLARATION_KEYWORD}", int, float, +, - or (',
                )
            )
        return res.success(node)