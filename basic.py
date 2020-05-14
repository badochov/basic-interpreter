from __future__ import annotations

from sys import getrecursionlimit, setrecursionlimit
from typing import Tuple, TYPE_CHECKING, Optional, List

from context import Context
from interpreter.interpreter import Interpreter
from lang_types.lang_bool import LangBool
from lang_types.lang_number import LangNumber
from lexer.lexer import Lexer
from parser.parser import Parser
from symbol_table import SymbolTable

if TYPE_CHECKING:
    from errors.error import Error
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
    ) -> List[Tuple[Optional[LangType], Optional[Error]]]:
        lexer = Lexer(text, file_name)
        tokens, err = lexer.make_tokens()
        if err:
            return [(None, err)]

        if print_tokens:
            print(tokens)
        # Generate AST
        parser = Parser(tokens)
        asts = parser.parse(repl_mode)

        results: List[Tuple[Optional[LangType], Optional[Error]]] = []
        for ast in asts:
            if ast.error or not ast.node:
                return [(None, ast.error)]

            interpreter = Interpreter()

            context = Context(file_name, global_syntax_table)
            res = interpreter.visit(ast.node, context)
            results.append((res.value, res.error))
        return results
