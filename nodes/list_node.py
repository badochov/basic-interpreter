from __future__ import annotations

from typing import TYPE_CHECKING

from lang_types.lang_variant_type import LangVariantType
from nodes.node import Node
from tokens.lang_empty_token import EmptyToken

if TYPE_CHECKING:
    from context import Context


class ListNode(Node):
    def __init__(self, value_node: Node, tail_node: Node):
        super().__init__(value_node.pos_start, tail_node.pos_end)
        self.value_node = value_node
        self.tail_node = tail_node

    def __repr__(self) -> str:
        return f"{self.value_node} {self.tail_node}"

    def visit(self, context: Context) -> LangVariantType:
        return LangVariantType(
            [self.value_node.visit(context), self.tail_node.visit(context)],
            "List",
            self.pos_start,
            self.pos_end,
            context,
        )


class ListEndNode(Node):
    def __init__(self, end_token: EmptyToken):
        super().__init__(end_token.pos_start, end_token.pos_end)
        self.end_token = end_token

    def __repr__(self) -> str:
        return f"Empty"

    def visit(self, context: Context) -> LangVariantType:
        return LangVariantType([], "Empty", self.pos_start, self.pos_end, context,)
