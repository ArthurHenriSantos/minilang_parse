# Analisador Sintático (Parser) - MiniLang

## Integrantes

* `Arthur Henrique dos Santos` RA : 2018881
* `Lucas Gabriel dos Santos Silva` RA : 1996558
* `Victor Micheletti Gaspareto` RA : 2018051
* `Rafel Costa Honorio` RA : 2018872
* `José Monteiro Guedes Neto` RA : 1994079
* `Aryane Caroline da Silva de Souza` RA : 2013047
* `Sofia Pereira Deniz` RA : 2010932
* `Jeniffer Scarpini Quintan` RA : 1993338
  
## Sobre o Projeto

Este projeto implementa a segunda fase de um compilador (Análise Sintática) para a linguagem fictícia MiniLang. Ele consome a lista de tokens gerada pelo Lexer e constrói uma Árvore Sintática Abstrata (AST) que representa a hierarquia e a ordem matemática das operações.

## Como Executar

O projeto foi desenvolvido em Python puro, sem dependências externas. Para rodar a demonstração principal, utilize o comando no terminal:

```
python main.py examples/programa.min
```

### O que observar no resultado (Validação):
Ao rodar o comando acima com sucesso, o terminal imprimirá a Árvore Sintática Abstrata (AST). Para confirmar que a gramática foi implementada corretamente, verifique os seguintes pontos no terminal:

1. **Precedência Matemática (Multiplicação antes da Soma):**
   * No arquivo de teste, temos a linha `x = 2 + 3 * 4;`.
   * Na árvore impressa, observe que o nó `Binaria(*)` (contendo o 3 e o 4) está desenhado um nível **abaixo/dentro** do lado direito do nó `Binaria(+)`. Isso prova que o parser prioriza a multiplicação na estrutura.
2. **Associatividade à Esquerda:**
   * Temos a linha `print(10 - 3 - 2);`.
   * Na árvore, o parser agrupa primeiro o 10 e o 3 em uma `Binaria(-)` mais profunda à esquerda, e só depois usa esse resultado no lado esquerdo da próxima subtração por 2. Isso garante a conta matemática `(10 - 3) - 2` (resultado 5), evitando o erro comum de agrupar pela direita `10 - (3 - 2)`.
3. **Teste de Erros (Fail-Fast):**
   * Você pode editar o arquivo `programa.min` e forçar um erro de sintaxe (ex: apagar um `;` ou escrever `print(2 + );`). 
   * Ao rodar novamente, o programa deve abortar imediatamente a criação da árvore e mostrar a linha e coluna exatas do erro capturado pelo sistema de diagnósticos.

---

## Decisões de Arquitetura e Justificativas

* **Parser Descendente Recursivo (Top-Down):** A leitura dos tokens é feita de cima para baixo, partindo da regra mais geral (`programa()`) até a mais específica (`fator()`).
  * **Por que?** É a implementação mais direta e legível para gramáticas LL(1) (onde basta espiar o próximo token com o `peek()` para decidir o caminho).

* **Camadas de Precedência Matemática:** As operações matemáticas não foram validadas em uma única função. O código foi dividido em `expressao()` (somas/subtrações) e `termo()` (multiplicações/divisões).
  * **Por que?** Ao forçar a gramática a resolver o `termo()` antes de procurar por somas, garantimos estruturalmente que multiplicações fiquem mais profundas na árvore da AST, sendo resolvidas primeiro logicamente.

* **Associatividade à Esquerda usando Laços (`while`):** Em vez de usar recursividade do lado direito para resolver contas sequenciais como `10 - 3 - 2`, as funções usam laços de repetição.
  * **Por que?** Isso garante que a árvore construa primeiro o agrupamento da esquerda `(10 - 3)` e só depois subtraia o `2`, preservando a lógica matemática correta e evitando agrupar pela direita.

* **Estratégia "Fail-Fast" para Erros:** O parser utiliza uma exceção personalizada (`ParseError`) que interrompe a execução completa do programa assim que encontra qualquer símbolo inesperado.
  * **Por que?** O trabalho exigia parar no primeiro erro sintático encontrado. Isso evita relatórios de erros em cascata, que geralmente acontecem quando o código tenta adivinhar o resto de uma linha já quebrada.
