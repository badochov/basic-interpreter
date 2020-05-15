from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from interpreter.runtime_result import RuntimeResult
    from context import Context
    from position import Position


class Node(ABC):
    def __init__(self, pos_start: Position, pos_end: Position):
        self.pos_start = pos_start
        self.pos_end = pos_end

    @abstractmethod
    def visit(self, context: Context) -> RuntimeResult:
        raise NotImplemented
