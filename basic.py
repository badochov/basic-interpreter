from __future__ import annotations

from sys import getrecursionlimit, setrecursionlimit
from typing import TYPE_CHECKING, List

from context import Context
from interpreter.interpreter import Interpreter
from lang_types.lang_bool import LangBool
from lang_types.lang_number import LangNumber
from lexer.lexer import Lexer
from parser.parser import Parser
from symbol_table import SymbolTable

if TYPE_CHECKING:
    from lang_types.lang_type import LangType

global_syntax_table = SymbolTable()
global_syntax_table.set("null", LangNumber(0))
global_syntax_table.set("true", LangBool(True))
global_syntax_table.set("false", LangBool(False))

setrecursionlimit(getrecursionlimit() * 1000)


# TODO think about cross compatibility with python mby some decorator
class Basic:
    @staticmethod
    def run(
        text: str, file_name: str, repl_mode: bool = False, print_tokens: bool = False
    ) -> List[LangType]:
        lexer = Lexer(text, file_name)
        tokens = lexer.make_tokens()

        if print_tokens:
            print(tokens)
        # Generate AST
        parser = Parser(tokens)

        results: List[LangType] = []
        for ast in parser.parse(repl_mode):

            interpreter = Interpreter()

            context = Context(file_name, global_syntax_table)
            res = interpreter.visit(ast, context)
            results.append(res)
        return results
