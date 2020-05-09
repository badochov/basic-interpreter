from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from interpreter.runtime_result import RuntimeResult
from lang_token import Token
from lang_types.lang_variant_type import LangVariantType
from nodes.node import Node

if TYPE_CHECKING:
    from context import Context


class MatchCaseNode(Node):
    def __init__(
        self, type_variant_name_token: Token, arg_nodes: List[Token], expr_node: Node
    ):
        super().__init__(type_variant_name_token.pos_start, expr_node.pos_end)
        self.type_variant_name_token = type_variant_name_token
        self.arg_nodes = arg_nodes
        self.expr_node = expr_node
        self.var: Optional[LangVariantType] = None

    def __repr__(self) -> str:
        res = "(" + f"{self.expr_node}("
        for case_node in self.arg_nodes:
            res += f"{case_node},"

        return ")" + res + ")"

    def set_matched_variable(self, var: LangVariantType) -> None:
        self.var = var

    def visit(self, context: Context) -> RuntimeResult:
        res = RuntimeResult()
        return res
        condition = res.register(self.condition_node.visit(context))
        if res.error or condition is None:
            return res

        if condition.is_truthy():
            node = res.register(self.then_node.visit(context))
            if res.error or node is None:
                return res
            return res.success(node)

        node = res.register(self.else_node.visit(context))
        if res.error or node is None:
            return res
        return res.success(node)
