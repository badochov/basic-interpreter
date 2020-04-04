from __future__ import annotations

from typing import TYPE_CHECKING

from errors.error import Error

if TYPE_CHECKING:
    from position import Position


class InvalidSyntaxError(Error):
    def __init__(self, pos_start: Position, pos_end: Position, details: str):
        super().__init__(pos_start, pos_end, "Illegal Syntax", details)
