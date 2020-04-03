import re
from typing import Optional, List, Tuple

from Position import Position
from Token import Token
from errors.Error import Error
from errors.IllegalCharacterError import IllegalCharacterError
from token_types import *


class Lexer:
    def __init__(self, text: str, file_name: str):
        self.text = text
        self.pos = Position(-1, 0, -1, file_name, text)
        self.current_char: Optional[str] = None

    def advance(self) -> None:
        self.pos.advance(self.current_char)
        self.current_char = (
            self.text[self.pos.index] if self.pos.index < len(self.text) else None
        )

    @staticmethod
    def is_digit(char: str) -> bool:
        return re.match(r"\d", char) is not None

    def make_tokens(self) -> Tuple[List[Token], Optional[Error]]:
        tokens = []

        self.advance()
        while self.current_char is not None:
            if self.current_char == "+":
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
            elif self.current_char == "-":
                tokens.append(Token(TT_MINUS, pos_start=self.pos))
            elif self.current_char == "*":
                tokens.append(Token(TT_MUL, pos_start=self.pos))
            elif self.current_char == "^":
                tokens.append(Token(TT_POW, pos_start=self.pos))
            elif self.current_char == "/":
                tokens.append(Token(TT_DIV, pos_start=self.pos))
            elif self.current_char == "(":
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
            elif self.current_char == ")":
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
            elif Lexer.is_digit(self.current_char):
                tokens.append(self.make_number())
                continue
            elif not self.current_char.isspace():
                post_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharacterError(post_start, self.pos, char)
            self.advance()
        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self) -> Token:
        num = ""
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char is not None:
            if Lexer.is_digit(self.current_char):
                num += self.current_char
            elif self.current_char == ".":
                if dot_count == 0:
                    dot_count += 1
                    num += "."
                else:
                    break
            else:
                break
            self.advance()
        if dot_count == 0:
            return Token(TT_INT, int(num), pos_start, self.pos)
        return Token(TT_FLOAT, float(num), pos_start, self.pos)
