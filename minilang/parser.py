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
