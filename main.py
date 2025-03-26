from Lexer import Lexer
from Parser import Parser
from AST import Program
import json

LEXER_DEBUG: bool = True
PARSER_DEBUG: bool = True

if __name__ == '__main__':
    with open("tests/parser.tl", "r") as f:
        code: str = f.read()

    if LEXER_DEBUG:
        debug_lex = Lexer(source=code)
        while debug_lex.current_char is not None:
            print(debug_lex.next_token())

    lexer: Lexer = Lexer(source=code)
    parser: Parser = Parser(lexer=lexer)

    if PARSER_DEBUG:
        program: Program = parser.parse_program()

        with open("debug/ast.json", "w") as f:
            print(program.json())
            json.dump(program.json(), f, indent=4)
