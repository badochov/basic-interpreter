from types_.Type import Type
from errors.RTError import RTError
from typing import Union, Tuple


class Number(Type):
    def __init__(self, value: float):
        super().__init__()
        self.value = value

    def added_to(self, other: Type):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def multiplied_by(self, other: Type):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def subtracted_by(self, other: Type):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def divided_by(self, other: Type):
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

    def __repr__(self):
        return f"{self.value}"
