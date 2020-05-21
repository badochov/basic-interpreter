from __future__ import annotations

from sys import getrecursionlimit, setrecursionlimit
from typing import TYPE_CHECKING, List

from context import Context
from lang_types.lang_bool import LangBool
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
        self.syntax_table.set(LangBool.true_name(), LangBool.true_def())
        self.syntax_table.set(LangBool.false_name(), LangBool.false_def())

        self.syntax_table.set(
            LangVariantTypeDefinition.some_type_name(),
            LangVariantTypeDefinition.some_type_def(),
        )
        self.syntax_table.set(
            LangVariantTypeDefinition.none_type_name(),
            LangVariantTypeDefinition.none_type_def(),
        )
        self.syntax_table.set(
            LangTypeDefinition.option_type_name(), LangTypeDefinition.option_type_def()
        )

        self.syntax_table.set(
            LangVariantTypeDefinition.list_type_name(),
            LangVariantTypeDefinition.list_type_def(),
        )
        self.syntax_table.set(
            LangVariantTypeDefinition.empty_list_type_name(),
            LangVariantTypeDefinition.empty_list_type_def(),
        )
        self.syntax_table.set(
            LangTypeDefinition.linked_list_type_name(),
            LangTypeDefinition.linked_list_type_def(),
        )

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
