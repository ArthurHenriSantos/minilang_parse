import sys, os
from minilang.lexer import Lexer
from minilang.parser import Parser
from minilang.ast import imprimir_ast

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
    else:
        print("\n=== AST GERADA COM SUCESSO ===")
        imprimir_ast(resultado)

if __name__ == "__main__":
    main()