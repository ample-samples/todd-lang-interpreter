from ast import expr
from Lexer import Lexer
from Token import Token, TokenType
from typing import Callable
from enum import Enum, auto
from AST import Statement, Expression, Program
from AST import ExpressionStatement
from AST import InfixEpression
from AST import IntegerLiteral, FloatLiteral

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

        self.current_token: Token = None
        self.peek_token: Token = None

        self.prefix_parse_fns: dict[TokenType, Callable] = {
            TokenType.INT: self.__parse_int_literal,
            TokenType.FLOAT: self.__parse_float_literal,
            TokenType.LPAREN: self.__parse_grouped_expression
        }
        self.infix_parse_fns: dict[TokenType, Callable] = {
            TokenType.PLUS: self.__parse_infix_expression,
            TokenType.MINUS: self.__parse_infix_expression,
            TokenType.DIVD: self.__parse_infix_expression,
            TokenType.MULT: self.__parse_infix_expression,
            TokenType.MODUL: self.__parse_infix_expression,
            TokenType.POW: self.__parse_infix_expression
        }

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



    def parse_program(self) -> Program:
        program: Program = Program()

        while self.current_token.type != TokenType.EOF:
            statement: Statement = self.__parse_statement()
            if statement is not None:
                program.statements.append(statement)

            self.__next_token()

        return program

    def __parse_statement(self) -> Statement:
        return self.__parse_expression_statement()

    def __parse_expression_statement(self) -> ExpressionStatement:
        expr = self.__parse_expression(PrecedenceType.P_LOWEST)

        if self.__peek_token_is(TokenType.SEMICOLON):
            self.__next_token()

        statement: ExpressionStatement = ExpressionStatement(expr=expr)

        return statement

    def __parse_expression(self, precendence: PrecedenceType) -> Expression:
        prefix_fn: Callable | None = self.prefix_parse_fns.get(self.current_token.type)
        if prefix_fn is None:
            self.__no_prefix_parse_fn_error(self.current_token.type)
            return None  # pyright: ignore[reportReturnType]

        left_expr: Expression = prefix_fn()
        while not self.__peek_token_is(TokenType.SEMICOLON) and precendence.value < self.__peek_precedence().value:
            infix_fn: Callable | None = self.infix_parse_fns.get(self.peek_token.type)
            if infix_fn is None:
                return left_expr
            self.__next_token()
            left_expr = infix_fn(left_expr)

        return left_expr

    def __parse_infix_expression(self, left_node: Expression) -> Expression:
        infix_expr: InfixEpression = InfixEpression(left_node=left_node, operator=self.current_token.literal)

        precedence = self.__current_prededence()

        self.__next_token()

        infix_expr.right_node = self.__parse_expression(precedence)

        return infix_expr

    def __parse_grouped_expression(self) -> Expression | None:
        self.__next_token()
        expr: Expression = self.__parse_expression(PrecedenceType.P_LOWEST)

        if not self.__expect_peek(TokenType.RPAREN):
            return None

        return expr

    def __parse_int_literal(self) -> Expression | None:
        int_lit: IntegerLiteral = IntegerLiteral()

        try:
            int_lit.value = int(self.current_token.literal)
        except:
            self.errors.append(f"Could not pars `{self.current_token.literal}` as an integer.")
            return None
        return int_lit

    def __parse_float_literal(self) -> Expression | None:
        float_lit: FloatLiteral = FloatLiteral()

        try:
            float_lit.value = int(self.current_token.literal)
        except:
            self.errors.append(f"Could not pars `{self.current_token.literal}` as a float.")
            return None
        return float_lit
