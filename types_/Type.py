from __future__ import annotations

from typing import Optional, Tuple

from Context import Context
from Position import Position
from errors.Error import Error
from errors.NotImplError import NotImplError


class Type:
    def __init__(
        self,
        pos_start: Position = None,
        pos_end: Position = None,
        context: Context = None,
    ):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.context = context

    def set_pos(self, pos_start: Position = None, pos_end: Position = None) -> Type:
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context: Context = None) -> Type:
        self.context = context
        return self

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
