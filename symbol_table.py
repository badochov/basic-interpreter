from __future__ import annotations

from typing import Optional, Union, Dict, TYPE_CHECKING, List

if TYPE_CHECKING:
    from lang_types.lang_type import LangType

    Value = LangType


class SymbolTable:
    def __init__(self, parent: SymbolTable = None) -> None:
        self.symbols: Dict[str, Value] = {}
        self.parents: List[Optional[SymbolTable]] = [parent]

    def get(self, name: str) -> Union[Value, None]:
        if name in self.symbols:
            return self.symbols[name]

        for parent in self.parents:
            if parent:
                val = parent.get(name)
                if val:
                    return val
        return None

    def set(self, name: str, value: Value) -> None:
        self.symbols[name] = value

    def remove(self, name: str) -> None:
        del self.symbols[name]

    def add_parent(self, table: Optional[SymbolTable]) -> SymbolTable:
        self.parents.insert(0, table)
        return self

    def __repr__(self) -> str:
        s = ""
        for key, value in self.symbols.items():
            s += str(key) + ": " + str(value) + "\n"
        parent = "Parent\n" + str(self.parents)
        return s + parent.replace("\n", "\n\t")
