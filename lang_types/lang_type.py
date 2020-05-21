from __future__ import annotations

from copy import deepcopy
from typing import TypeVar, TYPE_CHECKING, List, cast, Any, NoReturn

from errors.not_impl_error import NotImplError
from keywords import *
from position import Position

if TYPE_CHECKING:
    from context import Context
    from lang_types.lang_bool import LangBool

    CompType = LangBool

T = TypeVar("T", bound="LangType")


class LangType:
    def __init__(
        self,
        type_name: str,
        pos_start: Position,
        pos_end: Position,
        context: Context,
        deep_copied: List[str] = None,
    ):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.context = context
        self.deep_copied = deep_copied if deep_copied else []
        self.type_name = type_name

    def set_pos(self: T, pos_start: Position, pos_end: Position) -> T:
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self: T, context: Context) -> T:
        self.context = context
        return self

    def copy(self: T) -> T:
        cls = type(self)
        result = cast(T, cls.__new__(cls))
        for key, value in self.__dict__.items():
            if key in self.deep_copied:
                setattr(result, key, deepcopy(value))
            else:
                setattr(result, key, value)
        return result

    def added_to(self, other: LangType) -> OperType:
        return self._not_impl("+")

    def multiplied_by(self, other: LangType) -> OperType:
        return self._not_impl("*")

    def subtracted_by(self, other: LangType) -> OperType:
        return self._not_impl("-")

    def divided_by(self, other: LangType) -> OperType:
        return self._not_impl("/")

    def raised_to_power_by(self, other: LangType) -> OperType:
        return self._not_impl("^")

    def get_comparison_eq(self, other: LangType) -> CompType:
        return self._not_impl("==")

    def get_comparison_ne(self, other: LangType) -> CompType:
        return self._not_impl("!=")

    def get_comparison_lt(self, other: LangType) -> CompType:
        return self._not_impl("<")

    def get_comparison_gt(self, other: LangType) -> CompType:
        return self._not_impl(">")

    def get_comparison_lte(self, other: LangType) -> CompType:
        return self._not_impl("<=")

    def get_comparison_gte(self, other: LangType) -> CompType:
        return self._not_impl(">=")

    def anded_by(self, other: LangType) -> CompType:
        return self._not_impl(f'KEYWORD:{KEYWORDS["AND"]}')

    def ored_by(self, other: LangType) -> CompType:
        return self._not_impl(f'KEYWORD:{KEYWORDS["OR"]}')

    def notted(self) -> CompType:
        return self._not_impl(f'KEYWORD:{KEYWORDS["NOT"]}')

    def call(self, context: Context, args: List[LangType]) -> LangType:
        raise NotImplError(self.pos_start, self.pos_end, "Call")

    def _not_impl(self, error_msg: str) -> NoReturn:
        raise NotImplError(self.pos_start, self.pos_end, error_msg)

    @property
    def value(self) -> Any:
        return None


OperType = LangType
