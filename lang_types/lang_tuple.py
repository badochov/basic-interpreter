from __future__ import annotations

from typing import List, TYPE_CHECKING

from lang_types.lang_type import LangType

if TYPE_CHECKING:
    from position import Position
    from context import Context


class LangTuple(LangType):
    def __init__(
        self,
        values: List[LangType],
        pos_start: Position,
        pos_end: Position,
        context: Context,
    ):
        super().__init__("variant_type", pos_start, pos_end, context)
        self.values = values

    def __repr__(self) -> str:
        return f"Tuple: {self.values}"

    def values_count(self) -> int:
        return len(self.values)

    def nth_value(self, n: int) -> LangType:
        return self.values[n]
