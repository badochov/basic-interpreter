from __future__ import annotations

from sys import getrecursionlimit, setrecursionlimit
from typing import Tuple, TYPE_CHECKING, Optional

from context import Context
from interpreter.interpreter import Interpreter
from lang_types.lang_number import LangNumber
from lexer.lexer import Lexer
from parser.parser import Parser
from symbol_table import SymbolTable

if TYPE_CHECKING:
    from errors.error import Error
    from lang_types.lang_type import LangType

global_syntax_table = SymbolTable()
global_syntax_table.set("null", LangNumber(0))
global_syntax_table.set("true", LangNumber(1))
global_syntax_table.set("false", LangNumber(0))

setrecursionlimit(getrecursionlimit() * 1000)


# TODO think about cross compatibility with python mby some decorator
class Basic:
    @staticmethod
    def run(
        text: str, file_name: str, repl_mode: bool = False, print_tokens: bool = False
    ) -> Tuple[Optional[LangType], Optional[Error]]:
        lexer = Lexer(text, file_name)
        tokens, err = lexer.make_tokens()
        if err:
            return None, err

        if print_tokens:
            print(tokens)
        # Generate AST
        parser = Parser(tokens)
        ast = parser.parse(repl_mode)
        if ast.error or not ast.node:
            return None, ast.error

        interpreter = Interpreter()

        context = Context(file_name, global_syntax_table)
        res = interpreter.visit(ast.node, context)

        return res.value, res.error
