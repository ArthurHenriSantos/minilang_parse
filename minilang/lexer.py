from enum import Enum
from dataclasses import dataclass

class TokenType(Enum):
    KW_INT = "KW_INT"
    KW_PRINT = "KW_PRINT"
    IDENT = "IDENT"
    INT_LITERAL = "INT_LITERAL"
    ASSIGN = "ASSIGN"
    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    SEMICOLON = "SEMICOLON"
    EOF = "EOF"

@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int

@dataclass
class Diagnostic:
    line: int
    column: int
    message: str

DIGITS = "0123456789"
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"

KEYWORDS = {
    "int": TokenType.KW_INT,
    "print": TokenType.KW_PRINT
}

class Lexer:
    def __init__(self, source: str):
        self.source = source.replace("\r\n", "\n").replace("\r", "\n")
        self.current = 0
        self.line = 1
        self.column = 1
        self.start_line = 1
        self.start_column = 1
        self.tokens = []
        self.diagnostics = []

    def at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        c = self.source[self.current]
        self.current += 1
        if c == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return c

    def peek(self):
        if self.at_end(): return "\0"
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source): return "\0"
        return self.source[self.current + 1]

    def add_token(self, start, type):
        lexeme = self.source[start:self.current]
        self.tokens.append(Token(type, lexeme, self.start_line, self.start_column))

    def scan_tokens(self):
        while not self.at_end():
            start = self.current
            self.start_line = self.line
            self.start_column = self.column

            if self.peek() == '/' and self.peek_next() == '/':
                self.advance()
                self.advance()
                while not self.at_end() and self.peek() != '\n': self.advance()
                continue

            c = self.advance()

            if c in " \t\r\n": continue
            elif c in LETTERS:
                while self.peek() in LETTERS or self.peek() in DIGITS: self.advance()
                lexeme = self.source[start:self.current]
                self.add_token(start, KEYWORDS.get(lexeme, TokenType.IDENT))
            elif c in DIGITS:
                while self.peek() in DIGITS: self.advance()
                self.add_token(start, TokenType.INT_LITERAL)
            elif c == '=': self.add_token(start, TokenType.ASSIGN)
            elif c == '+': self.add_token(start, TokenType.PLUS)
            elif c == '-': self.add_token(start, TokenType.MINUS)
            elif c == '*': self.add_token(start, TokenType.STAR)
            elif c == '/': self.add_token(start, TokenType.SLASH)
            elif c == '(': self.add_token(start, TokenType.LPAREN)
            elif c == ')': self.add_token(start, TokenType.RPAREN)
            elif c == ';': self.add_token(start, TokenType.SEMICOLON)
            else:
                self.diagnostics.append(Diagnostic(self.start_line, self.start_column, f"Símbolo inválido '{c}'"))

        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens, self.diagnostics
