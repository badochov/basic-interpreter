from __future__ import annotations

from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from position import Position


class Token:
    def __init__(
        self,
        type_: str,
        pos_start: Position,
        pos_end: Position,
        value: Union[str, float] = None,
    ):
        self.type = type_
        self.value = value
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy().advance()
        if pos_end:
            self.pos_end = pos_end.copy()

    def matches(self, type_: str, value: str) -> bool:
        return self.type == type_ and self.value == value

    def __repr__(self) -> str:
        if self.value is not None:
            return f"{self.type}:{self.value}"
        return f"{self.type}"
