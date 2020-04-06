from __future__ import annotations

from typing import TYPE_CHECKING

from interpreter.runtime_result import RuntimeResult
from nodes.node import Node

if TYPE_CHECKING:
    from context import Context
    from lang_types.lang_function import LangFunction


class FunctionNode(Node):
    def __init__(self, fun: LangFunction):
        super().__init__(fun.pos_start, fun.pos_end)
        self.fun = fun

    def __repr__(self) -> str:
        return f"{self.fun}"

    def visit(self, context: Context) -> RuntimeResult:
        self.fun.context = context
        return RuntimeResult().success(self.fun)
