from __future__ import annotations

from typing import Optional, Union, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from types_.type import Type

    Value = Type


class SymbolTable:
    def __init__(self) -> None:
        self.symbols: Dict[str, Value] = {}
        self.parent: Optional[SymbolTable] = None

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