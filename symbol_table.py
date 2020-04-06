from __future__ import annotations

from typing import Optional, Union, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from lang_types.lang_type import LangType

    Value = LangType


class SymbolTable:
    def __init__(self, parent: SymbolTable = None) -> None:
        self.symbols: Dict[str, Value] = {}
        self.parent: Optional[SymbolTable] = parent

    def get(self, name: str) -> Union[Value, None]:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.get(name)
        return None

    def set(self, name: str, value: Value) -> None:
        self.symbols[name] = value

    def remove(self, name: str) -> None:
        del self.symbols[name]

    def add_root(self, table: Optional[SymbolTable]) -> SymbolTable:
        if self.parent:
            self.parent.add_root(table)
        else:
            self.parent = table
        return self
