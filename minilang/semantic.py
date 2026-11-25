from dataclasses import dataclass
from minilang.lexer import Diagnostic
from minilang.ast import (
    Programa, Declaracao, Atribuicao, Saida, Binaria,
    Inteiro, Booleano, Variavel, Bloco, Se, Enquanto, Para
)

TIPO_ERRO = "<erro>"

@dataclass
class Simbolo:
    nome: str
    tipo: str
    linha: int
    coluna: int
    escopo: str

class Escopo:
    def __init__(self, nome: str, pai=None):
        self.nome = nome
        self.pai = pai
        self.simbolos = {}

    def declarar(self, simbolo: Simbolo):
        if simbolo.nome in self.simbolos:
            return False, self.simbolos[simbolo.nome]
        self.simbolos[simbolo.nome] = simbolo
        return True, simbolo

    def buscar(self, nome: str):
        if nome in self.simbolos:
            return self.simbolos[nome]
        if self.pai is not None:
            return self.pai.buscar(nome)
        return None

class AnalisadorSemantico:
    def __init__(self):
        self.escopo_global = Escopo("Global")
        self.escopo_atual = self.escopo_global
        self.todos_escopos = [self.escopo_global]
        self.contador_blocos = 0
        self.diagnosticos = []

    def reportar(self, linha, coluna, mensagem):
        self.diagnosticos.append(Diagnostic(linha, coluna, mensagem))

    def entrar_escopo(self, linha, coluna):
        self.contador_blocos += 1
        nome = f"Bloco {self.contador_blocos} (L{linha}:C{coluna})"
        novo = Escopo(nome, pai=self.escopo_atual)
        self.todos_escopos.append(novo)
        self.escopo_atual = novo
        return novo

    def sair_escopo(self):
        if self.escopo_atual.pai is not None:
            self.escopo_atual = self.escopo_atual.pai

    def analisar(self, node):
        if isinstance(node, Programa):
            for cmd in node.comandos:
                self.analisar(cmd)

        elif isinstance(node, Bloco):
            escopo = self.entrar_escopo(node.line, node.column)
            node.escopo_nome = escopo.nome
            for cmd in node.comandos:
                self.analisar(cmd)
            self.sair_escopo()

        elif isinstance(node, Declaracao):
            simbolo = Simbolo(node.nome, node.tipo, node.line, node.column, self.escopo_atual.nome)
            sucesso, existente = self.escopo_atual.declarar(simbolo)
            if not sucesso:
                self.reportar(
                    node.line, node.column,
                    f"Redeclaração da variável '{node.nome}' no escopo {self.escopo_atual.nome} "
                    f"(já declarada em Linha {existente.linha}, Col {existente.coluna})."
                )
            else:
                node.simbolo = simbolo

        elif isinstance(node, Atribuicao):
            simbolo = self.escopo_atual.buscar(node.nome)
            node.simbolo = simbolo
            tipo_expr = self.analisar_expressao(node.expressao)

            if simbolo is None:
                self.reportar(
                    node.line, node.column,
                    f"Variável '{node.nome}' não declarada neste escopo."
                )
                node.tipo_inferido = TIPO_ERRO
            else:
                node.tipo_inferido = simbolo.tipo
                # Só reporta incompatibilidade se a expressão não tiver falhado antes (evita cascata)
                if tipo_expr != TIPO_ERRO and simbolo.tipo != tipo_expr:
                    self.reportar(
                        node.line, node.column,
                        f"Atribuição incompatível para '{node.nome}': esperado '{simbolo.tipo}', recebido '{tipo_expr}'."
                    )

        elif isinstance(node, Saida):
            self.analisar_expressao(node.expressao)

        elif isinstance(node, Se):
            tipo_cond = self.analisar_expressao(node.condicao)
            if tipo_cond != TIPO_ERRO and tipo_cond != "bool":
                self.reportar(
                    node.condicao.line, node.condicao.column,
                    f"Condição do 'if' deve ser do tipo 'bool', recebido '{tipo_cond}'."
                )
            self.analisar(node.bloco_if)
            if node.bloco_else:
                self.analisar(node.bloco_else)

        elif isinstance(node, Enquanto):
            tipo_cond = self.analisar_expressao(node.condicao)
            if tipo_cond != TIPO_ERRO and tipo_cond != "bool":
                self.reportar(
                    node.condicao.line, node.condicao.column,
                    f"Condição do 'while' deve ser do tipo 'bool', recebido '{tipo_cond}'."
                )
            self.analisar(node.bloco)

        elif isinstance(node, Para):
            self.analisar(node.inicializacao)
            tipo_cond = self.analisar_expressao(node.condicao)
            if tipo_cond != TIPO_ERRO and tipo_cond != "bool":
                self.reportar(
                    node.condicao.line, node.condicao.column,
                    f"Condição do 'for' deve ser do tipo 'bool', recebido '{tipo_cond}'."
                )
            self.analisar(node.incremento)
            self.analisar(node.bloco)

    def analisar_expressao(self, expr):
        if isinstance(expr, Inteiro):
            expr.tipo_inferido = "int"
            return "int"

        elif isinstance(expr, Booleano):
            expr.tipo_inferido = "bool"
            return "bool"

        elif isinstance(expr, Variavel):
            simbolo = self.escopo_atual.buscar(expr.nome)
            expr.simbolo = simbolo
            if simbolo is None:
                self.reportar(
                    expr.line, expr.column,
                    f"Variável '{expr.nome}' não declarada neste escopo."
                )
                expr.tipo_inferido = TIPO_ERRO
                return TIPO_ERRO
            expr.tipo_inferido = simbolo.tipo
            return simbolo.tipo

        elif isinstance(expr, Binaria):
            tipo_esq = self.analisar_expressao(expr.esquerda)
            tipo_dir = self.analisar_expressao(expr.direita)

            # Propaga erro silenciosamente para não duplicar diagnósticos
            if tipo_esq == TIPO_ERRO or tipo_dir == TIPO_ERRO:
                expr.tipo_inferido = TIPO_ERRO
                return TIPO_ERRO

            if expr.operador in ("+", "-", "*", "/"):
                if tipo_esq == "int" and tipo_dir == "int":
                    expr.tipo_inferido = "int"
                    return "int"
                self.reportar(
                    expr.line, expr.column,
                    f"Operador aritmético '{expr.operador}' requer operandos 'int', recebido '{tipo_esq}' e '{tipo_dir}'."
                )
                expr.tipo_inferido = TIPO_ERRO
                return TIPO_ERRO

            if expr.operador in ("<", "<=", ">", ">="):
                if tipo_esq == "int" and tipo_dir == "int":
                    expr.tipo_inferido = "bool"
                    return "bool"
                self.reportar(
                    expr.line, expr.column,
                    f"Operador relacional '{expr.operador}' requer operandos 'int', recebido '{tipo_esq}' e '{tipo_dir}'."
                )
                expr.tipo_inferido = TIPO_ERRO
                return TIPO_ERRO

            if expr.operador in ("==", "!="):
                if tipo_esq == tipo_dir:
                    expr.tipo_inferido = "bool"
                    return "bool"
                self.reportar(
                    expr.line, expr.column,
                    f"Operador '{expr.operador}' requer operandos do mesmo tipo, recebido '{tipo_esq}' e '{tipo_dir}'."
                )
                expr.tipo_inferido = TIPO_ERRO
                return TIPO_ERRO

        return TIPO_ERRO

    def imprimir_tabelas_simbolos(self):
        for escopo in self.todos_escopos:
            pai = f" (pai: {escopo.pai.nome})" if escopo.pai else ""
            print(f"\nEscopo: {escopo.nome}{pai}")
            if not escopo.simbolos:
                print("  (vazio)")
            else:
                print(f"  {'Nome':<15} {'Tipo':<8} {'Posição'}")
                print(f"  {'-'*15} {'-'*8} {'-'*12}")
                for simb in escopo.simbolos.values():
                    print(f"  {simb.nome:<15} {simb.tipo:<8} Linha {simb.linha}, Col {simb.coluna}")