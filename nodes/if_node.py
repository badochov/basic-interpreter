from __future__ import annotations

from typing import TYPE_CHECKING

from errors.rt_error import RTError
from keywords import KEYWORDS
from lang_types.lang_bool import LangBool
from lang_types.lang_type import LangType
from nodes.node import Node

if TYPE_CHECKING:
    from context import Context


class IfNode(Node):
    __slots__ = ["condition_node", "then_node", "else_node"]

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

    def visit(self, context: Context) -> LangType:
        condition = self.condition_node.visit(context)

        if not isinstance(condition, LangBool):
            raise RTError(
                self.condition_node.pos_start,
                self.condition_node.pos_end,
                "Expected bool",
                context,
            )
        if condition.value:
            return self.then_node.visit(context)

        return self.else_node.visit(context)
