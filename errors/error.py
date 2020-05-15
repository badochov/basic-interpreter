from __future__ import annotations

from typing import TYPE_CHECKING

from errors.string_with_arrows import string_with_arrows

if TYPE_CHECKING:
    from position import Position


class Error(BaseException):
    def __init__(
        self, pos_start: Position, pos_end: Position, error_name: str, details: str
    ):
        self.error_name = error_name
        self.details = details
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __str__(self) -> str:
        result = f"{self.error_name}: {self.details}\n"
        result += f"File {self.pos_start.file_name}, line {self.pos_start.line + 1}"
        result += "\n\n" + string_with_arrows(
            self.pos_start.file_content, self.pos_start, self.pos_end
        )
        return result
