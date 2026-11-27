from minilang.lexer import Diagnostic
from minilang.ast import Programa, Declaracao, Atribuicao, Saida, Binaria, Inteiro, Booleano, Variavel, Bloco, Se, Enquanto, Para

class Simbolo:
    def __init__(self, nome, tipo, linha, coluna, escopo):
        self.nome = nome
        self.tipo = tipo
        self.linha = linha
        self.coluna = coluna
        self.escopo = escopo

class AnalisadorSemantico:
    def __init__(self):
        global_scope = {"nome": "Global", "pai": None, "vars": {}}
        self.pilha = [global_scope]
        self.escopos = [global_scope]
        self.num_bloco = 0
        self.diagnosticos = []

    def add_erro(self, linha, col, msg):
        self.diagnosticos.append(Diagnostic(linha, col, msg))

    def buscar_var(self, nome):
        for esc in reversed(self.pilha):
            if nome in esc["vars"]:
                return esc["vars"][nome]
        return None

    def analisar(self, no):
        if isinstance(no, Programa):
            for c in no.comandos:
                self.analisar(c)

        elif isinstance(no, Bloco):
            self.num_bloco += 1
            pai = self.pilha[-1]["nome"]
            novo = {"nome": f"Bloco {self.num_bloco} (L{no.line}:C{no.column})", "pai": pai, "vars": {}}
            no.escopo_nome = novo["nome"]
            self.pilha.append(novo)
            self.escopos.append(novo)
            for c in no.comandos:
                self.analisar(c)
            self.pilha.pop()

        elif isinstance(no, Declaracao):
            atual = self.pilha[-1]
            if no.nome in atual["vars"]:
                velho = atual["vars"][no.nome]
                self.add_erro(no.line, no.column, f"Variável '{no.nome}' já declarada em Linha {velho.linha}, Col {velho.coluna}.")
            else:
                s = Simbolo(no.nome, no.tipo, no.line, no.column, atual["nome"])
                atual["vars"][no.nome] = s
                no.simbolo = s

        elif isinstance(no, Atribuicao):
            s = self.buscar_var(no.nome)
            no.simbolo = s
            tipo_val = self.checar_expr(no.expressao)

            if s is None:
                self.add_erro(no.line, no.column, f"Variável '{no.nome}' não foi declarada.")
                no.tipo_inferido = "<erro>"
            else:
                no.tipo_inferido = s.tipo
                if tipo_val != "<erro>" and s.tipo != tipo_val:
                    self.add_erro(no.line, no.column, f"Tipo incompatível em '{no.nome}': esperado {s.tipo}, veio {tipo_val}.")

        elif isinstance(no, Saida):
            self.checar_expr(no.expressao)

        elif isinstance(no, Se):
            t = self.checar_expr(no.condicao)
            if t != "<erro>" and t != "bool":
                self.add_erro(no.condicao.line, no.condicao.column, f"If precisa de condição bool, mas veio {t}.")
            self.analisar(no.bloco_if)
            if no.bloco_else:
                self.analisar(no.bloco_else)

        elif isinstance(no, Enquanto):
            t = self.checar_expr(no.condicao)
            if t != "<erro>" and t != "bool":
                self.add_erro(no.condicao.line, no.condicao.column, f"While precisa de condição bool, mas veio {t}.")
            self.analisar(no.bloco)

        elif isinstance(no, Para):
            self.analisar(no.inicializacao)
            t = self.checar_expr(no.condicao)
            if t != "<erro>" and t != "bool":
                self.add_erro(no.condicao.line, no.condicao.column, f"Condição do for precisa ser bool, mas veio {t}.")
            self.analisar(no.incremento)
            self.analisar(no.bloco)

    def checar_expr(self, expr):
        if isinstance(expr, Inteiro):
            expr.tipo_inferido = "int"
            return "int"

        if isinstance(expr, Booleano):
            expr.tipo_inferido = "bool"
            return "bool"

        if isinstance(expr, Variavel):
            s = self.buscar_var(expr.nome)
            expr.simbolo = s
            if s is None:
                self.add_erro(expr.line, expr.column, f"Variável '{expr.nome}' não declarada.")
                expr.tipo_inferido = "<erro>"
                return "<erro>"
            expr.tipo_inferido = s.tipo
            return s.tipo

        if isinstance(expr, Binaria):
            esq = self.checar_expr(expr.esquerda)
            dir = self.checar_expr(expr.direita)

            if esq == "<erro>" or dir == "<erro>":
                expr.tipo_inferido = "<erro>"
                return "<erro>"

            op = expr.operador
            if op in ("+", "-", "*", "/"):
                if esq == "int" and dir == "int":
                    expr.tipo_inferido = "int"
                    return "int"
                self.add_erro(expr.line, expr.column, f"Operação '{op}' só aceita int, recebeu {esq} e {dir}.")
                expr.tipo_inferido = "<erro>"
                return "<erro>"

            if op in ("<", "<=", ">", ">="):
                if esq == "int" and dir == "int":
                    expr.tipo_inferido = "bool"
                    return "bool"
                self.add_erro(expr.line, expr.column, f"Comparação '{op}' só aceita int, recebeu {esq} e {dir}.")
                expr.tipo_inferido = "<erro>"
                return "<erro>"

            if op in ("==", "!="):
                if esq == dir:
                    expr.tipo_inferido = "bool"
                    return "bool"
                self.add_erro(expr.line, expr.column, f"Operador '{op}' exige tipos iguais, recebeu {esq} e {dir}.")
                expr.tipo_inferido = "<erro>"
                return "<erro>"

        return "<erro>"

    def imprimir_tabelas_simbolos(self):
        for esc in self.escopos:
            print(f"\n[{esc['nome']}]")
            if len(esc["vars"]) == 0:
                print("  (vazio)")
            else:
                for s in esc["vars"].values():
                    print(f"  {s.nome}: {s.tipo} (L{s.linha}:C{s.coluna})")