from __future__ import annotations

from typing import List, Iterable, TYPE_CHECKING, Callable, TypeVar, cast

from lang_types.lang_bool import LangBool
from lang_types.lang_type import (
    LangType,
    IllegalOperationType,
    NotImplementedOperationType,
)
from lang_types.lang_variant_type import LangVariantType

if TYPE_CHECKING:
    from lang_types.lang_type import OperType, CompType

    T = TypeVar("T", CompType, OperType)


def _valid_args(
    func: Callable[[LangTuple, LangType], T]
) -> Callable[[LangTuple, LangType], T]:
    def check_variant_type(self: LangTuple, other: LangType) -> T:
        if isinstance(other, LangTuple) and other.values_count() != self.values_count():
            return IllegalOperationType(
                "Tuples must have the same number of arguments for comparison"
            )
        return func(self, other)

    return check_variant_type


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

    @_valid_args
    def added_by(self, other: LangType) -> OperType:
        return self.perform_operation(self, other, "add")

    @_valid_args
    def multiplied_by(self, other: LangType) -> OperType:
        return self.perform_operation(self, other, "multiply")

    @_valid_args
    def subtracted_by(self, other: LangType) -> OperType:
        return self.perform_operation(self, other, "subtract")

    @_valid_args
    def divided_by(self, other: LangType) -> OperType:
        return self.perform_operation(self, other, "divide")

    @_valid_args
    def raised_to_power_by(self, other: LangType) -> OperType:
        return self.perform_operation(self, other, "raise_to_power")

    @_valid_args
    def added_from(self, other: LangType) -> OperType:
        return self.perform_operation(self, other, "add", False)

    @_valid_args
    def multiplied_from(self, other: LangType) -> OperType:
        return self.perform_operation(self, other, "multiply", False)

    @_valid_args
    def subtracted_from(self, other: LangType) -> OperType:
        return self.perform_operation(self, other, "subtract", False)

    @_valid_args
    def divided_from(self, other: LangType) -> OperType:
        return self.perform_operation(self, other, "divide", False)

    @_valid_args
    def raised_to_power_from(self, other: LangType) -> OperType:
        return self.perform_operation(self, other, "raise_to_power", False)

    @_valid_args
    def get_comparison_eq_by(self, other: LangType) -> CompType:
        return LangTuple.compare(self, other, "get_comparison_eq")

    @_valid_args
    def get_comparison_ne_by(self, other: LangType) -> CompType:
        eq = self.get_comparison_eq(other)
        if isinstance(eq, LangBool):
            return eq.notted()
        return eq

    @_valid_args
    def get_comparison_lt_by(self, other: LangType) -> CompType:
        return LangTuple.compare(self, other, "get_comparison_lt")

    @_valid_args
    def get_comparison_lte_by(self, other: LangType) -> CompType:
        return LangTuple.compare(self, other, "get_comparison_lte")

    @_valid_args
    def get_comparison_gt_by(self, other: LangType) -> CompType:
        return LangTuple.compare(self, other, "get_comparison_gt")

    @_valid_args
    def get_comparison_gte_by(self, other: LangType) -> CompType:
        return LangTuple.compare(self, other, "get_comparison_gte")

    # @_valid_args
    # def anded_by(self, other: LangType) -> CompType:
    #     return LangTuple.compare(self, other, "anded")
    #
    # @_valid_args
    # def ored_by(self, other: LangType) -> CompType:
    #     return LangTuple.compare(self, other, "anded")

    @staticmethod
    def compare(first: LangTuple, second: LangType, method: str) -> CompType:
        if isinstance(second, LangTuple):
            second_values = second._values
        else:
            second_values = [second] * len(first._values)

        for first_arg, second_arg in zip(first._values, second_values):
            res = cast(CompType, getattr(first_arg, method)(second_arg))
            if isinstance(res, LangBool):
                if res.is_truthy():
                    continue
            return res

        return LangBool.true_def()

    @staticmethod
    def perform_operation(
        first: LangTuple, second: LangType, method: str, by: bool = True
    ) -> OperType:
        if isinstance(second, LangTuple):
            second_values = second._values
        else:
            second_values = [second] * len(first._values)

        res_values: List[LangType] = []
        for first_arg, second_arg in zip(first._values, second_values):
            if by:
                res = cast(CompType, getattr(first_arg, method)(second_arg))
            else:
                res = cast(CompType, getattr(second_arg, method)(first_arg))
            if isinstance(res, IllegalOperationType) or isinstance(
                res, NotImplementedOperationType
            ):
                return res

            res_values.append(res)

        return LangTuple(res_values)
