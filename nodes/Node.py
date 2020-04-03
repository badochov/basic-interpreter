from Context import Context
from Position import Position
from RuntimeResult import RuntimeResult
from errors.NotImplError import NotImplError


class Node:
    def __init__(self, pos_start: Position = None, pos_end: Position = None):
        self.pos_start = pos_start
        self.pos_end = pos_end

    def visit(self, context: Context) -> RuntimeResult:
        return RuntimeResult().failure(
            NotImplError(self.pos_start, self.pos_end, "Visit")
        )
