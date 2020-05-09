from __future__ import annotations

from typing import List, Callable, TYPE_CHECKING, Union, Tuple, Optional, cast

from errors.invalid_syntax_error import InvalidSyntaxError
from keywords import KEYWORDS
from nodes.binary_operation_node import BinaryOperationNode
from nodes.function_call_node import FunctionCallNode
from nodes.function_definition_node import FunctionDefinitionNode
from nodes.if_node import IfNode
from nodes.match_case_node import MatchCaseNode
from nodes.match_node import MatchNode
from nodes.node import Node
from nodes.number_node import NumberNode
from nodes.type_definition_node import TypeDefinitionNode
from nodes.type_variant_node import TypeVariantNode
from nodes.unary_operation_node import UnaryOperationNode
from nodes.variable_access_node import VariableAccessNode
from parser.parse_result import ParseResult
from position import mock_position
from token_types import *

if TYPE_CHECKING:
    from lang_token import Token


class Parser:
    def __init__(self, tokens: List[Token]):
        # TODO handle multiple statements
        # TODO think about change variable assignment to not return value
        self.tokens = tokens
        self.token_index = 0
        self.current_token: Token = tokens[0] if tokens else Token(
            TT_EOF, mock_position, mock_position
        )

    def parse(self, repl: bool = False) -> ParseResult:
        if self.current_token.type == TT_EOF:
            return ParseResult()
        res = self.repl_top_level() if repl else self.top_level()
        if not res.error and self.current_token.type != TT_EOF:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected '+', '-', '*', '/' or '^'",
                )
            )
        return res

    def advance(self) -> Token:
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def repl_top_level(self) -> ParseResult:
        if self.current_token.matches(TT_KEYWORD, KEYWORDS["VARIABLE_DECLARATION"]):
            return self.var_decl()
        if self.current_token.matches(TT_KEYWORD, KEYWORDS["TYPE_DECLARATION"]):
            return self.type_decl()
        return self.expression()

    def top_level(self) -> ParseResult:
        if self.current_token.matches(TT_KEYWORD, KEYWORDS["VARIABLE_DECLARATION"]):
            return self.var_decl()
        if self.current_token.matches(TT_KEYWORD, KEYWORDS["TYPE_DECLARATION"]):
            return self.type_decl()
        return ParseResult().failure(
            InvalidSyntaxError(
                self.current_token.pos_start,
                self.current_token.pos_end,
                f'Expected "{KEYWORDS["VARIABLE_DECLARATION"]}" or "{KEYWORDS["TYPE_DECLARATION"]}"',
            )
        )

    def type_decl(self) -> ParseResult:
        res = ParseResult()

        if not self.current_token.matches(TT_KEYWORD, KEYWORDS["TYPE_DECLARATION"]):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f'Expected "{KEYWORDS["TYPE_DECLARATION"]}"',
                )
            )
        res.register_advancement(self.advance())
        type_name: Token = self.current_token
        res.register_advancement(self.advance())
        if self.current_token.type != TT_EQUALS:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f'Expected "="',
                )
            )
        res.register_advancement(self.advance())

        variants: List[TypeVariantNode] = []
        variant = res.register(self._variant_type_identifier())
        if variant is None or res.error or not isinstance(variant, TypeVariantNode):
            return res
        variants.append(variant)

        while self.current_token.matches(TT_KEYWORD, KEYWORDS["OR"]):
            res.register_advancement(self.advance())
            variant = res.register(self._variant_type_identifier())
            if variant is None or res.error or not isinstance(variant, TypeVariantNode):
                return res
            variants.append(variant)

        return res.success(TypeDefinitionNode(type_name, variants))

    def var_decl(self) -> ParseResult:
        res = ParseResult()

        if not self.current_token.matches(TT_KEYWORD, KEYWORDS["VARIABLE_DECLARATION"]):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f'Expected "{KEYWORDS["VARIABLE_DECLARATION"]}"',
                )
            )
        fun_def = res.register(
            self.function_definition(KEYWORDS["VARIABLE_DECLARATION"], True, TT_EQUALS)
        )
        if res.error or fun_def is None:
            return res
        return res.success(fun_def)

    def expression(self) -> ParseResult:
        res = ParseResult()
        if self.current_token.matches(TT_KEYWORD, KEYWORDS["VARIABLE_DECLARATION"]):
            return self._binary_operation(
                self.var_decl, [(TT_KEYWORD, KEYWORDS["IN"])], self.expression
            )

        node = res.register(
            self._binary_operation(
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
            self._binary_operation(
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
        return self._binary_operation(self.term, [TT_PLUS, TT_MINUS])

    def term(self) -> ParseResult:
        return self._binary_operation(self.factor, [TT_DIV, TT_MUL])

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

    def power(self) -> ParseResult:
        return self._binary_operation(self.atom, [TT_POW], self.factor)

    def atom(self) -> ParseResult:
        res = ParseResult()

        token = self.current_token

        if token.type in (TT_IDENTIFIER,):
            call_node = res.register(self._function_call())
            if res.error or call_node is None:
                return res
            return res.success(call_node)
        elif token.matches(TT_KEYWORD, KEYWORDS["IF"]):
            if_expr = res.register(self.if_expression())
            if res.error or if_expr is None:
                return res
            return res.success(if_expr)
        elif token.matches(TT_KEYWORD, KEYWORDS["FUN"]):
            fun_def = res.register(self.function_definition())
            if res.error or fun_def is None:
                return res
            return res.success(fun_def)
        elif token.matches(TT_KEYWORD, KEYWORDS["MATCH"]):
            match_def = res.register(self.match())
            if res.error or match_def is None:
                return res
            return res.success(match_def)
        return self.argument()

    def argument(self) -> ParseResult:
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
                token.pos_start, token.pos_end, "Expected int, float, variable or ("
            )
        )

    def match(self) -> ParseResult:
        res = ParseResult()
        if not self.current_token.matches(TT_KEYWORD, KEYWORDS["MATCH"]):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f'Expected "{KEYWORDS["MATCH"]}"',
                )
            )

        res.register_advancement(self.advance())
        expr = res.register(self.expression())
        if res.error or expr is None:
            return res

        if not self.current_token.matches(TT_KEYWORD, KEYWORDS["WITH"]):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f'Expected "{KEYWORDS["WITH"]}"',
                )
            )
        res.register_advancement(self.advance())
        if self.current_token.matches(TT_KEYWORD, KEYWORDS["MATCH_OR"]):
            res.register_advancement(self.advance())

        cases: List[MatchCaseNode] = []
        case = res.register(self._match_case())
        if res.error or case is None:
            return res
        cases.append(cast(MatchCaseNode, case))
        while self.current_token.matches(TT_KEYWORD, KEYWORDS["MATCH_OR"]):
            res.register_advancement(self.advance())
            case = res.register(self._match_case())
            if res.error or case is None:
                return res
            cases.append(cast(MatchCaseNode, case))

        if not self.current_token.matches(TT_KEYWORD, KEYWORDS["END"]):
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f'Expected "{KEYWORDS["END"]}"',
                )
            )
        res.register_advancement(self.advance())

        return res.success(MatchNode(expr, cases))

    def if_expression(self, keyword_type: str = "IF") -> ParseResult:
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

    def function_definition(
        self,
        keyword: str = KEYWORDS["FUN"],
        has_name: bool = False,
        end_def_token: str = TT_ARROW,
    ) -> ParseResult:
        res = ParseResult()
        if not self.current_token.matches(TT_KEYWORD, keyword):
            res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f"Expected {keyword}",
                )
            )

        res.register_advancement(self.advance())

        var_name = None
        if has_name:
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

        arg_tokens: List[Token] = []
        while self.current_token.type == TT_IDENTIFIER:
            arg_tokens.append(self.current_token)
            res.register_advancement(self.advance())

        if self.current_token.type != end_def_token:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    f'Expected "{end_def_token}"',
                )
            )
        res.register_advancement(self.advance())
        expr = res.register(self.expression())
        if res.error or expr is None:
            return res
        fun = res.register(Parser._make_function_definition(var_name, arg_tokens, expr))
        if res.error or fun is None:
            return res
        return res.success(fun)

    @staticmethod
    def _make_function_definition(
        var_name: Optional[Token], args: List[Token], body: Node
    ) -> ParseResult:
        res = ParseResult()
        id_tokens = [var_name, *args] if var_name else args
        if not Parser._check_if_tokens_values_are_distinct(id_tokens):
            pos_start = var_name.pos_start if var_name else args[0].pos_start
            return res.failure(
                InvalidSyntaxError(
                    pos_start,
                    id_tokens[-1].pos_end,
                    "Names let_in this function declaration are not unique",
                )
            )
        if not args:
            return res.success(FunctionDefinitionNode(var_name, None, body))
        prev_fun = body
        for arg in reversed(args):
            prev_fun = FunctionDefinitionNode(None, arg, prev_fun)
        return res.success(FunctionDefinitionNode(var_name, None, prev_fun))

    @staticmethod
    def _check_if_tokens_values_are_distinct(tokens: List[Token]) -> bool:
        ids = list(map(lambda t: t.value, tokens))
        return len(set(ids)) == len(ids)

    def _function_call(self) -> ParseResult:
        res = ParseResult()

        var_name = self.current_token

        if var_name.type != TT_IDENTIFIER:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected identifier",
                )
            )

        res.register_advancement(self.advance())

        arg_tokens: List[Node] = []
        while self.current_token.type in (TT_LPAREN, TT_IDENTIFIER, TT_INT, TT_FLOAT):
            arg = res.register(self.argument())
            if arg is None or res.error:
                return res
            arg_tokens.append(arg)

        if arg_tokens:
            return res.success(FunctionCallNode(var_name, arg_tokens))
        return res.success(VariableAccessNode(var_name))

    def _binary_operation(
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

    def _variant_type_identifier(self) -> ParseResult:
        res = ParseResult()

        variant_type_name = self.current_token

        if variant_type_name.type != TT_IDENTIFIER:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected variant type name",
                )
            )

        res.register_advancement(self.advance())
        args_tokens: List[Token] = []
        if self.current_token.matches(TT_KEYWORD, KEYWORDS["TYPE_DESCRIPTION"]):
            res.register_advancement(self.advance())
            while self.current_token.type == TT_IDENTIFIER:
                args_tokens.append(self.current_token)
                res.register_advancement(self.advance())
                if self.current_token.type == TT_MUL:
                    res.register_advancement(self.advance())
                    if self.current_token.type != TT_IDENTIFIER:
                        return res.failure(
                            InvalidSyntaxError(
                                self.current_token.pos_start,
                                self.current_token.pos_end,
                                "Expected type identifier",
                            )
                        )

        return res.success(TypeVariantNode(variant_type_name, args_tokens))

    def _match_case(self) -> ParseResult:
        res = ParseResult()

        type_name = self.current_token

        if type_name.type != TT_IDENTIFIER:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected type name",
                )
            )

        res.register_advancement(self.advance())

        arg_tokens: List[Token] = []
        if self.current_token.type == TT_LPAREN:
            res.register_advancement(self.advance())
            while self.current_token.type == TT_IDENTIFIER:
                arg_tokens.append(self.current_token)
                res.register_advancement(self.advance())

                if self.current_token.type == TT_COMA:
                    res.register_advancement(self.advance())
                else:
                    break

            if self.current_token.type != TT_RPAREN:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start,
                        self.current_token.pos_end,
                        'Expected ")"',
                    )
                )
            res.register_advancement(self.advance())

        if self.current_token.type != TT_ARROW:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    'Expected "->"',
                )
            )
        res.register_advancement(self.advance())

        expr_node = res.register(self.expression())
        if res.error or expr_node is None:
            return res
        return res.success(MatchCaseNode(type_name, arg_tokens, expr_node))
