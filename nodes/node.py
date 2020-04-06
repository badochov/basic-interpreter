from __future__ import annotations

from typing import TYPE_CHECKING, Union

from interpreter.runtime_result import RuntimeResult

if TYPE_CHECKING:
    from context import Context
    from position import Position
    from errors.not_impl_error import NotImplError


class Node:
    def __init__(self, pos_start: Position, pos_end: Position):
        self.pos_start = pos_start
        self.pos_end = pos_end

    def visit(self, context: Context) -> RuntimeResult:
        return RuntimeResult().failure(
            NotImplError(self.pos_start, self.pos_end, "Visit")
        )
