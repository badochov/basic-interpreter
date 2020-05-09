from __future__ import annotations

from typing import Tuple, Optional, TYPE_CHECKING

from errors.error import Error
from errors.rt_error import RTError
from lang_types.lang_type import LangType

if TYPE_CHECKING:
    from position import Position
    from context import Context


class LangNumber(LangType):
    def __init__(
        self,
        value: float,
        pos_start: Position = None,
        pos_end: Position = None,
        context: Context = None,
    ):
        super().__init__("number", pos_start, pos_end, context)
        self.value = value

    def added_to(self, other: LangType) -> OperType:
        if isinstance(other, LangNumber):
            return (
                LangNumber(
                    self.value + other.value,
                    self.pos_start,
                    other.pos_end,
                    self.context,
                ),
                None,
            )
        return None, None

    def multiplied_by(self, other: LangType) -> OperType:
        if isinstance(other, LangNumber):
            return (
                LangNumber(
                    self.value * other.value,
                    self.pos_start,
                    other.pos_end,
                    self.context,
                ),
                None,
            )
        return None, None

    def subtracted_by(self, other: LangType) -> OperType:
        if isinstance(other, LangNumber):
            return (
                LangNumber(
                    self.value - other.value,
                    self.pos_start,
                    other.pos_end,
                    self.context,
                ),
                None,
            )
        return None, None

    def divided_by(self, other: LangType) -> OperType:
        if isinstance(other, LangNumber):
            if other.value == 0:
                return (
                    None,
                    RTError(
                        other.pos_start,
                        other.pos_end,
                        "Division by zero",
                        self.context,
                    ),
                )
            return (
                LangNumber(
                    self.value / other.value,
                    self.pos_start,
                    other.pos_end,
                    self.context,
                ),
                None,
            )
        return None, None

    def raised_to_power_by(self, other: LangType) -> OperType:
        if isinstance(other, LangNumber):
            return (
                LangNumber(
                    self.value ** other.value,
                    self.pos_start,
                    other.pos_end,
                    self.context,
                ),
                None,
            )
        return None, None

    def get_comparison_eq(self, other: LangType) -> CompType:
        if isinstance(other, LangNumber):
            return (
                LangNumber(
                    int(self.value == other.value),
                    self.pos_start,
                    other.pos_end,
                    self.context,
                ),
                None,
            )

        return super().get_comparison_eq(other)

    def get_comparison_ne(self, other: LangType) -> CompType:
        if isinstance(other, LangNumber):
            return (
                LangNumber(
                    int(self.value != other.value),
                    self.pos_start,
                    other.pos_end,
                    self.context,
                ),
                None,
            )

        return super().get_comparison_ne(other)

    def get_comparison_lt(self, other: LangType) -> CompType:
        if isinstance(other, LangNumber):
            return (
                LangNumber(
                    int(self.value < other.value),
                    self.pos_start,
                    other.pos_end,
                    self.context,
                ),
                None,
            )

        return super().get_comparison_lt(other)

    def get_comparison_gt(self, other: LangType) -> CompType:
        if isinstance(other, LangNumber):
            return (
                LangNumber(
                    int(self.value > other.value),
                    self.pos_start,
                    other.pos_end,
                    self.context,
                ),
                None,
            )

        return super().get_comparison_gt(other)

    def get_comparison_lte(self, other: LangType) -> CompType:
        if isinstance(other, LangNumber):
            return (
                LangNumber(
                    int(self.value <= other.value),
                    self.pos_start,
                    other.pos_end,
                    self.context,
                ),
                None,
            )

        return super().get_comparison_lte(other)

    def get_comparison_gte(self, other: LangType) -> CompType:
        if isinstance(other, LangNumber):
            return (
                LangNumber(
                    int(self.value >= other.value),
                    self.pos_start,
                    other.pos_end,
                    self.context,
                ),
                None,
            )

        return super().get_comparison_gte(other)

    def anded_by(self, other: LangType) -> CompType:
        if isinstance(other, LangNumber):
            return (
                LangNumber(
                    int(self.value and other.value),
                    self.pos_start,
                    other.pos_end,
                    self.context,
                ),
                None,
            )

        return super().anded_by(other)

    def ored_by(self, other: LangType) -> CompType:
        if isinstance(other, LangNumber):
            return (
                LangNumber(
                    int(self.value or other.value),
                    self.pos_start,
                    other.pos_end,
                    self.context,
                ),
                None,
            )

        return super().ored_by(other)

    def notted(self) -> CompType:
        return (
            LangNumber(
                int(not self.value), self.pos_start, self.pos_end, self.context,
            ),
            None,
        )

    def is_truthy(self) -> bool:
        return self.value != 0

    def __repr__(self) -> str:
        return f"{self.value}"


OperType = Tuple[Optional[LangNumber], Optional[Error]]
CompType = Tuple[Optional[LangNumber], Optional[Error]]
