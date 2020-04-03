from Context import Context
from nodes.Node import Node
from RuntimeResult import RuntimeResult


class Interpreter:
    @staticmethod
    def visit(node: Node, context: Context) -> RuntimeResult:
        return node.visit(context)
