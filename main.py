import sys, os
from minilang.lexer import Lexer
from minilang.parser import Parser
from minilang.ast import imprimir_ast
from minilang.semantic import AnalisadorSemantico

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo.min>")
        return

    arq = sys.argv[1]
    if not os.path.exists(arq):
        return print(f"Arquivo '{arq}' não encontrado.")

    with open(arq, 'r', encoding='utf-8') as f:
        codigo = f.read()

    lexer = Lexer(codigo)
    tokens, erros_lex = lexer.scan_tokens()
    if erros_lex:
        print("Erros léxicos encontrados:")
        for e in erros_lex:
            print(f"  L{e.line}:C{e.column} -> {e.message}")
        return

    parser = Parser(tokens)
    res = parser.parse()

    if isinstance(res, Exception):
        print("\nErro sintático:")
        print(res)
        return

    sem = AnalisadorSemantico()
    sem.analisar(res)

    print("\n--- Tabelas de Símbolos ---")
    sem.imprimir_tabelas_simbolos()

    print("\n--- AST Anotada ---")
    imprimir_ast(res)

    print("\n--- Diagnósticos Semânticos ---")
    if len(sem.diagnosticos) == 0:
        print("Nenhum erro semântico.")
    else:
        for d in sem.diagnosticos:
            print(f"[Linha {d.line}, Col {d.column}] {d.message}")

if __name__ == "__main__":
    main()