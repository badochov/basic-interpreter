from __future__ import annotations

from typing import Tuple, Optional

from errors.Error import Error
from errors.RTError import RTError
from types_.Type import Type


class Number(Type):
    def __init__(self, value: float):
        super().__init__()
        self.value = value

    def added_to(self, other: Type) -> oper_type:
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        return None, None

    def multiplied_by(self, other: Type) -> oper_type:
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        return None, None

    def subtracted_by(self, other: Type) -> oper_type:
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        return None, None

    def divided_by(self, other: Type) -> oper_type:
        if isinstance(other, Number):
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
            return Number(self.value / other.value).set_context(self.context), None
        return None, None

    def raised_to_power_by(self, other: Type) -> oper_type:
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
        return None, None

    def __repr__(self) -> str:
        return f"{self.value}"


oper_type = Tuple[Optional[Number], Optional[Error]]
