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
        return print(f"Erro Léxico: {erros[0].message} na linha {erros[0].line}")

    parser = Parser(tokens)
    resultado = parser.parse()

    if isinstance(resultado, Exception):
        print(resultado)
    else:
        imprimir_ast(resultado)

if __name__ == "__main__":
    main()

