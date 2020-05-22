from __future__ import annotations

from typing import Optional, Union, Dict, TYPE_CHECKING, List

if TYPE_CHECKING:
    from lang_types.lang_type import LangType

    Value = LangType


class SymbolTable:
    __slots__ = ["symbols", "parent"]

    def __init__(self, parent: Optional[SymbolTable] = None) -> None:
        self.symbols: Dict[str, Value] = {}
        self.parent = parent

    def get(self, name: str) -> Optional[Value]:
        if name in self.symbols:
            return self.symbols[name]

        if self.parent:
            return self.parent.get(name)
        return None

    def set(self, name: str, value: Value) -> None:
        if name != "_":
            self.symbols[name] = value

    def remove(self, name: str) -> None:
        del self.symbols[name]

    def __repr__(self) -> str:
        s = ""
        for key, value in self.symbols.items():
            s += str(key) + ": " + str(value) + "\n"
        parent = "Parent\n" + str(self.parent)
        return s + parent.replace("\n", "\n\t")
