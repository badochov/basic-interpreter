from __future__ import annotations

from copy import deepcopy
from typing import Optional, Tuple, TypeVar, TYPE_CHECKING, List

from context import Context, mock_context
from errors.error import Error
from errors.not_impl_error import NotImplError
from interpreter.runtime_result import RuntimeResult
from keywords import *
from position import Position, mock_position

if TYPE_CHECKING:
    from lang_types.lang_number import LangNumber

    CompType = Tuple[Optional[LangNumber], Optional[Error]]

T = TypeVar("T", bound="LangType")


class LangType:
    def __init__(
        self,
        pos_start: Position = None,
        pos_end: Position = None,
        context: Context = None,
        deep_copied: List[str] = None,
    ):
        if pos_start is None:
            pos_start = mock_position
        if pos_end is None:
            pos_end = mock_position
        if context is None:
            context = mock_context

        self.pos_start = pos_start
        self.pos_end = pos_end
        self.context = context
        self.deep_copied = deep_copied if deep_copied else []

    def set_pos(self: T, pos_start: Position, pos_end: Position) -> T:
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self: T, context: Context) -> T:
        self.context = context
        return self

    # todo improve copy
    def copy(self: T) -> T:
        cls = self.__class__
        result = cls.__new__(cls)
        for k, v in self.__dict__.items():
            if k in self.deep_copied:
                setattr(result, k, deepcopy(v))
            else:
                setattr(result, k, v)
        return result

    def added_to(self, other: LangType) -> OperType:
        return None, NotImplError(self.pos_start, self.pos_end, "+")

    def multiplied_by(self, other: LangType) -> OperType:
        return None, NotImplError(self.pos_start, self.pos_end, "*")

    def subtracted_by(self, other: LangType) -> OperType:
        return None, NotImplError(self.pos_start, self.pos_end, "-")

    def divided_by(self, other: LangType) -> OperType:
        return None, NotImplError(self.pos_start, self.pos_end, "/")

    def raised_to_power_by(self, other: LangType) -> OperType:
        return None, NotImplError(self.pos_start, self.pos_end, "/")

    def get_comparison_eq(self, other: LangType) -> CompType:
        return None, NotImplError(self.pos_start, self.pos_end, "==")

    def get_comparison_ne(self, other: LangType) -> CompType:
        return None, NotImplError(self.pos_start, self.pos_end, "!=")

    def get_comparison_lt(self, other: LangType) -> CompType:
        return None, NotImplError(self.pos_start, self.pos_end, "<")

    def get_comparison_gt(self, other: LangType) -> CompType:
        return None, NotImplError(self.pos_start, self.pos_end, ">")

    def get_comparison_lte(self, other: LangType) -> CompType:
        return None, NotImplError(self.pos_start, self.pos_end, "<=")

    def get_comparison_gte(self, other: LangType) -> CompType:
        return None, NotImplError(self.pos_start, self.pos_end, ">=")

    def anded_by(self, other: LangType) -> CompType:
        return (
            None,
            NotImplError(self.pos_start, self.pos_end, f'KEYWORD:{KEYWORDS["AND"]}'),
        )

    def ored_by(self, other: LangType) -> CompType:
        return (
            None,
            NotImplError(self.pos_start, self.pos_end, f'KEYWORD:{KEYWORDS["OR"]}'),
        )

    def notted(self) -> CompType:
        return (
            None,
            NotImplError(self.pos_start, self.pos_end, f'KEYWORD:{KEYWORDS["NOT"]}'),
        )

    def is_truthy(self) -> bool:
        return False

    def call(self, context: Context, args: List[LangType]) -> RuntimeResult:
        return RuntimeResult().failure(
            NotImplError(self.pos_start, self.pos_end, "Call")
        )


OperType = Tuple[Optional[LangType], Optional[Error]]
