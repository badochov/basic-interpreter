from __future__ import annotations

from typing import List, Iterable

from lang_types.lang_type import LangType
from lang_types.lang_variant_type import LangVariantType


class LangTuple(LangType):
    def __init__(self, values: List[LangType]):
        super().__init__("variant_type")
        self.values = values

    def __repr__(self) -> str:
        return f"Tuple: {self.values}"

    def values_count(self) -> int:
        return len(self.values)

    def nth_value(self, n: int) -> LangType:
        return self.values[n]

    def is_of_type(self, names: Iterable[str]) -> bool:
        for i, name in enumerate(names):
            value = self.nth_value(i)
            if not isinstance(value, LangVariantType) or not value.is_of_type(name):
                return False
        return True

    def nth_value_args(self, n: int) -> List[LangType]:
        value = self.nth_value(n)
        return value.args if isinstance(value, LangVariantType) else []
