from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, NoReturn

from errors.rt_error import RTError
from lang_types.lang_type import LangType

if TYPE_CHECKING:
    from context import Context
    from position import Position


class Node(ABC):
    def __init__(self, pos_start: Position, pos_end: Position):
        self.pos_start = pos_start
        self.pos_end = pos_end

    @abstractmethod
    def visit(self, context: Context) -> LangType:
        ...

    def _fail_with(self, msg: str, context: Context) -> NoReturn:
        raise RTError(self.pos_start, self.pos_end, msg, context)
