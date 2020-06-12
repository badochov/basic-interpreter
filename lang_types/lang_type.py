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
    final,
    Optional,
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

    def get_comparison_lt_by(self, other: LangType) -> CompType:
        return self._not_impl("<")

    def get_comparison_gt_by(self, other: LangType) -> CompType:
        return self._not_impl(">")

    def get_comparison_lte_by(self, other: LangType) -> CompType:
        return self._not_impl("<=")

    def get_comparison_gte_by(self, other: LangType) -> CompType:
        return self._not_impl(">=")

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

    @final
    def add(self, other: LangType) -> OperType:
        return self._try_oper(self.added_by, self.added_from, other)

    @final
    def multiply(self, other: LangType) -> OperType:
        return self._try_oper(self.multiplied_by, self.multiplied_from, other)

    @final
    def subtract(self, other: LangType) -> OperType:
        return self._try_oper(self.subtracted_by, self.subtracted_from, other)

    @final
    def divide(self, other: LangType) -> OperType:
        return self._try_oper(self.divided_by, self.divided_from, other)

    @final
    def raise_to_power(self, other: LangType) -> OperType:
        return self._try_oper(self.raised_to_power_by, self.raised_to_power_from, other)

    @final
    def get_comparison_eq(self, other: LangType) -> CompType:
        return self._try_symmetric_logic_oper(
            self.get_comparison_eq_by, other.get_comparison_eq_by, self, other
        )

    @final
    def get_comparison_ne(self, other: LangType) -> CompType:
        return self._comp_type_negation(self.get_comparison_eq(other))

    @final
    def get_comparison_lt(self, other: LangType) -> CompType:
        return self._try_symmetric_logic_oper(
            self.get_comparison_lt_by, other.get_comparison_gt_by, self, other
        )

    @final
    def get_comparison_gt(self, other: LangType) -> CompType:
        return self._try_symmetric_logic_oper(
            self.get_comparison_gt_by, other.get_comparison_lt_by, self, other
        )

    @final
    def get_comparison_lte(self, other: LangType) -> CompType:
        return self._try_symmetric_logic_oper(
            self.get_comparison_lte_by, self.get_comparison_gte_by, self, other
        )

    @final
    def get_comparison_gte(self, other: LangType) -> CompType:
        return self._try_symmetric_logic_oper(
            self.get_comparison_gte_by, other.get_comparison_lte_by, self, other
        )

    def anded(self, other: LangType) -> CompType:
        return self._not_impl(f'KEYWORD:{KEYWORDS["OR"]}')

    def ored(self, other: LangType) -> CompType:
        return self._not_impl(f'KEYWORD:{KEYWORDS["OR"]}')

    def notted(self) -> CompType:
        return self._not_impl(f'KEYWORD:{KEYWORDS["NOT"]}')

    def call(
        self, context: Context, args: List[LangType], add_parent: bool = True
    ) -> LangType:
        return self._not_impl("call")

    @staticmethod
    def _not_impl(error_msg: str) -> NotImplementedOperationType:
        return NotImplementedOperationType("Not implemented: " + error_msg)

    @staticmethod
    def _comp_type_negation(comp_res: CompType) -> CompType:
        if isinstance(comp_res, NotImplementedOperationType) or isinstance(
            comp_res, IllegalOperationType
        ):
            return comp_res
        return comp_res.notted()

    @staticmethod
    def _try_oper(
        oper_by: OperFunction, oper_from: OperFunction, other: LangType,
    ) -> OperType:
        if not LangType.not_implemented(res := oper_by(other)):
            return res

        return oper_from(other)

    @staticmethod
    def _try_logic_oper(
        oper_by: CompFunction, oper_from: CompFunction, other: LangType,
    ) -> CompType:
        if not LangType.not_implemented(res := oper_by(other)):
            return res

        return oper_from(other)

    @staticmethod
    def _try_symmetric_logic_oper(
        oper_by: CompFunction,
        oper_from: CompFunction,
        first: LangType,
        second: LangType,
    ) -> CompType:
        if not LangType.not_implemented(res := oper_by(second)):
            return res

        return oper_from(first)

    # @staticmethod
    # def _try_negation_symmetric_logic_oper(
    #     oper_by: CompFunction,
    #     oper_from: CompFunction,
    #     first: LangType,
    #     second: LangType,
    # ) -> CompType:
    #     if not LangType.not_implemented(res := oper_by(second)):
    #         return res
    #
    #     return LangType._comp_type_negation(oper_from(first))

    @staticmethod
    def not_implemented(lang_type: LangType) -> bool:
        return isinstance(lang_type, NotImplementedOperationType)

    @staticmethod
    def illegal_operation(lang_type: LangType) -> bool:
        return isinstance(lang_type, IllegalOperationType)

    @staticmethod
    def valid(lang_type: LangType) -> bool:
        return not LangType.illegal_operation(
            lang_type
        ) and not LangType.not_implemented(lang_type)

    @property
    def value(self) -> Any:
        return None


def check_type(first: LangType, second: LangType) -> Optional[IllegalOperationType]:
    if type(first) is not type(second):
        return IllegalOperationType("Types are not the same")
    return None


class NotImplementedOperationType(LangType):
    def __init__(self, msg: str) -> None:
        super().__init__("NotImplementedType")
        self.msg = msg


class IllegalOperationType(LangType):
    def __init__(self, msg: str) -> None:
        super().__init__("IllegalOperationType")
        self.msg = msg


if TYPE_CHECKING:
    OperType = LangType

    CompType = Union[LangBool, NotImplementedOperationType, IllegalOperationType]
    OperFunction = Callable[[LangType], OperType]
    CompFunction = Callable[[LangType], CompType]
