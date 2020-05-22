from __future__ import annotations

from typing import TYPE_CHECKING, List

from lang_types.type_def import LangVariantTypeDefinition, LangTypeDefinition
from nodes.node import Node
from nodes.type_variant_node import TypeVariantNode

if TYPE_CHECKING:
    from context import Context
    from tokens.lang_string_token import StringToken


class TypeDefinitionNode(Node):
    __slots__ = ["var_name_token", "variant_nodes"]

    def __init__(
        self, var_name_token: StringToken, variant_nodes: List[TypeVariantNode]
    ) -> None:
        super().__init__(var_name_token.pos_start, variant_nodes[-1].pos_end)
        self.var_name_token = var_name_token
        self.variant_nodes = variant_nodes

    def __repr__(self) -> str:
        return f"({self.var_name_token}: {self.variant_nodes})"

    def visit(self, context: Context) -> LangTypeDefinition:
        var_name = self.var_name_token.value

        variants: List[LangVariantTypeDefinition] = []
        for variant_node in self.variant_nodes:
            variants.append(variant_node.visit(context))
        type_def = LangTypeDefinition(variants)
        context.set(var_name, type_def)

        return type_def
