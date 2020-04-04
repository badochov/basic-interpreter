from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from context import Context
    from nodes.node import Node
    from interpreter.runtime_result import RuntimeResult


class Interpreter:
    @staticmethod
    def visit(node: Node, context: Context) -> RuntimeResult:
        return node.visit(context)
