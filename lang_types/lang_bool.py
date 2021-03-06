from __future__ import annotations

from typing import TYPE_CHECKING

from context import mock_context
from lang_types.lang_type import LangType
from position import mock_position

if TYPE_CHECKING:
    from position import Position
    from context import Context
    from lang_types.lang_type import CompType


class LangBool(LangType):
    def __init__(
        self, value: bool, pos_start: Position, pos_end: Position, context: Context,
    ):
        super().__init__("number", pos_start, pos_end, context)
        self._value = value

    @property
    def value(self) -> bool:
        return self._value

    def get_comparison_eq(self, other: LangType) -> CompType:
        if isinstance(other, LangBool):
            return LangBool(
                self._value == other.value, self.pos_start, other.pos_end, self.context,
            )

        return super().get_comparison_eq(other)

    def get_comparison_ne(self, other: LangType) -> CompType:
        if isinstance(other, LangBool):
            return LangBool(
                self._value != other.value, self.pos_start, other.pos_end, self.context,
            )

        return super().get_comparison_ne(other)

    def anded_by(self, other: LangType) -> CompType:
        if isinstance(other, LangBool):
            return LangBool(
                self._value and other.value,
                self.pos_start,
                other.pos_end,
                self.context,
            )

        return super().anded_by(other)

    def ored_by(self, other: LangType) -> CompType:
        if isinstance(other, LangBool):
            return LangBool(
                self.value or other.value, self.pos_start, other.pos_end, self.context,
            )

        return super().ored_by(other)

    def notted(self) -> CompType:
        return LangBool(not self._value, self.pos_start, self.pos_end, self.context,)

    def is_truthy(self) -> bool:
        return self._value

    def __repr__(self) -> str:
        return f"{self._value}"

    @staticmethod
    def true_name() -> str:
        return "true"

    @staticmethod
    def false_name() -> str:
        return "false"

    @staticmethod
    def false_def() -> LangBool:
        return LangBool(False, mock_position, mock_position, mock_context)

    @staticmethod
    def true_def() -> LangBool:
        return LangBool(True, mock_position, mock_position, mock_context)
