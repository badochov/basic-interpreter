from __future__ import annotations

from typing import TYPE_CHECKING, Union

from lang_types.lang_bool import LangBool
from lang_types.lang_type import (
    LangType,
    NotImplementedOperationType,
    IllegalOperationType,
)

if TYPE_CHECKING:
    from lang_types.lang_type import CompType


class LangNumber(LangType):
    __slots__ = ["_value"]

    def __init__(self, value: float):
        super().__init__("number")
        self._value = value

    @property
    def value(self) -> float:
        return self._value

    def added_by(self, other: LangType) -> OperType:
        if isinstance(other, LangNumber):
            return LangNumber(self._value + other._value)
        return self._not_impl("-")

    def multiplied_by(self, other: LangType) -> OperType:
        if isinstance(other, LangNumber):
            return LangNumber(self._value * other._value)
        return self._not_impl("*")

    def subtracted_by(self, other: LangType) -> OperType:
        if isinstance(other, LangNumber):
            return LangNumber(self._value - other._value)
        return self._not_impl("-")

    def divided_by(self, other: LangType) -> Union[OperType, IllegalOperationType]:
        if isinstance(other, LangNumber):
            if other._value == 0:
                return IllegalOperationType("Division by zero")

            return LangNumber(self._value / other._value)
        return self._not_impl("/")

    def raised_to_power_by(self, other: LangType) -> OperType:
        if isinstance(other, LangNumber):
            return LangNumber(self._value ** other._value)
        return self._not_impl("^")

    def get_comparison_eq_by(self, other: LangType) -> CompType:
        if isinstance(other, LangNumber):
            return LangBool((self._value == other.value))

        return super().get_comparison_eq(other)

    def get_comparison_lt_by(self, other: LangType) -> CompType:
        if isinstance(other, LangNumber):
            return LangBool((self._value < other.value))

        return super().get_comparison_lt(other)

    def get_comparison_gt_by(self, other: LangType) -> CompType:
        if isinstance(other, LangNumber):
            return LangBool((self._value > other.value))

        return super().get_comparison_gt(other)

    def get_comparison_lte_by(self, other: LangType) -> CompType:
        if isinstance(other, LangNumber):
            return LangBool((self._value <= other.value))

        return super().get_comparison_lte(other)

    def get_comparison_gte_by(self, other: LangType) -> CompType:
        if isinstance(other, LangNumber):
            return LangBool((self._value >= other.value))

        return super().get_comparison_gte(other)

    def __repr__(self) -> str:
        return f"{self._value}"


if TYPE_CHECKING:
    OperType = Union[LangNumber, NotImplementedOperationType]
