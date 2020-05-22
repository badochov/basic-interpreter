from __future__ import annotations

from typing import List, Callable, TYPE_CHECKING, Union, Tuple, Optional, NoReturn

from errors.invalid_syntax_error import InvalidSyntaxError
from keywords import KEYWORDS
from nodes.binary_operation_node import BinaryOperationNode
from nodes.function_call_node import FunctionCallNode
from nodes.function_definition_node import FunctionDefinitionNode
from nodes.if_node import IfNode
from nodes.list_node import ListEndNode, ListNode
from nodes.match_case_node import MatchCaseNode
from nodes.match_node import MatchNode
from nodes.number_node import NumberNode
from nodes.tuple_node import TupleNode
from nodes.type_definition_node import TypeDefinitionNode
from nodes.type_variant_node import TypeVariantNode
from nodes.unary_operation_node import UnaryOperationNode
from nodes.variable_access_node import VariableAccessNode
from nodes.variable_assignment_node import VariableAssignmentNode, VariableType
from position import mock_position
from token_types import *
from tokens.lang_asterix_token import AsterixToken
from tokens.lang_empty_token import EmptyToken
from tokens.lang_number_token import NumberToken
from tokens.lang_string_token import StringToken

if TYPE_CHECKING:
    from tokens.lang_token import Token
    from nodes.node import Node
    from nodes.variable_assignment_node import NamesType


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.token_index = 0
        self.current_token: Token = tokens[0] if tokens else EmptyToken(
            TT_EOF, mock_position, mock_position
        )

    def parse(self, repl: bool = False) -> List[Node]:
        results: List[Node] = []
        while self.current_token.type != TT_EOF:
            res = self.repl_top_level() if repl else self.top_level()
            results.append(res)
        return results

    def advance(self) -> Token:
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def repl_top_level(self) -> Node:
        if self.current_token.matches(TT_KEYWORD, KEYWORDS["VARIABLE_DECLARATION"]):
            return self.var_decl()
        if self.current_token.matches(TT_KEYWORD, KEYWORDS["TYPE_DECLARATION"]):
            return self.type_decl()
        return self._tuple()

    def top_level(self) -> Node:
        if self.current_token.matches(TT_KEYWORD, KEYWORDS["VARIABLE_DECLARATION"]):
            return self.var_decl()
        if self.current_token.matches(TT_KEYWORD, KEYWORDS["TYPE_DECLARATION"]):
            return self.type_decl()
        return self._fail_with_invalid_syntax_error(
            f'Expected "{KEYWORDS["VARIABLE_DECLARATION"]}"'
            f' or "{KEYWORDS["TYPE_DECLARATION"]}"'
        )

    def type_decl(self) -> TypeDefinitionNode:

        if not self.current_token.matches(TT_KEYWORD, KEYWORDS["TYPE_DECLARATION"]):
            return self._fail_with_invalid_syntax_error(
                f'Expected "{KEYWORDS["TYPE_DECLARATION"]}"',
            )

        if not self.advance().type == TT_IDENTIFIER:
            return self._fail_with_invalid_syntax_error("Expected type name")

        type_name: StringToken = StringToken.as_string_token(self.current_token)

        if self.advance().type != TT_EQUALS:
            return self._fail_with_invalid_syntax_error(f'Expected "="',)
        self.advance()
        variants: List[TypeVariantNode] = [self._variant_type_identifier()]

        while self.current_token.matches(TT_KEYWORD, KEYWORDS["OR"]):
            self.advance()
            variants.append(self._variant_type_identifier())

        return TypeDefinitionNode(type_name, variants)

    def var_decl(self) -> Node:

        if not self.current_token.matches(TT_KEYWORD, KEYWORDS["VARIABLE_DECLARATION"]):
            return self._fail_with_invalid_syntax_error(
                f'Expected "{KEYWORDS["VARIABLE_DECLARATION"]}"',
            )
        return self.function_definition(
            KEYWORDS["VARIABLE_DECLARATION"], True, TT_EQUALS
        )

    def expression(self) -> Node:

        if self.current_token.matches(TT_KEYWORD, KEYWORDS["VARIABLE_DECLARATION"]):
            return self._binary_operation(
                self.var_decl, [(TT_KEYWORD, KEYWORDS["IN"])], self._tuple
            )

        return self._binary_operation(
            self.logic_expression,
            [(TT_KEYWORD, KEYWORDS["AND"]), (TT_KEYWORD, KEYWORDS["OR"])],
        )

    def logic_expression(self) -> Node:

        if self.current_token.matches(TT_KEYWORD, KEYWORDS["NOT"]):
            token: EmptyToken = EmptyToken.as_empty_token(self.current_token)
            self.advance()

            return UnaryOperationNode(token, self.logic_expression())

        return self._binary_operation(
            self.arithmetic_expression, [TT_EE, TT_GT, TT_NE, TT_LT, TT_LTE, TT_GTE],
        )

    def arithmetic_expression(self) -> Node:
        return self._binary_operation(self.term, [TT_PLUS, TT_MINUS])

    def term(self) -> Node:
        return self._binary_operation(self.factor, [TT_DIV, TT_MUL])

    def factor(self) -> Node:

        token = self.current_token

        if token.is_empty_token() and token.type in (TT_PLUS, TT_MINUS):
            self.advance()

            return UnaryOperationNode(EmptyToken.as_empty_token(token), self.factor())

        return self.power()

    def power(self) -> Node:
        return self._binary_operation(self.atom, [TT_POW], self.factor)

    def atom(self) -> Node:

        token = self.current_token
        if token.type in (TT_IDENTIFIER,):
            return self._function_call()
        elif token.matches(TT_KEYWORD, KEYWORDS["IF"]):
            return self.if_expression()
        elif token.matches(TT_KEYWORD, KEYWORDS["FUN"]):
            return self.function_definition()
        elif token.matches(TT_KEYWORD, KEYWORDS["MATCH"]):
            return self.match()
        return self.argument()

    def argument(self) -> Node:

        token = self.current_token

        if token.type in (TT_FLOAT, TT_INT):
            self.advance()
            return NumberNode(NumberToken.as_number_token(token))
        elif token.type == TT_IDENTIFIER:
            self.advance()
            return VariableAccessNode(StringToken.as_string_token(token))
        elif token.type == TT_LPAREN:
            self.advance()
            expr = self._tuple()
            if self.current_token and self.current_token.type == TT_RPAREN:
                self.advance()
                return expr
            raise InvalidSyntaxError(token.pos_start, token.pos_end, "Expected ')'")
        elif token.type == TT_LBRACKET:
            self.advance()
            return self._make_list()
        raise InvalidSyntaxError(
            token.pos_start, token.pos_end, 'Expected int, float, variable or "("'
        )

    def match(self) -> Node:

        if not self.current_token.matches(TT_KEYWORD, KEYWORDS["MATCH"]):
            return self._fail_with_invalid_syntax_error(
                f'Expected "{KEYWORDS["MATCH"]}"',
            )

        self.advance()
        expr = self._tuple()

        if not self.current_token.matches(TT_KEYWORD, KEYWORDS["WITH"]):
            return self._fail_with_invalid_syntax_error(
                f'Expected "{KEYWORDS["WITH"]}"',
            )

        if self.advance().matches(TT_KEYWORD, KEYWORDS["MATCH_OR"]):
            self.advance()

        cases: List[MatchCaseNode] = [self._match_case()]

        while self.current_token.matches(TT_KEYWORD, KEYWORDS["MATCH_OR"]):
            self.advance()
            cases.append(self._match_case())

        if not self.current_token.matches(TT_KEYWORD, KEYWORDS["END"]):
            return self._fail_with_invalid_syntax_error(
                f'Expected "{KEYWORDS["END"]}"',
            )
        self.advance()

        return MatchNode(expr, cases)

    def _get_variable_assignment(
        self,
        tuple_in_paren: bool = True,
        var_type: VariableType = VariableType.Tuple,
        can_be_variant_type: bool = False,
        can_be_empty: bool = False,
        in_paren: bool = False,
    ) -> VariableAssignmentNode:
        names: NamesType = []
        was_asterix = False
        break_on_coma = (
            var_type is VariableType.Tuple and tuple_in_paren and not in_paren
        )
        while True:
            if self.current_token.type == TT_IDENTIFIER:
                name_token = StringToken.as_string_token(self.current_token)
                self.advance()
                if can_be_variant_type:
                    args = self._get_variant_type_args()

                    if args:
                        names.append(
                            VariableAssignmentNode(
                                [name_token, *args], VariableType.VariantType
                            )
                        )
                    else:
                        names.append(name_token)

                else:
                    names.append(name_token)
                    self._make_type_hint()
            elif self.current_token.type == TT_MUL:
                if was_asterix:
                    return self._fail_with_invalid_syntax_error(
                        'Unexpected multiple "*"'
                    )
                was_asterix = True
                asterix_token = self.current_token
                self.advance()
                if self.current_token.type == TT_IDENTIFIER:
                    if var_type is VariableType.List:
                        names.append(
                            AsterixToken.from_string_token(
                                StringToken.as_string_token(self.current_token)
                            )
                        )
                    else:
                        return self._fail_with_invalid_syntax_error('Unexpected "*"')
                    self.advance()
                else:
                    names.append(
                        AsterixToken(
                            asterix_token.pos_start, asterix_token.pos_end, "_"
                        )
                    )
            elif self.current_token.type == TT_LBRACKET:
                self.advance()
                names.append(
                    self._get_variable_assignment(True, VariableType.List, True)
                )
                if self.current_token.type == TT_RBRACKET:
                    self.advance()
                else:
                    return self._fail_with_invalid_syntax_error('Expected "]"')
            elif self.current_token.type == TT_LPAREN:
                self.advance()
                names.append(
                    self._get_variable_assignment(
                        False, VariableType.Tuple, True, False, True
                    )
                )
                if self.current_token.type == TT_RPAREN:
                    self.advance()
                else:
                    return self._fail_with_invalid_syntax_error('Expected ")"')
            else:
                if not can_be_empty:
                    return self._fail_with_invalid_syntax_error("Expected name")
                break
            if self.current_token.type == TT_COMA:
                if break_on_coma:
                    break
                self.advance()
            else:
                break

        if len(names) > 1:
            if not in_paren and tuple_in_paren and var_type is not VariableType.List:
                return self._fail_with_invalid_syntax_error(
                    "This tuple was expected to be in parentheses"
                )
        if (
            len(names) == 1
            and isinstance(names[0], VariableAssignmentNode)
            and var_type is VariableType.Tuple
        ):
            return names[0]
        return VariableAssignmentNode(names, var_type)

    def if_expression(self, keyword_type: str = "IF") -> Node:

        if not self.current_token.matches(TT_KEYWORD, KEYWORDS[keyword_type]):
            return self._fail_with_invalid_syntax_error(
                f"Expected {KEYWORDS[keyword_type]}",
            )

        self.advance()
        condition = self.expression()

        if not self.current_token.matches(TT_KEYWORD, KEYWORDS["THEN"]):
            return self._fail_with_invalid_syntax_error(f'Expected {KEYWORDS["THEN"]}',)

        self.advance()

        expr = self._tuple()
        if self.current_token.matches(TT_KEYWORD, KEYWORDS["ELIF"]):
            return IfNode(condition, expr, self.if_expression("ELIF"))
        elif self.current_token.matches(TT_KEYWORD, KEYWORDS["ELSE"]):
            self.advance()
            return IfNode(condition, expr, self._tuple())

        return self._fail_with_invalid_syntax_error(
            f'Expected {KEYWORDS["ELIF"]} or {KEYWORDS["ELSE"]}',
        )

    def function_definition(
        self,
        keyword: str = KEYWORDS["FUN"],
        has_name: bool = False,
        end_def_token: str = TT_EQUALS,
        end_def_match_token: str = TT_ARROW,
    ) -> Node:

        if not self.current_token.matches(TT_KEYWORD, keyword):
            return self._fail_with_invalid_syntax_error(f"Expected {keyword}",)

        self.advance()

        var_name: Optional[VariableAssignmentNode] = None
        can_be_function = True
        if has_name:
            if self.current_token.type != TT_IDENTIFIER:
                can_be_function = False
            var_name = self._get_variable_assignment(False)
        else:
            self._make_type_hint()
        arg_tokens: List[VariableAssignmentNode] = []
        if can_be_function:
            while self.current_token.type in (TT_IDENTIFIER, TT_LPAREN):
                arg_tokens.append(self._get_variable_assignment(True))

        if self.current_token.type not in (end_def_token, end_def_match_token):
            return self._fail_with_invalid_syntax_error(f'Expected "{end_def_token}"')
        if self.current_token.type == end_def_match_token:
            if not arg_tokens:
                return self._fail_with_invalid_syntax_error(
                    'Definition with "->" can only be used with arguments.'
                )
            self._add_match(arg_tokens[-1])
        self.advance()
        return Parser._make_function_definition(var_name, arg_tokens, self._tuple())

    @staticmethod
    def _make_function_definition(
        var_name: Optional[VariableAssignmentNode],
        args: List[VariableAssignmentNode],
        body: Node,
    ) -> FunctionDefinitionNode:
        names: List[str] = [
            *([name for name in var_name.get_names()] if var_name else []),
            *[name for arg in args for name in arg.get_names()],
        ]
        if not Parser._check_if_names_are_distinct(names):
            raise InvalidSyntaxError(
                var_name.pos_start if var_name else args[0].pos_start,
                (var_name.pos_end if var_name else mock_position)
                if not args
                else args[-1].pos_end,
                "Names in this function declaration are not unique",
            )

        if not args:
            return FunctionDefinitionNode(var_name, None, body)
        prev_fun = body
        for arg in reversed(args):
            prev_fun = FunctionDefinitionNode(var_name, arg, prev_fun, False)
        return FunctionDefinitionNode(var_name, None, prev_fun, var_name is not None)

    @staticmethod
    def _check_if_names_are_distinct(names: List[str]) -> bool:
        ids = list(filter(lambda s: s != "_", names))
        return len(set(ids)) == len(ids)

    def _function_call(self) -> Union[FunctionCallNode, VariableAccessNode]:
        if self.current_token.type != TT_IDENTIFIER:
            return self._fail_with_invalid_syntax_error("Expected identifier",)
        var_name = StringToken.as_string_token(self.current_token)

        self.advance()

        arg_tokens: List[Node] = []
        while self.current_token.type in (
            TT_LPAREN,
            TT_IDENTIFIER,
            TT_INT,
            TT_FLOAT,
            TT_LBRACKET,
        ):
            arg_tokens.append(self.argument())

        if arg_tokens:
            return FunctionCallNode(var_name, arg_tokens)
        return VariableAccessNode(var_name)

    def _binary_operation(
        self,
        function: Callable[[], Node],
        operands: Union[List[str], List[Tuple[str, str]]],
        function2: Optional[Callable[[], Node]] = None,
    ) -> Node:
        if function2 is None:
            function2 = function

        left = function()
        while (
            self.current_token.type in operands
            or (self.current_token.type, self.current_token.value) in operands
        ):
            op_token = self.current_token
            self.advance()
            left = BinaryOperationNode(left, op_token, function2())

        return left

    def _get_variant_type_args(self) -> List[VariableAssignmentNode]:
        args: List[VariableAssignmentNode] = []
        was_asterix_in_variant_type = False
        while arg := self._get_variable_assignment(can_be_empty=True):
            if arg.is_empty():
                break
            if len(arg.names) == 1 and isinstance(arg.names[0], AsterixToken):
                if was_asterix_in_variant_type:
                    return self._fail_with_invalid_syntax_error(
                        'Unexpected multiple "*"'
                    )
                else:
                    was_asterix_in_variant_type = True
            args.append(arg)
        return args

    def _variant_type_identifier(self) -> TypeVariantNode:
        if self.current_token.type != TT_IDENTIFIER:
            return self._fail_with_invalid_syntax_error("Expected variant type name",)
        variant_type_name = StringToken.as_string_token(self.current_token)
        self.advance()

        args_tokens: List[StringToken] = []
        if self.current_token.matches(TT_KEYWORD, KEYWORDS["TYPE_DESCRIPTION"]):
            self.advance()
            while self.current_token.type == TT_IDENTIFIER:
                args_tokens.append(StringToken.as_string_token(self.current_token))
                if self.advance().type == TT_MUL:
                    if self.advance().type != TT_IDENTIFIER:
                        return self._fail_with_invalid_syntax_error(
                            "Expected type identifier",
                        )

        return TypeVariantNode(variant_type_name, args_tokens)

    def _match_case(self) -> MatchCaseNode:
        in_paren = False
        if self.current_token.type == TT_LPAREN:
            self.advance()
            in_paren = True
        types: List[Tuple[StringToken, List[VariableAssignmentNode]]] = []
        while True:
            if self.current_token.type != TT_IDENTIFIER:
                return self._fail_with_invalid_syntax_error("Expected type name",)
            type_name = StringToken.as_string_token(self.current_token)
            self.advance()

            types.append((type_name, self._get_variant_type_args()))
            if self.current_token.type == TT_COMA:
                self.advance()
            else:
                break
        if in_paren:
            if self.current_token.type != TT_RPAREN:
                return self._fail_with_invalid_syntax_error('Expected ")"')
            self.advance()
        if self.current_token.type != TT_ARROW:
            return self._fail_with_invalid_syntax_error('Expected "->"')
        self.advance()

        return MatchCaseNode(types, self._tuple())

    def _fail_with_invalid_syntax_error(self, msg: str) -> NoReturn:
        raise (
            InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end, msg
            )
        )

    # TODO support for tuples
    def _make_type_hint(self) -> Optional[Node]:
        if not self.current_token.type == TT_COLON:
            return None
        lparen = 0
        self.advance()
        ended = False
        while self.current_token.type in (TT_IDENTIFIER, TT_LPAREN) and not ended:
            if self.current_token.type == TT_LPAREN:
                lparen += 1

            if self.advance().type == TT_RPAREN:
                lparen -= 1
                self.advance()

            if self.current_token.type == TT_ARROW:
                self.advance()
            else:
                ended = True

        if ended and lparen == 0:
            return None
        return self._fail_with_invalid_syntax_error("Expected type hint")

    def _add_match(self, variable_name: VariableAssignmentNode) -> None:
        pos_start = variable_name.pos_start
        pos_end = variable_name.pos_end
        self._add_token(StringToken(TT_KEYWORD, pos_start, pos_end, KEYWORDS["WITH"],))
        names = variable_name.get_names()
        if len(names) != 1:
            raise InvalidSyntaxError(pos_start, pos_end, '"->" with invalid argument')
        for name in names:
            self._add_token(StringToken(TT_IDENTIFIER, pos_start, pos_end, name))

        self._add_token(StringToken(TT_KEYWORD, pos_start, pos_end, KEYWORDS["MATCH"]))

    def _add_token(self, token: Token) -> None:
        self.tokens.insert(self.token_index + 1, token)

    def _make_list(self) -> Union[ListNode, ListEndNode]:
        values: List[Node] = []
        should_end = False
        while self.current_token.type != TT_RBRACKET and not should_end:
            values.append(self.expression())
            if self.current_token.type == TT_LIST_SEP:
                self.advance()
            else:
                should_end = True
        end_token = self.current_token
        if end_token.type != TT_RBRACKET:
            self._fail_with_invalid_syntax_error(f'Expected "]"')
        self.advance()
        list_node: Union[ListNode, ListEndNode] = ListEndNode(
            EmptyToken.as_empty_token(end_token)
        )
        for value in reversed(values):
            list_node = ListNode(value, list_node)
        return list_node

    def _tuple(self) -> Node:
        nodes: List[Node] = [self.expression()]
        while self.current_token.type == TT_COMA:
            self.advance()
            nodes.append(self.expression())
        if len(nodes) == 1:
            return nodes[0]
        return TupleNode(nodes)
