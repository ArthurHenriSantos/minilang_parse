class ASTNode:
    pass

class Programa(ASTNode):
    def _init_(self, comandos):
        self.comandos = comandos

class Declaracao(ASTNode):
    def _init_(self, nome):
        self.nome = nome

class Atribuicao(ASTNode):
    def _init_(self, nome, expressao):
        self.nome = nome
        self.expressao = expressao

class Saida(ASTNode):
    def _init_(self, expressao):
        self.expressao = expressao

class Binaria(ASTNode):
    def _init_(self, operador, esquerda, direita):
        self.operador = operador
        self.esquerda = esquerda
        self.direita = direita

class Inteiro(ASTNode):
    def _init_(self, valor):
        self.valor = valor

class Variavel(ASTNode):
    def _init_(self, nome):
        self.nome = nome