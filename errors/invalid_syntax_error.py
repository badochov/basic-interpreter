from __future__ import annotations

from typing import TYPE_CHECKING

from errors.error import Error

if TYPE_CHECKING:
    from position import Position


class InvalidSyntaxError(Error):
    def __init__(self, pos_start: Position, pos_end: Position, details: str):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.message = "Illegal Syntax:" + details
