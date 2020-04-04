from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from errors.Error import Error
    from nodes.Node import Node
    from Token import Token


class ParseResult:
    def __init__(self) -> None:
        self.error: Optional[Error] = None
        self.node: Optional[Node] = None
        self.advance_count = 0

    def register(self, res: ParseResult) -> Optional[Node]:
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def register_advancement(self, advancement: Token) -> None:
        self.advance_count += 1

    def success(self, node: Node) -> ParseResult:
        self.node = node
        return self

    def failure(self, error: Error) -> ParseResult:
        if not self.error or self.advance_count == 0:
            self.error = error
        return self

    def __repr__(self) -> str:
        return f"{self.node, self.error}"
