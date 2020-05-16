from __future__ import annotations

from sys import getrecursionlimit, setrecursionlimit
from typing import TYPE_CHECKING, List

from context import Context
from lang_types.lang_bool import LangBool
from lang_types.lang_number import LangNumber
from lang_types.type_def import LangVariantTypeDefinition, LangTypeDefinition
from lexer.lexer import Lexer
from parser.parser import Parser
from symbol_table import SymbolTable

if TYPE_CHECKING:
    from lang_types.lang_type import LangType

setrecursionlimit(getrecursionlimit() * 1000)


# TODO think about cross compatibility with python mby some decorator
class Basic:
    def __init__(self) -> None:
        self.syntax_table = SymbolTable()
        self.syntax_table.set("null", LangNumber(0))
        self.syntax_table.set("true", LangBool(True))
        self.syntax_table.set("false", LangBool(False))

        some = LangVariantTypeDefinition("Some", ["Any"])
        none = LangVariantTypeDefinition("None", [])
        self.syntax_table.set("Some", some)
        self.syntax_table.set("None", none)
        self.syntax_table.set("Option", LangTypeDefinition([some, none]))

        head = LangVariantTypeDefinition("List", ["Any", "List"])
        empty = LangVariantTypeDefinition("Empty", [])
        self.syntax_table.set("List", head)
        self.syntax_table.set("Empty", empty)
        self.syntax_table.set("LinkedList", LangTypeDefinition([head, empty]))

    def run(
        self,
        text: str,
        file_name: str,
        repl_mode: bool = False,
        print_tokens: bool = False,
    ) -> List[LangType]:
        lexer = Lexer(text, file_name)
        tokens = lexer.make_tokens()

        if print_tokens:
            print(tokens)
        # Generate AST
        parser = Parser(tokens)

        results: List[LangType] = []
        for ast in parser.parse(repl_mode):
            context = Context(file_name, self.syntax_table)
            res = ast.visit(context)
            results.append(res)
        return results
