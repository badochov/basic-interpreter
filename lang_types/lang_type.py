from __future__ import annotations

from abc import ABC
from copy import copy
from typing import (
    TypeVar,
    TYPE_CHECKING,
    List,
    Any,
    Callable,
    Union,
)

from keywords import *


if TYPE_CHECKING:
    from context import Context
    from lang_types.lang_bool import LangBool


T = TypeVar("T", bound="LangType")


class LangType(ABC):
    __slots__ = ["type_name"]

    def __init__(self, type_name: str = "LangType"):
        self.type_name = type_name

    def copy(self: T) -> T:
        return copy(self)

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

    def notted(self) -> CompType:
        return self._not_impl(f'KEYWORD:{KEYWORDS["NOT"]}')

    def call(
        self, context: Context, args: List[LangType], add_parent: bool = True
    ) -> LangType:
        return self._not_impl("call")

    def _not_impl(self, error_msg: str) -> NotImplementedOperationType:
        return NotImplementedOperationType("Not implemented: " + error_msg)

    @property
    def value(self) -> Any:
        return None


def _try_oper(
    oper_by: OperFunction, oper_from: OperFunction, other: LangType,
) -> OperType:
    if not not_implemented(res := oper_by(other)):
        return res

    return oper_from(other)


def _try_logic_oper(
    oper_by: CompFunction, oper_from: CompFunction, other: LangType,
) -> CompType:
    if not not_implemented(res := oper_by(other)):
        return res

    return oper_from(other)


def add(first: LangType, second: LangType) -> OperType:
    return _try_oper(first.added_by, first.added_from, second)


def multiply(first: LangType, second: LangType) -> OperType:
    return _try_oper(first.multiplied_by, first.multiplied_from, second)


def subtract(first: LangType, second: LangType) -> OperType:
    return _try_oper(first.subtracted_by, first.subtracted_from, second)


def divide(first: LangType, second: LangType) -> OperType:
    return _try_oper(first.divided_by, first.divided_from, second)


def raise_to_power(first: LangType, second: LangType) -> OperType:
    return _try_oper(first.raised_to_power_by, first.raised_to_power_from, second)


def get_comparison_eq(first: LangType, second: LangType) -> CompType:
    return _try_logic_oper(
        first.get_comparison_eq_by, first.get_comparison_eq_from, second
    )


def get_comparison_ne(first: LangType, second: LangType) -> CompType:
    return _try_logic_oper(
        first.get_comparison_ne_by, first.get_comparison_ne_from, second
    )


def get_comparison_lt(first: LangType, second: LangType) -> CompType:
    return _try_logic_oper(
        first.get_comparison_lt_by, first.get_comparison_lt_from, second
    )


def get_comparison_gt(first: LangType, second: LangType) -> CompType:
    return _try_logic_oper(
        first.get_comparison_gt_by, first.get_comparison_gt_from, second
    )


def get_comparison_lte(first: LangType, second: LangType) -> CompType:
    return _try_logic_oper(
        first.get_comparison_lte_by, first.get_comparison_lte_from, second
    )


def get_comparison_gte(first: LangType, second: LangType) -> CompType:
    return _try_logic_oper(
        first.get_comparison_gte_by, first.get_comparison_gte_from, second
    )


def anded(first: LangType, second: LangType) -> CompType:
    return _try_logic_oper(first.anded_by, first.anded_from, second)


def ored(first: LangType, second: LangType) -> CompType:
    return _try_logic_oper(first.ored_by, first.ored_from, second)


def not_implemented(lang_type: LangType) -> bool:
    return isinstance(lang_type, NotImplementedOperationType)


class NotImplementedOperationType(LangType):
    def __init__(self, msg: str) -> None:
        super().__init__("NotImplementedType")
        self.msg = msg


if TYPE_CHECKING:
    OperType = LangType

    CompType = Union[LangBool, NotImplementedOperationType]
    OperFunction = Callable[[LangType], OperType]
    CompFunction = Callable[[LangType], CompType]
