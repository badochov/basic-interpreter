from __future__ import annotations

from typing import TYPE_CHECKING, Union

from symbol_table import SymbolTable

if TYPE_CHECKING:
    from position import Position

    from lang_types.lang_type import LangType

    Value = LangType


class Context:
    def __init__(
        self,
        display_name: str,
        symbol_table: SymbolTable,
        parent: Context = None,
        parent_entry_pos: Position = None,
    ):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos

        self.symbol_table = symbol_table

    def get(self, name: str) -> Union[Value, None]:
        val = self.symbol_table.get(name)
        if val:
            return val
        if self.parent:
            return self.parent.get(name)
        return None


mock_context = Context("", SymbolTable())
