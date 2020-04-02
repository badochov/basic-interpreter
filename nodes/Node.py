from Context import Context
from Position import Position


class Node:
    def __init__(self, pos_start: Position = None, pos_end: Position = None):
        self.pos_start = pos_start
        self.pos_end = pos_end

    def visit(self, context: Context):
        raise NotImplementedError(f'No visit method for node type: {type(self)}')
