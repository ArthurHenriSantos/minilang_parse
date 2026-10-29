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

    def check(self, tipo):
        if self.at_end() and tipo != TokenType.EOF: return False
        return self.peek().type == tipo

    def match(self, *tipos):
        for tipo in tipos:
            if self.check(tipo):
                self.advance()
                return True
        return False

    def expect(self, tipo_esperado, mensagem):
        if self.check(tipo_esperado): return self.advance()
        raise ParseError(self.peek(), mensagem)

    def parse(self):
        try:
            return self.programa()
        except ParseError as erro:
            return erro

    def programa(self):
        comandos = self.lista_itens()
        self.expect(TokenType.EOF, "Esperado fim do arquivo.")
        return Programa(comandos)

    def lista_itens(self):
        comandos = []
        while not self.at_end():
            comandos.append(self.item())
        return comandos

    def item(self):
        if self.match(TokenType.KW_INT): return self.declaracao()
        if self.match(TokenType.KW_PRINT): return self.saida()
        return self.atribuicao()

    def declaracao(self):
        nome = self.expect(TokenType.IDENT, "Esperado nome da variável após 'int'.").lexeme
        self.expect(TokenType.SEMICOLON, "Esperado ';' após declaração.")
        return Declaracao(nome)

    def saida(self):
        self.expect(TokenType.LPAREN, "Esperado '(' após 'print'.")
        expr = self.expressao()
        self.expect(TokenType.RPAREN, "Esperado ')' após a expressão.")
        self.expect(TokenType.SEMICOLON, "Esperado ';' no final do comando print.")
        return Saida(expr)

    def atribuicao(self):
        nome = self.expect(TokenType.IDENT, "Comando inválido ou esperado nome de variável.").lexeme
        self.expect(TokenType.ASSIGN, "Esperado '=' na atribuição.")
        expr = self.expressao()
        self.expect(TokenType.SEMICOLON, "Esperado ';' após atribuição.")
        return Atribuicao(nome, expr)

    def expressao(self):
        expr = self.termo()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operador = self.previous().lexeme
            direita = self.termo()
            expr = Binaria(operador, expr, direita)
        return expr

    def termo(self):
        expr = self.fator()
        while self.match(TokenType.STAR, TokenType.SLASH):
            operador = self.previous().lexeme
            direita = self.fator()
            expr = Binaria(operador, expr, direita)
        return expr

    def fator(self):
        if self.match(TokenType.INT_LITERAL):
            return Inteiro(int(self.previous().lexeme))
        if self.match(TokenType.IDENT):
            return Variavel(self.previous().lexeme)
        if self.match(TokenType.LPAREN):
            expr = self.expressao()
            self.expect(TokenType.RPAREN, "Esperado ')' fechando a expressão.")
            return expr
        raise ParseError(self.peek(), "Expressão inválida. Esperado número, variável ou '('.")
