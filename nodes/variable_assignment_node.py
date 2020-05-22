from __future__ import annotations

from enum import Enum, auto, unique
from typing import TYPE_CHECKING, List, Union, Optional

from lang_types.lang_tuple import LangTuple
from lang_types.lang_variant_type import LangVariantType
from nodes.node import Node
from position import mock_position
from tokens.lang_asterix_token import AsterixToken
from tokens.lang_token import Token
from tokens.lang_string_token import StringToken

if TYPE_CHECKING:
    from lang_types.lang_type import LangType
    from context import Context


@unique
class VariableType(Enum):
    Tuple = auto()
    List = auto()
    VariantType = auto()


class VariableAssignmentNode(Node):
    __slots__ = ["type_name", "names", "value", "var_type"]

    def __init__(
        self,
        names: NamesType,
        var_type: VariableType = VariableType.Tuple,
        type_name: Optional[str] = None,
    ):
        if names:
            super().__init__(names[0].pos_start, names[-1].pos_end)
        else:
            super().__init__(mock_position, mock_position)

        self.type_name = type_name
        self.names = names
        self.value: Optional[LangType] = None
        self.var_type = var_type

    def __repr__(self) -> str:
        return f"({self.names})"

    def is_empty(self) -> bool:
        return not bool(self.names)

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

        if len(self.names) == 1 and self.var_type is VariableType.Tuple:
            if isinstance(self.names[0], VariableAssignmentNode):
                self.names[0].set_value(self.value)
                self.names[0].visit(context)
            else:
                context.set(self.names[0].value, self.value)
        else:
            val: Union[LangType, ListWrapper] = self._get_value(context)

            if not isinstance(val, LangTuple) and not isinstance(val, ListWrapper):
                return self._fail_with("Unexpected type", context)
            if not self._handle_asterix(val, context):
                if len(self.names) != val.values_count():
                    return self._fail_with(
                        "Wrong number of arguments to unpack", context
                    )
                self._handle_names(self.names, context, val)
        return self.value

    def _asterix_position(self) -> int:
        for i, name in enumerate(self.names):
            if isinstance(name, AsterixToken):
                return i
        return -1

    def _handle_asterix(
        self, val: Union[ListWrapper, LangTuple], context: Context
    ) -> bool:
        asterix_pos = self._asterix_position()
        if asterix_pos == -1:
            return False
        if len(self.names) - 1 > val.values_count():
            return self._fail_with("Wrong number of arguments to unpack", context)
        self._handle_names(self.names[0:asterix_pos], context, val)
        end_pos = val.values_count() - len(self.names) + asterix_pos + 1
        if isinstance(val, ListWrapper):
            self._handle_names(
                [self.names[asterix_pos]],
                context,
                ListWrapper(
                    [LangVariantType.make_list(val.values[asterix_pos:end_pos],)]
                ),
            )

        self._handle_names(self.names[asterix_pos + 1 :], context, val, end_pos)
        return True

    @staticmethod
    def _handle_names(
        names: NamesType,
        context: Context,
        val: Union[LangTuple, ListWrapper],
        start: int = 0,
    ) -> None:
        for i, name in enumerate(names, start=start):
            value = val.nth_value(i)
            if isinstance(name, VariableAssignmentNode):
                name.set_value(value)
                name.visit(context)
            else:
                context.set(name.value, value)

    def _get_value(self, context: Context) -> Union[ListWrapper, LangType]:
        assert self.value
        if self.var_type is VariableType.List:
            if not isinstance(self.value, LangVariantType):
                return self._fail_with("Expected list", context)
            try:
                return ListWrapper(LangVariantType.parse_list(self.value))
            except TypeError:
                return self._fail_with("Expected list", context)
        elif self.var_type is VariableType.VariantType:
            if not isinstance(self.value, LangVariantType):
                return self._fail_with("Expected variant_type", context)
            if not self.value.is_of_type(self.type_name or ""):
                return self._fail_with("Type mismatch", context)

            return ListWrapper(self.value.get_args())
        return self.value


NamesType = List[Union[VariableAssignmentNode, StringToken, AsterixToken]]


class ListWrapper:
    def __init__(self, values: List[LangType]):
        self.values = values

    def nth_value(self, i: int) -> LangType:
        return self.values[i]

    def values_count(self) -> int:
        return len(self.values)
