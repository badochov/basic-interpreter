from Position import Position
from typing import Union


class Token:
    def __init__(self, type_: str, value: Union[str, float] = None, pos_start: Position = None,
                 pos_end: Position = None):
        self.type = type_
        self.value = value
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy().advance()
        if pos_end:
            self.pos_end = pos_end.copy()

    def __repr__(self):
        if self.value:
            return f"{self.type}:{self.value}"
        return f"{self.type}"
