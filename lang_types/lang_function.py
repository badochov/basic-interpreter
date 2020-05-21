from __future__ import annotations

from typing import Optional, TYPE_CHECKING, List

from context import Context
from lang_types.lang_type import LangType
from nodes.node import Node
from nodes.variable_assignment_node import VariableAssignmentNode
from position import Position
from symbol_table import SymbolTable

if TYPE_CHECKING:
    ...


class LangFunction(LangType):
    def __init__(
        self,
        name: Optional[str],
        arg: VariableAssignmentNode,
        body_node: Node,
        pos_start: Position,
        pos_end: Position,
        context: Context,
    ):
        super().__init__("function", pos_start, pos_end, context)
        self.arg = arg
        self.body_node = body_node
        self.name = name if name else "<anonymous>"

    def __repr__(self) -> str:
        return f"fn {self.arg}"

    def call(self, context: Context, args: List[LangType]) -> LangType:
        new_ctx = Context(self.name, SymbolTable(), context, self.pos_start,)
        new_ctx.add_parent(self.context)

        self.arg.set_value(args.pop())
        self.arg.visit(new_ctx)
        result_cpy = self.body_node.visit(new_ctx).copy()
        if args:
            val = result_cpy.call(new_ctx, args)
            result_cpy = val.copy()

        return result_cpy


# (UMPALUMP([IDENTIFIER:fib_pom])(None) -> (UMPALUMP([IDENTIFIER:fib_pom])(UMPALUMP([IDENTIFIER:a])) -> (UMPALUMP([IDENTIFIER:fib_pom])(UMPALUMP([IDENTIFIER:b])) -> (UMPALUMP([IDENTIFIER:fib_pom])(UMPALUMP([IDENTIFIER:n])) -> (if ((IDENTIFIER:n), EE, INT:0) then (IDENTIFIER:a) else (IDENTIFIER:fib_pom, [(IDENTIFIER:b), ((IDENTIFIER:a), PLUS, (IDENTIFIER:b)), ((IDENTIFIER:n), MINUS, INT:1)]))))))
