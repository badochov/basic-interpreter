from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from errors.error import Error
    from lang_types.lang_type import LangType


class RuntimeResult:
    def __init__(self) -> None:
        self.value: Optional[LangType] = None
        self.error: Optional[Error] = None

    def __repr__(self) -> str:
        return f"{self.value} {self.error}"

    def register(self, res: RuntimeResult) -> Optional[LangType]:
        if res.error:
            self.error = res.error
        return res.value

    def success(self, value: LangType) -> RuntimeResult:
        self.value = value
        return self

    def failure(self, error: Error) -> RuntimeResult:
        self.error = error
        return self
