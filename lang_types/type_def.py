from __future__ import annotations

from typing import List

from lang_types.lang_type import LangType


class LangVariantTypeDefinition(LangType):
    __slots__ = ["name", "args"]

    def __init__(self, name: str, args: List[str]):
        super().__init__("variant_type_definition")
        self.name = name
        self.args = args

    @staticmethod
    def some_type_name() -> str:
        return "Some"

    @staticmethod
    def none_type_name() -> str:
        return "None"

    @staticmethod
    def list_type_name() -> str:
        return "List"

    @staticmethod
    def empty_list_type_name() -> str:
        return "Empty"

    @staticmethod
    def some_type_def() -> LangVariantTypeDefinition:
        return LangVariantTypeDefinition(
            LangVariantTypeDefinition.some_type_name(), ["Any"],
        )

    @staticmethod
    def none_type_def() -> LangVariantTypeDefinition:
        return LangVariantTypeDefinition(
            LangVariantTypeDefinition.none_type_name(), [],
        )

    @staticmethod
    def list_type_def() -> LangVariantTypeDefinition:
        return LangVariantTypeDefinition(
            LangVariantTypeDefinition.list_type_name(), ["Any", "List"],
        )

    @staticmethod
    def empty_list_type_def() -> LangVariantTypeDefinition:
        return LangVariantTypeDefinition(
            LangVariantTypeDefinition.empty_list_type_name(), [],
        )


class LangTypeDefinition(LangType):
    __slots__ = ["variants"]

    def __init__(
        self, variants: List[LangVariantTypeDefinition],
    ):
        super().__init__("type_definition")
        self.variants = variants

    @staticmethod
    def option_type_name() -> str:
        return "Option"

    @staticmethod
    def linked_list_type_name() -> str:
        return "LinkedList"

    @staticmethod
    def option_type_def() -> LangTypeDefinition:
        return LangTypeDefinition(
            [
                LangVariantTypeDefinition.none_type_def(),
                LangVariantTypeDefinition.some_type_def(),
            ],
        )

    @staticmethod
    def linked_list_type_def() -> LangTypeDefinition:
        return LangTypeDefinition(
            [
                LangVariantTypeDefinition.list_type_def(),
                LangVariantTypeDefinition.empty_list_type_def(),
            ],
        )
