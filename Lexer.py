from Token import Token, TokenType
from typing import Any

class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source
        self.position: int = -1
        self.read_postion: int = 0
        self.line_no: int = 1

        self.current_char: str | None = None

        self.__read_char()

    def __read_char(self) -> None:
        if self.read_postion >= len(self.source):
            self.current_char = None
        else:
            self.current_char = self.source[self.read_postion]

        self.position = self.read_postion
        self.read_postion += 1

    def __skip_whitespace(self) -> None:
        while self.current_char in [' ', '\n', '\t', '\r']:
            if self.current_char == '\n':
                self.line_no += 1
            self.__read_char()

    def __new_token(self, tt: TokenType, literal: Any) -> Token:
        return Token(type=tt, literal=literal, line_no=self.line_no, position=self.position)

    def __is_digit(self, ch: str) -> bool:
        return '0' <= ch and ch <= '9'

    def __read_number(self) -> Token:
        start_position: int = self.position
        dot_count: int = 0
        output: str = ""
        while self.__is_digit(self.current_char) or self.current_char == '.': # pyright: ignore[reportArgumentType]
            if self.current_char =='.':
                dot_count += 1
            if dot_count > 1:
                print(f"Too many decimals in number in line {self.line_no}, position {self.position}")
                return self.__new_token(TokenType.ILLEGAL, self.source[start_position:self.position])
            output += self.source[self.position]
            self.__read_char()
            if self.current_char is None:
                break
        if dot_count == 0:
            return self.__new_token(TokenType.INT, int(output))
        else:
            return self.__new_token(TokenType.FLOAT, float(output))


    def next_token(self) -> Token:
        tok: Token = None
        self.__skip_whitespace()

        match self.current_char:
            case '+':
                tok = self.__new_token(TokenType.PLUS, self.current_char)
            case '-':
                tok = self.__new_token(TokenType.MINUS, self.current_char)
            case '*':
                tok = self.__new_token(TokenType.MULT, self.current_char)
            case '/':
                tok = self.__new_token(TokenType.DIVD, self.current_char)
            case '^':
                tok = self.__new_token(TokenType.POW, self.current_char)
            case '%':
                tok = self.__new_token(TokenType.MODUL, self.current_char)
            case '(':
                tok = self.__new_token(TokenType.LPAREN, self.current_char)
            case ')':
                tok = self.__new_token(TokenType.RPAREN, self.current_char)
            case ';':
                tok = self.__new_token(TokenType.SEMICOLON, self.current_char)
            case None:
                tok = self.__new_token(TokenType.EOF, self.current_char)
            case _:
                if self.__is_digit(self.current_char):
                    tok = self.__read_number()
                    return tok
                else:
                    tok = self.__new_token(TokenType.ILLEGAL, self.current_char)
        self.__read_char()
        return tok

