from __future__ import annotations
from types_.Type import Type
from typing import Optional
from errors.Error import Error


class RuntimeResult:
    def __init__(self) -> None:
        self.value: Optional[Type] = None
        self.error: Optional[Error] = None

    def __repr__(self) -> str:
        return f"{self.value} {self.error}"

    def register(self, res: RuntimeResult) -> Type:
        if res.error:
            self.error = res.error
        return res.value

    def success(self, value: Type) -> RuntimeResult:
        self.value = value
        return self

    def failure(self, error: Error) -> RuntimeResult:
        self.error = error
        return self
