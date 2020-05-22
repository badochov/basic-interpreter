from __future__ import annotations

from typing import List

from lang_types.lang_type import LangType
from lang_types.type_def import LangVariantTypeDefinition


class LangVariantType(LangType):
    def __init__(self, args: List[LangType], name: str):
        super().__init__("variant_type")
        self.args = args
        self.type_variant_name = name

    def __repr__(self) -> str:
        return f"{self.type_variant_name} of {self.args}"

    def is_of_type(self, name: str) -> bool:
        return name == self.type_variant_name

    @staticmethod
    def parse_list(variant_type: LangVariantType) -> List[LangType]:
        if variant_type.is_of_type(LangVariantTypeDefinition.list_type_name()):
            head = [variant_type.args[0]]
            tail = variant_type.args[1]
            if isinstance(tail, LangVariantType):
                head.extend(LangVariantType.parse_list(tail))
                return head
        elif variant_type.is_of_type(LangVariantTypeDefinition.empty_list_type_name()):
            return []
        raise TypeError

    @staticmethod
    def make_list(values: List[LangType]) -> LangVariantType:
        res = LangVariantType([], LangVariantTypeDefinition.empty_list_type_name(),)
        for value in reversed(values):
            res = LangVariantType(
                [value, res], LangVariantTypeDefinition.list_type_name()
            )

        return res

    def get_args(self) -> List[LangType]:
        return self.args
