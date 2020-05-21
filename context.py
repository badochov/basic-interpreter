from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from symbol_table import SymbolTable

if TYPE_CHECKING:
    from position import Position
    from symbol_table import Value


class Context:
    def __init__(
        self,
        display_name: str,
        symbol_table: SymbolTable,
        parent: Optional[Context] = None,
        parent_entry_pos: Optional[Position] = None,
    ):
        self.display_name = display_name
        self.parents: List[Context] = [parent] if parent else []
        self.parent_entry_pos = parent_entry_pos

        self.symbol_table = symbol_table

    def get(self, name: str) -> Optional[Value]:
        if val := self.symbol_table.get(name):
            return val
        for parent in reversed(self.parents):
            if val := parent.get(name):
                return val
        return None

    def add_parent(self, context: Optional[Context]) -> Context:
        if context:
            self.parents.append(context)
        return self

    def set(self, name: str, value: Value) -> None:
        self.symbol_table.set(name, value)

    def __repr__(self) -> str:
        parent = "Parent\n" + str(self.parents)
        return str(self.symbol_table) + parent.replace("\n", "\n\t")


mock_context = Context("", SymbolTable())
