class ASTNode:
    pass

class Programa(ASTNode):
    def __init__(self, comandos):
        self.comandos = comandos

class Declaracao(ASTNode):
    def __init__(self, nome):
        self.nome = nome

class Atribuicao(ASTNode):
    def __init__(self, nome, expressao):
        self.nome = nome
        self.expressao = expressao

class Saida(ASTNode):
    def __init__(self, expressao):
        self.expressao = expressao

class Binaria(ASTNode):
    def __init__(self, operador, esquerda, direita):
        self.operador = operador
        self.esquerda = esquerda
        self.direita = direita

class Inteiro(ASTNode):
    def __init__(self, valor):
        self.valor = valor

class Variavel(ASTNode):
    def __init__(self, nome):
        self.nome = nome

class Bloco(ASTNode):
    def __init__(self, comandos):
        self.comandos = comandos

class Condicao(ASTNode):
    def __init__(self, operador, esquerda, direita):
        self.operador = operador
        self.esquerda = esquerda
        self.direita = direita

class Se(ASTNode):
    def __init__(self, condicao, bloco_if, bloco_else=None):
        self.condicao = condicao
        self.bloco_if = bloco_if
        self.bloco_else = bloco_else

class Enquanto(ASTNode):
    def __init__(self, condicao, bloco):
        self.condicao = condicao
        self.bloco = bloco

class Para(ASTNode):
    def __init__(self, inicializacao, condicao, incremento, bloco):
        self.inicializacao = inicializacao
        self.condicao = condicao
        self.incremento = incremento
        self.bloco = bloco

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
    elif isinstance(node, Bloco):
        print(f"{indent}Bloco")
        if not node.comandos:
            print(f"{indent}  (vazio)")
        for cmd in node.comandos: imprimir_ast(cmd, nivel + 1)
    elif isinstance(node, Condicao):
        print(f"{indent}Condicao({node.operador})")
        imprimir_ast(node.esquerda, nivel + 1)
        imprimir_ast(node.direita, nivel + 1)
    elif isinstance(node, Se):
        print(f"{indent}Se")
        imprimir_ast(node.condicao, nivel + 1)
        imprimir_ast(node.bloco_if, nivel + 1)
        if node.bloco_else:
            print(f"{indent}Senao")
            imprimir_ast(node.bloco_else, nivel + 1)
    elif isinstance(node, Enquanto):
        print(f"{indent}Enquanto")
        imprimir_ast(node.condicao, nivel + 1)
        imprimir_ast(node.bloco, nivel + 1)
    elif isinstance(node, Para):
        print(f"{indent}Para")
        print(f"{indent}  Inicializacao:")
        imprimir_ast(node.inicializacao, nivel + 2)
        print(f"{indent}  Condicao:")
        imprimir_ast(node.condicao, nivel + 2)
        print(f"{indent}  Incremento:")
        imprimir_ast(node.incremento, nivel + 2)
        print(f"{indent}  Bloco:")
        imprimir_ast(node.bloco, nivel + 2)