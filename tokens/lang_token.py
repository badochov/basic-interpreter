from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, TypeVar, Generic

if TYPE_CHECKING:
    from position import Position

T = TypeVar("T")


class Token(ABC, Generic[T]):
    def __init__(
        self, type_: str, pos_start: Position, pos_end: Position, value: T,
    ) -> None:
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
