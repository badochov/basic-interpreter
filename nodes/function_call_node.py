from __future__ import annotations

from typing import TYPE_CHECKING, List

from errors.rt_error import RTError
from interpreter.runtime_result import RuntimeResult
from lang_types.lang_function import LangFunction
from lang_types.lang_variant_type import LangVariantType
from lang_types.type_def import LangVariantTypeDefinition
from nodes.node import Node

if TYPE_CHECKING:
    from context import Context
    from tokens.lang_string_token import StringToken


class FunctionCallNode(Node):
    def __init__(self, fun_name_token: StringToken, arg_nodes: List[Node]):

        super().__init__(fun_name_token.pos_start, arg_nodes[-1].pos_end)
        self.fun_name_token = fun_name_token
        self.arg_nodes = arg_nodes

    def __repr__(self) -> str:
        return f"({self.fun_name_token}, {self.arg_nodes})"

    def visit(self, context: Context) -> RuntimeResult:
        res = RuntimeResult()
        name = self.fun_name_token.value

        if not (fun := context.get(name)):
            return res.failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f'"{self.fun_name_token}" is not defined',
                    context,
                )
            )
        is_fun = isinstance(fun, LangFunction)
        is_variant = isinstance(fun, LangVariantTypeDefinition)
        if not is_fun and not is_variant:
            return res.failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f'"{self.fun_name_token}" is not a function',
                    context,
                )
            )

        args = []
        for arg_node in reversed(self.arg_nodes):
            arg = res.register(arg_node.visit(context))
            if arg is None or res.error:
                return res

            args.append(arg)

        if isinstance(fun, LangVariantTypeDefinition):
            if len(args) != len(fun.args):
                return res.failure(
                    RTError(
                        self.pos_start,
                        self.pos_end,
                        f'"{self.fun_name_token}" got to few arguments',
                        context,
                    )
                )
            return res.success(
                LangVariantType(
                    list(reversed(args)), name, self.pos_start, self.pos_end, context,
                )
            )
        else:
            fun_cpy = fun.copy().set_pos(self.pos_start, self.pos_end)
            call_res = res.register(fun_cpy.call(context, args))
            if call_res is None or res.error:
                return res

            return res.success(call_res)
