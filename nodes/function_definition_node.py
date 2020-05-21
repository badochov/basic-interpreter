from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from lang_types.lang_function import LangFunction
from nodes.node import Node
from nodes.variable_assignment_node import VariableAssignmentNode

if TYPE_CHECKING:
    from lang_types.lang_type import LangType
    from context import Context


class FunctionDefinitionNode(Node):
    def __init__(
        self,
        var_name_node: Optional[VariableAssignmentNode],
        arg_names_nodes: Optional[VariableAssignmentNode],
        body_node: Node,
        save_name: bool = True,
    ):
        if var_name_node:
            pos_start = var_name_node.pos_start
        elif arg_names_nodes:
            pos_start = arg_names_nodes.pos_start
        else:
            pos_start = body_node.pos_start

        super().__init__(pos_start, body_node.pos_end)
        self.var_name_node = var_name_node
        self.arg_name_node = arg_names_nodes
        self.body_node = body_node
        self.save_name = save_name

    def __repr__(self) -> str:
        return (
            f"({self.var_name_node or '<anonymous>'}"
            f"({self.arg_name_node}) -> {self.body_node})"
        )

    def visit(self, context: Context) -> LangType:
        if self.arg_name_node:
            value: LangType = LangFunction(
                self.var_name_node.get_names()[0] if self.var_name_node else None,
                self.arg_name_node,
                self.body_node,
                self.pos_start,
                self.pos_end,
                context,
            )
        else:
            value = self.body_node.visit(context)
        if self.save_name:
            assert self.var_name_node is not None
            self.var_name_node.set_value(value)
            self.var_name_node.visit(context)
        return value
