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
    __slots__ = ["name", "body_node", "context", "pos_start", "arg"]

    def __init__(
        self,
        name: Optional[str],
        arg: VariableAssignmentNode,
        body_node: Node,
        pos_start: Position,
        context: Context,
    ):
        super().__init__("function")
        self.pos_start = pos_start
        self.context = context
        self.arg = arg
        self.body_node = body_node
        self.name = name if name else "<anonymous>"

    def set_context(self, context: Context) -> LangFunction:
        self.context = context
        return self

    def __repr__(self) -> str:
        return f"fn {self.arg}"

    def set_pos(self, pos_start: Position) -> LangFunction:
        self.pos_start = pos_start
        return self

    def call(
        self, context: Context, args: List[LangType], add_parent: bool = True
    ) -> LangType:
        new_ctx = Context(self.name, SymbolTable(), context, self.pos_start,)
        if add_parent:
            new_ctx.add_parent(self.context)

        self.arg.set_value(args.pop())
        self.arg.visit(new_ctx)
        result_cpy = self.body_node.visit(new_ctx).copy()
        if args:
            val = result_cpy.call(new_ctx, args, False)
            result_cpy = val.copy()

        return result_cpy
