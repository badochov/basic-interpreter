from Context import Context
from RuntimeResult import RuntimeResult
from Token import Token
from nodes.Node import Node
from token_types import *
from types_.Number import Number


class UnaryOperationNode(Node):
    def __init__(self, operation_token: Token, node: Node):
        super().__init__(operation_token.pos_start, node.pos_end)
        self.operation_token = operation_token
        self.node = node

    def __repr__(self) -> str:
        return f"({self.operation_token} {self.node})"

    def visit(self, context: Context) -> RuntimeResult:
        res = RuntimeResult()
        result = res.register(self.node.visit(context))
        if res.error:
            return res

        error = None
        if self.operation_token.type == TT_MINUS:
            result, error = result.multiplied_by(Number(-1))
        if error:
            return res.failure(error)
        return res.success(result.set_pos(self.pos_start, self.pos_end))
