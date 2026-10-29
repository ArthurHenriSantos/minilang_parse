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

def imprimir_ast(node, nivel=0):
    indent = "  " * nivel
    if isinstance(node, Programa):
        print(f"{indent}Programa")
        for cmd in node.comandos: imprimir_ast(cmd, nivel + 1)
    elif isinstance(node, Declaracao):
        print(f"{indent}Declaracao({node.nome})")
    elif isinstance(node, Atribuicao):
        print(f"{indent}Atribuicao({node.nome})")
        imprimir_ast(node.expressao, nivel + 1)
    elif isinstance(node, Saida):
        print(f"{indent}Saida")
        imprimir_ast(node.expressao, nivel + 1)
    elif isinstance(node, Binaria):
        print(f"{indent}Binaria({node.operador})")
        imprimir_ast(node.esquerda, nivel + 1)
        imprimir_ast(node.direita, nivel + 1)
    elif isinstance(node, Inteiro):
        print(f"{indent}Inteiro({node.valor})")
    elif isinstance(node, Variavel):
        print(f"{indent}Variavel({node.nome})")
