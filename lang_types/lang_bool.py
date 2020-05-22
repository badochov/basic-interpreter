from __future__ import annotations

from typing import TYPE_CHECKING

from lang_types.lang_type import LangType

if TYPE_CHECKING:
    from lang_types.lang_type import CompType


class LangBool(LangType):
    __slots__ = ["_value"]

    def __init__(self, value: bool):
        super().__init__("number")
        self._value = value

    @property
    def value(self) -> bool:
        return self._value

    def get_comparison_eq_by(self, other: LangType) -> CompType:
        if isinstance(other, LangBool):
            return LangBool(self._value == other.value)

        return super().get_comparison_eq_by(other)

    def get_comparison_ne_by(self, other: LangType) -> CompType:
        if isinstance(other, LangBool):
            return LangBool(self._value != other.value)

        return super().get_comparison_ne_by(other)

    def anded_by(self, other: LangType) -> CompType:
        if isinstance(other, LangBool):
            return LangBool(self._value and other.value)

        return super().anded_by(other)

    def ored_by(self, other: LangType) -> CompType:
        if isinstance(other, LangBool):
            return LangBool(self.value or other.value)

        return super().ored_by(other)

    def notted(self) -> CompType:
        return LangBool(not self._value)

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
        return LangBool(False)

    @staticmethod
    def true_def() -> LangBool:
        return LangBool(True)
