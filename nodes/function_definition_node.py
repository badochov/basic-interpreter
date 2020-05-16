from __future__ import annotations

from typing import TYPE_CHECKING, List

from lang_types.lang_function import LangFunction
from nodes.node import Node

if TYPE_CHECKING:
    from lang_types.lang_type import LangType
    from context import Context
    from tokens.lang_string_token import StringToken


class FunctionDefinitionNode(Node):
    def __init__(
        self,
        var_name_tokens: List[StringToken],
        arg_tokens: List[StringToken],
        body_node: Node,
        save_name: bool = True,
    ):
        if var_name_tokens:
            pos_start = var_name_tokens[0].pos_start
        elif arg_tokens:
            pos_start = arg_tokens[0].pos_start
        else:
            pos_start = body_node.pos_start

        super().__init__(pos_start, body_node.pos_end)
        self.var_name_tokens = var_name_tokens
        self.arg_tokens = arg_tokens
        self.body_node = body_node
        self.save_name = save_name

    def __repr__(self) -> str:
        return f"({self.var_name_tokens or '<anonymous>'},"

    def visit(self, context: Context) -> LangType:
        if self.arg_tokens:
            value: LangType = LangFunction(
                self.var_name_tokens[0] if self.var_name_tokens else None,
                list(map(lambda token: token.value, self.arg_tokens)),
                self.body_node,
                self.pos_start,
                self.pos_end,
                context,
            )
        else:
            value = self.body_node.visit(context)

        if self.var_name_tokens and self.save_name:
            context.set_multi(
                list(map(lambda token: token.value, self.var_name_tokens)),
                value,
                self.pos_start,
                self.pos_end,
            )
        return value
