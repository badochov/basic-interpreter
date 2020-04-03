from typing import List, Optional, Callable

from ParseResult import ParseResult
from Token import Token
from errors.InvalidSyntaxError import InvalidSyntaxError
from nodes.BinaryOperationNode import BinaryOperationNode
from nodes.NumberNode import NumberNode
from nodes.UnaryOperationNode import UnaryOperationNode
from token_types import *


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.token_index = -1
        self.current_token: Optional[Token] = None
        self.advance()

    def parse(self) -> ParseResult:
        res = self.expression()
        if not res.error and self.current_token and self.current_token.type != TT_EOF:
            res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected '+', '-', '*' or '/'",
                )
            )
        return res

    def advance(self) -> Optional[Token]:
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
        if res.error:
            return res
        while self.current_token and self.current_token.type in operands:
            op_token = self.current_token
            res.register(self.advance())
            right = res.register(function2())
            if res.error:
                return res
            left = BinaryOperationNode(left, op_token, right)

        return res.success(left)

    def atom(self) -> ParseResult:
        res = ParseResult()

        token = self.current_token
        if token is None:
            raise Exception

        if token.type in (TT_FLOAT, TT_INT):
            res.register(self.advance())
            return res.success(NumberNode(token))
        elif token.type in (TT_LPAREN,):
            res.register(self.advance())
            expr = res.register(self.expression())
            if res.error:
                return res
            if self.current_token and self.current_token.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            return res.failure(
                InvalidSyntaxError(token.pos_start, token.pos_end, "Expected ')'")
            )

        return res.failure(
            InvalidSyntaxError(token.pos_start, token.pos_end, "Expected int or float")
        )

    def power(self) -> ParseResult:
        return self.binary_operation(self.atom, [TT_POW], self.factor)

    def factor(self) -> ParseResult:
        res = ParseResult()

        token = self.current_token
        if token is None:
            raise Exception

        if token.type in (TT_PLUS, TT_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOperationNode(token, factor))

        return self.power()

    def term(self) -> ParseResult:
        return self.binary_operation(self.factor, [TT_DIV, TT_MUL])

    def expression(self) -> ParseResult:
        return self.binary_operation(self.term, [TT_PLUS, TT_MINUS])