from __future__ import annotations

from typing import List, Optional, Callable, cast, TYPE_CHECKING

from lang_types.lang_bool import LangBool
from lang_types.lang_type import LangType, IllegalOperationType
from lang_types.type_def import LangVariantTypeDefinition

if TYPE_CHECKING:
    from lang_types.lang_type import CompType
else:
    CompType = None


def _same_variant_type(
    func: Callable[[LangVariantType, LangVariantType], CompType]
) -> Callable[[LangVariantType, LangType], CompType]:
    def check_variant_type(self: LangVariantType, other: LangType) -> CompType:
        if isinstance(other, LangVariantType):
            if self.type_variant_name != other.type_variant_name:
                return IllegalOperationType(
                    "Variant types must be of the same time for comparison operators"
                )
        else:
            return IllegalOperationType(
                "Variant types can only be compared with themselves"
            )
        return func(self, other)

    return check_variant_type


class LangVariantType(LangType):
    __slots__ = ["args", "type_variant_name"]

    def __init__(self, args: List[LangType], name: str):
        super().__init__("variant_type")
        self.args = args
        self.type_variant_name = name

    def __repr__(self) -> str:
        return f"{self.type_variant_name} of {self.args}"

    def is_of_type(self, name: str) -> bool:
        return name == self.type_variant_name

    @staticmethod
    def parse_list(variant_type: LangVariantType) -> Optional[List[LangType]]:
        if variant_type.is_of_type(LangVariantTypeDefinition.list_type_name()):
            head = [variant_type.args[0]]
            tail = variant_type.args[1]
            if isinstance(tail, LangVariantType):
                if (t_list := LangVariantType.parse_list(tail)) is None:
                    return None
                head.extend(t_list)
                return head
        elif variant_type.is_of_type(LangVariantTypeDefinition.empty_list_type_name()):
            return []
        return None

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

    @_same_variant_type
    def get_comparison_eq_by(self, other: LangVariantType) -> CompType:
        return LangVariantType.compare(self, other, "get_comparison_eq")

    @_same_variant_type
    def get_comparison_lt_by(self, other: LangVariantType) -> CompType:
        return LangVariantType.compare(self, other, "get_comparison_lt")

    @_same_variant_type
    def get_comparison_lte_by(self, other: LangVariantType) -> CompType:
        return LangVariantType.compare(self, other, "get_comparison_lte")

    @_same_variant_type
    def get_comparison_gt_by(self, other: LangVariantType) -> CompType:
        return LangVariantType.compare(self, other, "get_comparison_gt")

    @_same_variant_type
    def get_comparison_gte_by(self, other: LangVariantType) -> CompType:
        return LangVariantType.compare(self, other, "get_comparison_gte")

    @staticmethod
    def compare(
        first: LangVariantType, second: LangVariantType, method: str
    ) -> CompType:
        for first_arg, second_arg in zip(first.args, second.args):
            res = cast(CompType, getattr(first_arg, method)(second_arg))
            if isinstance(res, LangBool):
                if res.is_truthy():
                    continue
            return res
        return LangBool.true_def()
