from __future__ import annotations

from typing import TYPE_CHECKING, List

from interpreter.runtime_result import RuntimeResult
from lang_types.type_def import LangVariantTypeDefinition, LangTypeDefinition
from nodes.node import Node
from nodes.type_variant_node import TypeVariantNode

if TYPE_CHECKING:
    from context import Context
    from tokens.lang_string_token import StringToken


class TypeDefinitionNode(Node):
    def __init__(
        self, var_name_token: StringToken, variant_nodes: List[TypeVariantNode]
    ) -> None:
        super().__init__(var_name_token.pos_start, variant_nodes[-1].pos_end)
        self.var_name_token = var_name_token
        self.variant_nodes = variant_nodes

    def __repr__(self) -> str:
        return f"({self.var_name_token}: {self.variant_nodes})"

    def visit(self, context: Context) -> RuntimeResult:
        res = RuntimeResult()
        var_name = self.var_name_token.value

        variants: List[LangVariantTypeDefinition] = []
        for variant_node in self.variant_nodes:
            variant = res.register(variant_node.visit(context))
            if res.error or not isinstance(variant, LangVariantTypeDefinition):
                return res
            variants.append(variant)
        type_def = LangTypeDefinition(variants, self.pos_start, self.pos_end, context)
        context.symbol_table.set(var_name, type_def)

        return res.success(type_def)
