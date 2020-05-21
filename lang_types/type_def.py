from __future__ import annotations

from typing import List, TYPE_CHECKING

from context import mock_context
from lang_types.lang_type import LangType
from position import mock_position

if TYPE_CHECKING:
    from context import Context
    from position import Position


class LangVariantTypeDefinition(LangType):
    def __init__(
        self,
        name: str,
        args: List[str],
        pos_start: Position,
        pos_end: Position,
        context: Context,
    ):
        super().__init__("variant_type_definition", pos_start, pos_end, context)
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
            LangVariantTypeDefinition.some_type_name(),
            ["Any"],
            mock_position,
            mock_position,
            mock_context,
        )

    @staticmethod
    def none_type_def() -> LangVariantTypeDefinition:
        return LangVariantTypeDefinition(
            LangVariantTypeDefinition.none_type_name(),
            [],
            mock_position,
            mock_position,
            mock_context,
        )

    @staticmethod
    def list_type_def() -> LangVariantTypeDefinition:
        return LangVariantTypeDefinition(
            LangVariantTypeDefinition.list_type_name(),
            ["Any", "List"],
            mock_position,
            mock_position,
            mock_context,
        )

    @staticmethod
    def empty_list_type_def() -> LangVariantTypeDefinition:
        return LangVariantTypeDefinition(
            LangVariantTypeDefinition.empty_list_type_name(),
            [],
            mock_position,
            mock_position,
            mock_context,
        )


class LangTypeDefinition(LangType):
    def __init__(
        self,
        variants: List[LangVariantTypeDefinition],
        pos_start: Position,
        pos_end: Position,
        context: Context,
    ):
        super().__init__("type_definition", pos_start, pos_end, context)
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
            mock_position,
            mock_position,
            mock_context,
        )

    @staticmethod
    def linked_list_type_def() -> LangTypeDefinition:
        return LangTypeDefinition(
            [
                LangVariantTypeDefinition.list_type_def(),
                LangVariantTypeDefinition.empty_list_type_def(),
            ],
            mock_position,
            mock_position,
            mock_context,
        )
