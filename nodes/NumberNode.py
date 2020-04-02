from nodes.Node import Node
from types_.Number import Number
from Token import Token
from RuntimeResult import RuntimeResult
from Context import Context


class NumberNode(Node):
    def __init__(self, token: Token):
        super().__init__(token.pos_start, token.pos_end)
        self.token = token

    def __repr__(self):
        return f"{self.token}"

    def visit(self, context: Context):
        return RuntimeResult().success(
            Number(self.token.value)
            .set_context(context)
            .set_pos(self.pos_start, self.pos_end)
        )
