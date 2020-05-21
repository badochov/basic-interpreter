from __future__ import annotations

from typing import TYPE_CHECKING

from errors.error import Error
from errors.string_with_arrows import string_with_arrows

if TYPE_CHECKING:
    from context import Context
    from position import Position


class RTError(Error):
    def __init__(
        self, pos_start: Position, pos_end: Position, details: str, context: Context
    ):
        super().__init__(pos_start, pos_end, "Runtime Error", details)
        self.context = context

    def __str__(self) -> str:
        result = self.generate_traceback()
        result += f"{self.error_name}: {self.details}"
        result += "\n\n" + string_with_arrows(
            self.pos_start.file_content, self.pos_start, self.pos_end
        )
        return result

    def generate_traceback(self) -> str:
        result = ""
        pos = self.pos_start
        q = [self.context]
        for ctx in q:
            result = (
                f"  File {pos.file_name}, line {pos.line + 1}, in {ctx.display_name}\n"
                + result
            )
            if ctx.parent_entry_pos is None:
                break
            pos = ctx.parent_entry_pos
            for parent in ctx.parents:
                q.append(parent)

        return "Traceback (most recent call last):\n" + result
