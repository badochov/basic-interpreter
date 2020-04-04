from __future__ import annotations

from copy import deepcopy
from typing import Optional, Tuple, TypeVar, TYPE_CHECKING

from context import Context, mock_context
from position import Position, mock_position
from errors.error import Error
from errors.not_impl_error import NotImplError

if TYPE_CHECKING:
    pass

T = TypeVar("T", bound="Type")


class Type:
    def __init__(
        self,
        pos_start: Position = None,
        pos_end: Position = None,
        context: Context = None,
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

    def set_pos(self: T, pos_start: Position, pos_end: Position) -> T:
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self: T, context: Context) -> T:
        self.context = context
        return self

    def copy(self: T) -> T:
        return deepcopy(self)

    def added_to(self, other: Type) -> oper_type:
        return None, NotImplError(self.pos_start, self.pos_end, "+")

    def multiplied_by(self, other: Type) -> oper_type:
        return None, NotImplError(self.pos_start, self.pos_end, "*")

    def subtracted_by(self, other: Type) -> oper_type:
        return None, NotImplError(self.pos_start, self.pos_end, "-")

    def divided_by(self, other: Type) -> oper_type:
        return None, NotImplError(self.pos_start, self.pos_end, "/")

    def raised_to_power_by(self, other: Type) -> oper_type:
        return None, NotImplError(self.pos_start, self.pos_end, "/")


oper_type = Tuple[Optional[Type], Optional[Error]]