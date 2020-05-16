from __future__ import annotations

from typing import TYPE_CHECKING, List

from errors.rt_error import RTError
from keywords import KEYWORDS
from lang_types.lang_type import LangType
from lang_types.lang_variant_type import LangVariantType
from nodes.match_case_node import MatchCaseNode, LangNoMatchType
from nodes.node import Node

if TYPE_CHECKING:
    from context import Context


class MatchNode(Node):
    def __init__(self, var_node: Node, cases_nodes: List[MatchCaseNode]):
        super().__init__(var_node.pos_start, cases_nodes[-1].pos_end)
        self.var_node = var_node
        self.cases_nodes = cases_nodes

    def __repr__(self) -> str:
        res = "(" + f'{KEYWORDS["MATCH"]} {self.var_node} WITH'
        for case_node in self.cases_nodes:
            res += f'\n{KEYWORDS["MATCH_OR"]} {case_node}'
        return res + ")"

    def visit(self, context: Context) -> LangType:
        var = self.var_node.visit(context)
        if not isinstance(var, LangVariantType):
            raise RTError(
                self.pos_start, self.pos_end, "Expected variant type", context
            )

        for case_node in self.cases_nodes:
            case_node.set_matched_variable(var)
            case_out = case_node.visit(context)
            if not isinstance(case_out, LangNoMatchType):
                return case_out

        raise RTError(self.pos_start, self.pos_end, "No match", context)
