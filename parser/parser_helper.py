from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

from errors.invalid_syntax_error import InvalidSyntaxError
from nodes.function_definition_node import FunctionDefinitionNode
from token_types import *
from position import mock_position
from tokens.lang_asterix_token import AsterixToken
from tokens.lang_string_token import StringToken
from nodes.variable_assignment_node import VariableAssignmentNode, VariableType

if TYPE_CHECKING:
    from parser.parser import Parser
    from nodes.node import Node
    from nodes.variable_assignment_node import NamesType


class ParserHelper:
    def __init__(self, parser: Parser) -> None:
        self.parser = parser

    def get_variable_assignment(
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
            if self.parser.current_token.type == TT_IDENTIFIER:
                self._handle_identifier(names, can_be_variant_type)
            elif self.parser.current_token.type == TT_MUL:
                was_asterix = self._handle_asterix(names, var_type, was_asterix)
            elif self.parser.current_token.type == TT_LBRACKET:
                self._handle_list(names)
            elif self.parser.current_token.type == TT_LPAREN:
                self._handle_tuple(names)
            else:
                if not can_be_empty:
                    return self.parser.fail_with_invalid_syntax_error("Expected name")
                break
            if self.parser.current_token.type == TT_COMA:
                if break_on_coma:
                    break
                self.parser.advance()
            else:
                break

        if len(names) > 1:
            if not in_paren and tuple_in_paren and var_type is not VariableType.List:
                return self.parser.fail_with_invalid_syntax_error(
                    "This tuple was expected to be in parentheses"
                )
        if (
            len(names) == 1
            and isinstance(names[0], VariableAssignmentNode)
            and var_type is VariableType.Tuple
        ):
            return names[0]
        return VariableAssignmentNode(names, var_type)

    def get_variant_type_args(self) -> List[VariableAssignmentNode]:
        args: List[VariableAssignmentNode] = []
        was_asterix_in_variant_type = False
        while arg := self.get_variable_assignment(can_be_empty=True):
            if arg.is_empty():
                break
            if len(arg.names) == 1 and isinstance(arg.names[0], AsterixToken):
                if was_asterix_in_variant_type:
                    return self.parser.fail_with_invalid_syntax_error(
                        'Unexpected multiple "*"'
                    )
                else:
                    was_asterix_in_variant_type = True
            args.append(arg)
        return args

    # TODO support for tuples, lists
    def make_type_hint(self) -> Optional[Node]:
        if not self.parser.current_token.type == TT_COLON:
            return None
        lparen = 0
        self.parser.advance()
        ended = False
        while (
            self.parser.current_token.type in (TT_IDENTIFIER, TT_LPAREN) and not ended
        ):
            if self.parser.current_token.type == TT_LPAREN:
                lparen += 1

            if self.parser.advance().type == TT_RPAREN:
                lparen -= 1
                self.parser.advance()

            if self.parser.current_token.type == TT_ARROW:
                self.parser.advance()
            else:
                ended = True

        if ended and lparen == 0:
            return None
        return self.parser.fail_with_invalid_syntax_error("Expected type hint")

    @staticmethod
    def make_function_definition(
        var_name: Optional[VariableAssignmentNode],
        args: List[VariableAssignmentNode],
        body: Node,
    ) -> FunctionDefinitionNode:
        names: List[str] = [
            *([name for name in var_name.get_names()] if var_name else []),
            *[name for arg in args for name in arg.get_names()],
        ]
        if not ParserHelper._check_if_names_are_distinct(names):
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

    def _handle_identifier(self, names: NamesType, can_be_variant_type: bool) -> None:
        name_token = StringToken.as_string_token(self.parser.current_token)
        self.parser.advance()
        if can_be_variant_type:
            args = self.get_variant_type_args()

            if args:
                return names.append(
                    VariableAssignmentNode(
                        args, VariableType.VariantType, name_token.value
                    )
                )

        names.append(name_token)
        self.make_type_hint()

    def _handle_asterix(
        self, names: NamesType, var_type: VariableType, was_asterix: bool
    ) -> bool:
        if was_asterix:
            return self.parser.fail_with_invalid_syntax_error('Unexpected multiple "*"')
        asterix_token = self.parser.current_token
        self.parser.advance()
        if self.parser.current_token.type == TT_IDENTIFIER:
            if var_type is VariableType.List:
                names.append(
                    AsterixToken.from_string_token(
                        StringToken.as_string_token(self.parser.current_token)
                    )
                )
            else:
                return self.parser.fail_with_invalid_syntax_error('Unexpected "*"')
            self.parser.advance()
            self.make_type_hint()
        else:
            names.append(
                AsterixToken(asterix_token.pos_start, asterix_token.pos_end, "_")
            )
        return True

    def _handle_list(self, names: NamesType) -> None:
        self.parser.advance()
        names.append(self.get_variable_assignment(True, VariableType.List, True))
        if self.parser.current_token.type == TT_RBRACKET:
            self.parser.advance()
        else:
            return self.parser.fail_with_invalid_syntax_error('Expected "]"')

    def _handle_tuple(self, names: NamesType) -> None:
        self.parser.advance()
        names.append(
            self.get_variable_assignment(False, VariableType.Tuple, True, False, True)
        )
        if self.parser.current_token.type == TT_RPAREN:
            self.parser.advance()
        else:
            return self.parser.fail_with_invalid_syntax_error('Expected ")"')
