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

def _fmt_vinculo(simbolo):
    if simbolo is None:
        return "vínculo: <não declarada>"
    return f"vínculo: {simbolo.nome}@{simbolo.escopo} (L{simbolo.linha}:C{simbolo.coluna})"

def _fmt_tipo(tipo):
    return f"tipo: {tipo}" if tipo else ""

def imprimir_ast(node, nivel=0):
    indent = "  " * nivel
    if isinstance(node, Programa):
        print(f"{indent}Programa")
        for cmd in node.comandos:
            imprimir_ast(cmd, nivel + 1)
    elif isinstance(node, Declaracao):
        print(f"{indent}Declaracao({node.tipo} {node.nome}) [L{node.line}:C{node.column}]")
    elif isinstance(node, Atribuicao):
        print(f"{indent}Atribuicao({node.nome}) [{_fmt_vinculo(node.simbolo)} | {_fmt_tipo(node.tipo_inferido)}]")
        imprimir_ast(node.expressao, nivel + 1)
    elif isinstance(node, Saida):
        print(f"{indent}Saida [L{node.line}:C{node.column}]")
        imprimir_ast(node.expressao, nivel + 1)
    elif isinstance(node, Binaria):
        print(f"{indent}Binaria({node.operador}) [{_fmt_tipo(node.tipo_inferido)}]")
        imprimir_ast(node.esquerda, nivel + 1)
        imprimir_ast(node.direita, nivel + 1)
    elif isinstance(node, Inteiro):
        print(f"{indent}Inteiro({node.valor}) [{_fmt_tipo(node.tipo_inferido)}]")
    elif isinstance(node, Booleano):
        print(f"{indent}Booleano({str(node.valor).lower()}) [{_fmt_tipo(node.tipo_inferido)}]")
    elif isinstance(node, Variavel):
        print(f"{indent}Variavel({node.nome}) [{_fmt_vinculo(node.simbolo)} | {_fmt_tipo(node.tipo_inferido)}]")
    elif isinstance(node, Bloco):
        nome = f" ({node.escopo_nome})" if node.escopo_nome else ""
        print(f"{indent}Bloco{nome} [L{node.line}:C{node.column}]")
        if not node.comandos:
            print(f"{indent}  (vazio)")
        for cmd in node.comandos:
            imprimir_ast(cmd, nivel + 1)
    elif isinstance(node, Se):
        print(f"{indent}Se [L{node.line}:C{node.column}]")
        imprimir_ast(node.condicao, nivel + 1)
        imprimir_ast(node.bloco_if, nivel + 1)
        if node.bloco_else:
            print(f"{indent}Senao")
            imprimir_ast(node.bloco_else, nivel + 1)
    elif isinstance(node, Enquanto):
        print(f"{indent}Enquanto [L{node.line}:C{node.column}]")
        imprimir_ast(node.condicao, nivel + 1)
        imprimir_ast(node.bloco, nivel + 1)
    elif isinstance(node, Para):
        print(f"{indent}Para [L{node.line}:C{node.column}]")
        print(f"{indent}  Inicializacao:")
        imprimir_ast(node.inicializacao, nivel + 2)
        print(f"{indent}  Condicao:")
        imprimir_ast(node.condicao, nivel + 2)
        print(f"{indent}  Incremento:")
        imprimir_ast(node.incremento, nivel + 2)
        print(f"{indent}  Bloco:")
        imprimir_ast(node.bloco, nivel + 2)