from __future__ import annotations

from typing import List, TYPE_CHECKING

from lang_types.lang_type import LangType

if TYPE_CHECKING:
    from position import Position
    from context import Context


class LangVariantType(LangType):
    def __init__(
        self,
        args: List[LangType],
        name: str,
        pos_start: Position,
        pos_end: Position,
        context: Context,
    ):
        super().__init__("variant_type", pos_start, pos_end, context)
        self.args = args
        self.type_variant_name = name

    def __repr__(self) -> str:
        return f"{self.type_variant_name} of {self.args}"

    def is_of_type(self, name: str) -> bool:
        return name == self.type_variant_name
