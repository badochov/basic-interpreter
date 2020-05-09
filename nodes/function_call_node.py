from __future__ import annotations

from typing import TYPE_CHECKING, List

from errors.rt_error import RTError
from interpreter.runtime_result import RuntimeResult
from lang_types.lang_function import LangFunction
from nodes.node import Node

if TYPE_CHECKING:
    from context import Context
    from lang_token import Token


# BUG
#  to działą
# let add x y = x + y
# let inc = add 1
# inc 2
#  to nie
# let add x y = x + y
# add 1 2
# let inc = add 1
# inc 2
class FunctionCallNode(Node):
    def __init__(self, fun_name_token: Token, arg_nodes: List[Node]):

        super().__init__(fun_name_token.pos_start, arg_nodes[-1].pos_end)
        self.fun_name_token = fun_name_token
        self.arg_nodes = arg_nodes

    def __repr__(self) -> str:
        return f"({self.fun_name_token}, {self.arg_nodes})"

    def visit(self, context: Context) -> RuntimeResult:
        res = RuntimeResult()
        fun = None
        if isinstance(self.fun_name_token.value, str):
            fun = context.get(self.fun_name_token.value)
        if not fun:
            return res.failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f'"{self.fun_name_token}" is not defined',
                    context,
                )
            )
        if not isinstance(fun, LangFunction):
            return res.failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f'"{self.fun_name_token}" is not a function',
                    context,
                )
            )

        fun_cpy = fun.copy().set_pos(self.pos_start, self.pos_end)
        args = []
        for arg_node in reversed(self.arg_nodes):
            arg = res.register(arg_node.visit(context))
            if arg is None or res.error:
                return res

            args.append(arg)
        # print(self.arg_nodes, args, context.get("n"))
        call_res = res.register(fun_cpy.call(fun_cpy.context, args))
        if call_res is None or res.error:
            return res
        return res.success(call_res)
