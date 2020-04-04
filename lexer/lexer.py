from __future__ import annotations

import re
from typing import Optional, List, Tuple, TYPE_CHECKING

from position import Position
from token import Token
from errors.illegal_character_error import IllegalCharacterError
from keywords import KEYWORDS
from token_types import *

if TYPE_CHECKING:
    from errors.error import Error


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

    @staticmethod
    def is_letter(char: str) -> bool:
        return Lexer.is_alphanumeric(char) and not Lexer.is_digit(char)

    @staticmethod
    def is_alphanumeric(char: str) -> bool:
        return re.match(r"\w", char) is not None

    def make_tokens(self) -> Tuple[List[Token], Optional[Error]]:
        tokens = []

        self.advance()
        while self.current_char is not None:
            if self.current_char == "+":
                tokens.append(Token(TT_PLUS, self.pos, self.pos))
            elif self.current_char == "-":
                tokens.append(Token(TT_MINUS, self.pos, self.pos))
            elif self.current_char == "*":
                tokens.append(Token(TT_MUL, self.pos, self.pos))
            elif self.current_char == "^":
                tokens.append(Token(TT_POW, self.pos, self.pos))
            elif self.current_char == "/":
                tokens.append(Token(TT_DIV, self.pos, self.pos))
            elif self.current_char == "(":
                tokens.append(Token(TT_LPAREN, self.pos, self.pos))
            elif self.current_char == ")":
                tokens.append(Token(TT_RPAREN, self.pos, self.pos))
            elif self.current_char == "=":
                tokens.append(Token(TT_EQUALS, self.pos, self.pos))
            elif Lexer.is_digit(self.current_char):
                tokens.append(self.make_number())
                continue
            elif Lexer.is_letter(self.current_char):
                tokens.append(self.make_identifier())
                continue
            elif not self.current_char.isspace():
                post_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharacterError(post_start, self.pos, char)
            self.advance()
        tokens.append(Token(TT_EOF, self.pos, self.pos))
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
            return Token(TT_INT, pos_start, self.pos, int(num))
        return Token(TT_FLOAT, pos_start, self.pos, float(num))

    def make_identifier(self) -> Token:
        id_str = ""
        pos_start = self.pos.copy()

        while self.current_char and Lexer.is_alphanumeric(self.current_char):
            id_str += self.current_char
            self.advance()

        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, pos_start, self.pos, id_str)
