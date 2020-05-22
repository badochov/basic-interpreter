from __future__ import annotations

from typing import TYPE_CHECKING, List

from lang_types.lang_tuple import LangTuple
from nodes.node import Node

if TYPE_CHECKING:
    from context import Context


class TupleNode(Node):
    def __init__(self, arg_nodes: List[Node]):
        super().__init__(arg_nodes[0].pos_start, arg_nodes[-1].pos_end)
        self.arg_nodes = arg_nodes

    def __repr__(self) -> str:
        return f"({self.arg_nodes})"

    def visit(self, context: Context) -> LangTuple:
        return LangTuple(list(map(lambda node: node.visit(context), self.arg_nodes)))
