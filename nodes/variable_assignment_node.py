from __future__ import annotations

from typing import TYPE_CHECKING

from lang_types.lang_type import LangType
from nodes.node import Node

if TYPE_CHECKING:
    from context import Context
    from tokens.lang_string_token import StringToken


class VariableAssignmentNode(Node):
    def __init__(self, var_name_token: StringToken, value_node: Node):
        super().__init__(var_name_token.pos_start, var_name_token.pos_end)
        self.var_name_token = var_name_token
        self.value_node = value_node

        self.pos_start = var_name_token.pos_start
        self.pos_end = var_name_token.pos_end

    def visit(self, context: Context) -> LangType:
        var_name = self.var_name_token.value

        value = self.value_node.visit(context)

        context.set(var_name, value)

        return value
