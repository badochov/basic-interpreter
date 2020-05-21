from __future__ import annotations

from typing import TYPE_CHECKING, List, Union, Optional

from lang_types.lang_tuple import LangTuple
from nodes.node import Node
from tokens.lang_asterix_token import AsterixToken
from tokens.lang_token import Token

if TYPE_CHECKING:
    from lang_types.lang_type import LangType
    from context import Context
    from tokens.lang_string_token import StringToken


class VariableAssignmentNode(Node):
    def __init__(
        self,
        names: List[Union[VariableAssignmentNode, StringToken, AsterixToken]],
        is_list: bool = False,
    ):
        super().__init__(names[0].pos_start, names[-1].pos_end)
        self.names = names
        self.value: Optional[LangType] = None
        self.is_list = is_list

    def __repr__(self) -> str:
        return f"UMPALUMP({self.names})"

    def set_value(self, value: LangType) -> None:
        self.value = value

    def get_names(self) -> List[str]:
        res = []
        for name in self.names:
            if isinstance(name, Token):
                res.append(name.value)
            else:
                res.extend(name.get_names())
        return res

    def visit(self, context: Context) -> LangType:
        assert self.value is not None
        asterix_pos = self._asterix_position()

        if self.is_list:
            assert False

        if len(self.names) == 1:
            if isinstance(self.names[0], VariableAssignmentNode):
                self.names[0].set_value(self.value)
                self.names[0].visit(context)
            else:
                context.set(self.names[0].value, self.value)

        else:
            if not isinstance(self.value, LangTuple):
                return self._fail_with("Expected tuple", context)
            if asterix_pos != -1:
                if len(self.names) - 1 > self.value.values_count():
                    return self._fail_with(
                        "Wrong number of arguments to unpack", context
                    )
                self._handle_tuple_names(self.names[0:asterix_pos], context)
                start_pos_tuple = (
                    self.value.values_count() - len(self.names) + asterix_pos + 1
                )
                self._handle_tuple_names(
                    self.names[asterix_pos + 1 :], context, start_pos_tuple
                )
            else:
                if len(self.names) != self.value.values_count():
                    return self._fail_with(
                        "Wrong number of arguments to unpack", context
                    )
                self._handle_tuple_names(self.names, context)
        return self.value

    def _asterix_position(self) -> int:
        for i, name in enumerate(self.names):
            if isinstance(name, AsterixToken):
                return i
        return -1

    def _handle_tuple_names(
        self,
        names: List[Union[AsterixToken, StringToken, VariableAssignmentNode]],
        context: Context,
        start: int = 0,
    ) -> None:
        if TYPE_CHECKING:
            assert isinstance(self.value, LangTuple)
        for i, name in enumerate(names, start=start):
            value = self.value.nth_value(i)
            if isinstance(name, VariableAssignmentNode):
                name.set_value(value)
                name.visit(context)
            else:
                context.set(name.value, value)
