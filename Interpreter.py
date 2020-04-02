from Context import Context
from nodes.Node import Node


class Interpreter:
    @staticmethod
    def visit(node: Node, context: Context):
        return node.visit(context)
