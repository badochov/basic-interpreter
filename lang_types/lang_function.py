from __future__ import annotations

from typing import Optional, TYPE_CHECKING, List

from context import Context
from errors.too_few_args_error import TooFewArgsError
from lang_types.lang_type import LangType
from nodes.node import Node
from position import Position
from symbol_table import SymbolTable
from tokens.lang_token import Token

if TYPE_CHECKING:
    ...


class LangFunction(LangType):
    def __init__(
        self,
        name_token: Optional[Token],
        arg_names: List[str],
        body_node: Node,
        pos_start: Position,
        pos_end: Position,
        context: Context,
    ):
        super().__init__("function", pos_start, pos_end, context)
        self.arg_names = arg_names
        self.body_node = body_node
        self.name = (
            name_token.value
            if name_token and isinstance(name_token.value, str)
            else "<anonymous>"
        )

    def __repr__(self) -> str:
        return f"fn {self.arg_names}"

    def call(self, context: Context, args: List[LangType]) -> LangType:
        new_ctx = Context(self.name, SymbolTable(), context, self.pos_start,)
        new_ctx.add_parent(self.context)
        if not args:
            raise TooFewArgsError(self.pos_start, self.pos_end, "")

        new_ctx.set_multi(self.arg_names, args.pop(), self.pos_start, self.pos_end)
        result_cpy = self.body_node.visit(new_ctx).copy()
        if args:
            val = result_cpy.call(new_ctx, args)
            result_cpy = val.copy()

        return result_cpy
