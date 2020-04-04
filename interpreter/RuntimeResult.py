from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from errors.Error import Error
    from types_.Type import Type


class RuntimeResult:
    def __init__(self) -> None:
        self.value: Optional[Type] = None
        self.error: Optional[Error] = None

    def __repr__(self) -> str:
        return f"{self.value} {self.error}"

    def register(self, res: RuntimeResult) -> Optional[Type]:
        if res.error:
            self.error = res.error
        return res.value

    def success(self, value: Type) -> RuntimeResult:
        self.value = value
        return self

    def failure(self, error: Error) -> RuntimeResult:
        self.error = error
        return self
