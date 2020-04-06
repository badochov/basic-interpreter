from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING, List

from context import Context
from errors.error import Error
from errors.rt_error import RTError
from errors.too_few_args_error import TooFewArgsError
from interpreter.runtime_result import RuntimeResult
from lang_types.lang_type import LangType
from nodes.node import Node
from position import Position

if TYPE_CHECKING:
    from lang_types.lang_number import LangNumber

    CompType = Tuple[Optional[LangNumber], Optional[Error]]


class LangFunction(LangType):
    def __init__(
        self,
        arg_name: str,
        body_node: Node,
        pos_start: Position = None,
        pos_end: Position = None,
        context: Context = None,
    ):
        super().__init__(pos_start, pos_end, context)
        self.arg_name = arg_name
        self.body_node = body_node

    def is_truthy(self) -> bool:
        return True

    def call(self, context: Context, args: List[Node]) -> RuntimeResult:
        res = RuntimeResult()
        if not args:
            return res.failure(TooFewArgsError(self.pos_start, self.pos_start, ""))
        if not self.body_node:
            return res.failure(
                RTError(self.pos_start, self.pos_start, "No function body", context)
            )

        val = res.register(args.pop().visit(context))
        if res.error or val is None:
            return res
        context.symbol_table.set(self.arg_name, val)

        result = res.register(self.body_node.visit(context))
        if res.error or result is None:
            return res
        if args:
            val = res.register(result.call(context, args))
            if val is None or res.error:
                return res
            return res.success(val)
        return res.success(result)
