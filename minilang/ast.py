class ASTNode:
    def __init__(self, line=0, column=0):
        self.line = line
        self.column = column
        self.tipo_inferido = None
        self.simbolo = None

class Programa(ASTNode):
    def __init__(self, comandos):
        super().__init__(1, 1)
        self.comandos = comandos

class Declaracao(ASTNode):
    def __init__(self, tipo, nome, line, column):
        super().__init__(line, column)
        self.tipo = tipo
        self.nome = nome

class Atribuicao(ASTNode):
    def __init__(self, nome, expressao, line, column):
        super().__init__(line, column)
        self.nome = nome
        self.expressao = expressao

class Saida(ASTNode):
    def __init__(self, expressao, line, column):
        super().__init__(line, column)
        self.expressao = expressao

class Binaria(ASTNode):
    def __init__(self, operador, esquerda, direita, line, column):
        super().__init__(line, column)
        self.operador = operador
        self.esquerda = esquerda
        self.direita = direita

class Inteiro(ASTNode):
    def __init__(self, valor, line, column):
        super().__init__(line, column)
        self.valor = valor

class Booleano(ASTNode):
    def __init__(self, valor, line, column):
        super().__init__(line, column)
        self.valor = valor

class Variavel(ASTNode):
    def __init__(self, nome, line, column):
        super().__init__(line, column)
        self.nome = nome

class Bloco(ASTNode):
    def __init__(self, comandos, line, column):
        super().__init__(line, column)
        self.comandos = comandos
        self.escopo_nome = None

class Se(ASTNode):
    def __init__(self, condicao, bloco_if, bloco_else=None, line=0, column=0):
        super().__init__(line, column)
        self.condicao = condicao
        self.bloco_if = bloco_if
        self.bloco_else = bloco_else

class Enquanto(ASTNode):
    def __init__(self, condicao, bloco, line=0, column=0):
        super().__init__(line, column)
        self.condicao = condicao
        self.bloco = bloco

class Para(ASTNode):
    def __init__(self, inicializacao, condicao, incremento, bloco, line=0, column=0):
        super().__init__(line, column)
        self.inicializacao = inicializacao
        self.condicao = condicao
        self.incremento = incremento
        self.bloco = bloco

def _ref(simbolo):
    if simbolo is None:
        return "não declarada"
    return f"decl L{simbolo.linha}:C{simbolo.coluna}"

def imprimir_ast(node, nivel=0):
    indent = "  " * nivel
    if isinstance(node, Programa):
        print(f"{indent}Programa")
        for cmd in node.comandos:
            imprimir_ast(cmd, nivel + 1)
    elif isinstance(node, Declaracao):
        print(f"{indent}Decl {node.tipo} {node.nome} (L{node.line}:C{node.column})")
    elif isinstance(node, Atribuicao):
        print(f"{indent}Atrib {node.nome} ({_ref(node.simbolo)}) : {node.tipo_inferido}")
        imprimir_ast(node.expressao, nivel + 1)
    elif isinstance(node, Saida):
        print(f"{indent}Print")
        imprimir_ast(node.expressao, nivel + 1)
    elif isinstance(node, Binaria):
        print(f"{indent}Op({node.operador}) : {node.tipo_inferido}")
        imprimir_ast(node.esquerda, nivel + 1)
        imprimir_ast(node.direita, nivel + 1)
    elif isinstance(node, Inteiro):
        print(f"{indent}Int({node.valor}) : {node.tipo_inferido}")
    elif isinstance(node, Booleano):
        print(f"{indent}Bool({str(node.valor).lower()}) : {node.tipo_inferido}")
    elif isinstance(node, Variavel):
        print(f"{indent}Var({node.nome} -> {_ref(node.simbolo)}) : {node.tipo_inferido}")
    elif isinstance(node, Bloco):
        print(f"{indent}{node.escopo_nome or 'Bloco'}")
        if not node.comandos:
            print(f"{indent}  (vazio)")
        for cmd in node.comandos:
            imprimir_ast(cmd, nivel + 1)
    elif isinstance(node, Se):
        print(f"{indent}If")
        imprimir_ast(node.condicao, nivel + 1)
        imprimir_ast(node.bloco_if, nivel + 1)
        if node.bloco_else:
            print(f"{indent}Else")
            imprimir_ast(node.bloco_else, nivel + 1)
    elif isinstance(node, Enquanto):
        print(f"{indent}While")
        imprimir_ast(node.condicao, nivel + 1)
        imprimir_ast(node.bloco, nivel + 1)
    elif isinstance(node, Para):
        print(f"{indent}For")
        imprimir_ast(node.inicializacao, nivel + 1)
        imprimir_ast(node.condicao, nivel + 1)
        imprimir_ast(node.incremento, nivel + 1)
        imprimir_ast(node.bloco, nivel + 1)