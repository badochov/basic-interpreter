from __future__ import annotations
from typing import Optional
from errors.Error import Error
from nodes.Node import Node
from typing import Any, Union


class ParseResult:
    def __init__(self) -> None:
        self.error: Optional[Error] = None
        self.node: Optional[Node] = None

    def register(self, res: Any) -> Node:
        if isinstance(res, ParseResult):
            if res.error:
                self.error = res.error
            return res.node
        return res

    def success(self, node: Node) -> ParseResult:
        self.node = node
        return self

    def failure(self, error: Error) -> ParseResult:
        self.error = error
        return self

    def __repr__(self) -> str:
        return f"{self.node, self.error}"
