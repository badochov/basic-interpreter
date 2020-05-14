from __future__ import annotations

from typing import Optional, TYPE_CHECKING, List

from context import Context
from errors.too_few_args_error import TooFewArgsError
from interpreter.runtime_result import RuntimeResult
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
        arg_name: str,
        body_node: Node,
        pos_start: Position = None,
        pos_end: Position = None,
        context: Context = None,
    ):
        super().__init__("function", pos_start, pos_end, context)
        self.arg_name = arg_name
        self.body_node = body_node
        self.name = (
            name_token.value
            if name_token and isinstance(name_token.value, str)
            else "<anonymous>"
        )

    def __repr__(self) -> str:
        return f"fn {self.arg_name}"

    def call(self, context: Context, args: List[LangType]) -> RuntimeResult:
        new_ctx = Context(self.name, SymbolTable(), context, self.pos_start,)
        new_ctx.symbol_table.add_parent(self.context.symbol_table)
        res = RuntimeResult()
        if not args:
            return res.failure(TooFewArgsError(self.pos_start, self.pos_end, ""))

        new_ctx.symbol_table.set(self.arg_name, args.pop())
        result = res.register(self.body_node.visit(new_ctx))
        if res.error or result is None:
            return res

        result_cpy = result.copy()
        if args:
            val = res.register(result_cpy.call(new_ctx, args))
            if val is None or res.error:
                return res
            result_cpy = val.copy()

        return res.success(result_cpy)
