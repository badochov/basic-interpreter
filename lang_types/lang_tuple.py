from __future__ import annotations

from typing import List, Iterable, TYPE_CHECKING

from lang_types.lang_type import LangType
from lang_types.lang_variant_type import LangVariantType

from keywords import KEYWORDS

if TYPE_CHECKING:
    from lang_types.lang_type import OperType, CompType


class LangTuple(LangType):
    __slots__ = ["_values"]

    def __init__(self, values: List[LangType]):
        super().__init__("variant_type")
        self._values = values

    def __repr__(self) -> str:
        return f"Tuple: {self._values}"

    def values_count(self) -> int:
        return len(self._values)

    def nth_value(self, n: int) -> LangType:
        return self._values[n]

    def is_of_type(self, names: Iterable[str]) -> bool:
        for i, name in enumerate(names):
            value = self.nth_value(i)
            if not isinstance(value, LangVariantType) or not value.is_of_type(name):
                return False
        return True

    def nth_value_args(self, n: int) -> List[LangType]:
        value = self.nth_value(n)
        return value.args if isinstance(value, LangVariantType) else []

    def added_by(self, other: LangType) -> OperType:
        return self._not_impl("+")

    def multiplied_by(self, other: LangType) -> OperType:
        return self._not_impl("*")

    def subtracted_by(self, other: LangType) -> OperType:
        return self._not_impl("-")

    def divided_by(self, other: LangType) -> OperType:
        return self._not_impl("/")

    def raised_to_power_by(self, other: LangType) -> OperType:
        return self._not_impl("^")

    def get_comparison_eq_by(self, other: LangType) -> CompType:
        return self._not_impl("==")

    def get_comparison_ne_by(self, other: LangType) -> CompType:
        return self._not_impl("!=")

    def get_comparison_lt_by(self, other: LangType) -> CompType:
        return self._not_impl("<")

    def get_comparison_gt_by(self, other: LangType) -> CompType:
        return self._not_impl(">")

    def get_comparison_lte_by(self, other: LangType) -> CompType:
        return self._not_impl("<=")

    def get_comparison_gte_by(self, other: LangType) -> CompType:
        return self._not_impl(">=")

    def anded_by(self, other: LangType) -> CompType:
        return self._not_impl(f'KEYWORD:{KEYWORDS["AND"]}')

    def ored_by(self, other: LangType) -> CompType:
        return self._not_impl(f'KEYWORD:{KEYWORDS["OR"]}')

    def added_from(self, other: LangType) -> OperType:
        return self._not_impl("+")

    def multiplied_from(self, other: LangType) -> OperType:
        return self._not_impl("*")

    def subtracted_from(self, other: LangType) -> OperType:
        return self._not_impl("-")

    def divided_from(self, other: LangType) -> OperType:
        return self._not_impl("/")

    def raised_to_power_from(self, other: LangType) -> OperType:
        return self._not_impl("^")

    def get_comparison_eq_from(self, other: LangType) -> CompType:
        return self._not_impl("==")

    def get_comparison_ne_from(self, other: LangType) -> CompType:
        return self._not_impl("!=")

    def get_comparison_lt_from(self, other: LangType) -> CompType:
        return self._not_impl("<")

    def get_comparison_gt_from(self, other: LangType) -> CompType:
        return self._not_impl(">")

    def get_comparison_lte_from(self, other: LangType) -> CompType:
        return self._not_impl("<=")

    def get_comparison_gte_from(self, other: LangType) -> CompType:
        return self._not_impl(">=")

    def anded_from(self, other: LangType) -> CompType:
        return self._not_impl(f'KEYWORD:{KEYWORDS["AND"]}')

    def ored_from(self, other: LangType) -> CompType:
        return self._not_impl(f'KEYWORD:{KEYWORDS["OR"]}')
