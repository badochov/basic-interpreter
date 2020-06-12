from __future__ import annotations

from typing import Optional, List, Tuple, TYPE_CHECKING

from errors.illegal_character_error import IllegalCharacterError
from errors.unexpected_char_error import UnexpectedCharError
from keywords import KEYWORDS
from position import Position
from token_types import *
from tokens.lang_empty_token import EmptyToken
from tokens.lang_number_token import NumberToken
from tokens.lang_string_token import StringToken
from tokens.lang_token import Token

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

    def make_tokens(self) -> List[Token]:
        comment = False
        tokens: List[Token] = []

        self.advance()
        while self.current_char is not None:
            if comment:
                if self.current_char in "\n\r":
                    comment = False
                else:
                    self.advance()
                    continue
            if self.current_char == "+":
                tokens.append(EmptyToken(TT_PLUS, self.pos, self.pos))
            elif self.current_char == "-":
                tokens.append(self.make_minus_or_arrow())
                continue
            elif self.current_char == "#":
                comment = True
            elif self.current_char == "*":
                tokens.append(EmptyToken(TT_MUL, self.pos, self.pos))
            elif self.current_char == "^":
                tokens.append(EmptyToken(TT_POW, self.pos, self.pos))
            elif self.current_char == "/":
                tokens.append(EmptyToken(TT_DIV, self.pos, self.pos))
            elif self.current_char == "(":
                tokens.append(EmptyToken(TT_LPAREN, self.pos, self.pos))
            elif self.current_char == ")":
                tokens.append(EmptyToken(TT_RPAREN, self.pos, self.pos))
            elif self.current_char == "[":
                tokens.append(EmptyToken(TT_LBRACKET, self.pos, self.pos))
            elif self.current_char == "]":
                tokens.append(EmptyToken(TT_RBRACKET, self.pos, self.pos))
            elif self.current_char == "{":
                tokens.append(EmptyToken(TT_LCURLY, self.pos, self.pos))
            elif self.current_char == "}":
                tokens.append(EmptyToken(TT_RCURLY, self.pos, self.pos))
            elif self.current_char == ";":
                tokens.append(EmptyToken(TT_SEMICOLON, self.pos, self.pos))
            elif self.current_char == "|":
                tokens.append(
                    StringToken(TT_KEYWORD, self.pos, self.pos, KEYWORDS["MATCH_OR"])
                )
            elif self.current_char == ",":
                tokens.append(EmptyToken(TT_COMA, self.pos, self.pos))
            elif self.current_char == ":":
                tokens.append(EmptyToken(TT_COLON, self.pos, self.pos))
            elif self.current_char == "=":
                tokens.append(self.make_equals())
                continue
            elif self.current_char == "<":
                tokens.append(self.make_less_than())
                continue
            elif self.current_char == ">":
                tokens.append(self.make_greater_than())
                continue
            elif self.current_char == "!":
                token, error = self.make_not_equals()
                if error or token is None:
                    return []
                tokens.append(token)
                continue
            elif self.current_char.isdigit():
                tokens.append(self.make_number())
                continue
            elif self.current_char == "_" or (
                self.current_char.isalnum() and not self.current_char.isdigit()
            ):
                tokens.append(self.make_identifier())
                continue
            elif not self.current_char.isspace():
                post_start = self.pos.copy()
                char = self.current_char
                self.advance()
                raise IllegalCharacterError(post_start, self.pos, char)
            self.advance()
        tokens.append(EmptyToken(TT_EOF, self.pos, self.pos))
        return tokens

    def make_number(self) -> Token:
        num = ""
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char is not None:
            if self.current_char.isdigit():
                pass
            elif self.current_char == ".":
                if dot_count == 0:
                    dot_count += 1
                else:
                    break
            else:
                break
            num += self.current_char
            self.advance()
        if dot_count == 0:
            return NumberToken(TT_INT, pos_start, self.pos, int(num))
        return NumberToken(TT_FLOAT, pos_start, self.pos, float(num))

    def make_identifier(self) -> Token:
        id_str = ""
        pos_start = self.pos.copy()

        while self.current_char and (
            self.current_char.isalnum() or self.current_char == "_"
        ):
            id_str += self.current_char
            self.advance()

        tok_type = TT_KEYWORD if id_str in KEYWORDS.values() else TT_IDENTIFIER
        return StringToken(tok_type, pos_start, self.pos, id_str)

    def make_not_equals(self) -> Tuple[Optional[Token], Optional[Error]]:
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == "=":
            self.advance()
            return EmptyToken(TT_NE, pos_start, self.pos), None
        return (
            None,
            UnexpectedCharError(pos_start, self.pos, 'after "!" should be "="'),
        )

    def make_equals(self) -> Token:
        token_type = TT_EQUALS
        pos_start = self.pos.copy()

        self.advance()
        if self.current_char == "=":
            self.advance()
            token_type = TT_EE

        return EmptyToken(token_type, pos_start, self.pos)

    def make_greater_than(self) -> Token:
        token_type = TT_GT
        pos_start = self.pos.copy()

        self.advance()
        if self.current_char == "=":
            self.advance()
            token_type = TT_GTE

        return EmptyToken(token_type, pos_start, self.pos)

    def make_less_than(self) -> Token:
        token_type = TT_LT
        pos_start = self.pos.copy()

        self.advance()
        if self.current_char == "=":
            self.advance()
            token_type = TT_LTE

        return EmptyToken(token_type, pos_start, self.pos)

    def make_minus_or_arrow(self) -> Token:
        token_type = TT_MINUS
        pos_start = self.pos.copy()

        self.advance()
        if self.current_char == ">":
            self.advance()
            token_type = TT_ARROW

        return EmptyToken(token_type, pos_start, self.pos)
