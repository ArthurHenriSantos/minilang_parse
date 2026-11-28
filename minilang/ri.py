from minilang.ast import Programa, Declaracao, Atribuicao, Saida, Binaria, Inteiro, Booleano, Variavel, Bloco

class Instrucao:
    def __init__(self, op, arg1=None, arg2=None, dest=None):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.dest = dest

    def _fmt(self, val):
        if isinstance(val, bool):
            return "true" if val else "false"
        return str(val)

    def __str__(self):
        if self.op == "ASSIGN":
            return f"{self.dest} = {self._fmt(self.arg1)}"
        if self.op == "PRINT":
            return f"PRINT {self._fmt(self.arg1)}"
        return f"{self.dest} = {self._fmt(self.arg1)} {self.op} {self._fmt(self.arg2)}"


class GeradorRI:
    def __init__(self):
        self.instrucoes = []
        self.temp_count = 0

    def novo_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def emitir(self, op, arg1=None, arg2=None, dest=None):
        self.instrucoes.append(Instrucao(op, arg1, arg2, dest))

    def gerar(self, no):
        if isinstance(no, Programa):
            for cmd in no.comandos:
                self.gerar(cmd)

        elif isinstance(no, Bloco):
            for cmd in no.comandos:
                self.gerar(cmd)

        elif isinstance(no, Declaracao):
            pass

        elif isinstance(no, Atribuicao):
            val = self.gerar_expr(no.expressao)
            self.emitir("ASSIGN", val, None, no.nome)

        elif isinstance(no, Saida):
            val = self.gerar_expr(no.expressao)
            self.emitir("PRINT", val)

    def gerar_expr(self, expr):
        if isinstance(expr, Inteiro):
            return expr.valor

        if isinstance(expr, Booleano):
            return expr.valor

        if isinstance(expr, Variavel):
            return expr.nome

        if isinstance(expr, Binaria):
            esq = self.gerar_expr(expr.esquerda)
            dir = self.gerar_expr(expr.direita)
            temp = self.novo_temp()
            self.emitir(expr.operador, esq, dir, temp)
            return temp

        return None

    def imprimir(self):
        for inst in self.instrucoes:
            print(f"  {inst}")