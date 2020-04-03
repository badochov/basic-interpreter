from typing import Tuple, Any

from Context import Context
from Interpreter import Interpreter
from Lexer import Lexer
from Parser import Parser
from errors.Error import Error


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

        if ast.error:
            return None, ast.error

        interpreter = Interpreter()

        context = Context("<program>")

        res = interpreter.visit(ast.node, context)

        return res.value, res.error
