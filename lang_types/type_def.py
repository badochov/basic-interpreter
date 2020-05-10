from typing import List

from context import Context
from lang_types.lang_type import LangType
from position import Position


class LangVariantTypeDefinition(LangType):
    def __init__(
        self,
        name: str,
        args: List[str],
        pos_start: Position = None,
        pos_end: Position = None,
        context: Context = None,
    ):
        super().__init__("variant_type_definition", pos_start, pos_end, context)
        self.name = name
        self.args = args


class LangTypeDefinition(LangType):
    def __init__(
        self,
        variants: List[LangVariantTypeDefinition],
        pos_start: Position = None,
        pos_end: Position = None,
        context: Context = None,
    ):
        super().__init__("type_definition", pos_start, pos_end, context)
        self.variants = variants
