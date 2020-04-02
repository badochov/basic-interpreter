from nodes.Node import Node
from token_types import *
from Token import Token
from RuntimeResult import RuntimeResult
from Context import Context


class BinaryOperationNode(Node):
    def __init__(self, left_node: Node, operation_token: Token, right_node: Node):
        super().__init__(left_node.pos_start, right_node.pos_end)
        self.left_node = left_node
        self.operation_token = operation_token
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.operation_token}, {self.right_node})'

    def visit(self, context: Context):
        res = RuntimeResult()
        left = res.register(self.left_node.visit(context))
        if res.error:
            return res
        right = res.register(self.right_node.visit(context))
        if res.error:
            return res

        result = None

        if self.operation_token.type == TT_PLUS:
            result, error = left.added_to(right)
        elif self.operation_token.type == TT_MINUS:
            result, error = left.subtracted_by(right)
        elif self.operation_token.type == TT_MUL:
            result, error = left.multiplied_by(right)
        elif self.operation_token.type == TT_DIV:
            result, error = left.divided_by(right)
        else:
            error = RuntimeError(f'Operation not found {self.operation_token.type}')

        if error:
            return res.failure(error)
        return res.success(result.set_pos(self.pos_start, self.pos_end))
