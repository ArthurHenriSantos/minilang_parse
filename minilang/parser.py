from minilang.lexer import TokenType
from minilang.ast import (
    Programa, Declaracao, Atribuicao, Saida, Binaria,
    Inteiro, Booleano, Variavel, Bloco, Se, Enquanto, Para
)

class ParseError(Exception):
    def __init__(self, token, mensagem):
        self.token = token
        self.mensagem = mensagem
        super().__init__(self.mensagem)

    def __str__(self):
        if self.token.type == TokenType.EOF:
            return f"Erro Sintático: {self.mensagem}"
        return f"Erro Sintático [Linha {self.token.line}, Col {self.token.column}]: Encontrado '{self.token.lexeme}'. {self.mensagem}"

class Parser:
    def __init__(self, tokens):
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
        if self.match(TokenType.KW_INT, TokenType.KW_BOOL): return self.declaracao()
        if self.match(TokenType.KW_PRINT): return self.saida()
        if self.match(TokenType.KW_IF): return self.se()
        if self.match(TokenType.KW_WHILE): return self.enquanto()
        if self.match(TokenType.KW_FOR): return self.para()
        if self.match(TokenType.LBRACE): return self.bloco()
        return self.atribuicao()

    def bloco(self):
        chave = self.previous()
        comandos = []
        while not self.at_end() and not self.check(TokenType.RBRACE):
            comandos.append(self.item())
        self.expect(TokenType.RBRACE, "Esperado '}' fechando o bloco.")
        return Bloco(comandos, chave.line, chave.column)

    def se(self):
        kw = self.previous()
        self.expect(TokenType.LPAREN, "Esperado '(' após 'if'.")
        cond = self.expressao()
        self.expect(TokenType.RPAREN, "Esperado ')' após a condição.")
        self.expect(TokenType.LBRACE, "Esperado '{' para iniciar o bloco do 'if'.")
        bloco_if = self.bloco()

        bloco_else = None
        if self.match(TokenType.KW_ELSE):
            self.expect(TokenType.LBRACE, "Esperado '{' para iniciar o bloco do 'else'.")
            bloco_else = self.bloco()

        return Se(cond, bloco_if, bloco_else, kw.line, kw.column)

    def enquanto(self):
        kw = self.previous()
        self.expect(TokenType.LPAREN, "Esperado '(' após 'while'.")
        cond = self.expressao()
        self.expect(TokenType.RPAREN, "Esperado ')' após a condição.")
        self.expect(TokenType.LBRACE, "Esperado '{' para iniciar o bloco do 'while'.")
        bloco = self.bloco()
        return Enquanto(cond, bloco, kw.line, kw.column)

    def para(self):
        kw = self.previous()
        self.expect(TokenType.LPAREN, "Esperado '(' após 'for'.")
        inicializacao = self.atribuicao()
        condicao = self.expressao()
        self.expect(TokenType.SEMICOLON, "Esperado ';' após a condição do 'for'.")

        tok_inc = self.expect(TokenType.IDENT, "Esperado nome de variável no incremento do 'for'.")
        self.expect(TokenType.ASSIGN, "Esperado '=' no incremento do 'for'.")
        expr_inc = self.expressao()
        incremento = Atribuicao(tok_inc.lexeme, expr_inc, tok_inc.line, tok_inc.column)

        self.expect(TokenType.RPAREN, "Esperado ')' fechando o 'for'.")
        self.expect(TokenType.LBRACE, "Esperado '{' para iniciar o bloco do 'for'.")
        bloco_for = self.bloco()

        return Para(inicializacao, condicao, incremento, bloco_for, kw.line, kw.column)

    def declaracao(self):
        tipo_tok = self.previous()
        nome_tok = self.expect(TokenType.IDENT, f"Esperado nome da variável após '{tipo_tok.lexeme}'.")
        self.expect(TokenType.SEMICOLON, "Esperado ';' após declaração.")
        return Declaracao(tipo_tok.lexeme, nome_tok.lexeme, nome_tok.line, nome_tok.column)

    def saida(self):
        kw = self.previous()
        self.expect(TokenType.LPAREN, "Esperado '(' após 'print'.")
        expr = self.expressao()
        self.expect(TokenType.RPAREN, "Esperado ')' após a expressão.")
        self.expect(TokenType.SEMICOLON, "Esperado ';' no final do comando print.")
        return Saida(expr, kw.line, kw.column)

    def atribuicao(self):
        nome_tok = self.expect(TokenType.IDENT, "Comando inválido ou esperado nome de variável.")
        self.expect(TokenType.ASSIGN, "Esperado '=' na atribuição.")
        expr = self.expressao()
        self.expect(TokenType.SEMICOLON, "Esperado ';' após atribuição.")
        return Atribuicao(nome_tok.lexeme, expr, nome_tok.line, nome_tok.column)

    def expressao(self):
        return self.igualdade()

    def igualdade(self):
        expr = self.comparacao()
        while self.match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            op = self.previous()
            direita = self.comparacao()
            expr = Binaria(op.lexeme, expr, direita, op.line, op.column)
        return expr

    def comparacao(self):
        expr = self.soma()
        while self.match(TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL):
            op = self.previous()
            direita = self.soma()
            expr = Binaria(op.lexeme, expr, direita, op.line, op.column)
        return expr

    def soma(self):
        expr = self.termo()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.previous()
            direita = self.termo()
            expr = Binaria(op.lexeme, expr, direita, op.line, op.column)
        return expr

    def termo(self):
        expr = self.fator()
        while self.match(TokenType.STAR, TokenType.SLASH):
            op = self.previous()
            direita = self.fator()
            expr = Binaria(op.lexeme, expr, direita, op.line, op.column)
        return expr

    def fator(self):
        if self.match(TokenType.INT_LITERAL):
            tok = self.previous()
            return Inteiro(int(tok.lexeme), tok.line, tok.column)
        if self.match(TokenType.KW_TRUE):
            tok = self.previous()
            return Booleano(True, tok.line, tok.column)
        if self.match(TokenType.KW_FALSE):
            tok = self.previous()
            return Booleano(False, tok.line, tok.column)
        if self.match(TokenType.IDENT):
            tok = self.previous()
            return Variavel(tok.lexeme, tok.line, tok.column)
        if self.match(TokenType.LPAREN):
            expr = self.expressao()
            self.expect(TokenType.RPAREN, "Esperado ')' fechando a expressão.")
            return expr
        raise ParseError(self.peek(), "Expressão inválida. Esperado número, booleano, variável ou '('.")