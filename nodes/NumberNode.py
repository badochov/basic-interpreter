from Context import Context
from RuntimeResult import RuntimeResult
from Token import Token
from nodes.Node import Node
from types_.Number import Number


class NumberNode(Node):
    def __init__(self, token: Token):
        super().__init__(token.pos_start, token.pos_end)
        self.token = token

    def __repr__(self) -> str:
        return f"{self.token}"

    def visit(self, context: Context) -> RuntimeResult:
        return RuntimeResult().success(
            Number(self.token.value)
            .set_context(context)
            .set_pos(self.pos_start, self.pos_end)
        )
