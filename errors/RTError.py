from typing import Optional

from Context import Context
from Position import Position
from errors.Error import Error
from errors.string_with_arrows import string_with_arrows


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
        ctx: Optional[Context] = self.context

        while ctx:
            result = (
                f"  File {pos.file_name}, line {pos.line + 1}, in {ctx.display_name}\n"
                + result
            )
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return "Traceback (most recent call last):\n" + result
