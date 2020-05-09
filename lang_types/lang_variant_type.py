from typing import List, TYPE_CHECKING

from lang_types.lang_type import LangType

if TYPE_CHECKING:
    from lang_types.variant import Variant


class LangVariantType(LangType):
    variants: List[Variant]
