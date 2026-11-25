import sys, os
from minilang.lexer import Lexer
from minilang.parser import Parser
from minilang.ast import imprimir_ast
from minilang.semantic import AnalisadorSemantico

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo.min>")
        return

    caminho = sys.argv[1]
    if not os.path.exists(caminho):
        return print(f"Erro: arquivo '{caminho}' não encontrado.")

    with open(caminho, 'r', encoding='utf-8') as f:
        codigo = f.read()

    lexer = Lexer(codigo)
    tokens, erros = lexer.scan_tokens()
    if erros:
        print("=== ERROS LÉXICOS ===")
        for erro in erros:
            print(f"Linha {erro.line}, Col {erro.column}: {erro.message}")
        return

    parser = Parser(tokens)
    resultado = parser.parse()

    if isinstance(resultado, Exception):
        print("\n=== ERRO SINTÁTICO ===")
        print(resultado)
        return

    semantico = AnalisadorSemantico()
    semantico.analisar(resultado)

    print("\n=== TABELAS DE SÍMBOLOS POR ESCOPO ===")
    semantico.imprimir_tabelas_simbolos()

    print("\n=== AST ANOTADA ===")
    imprimir_ast(resultado)

    print("\n=== DIAGNÓSTICOS SEMÂNTICOS ===")
    if not semantico.diagnosticos:
        print("Nenhum erro semântico encontrado.")
    else:
        for d in semantico.diagnosticos:
            print(f"[Linha {d.line}, Col {d.column}] {d.message}")

if __name__ == "__main__":
    main()