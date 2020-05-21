from __future__ import annotations

from typing import TYPE_CHECKING, List, Union, Optional

from lang_types.lang_tuple import LangTuple
from lang_types.lang_variant_type import LangVariantType
from nodes.match_case_node import LangNoMatchType
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
        return f"({self.names})"

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

        val: Union[LangType, ListWrapper] = self.value
        if self.is_list:
            if not isinstance(self.value, LangVariantType):
                return self._fail_with("Expected list", context)
            try:
                val = ListWrapper(LangVariantType.parse_list(self.value))
            except TypeError:
                return self._fail_with("Expected list", context)

        if len(self.names) == 1:
            if isinstance(self.names[0], VariableAssignmentNode):
                self.names[0].set_value(self.value)
                self.names[0].visit(context)
            else:
                if isinstance(val, ListWrapper):
                    if len(self.names) < val.values_count():
                        if asterix_pos == -1:
                            return self._fail_with(
                                "Too little arguments to unpack", context
                            )

                    else:
                        context.set(self.names[0].value, val.values[0])
                        return self.value
                context.set(self.names[0].value, self.value)
        else:
            if not isinstance(val, LangTuple) and not isinstance(val, ListWrapper):
                return self._fail_with("Expected tuple", context)
            if asterix_pos != -1:
                if len(self.names) - 1 > val.values_count():
                    return self._fail_with(
                        "Wrong number of arguments to unpack", context
                    )
                self._handle_names(self.names[0:asterix_pos], context, val)
                end_pos = val.values_count() - len(self.names) + asterix_pos + 1
                if isinstance(val, ListWrapper):
                    self._handle_names(
                        [self.names[asterix_pos]],
                        context,
                        ListWrapper(
                            [
                                LangVariantType.make_list(
                                    val.values[asterix_pos:end_pos],
                                    self.pos_start,
                                    self.pos_end,
                                    context,
                                )
                            ]
                        ),
                    )

                self._handle_names(self.names[asterix_pos + 1 :], context, val, end_pos)
            else:
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

    @staticmethod
    def _handle_names(
        names: List[Union[AsterixToken, StringToken, VariableAssignmentNode]],
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


class ListWrapper:
    def __init__(self, values: List[LangType]):
        self.values = values

    def nth_value(self, i: int) -> LangType:
        return self.values[i]

    def values_count(self) -> int:
        return len(self.values)
