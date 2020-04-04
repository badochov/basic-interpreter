from __future__ import annotations

from typing import Tuple, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from errors.Error import Error

from Context import Context
from types_.Number import Number
from SymbolTable import SymbolTable
from interpreter.Interpreter import Interpreter
from lexer.Lexer import Lexer
from parser.Parser import Parser

global_syntax_table = SymbolTable()
global_syntax_table.set("null", Number(0))


class Basic:
    @staticmethod
    def run(text: str, file_name: str) -> Tuple[Any, Error]:
        lexer = Lexer(text, file_name)
        tokens, err = lexer.make_tokens()
        if err:
            return None, err

        # Generate AST
        parser = Parser(tokens)
        ast = parser.parse()

        if ast.error or not ast.node:
            return None, ast.error

        interpreter = Interpreter()

        context = Context("<program>", global_syntax_table)

        res = interpreter.visit(ast.node, context)

        return res.value, res.error
