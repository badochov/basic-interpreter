from __future__ import annotations

from typing import TYPE_CHECKING

from interpreter.runtime_result import RuntimeResult
from keywords import KEYWORDS
from nodes.node import Node
from lang_types.lang_number import LangNumber

if TYPE_CHECKING:
    from context import Context


class IfNode(Node):
    def __init__(self, condition_node: Node, then_node: Node, else_node: Node):
        super().__init__(condition_node.pos_start, else_node.pos_end)
        self.condition_node = condition_node
        self.then_node = then_node
        self.else_node = else_node

    def __repr__(self) -> str:
        return (
            "("
            f'{KEYWORDS["IF"]} {self.condition_node} '
            f'{KEYWORDS["THEN"]} {self.then_node} '
            f'{KEYWORDS["ELSE"]} {self.else_node}'
            ")"
        )

    def visit(self, context: Context) -> RuntimeResult:
        res = RuntimeResult()
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
