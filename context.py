from __future__ import annotations

from typing import TYPE_CHECKING

from symbol_table import SymbolTable

if TYPE_CHECKING:
    from position import Position


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


mock_context = Context("", SymbolTable())
