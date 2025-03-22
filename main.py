from Lexer import Lexer

LEXER_DEBUG: bool = True

print(__name__)

if __name__ == '__main__':
    with open("tests/lexer.tl", "r") as f:
        code: str = f.read()

    if LEXER_DEBUG:
        debug_lex = Lexer(source=code)
        while debug_lex.current_char is not None:
            print(debug_lex.next_token())
