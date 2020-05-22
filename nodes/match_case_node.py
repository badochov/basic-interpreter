from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING, Tuple, Union

from context import Context, mock_context
from lang_types.lang_tuple import LangTuple
from lang_types.lang_type import LangType
from nodes.node import Node
from nodes.variable_assignment_node import VariableAssignmentNode, VariableType
from position import mock_position
from symbol_table import SymbolTable

if TYPE_CHECKING:
    from lang_types.lang_variant_type import LangVariantType
    from tokens.lang_string_token import StringToken


class LangNoMatchType(LangType):
    @staticmethod
    def instance() -> LangNoMatchType:
        return LangNoMatchType("no-match", mock_position, mock_position, mock_context)


# TODO add support for tuples
class MatchCaseNode(Node):
    def __init__(
        self,
        types: List[Tuple[StringToken, List[VariableAssignmentNode]]],
        expr_node: Node,
    ):
        super().__init__(types[0][0].pos_start, expr_node.pos_end)
        self.types = types
        self.expr_node = expr_node
        self.var: Optional[Union[LangTuple, LangVariantType]] = None

    def __repr__(self) -> str:
        res = "(("
        for type_desc in self.types:
            res += f"{type_desc[0]}("
            for case_node in type_desc[1]:
                res += f"{case_node},"
            res += ", "
        res += f") -> {self.expr_node}"
        return res + ")"

    def set_matched_variable(self, var: Union[LangTuple, LangVariantType]) -> None:
        self.var = var

    def visit(self, context: Context) -> LangType:
        assert self.var is not None

        type_name = self.types[0][0].value
        arg_tokens = self.types[0][1]

        new_ctx = Context(f"Case {type_name}", SymbolTable(), context, self.pos_start,)
        every = type_name == "_"

        if every:
            if arg_tokens:
                return self._fail_with("Unexpected arguments", context)
        else:
            if isinstance(self.var, LangTuple):
                return self._handle_tuple(context)
            if not self.var.is_of_type(type_name):
                return LangNoMatchType.instance()
            node = self._convert_nth_value_to_assignment_node(self.types[0])
            node.set_value(self.var)
            node.visit(context)
        return self.expr_node.visit(new_ctx)

    @staticmethod
    def _convert_nth_value_to_assignment_node(
        type_: Tuple[StringToken, List[VariableAssignmentNode]]
    ) -> VariableAssignmentNode:
        return VariableAssignmentNode([type_[0], *type_[1]], VariableType.VariantType)

    def _handle_tuple(self, context: Context) -> LangType:
        assert isinstance(self.var, LangTuple)
        type_names = map(lambda type_desc: type_desc[0].value, self.types)
        if not self.var.is_of_type(type_names):
            return LangNoMatchType.instance()
        new_ctx = Context(
            f"Case {list(type_names)}", SymbolTable(), context, self.pos_start,
        )
        node = VariableAssignmentNode(
            [self._convert_nth_value_to_assignment_node(value) for value in self.types]
        )
        node.set_value(self.var)
        node.visit(context)
        return self.expr_node.visit(new_ctx)
