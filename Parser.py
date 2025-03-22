from Lexer import Lexer
from Token import Token, TokenType
from typing import Callable
from enum import Enum, auto

# Precedence Types
class PrecedenceType(Enum):
    P_LOWEST = 0
    P_EQUALS = auto()
    P_LESSGREATER = auto()
    P_SUM = auto()
    P_PRODUCT = auto()
    P_EXPONENT = auto()
    P_PREFIX = auto()
    P_CALL = auto()
    P_INDEX = auto()

# Prededence Mapping
PRECEDENCIES: dict[TokenType, PrecedenceType] = {
    TokenType.PLUS: PrecedenceType.P_SUM,
    TokenType.MINUS: PrecedenceType.P_SUM,
    TokenType.DIVD: PrecedenceType.P_PRODUCT,
    TokenType.MULT: PrecedenceType.P_PRODUCT,
    TokenType.MODUL: PrecedenceType.P_PRODUCT,
    TokenType.POW: PrecedenceType.P_EXPONENT
}

class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer: Lexer = lexer

        self.errors: list[str] = []

        self.current_token: Token = lexer.__new_token(TokenType.EMPTY, "EMPTY")
        self.peek_token: Token = lexer.__new_token(TokenType.EMPTY, "EMPTY")

        self.prefix_parse_fns: dict[TokenType, Callable] = {}
        self.infix_parse_fns: dict[TokenType, Callable] = {}

        self.__next_token()
        self.__next_token()

    def __next_token(self) -> None:
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def __peek_token_is(self, tt: TokenType) -> bool:
        return self.peek_token.type == tt

    def __expect_peek(self, tt: TokenType) -> bool:
        if self.__peek_token_is(tt): 
            self.__next_token()
            return True
        else: 
            self.__peek_error(tt)
            return False

    def __current_prededence(self) -> PrecedenceType:
        prec: PrecedenceType | None = PRECEDENCIES.get(self.current_token.type)
        if prec is None:
            return PrecedenceType.P_LOWEST
        return prec

    def __peek_precedence(self) -> PrecedenceType:
        prec: PrecedenceType | None = PRECEDENCIES.get(self.peek_token.type)
        if prec is None:
            return PrecedenceType.P_LOWEST
        return prec

    def __peek_error(self, tt: TokenType) -> None:
        self.errors.append(f"Expected next token to be {tt}, got {self.peek_token.type}")

    def __no_prefix_parse_fn_error(self, tt: TokenType) -> None:
        self.errors.append(f"No Prefix Parse Function for {tt} found")



    def parse_program(self) -> None:
        pass
