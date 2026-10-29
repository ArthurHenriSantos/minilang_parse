from minilang.lexer import TokenType
from minilang.ast import Programa, Declaracao, Atribuicao, Saida, Binaria, Inteiro, Variavel

class ParseError(Exception):
    def _init_(self, token, mensagem):
        self.token = token
        self.mensagem = mensagem
        super()._init_(self.mensagem)

    def _str_(self):
        if self.token.type == TokenType.EOF:
            return f"Erro Sintático: {self.mensagem}"
        return f"Erro Sintático [Linha {self.token.line}, Col {self.token.column}]: Encontrado '{self.token.lexeme}'. {self.mensagem}"

class Parser:
    def _init_(self, tokens):
        self.tokens = tokens
        self.current = 0

    def peek(self): return self.tokens[self.current]
    def previous(self): return self.tokens[self.current - 1]
    def at_end(self): return self.peek().type == TokenType.EOF
    
    def advance(self):
        if not self.at_end(): self.current += 1
        return self.previous()
