from __future__ import annotations

from typing import TYPE_CHECKING

from lang_types.lang_type import LangType

if TYPE_CHECKING:
    from context import Context
    from nodes.node import Node


class Interpreter:
    @staticmethod
    def visit(node: Node, context: Context) -> LangType:
        return node.visit(context)
