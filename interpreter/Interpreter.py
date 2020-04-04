from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Context import Context
    from nodes.Node import Node
    from interpreter.RuntimeResult import RuntimeResult


class Interpreter:
    @staticmethod
    def visit(node: Node, context: Context) -> RuntimeResult:
        return node.visit(context)
