# Analisador Sintático (Parser) - MiniLang

## Integrantes
- `Arthur Henrique dos Santos` RA : 2018881
- `Lucas Gabriel dos Santos Silva` RA : 1996558
- `Victor Micheletti Gaspareto` RA : 2018051
- `Rafel Costa Honorio` RA : 2018872
- `José Monteiro Guedes Neto` RA : 1994079
- `Aryane Caroline da Silva de Souza` RA : 2013047
- `Sofia Pereira Deniz` RA : 2010932
- `Jeniffer Scarpini Quintan` RA : 1993338
  
## Sobre o Projeto
Este projeto implementa a segunda fase de um compilador (Análise Sintática) para a linguagem fictícia MiniLang. Ele consome a lista de tokens gerada pelo Lexer e constrói uma Árvore Sintática Abstrata (AST) que representa a hierarquia e a ordem matemática das operações, além de suportar estruturação avançada com blocos e controle de fluxo.

## Como Executar
O projeto foi desenvolvido em Python puro, sem dependências externas. Para rodar a demonstração principal, utilize o comando no terminal:

`python main.py examples/programa.min`

### O que observar no resultado (Validação):
Ao rodar o comando acima com sucesso, o terminal imprimirá a Árvore Sintática Abstrata (AST). Para confirmar que a gramática foi implementada corretamente, verifique os seguintes pontos no terminal:

1. **Precedência Matemática (Multiplicação antes da Soma):** No arquivo de teste, temos a linha `x = 2 + 3 * 4;`. Na árvore impressa, observe que o nó `Binaria(*)` (contendo o 3 e o 4) está desenhado um nível **abaixo/dentro** do lado direito do nó `Binaria(+)`. Isso prova que o parser prioriza a multiplicação na estrutura.
2. **Associatividade à Esquerda:** Temos a linha `print(10 - 3 - 2);`. Na árvore, o parser agrupa primeiro o 10 e o 3 em uma `Binaria(-)` mais profunda à esquerda, e só depois usa esse resultado no lado esquerdo da próxima subtração por 2. Isso garante a conta matemática `(10 - 3) - 2` (resultado 5), evitando o erro comum de agrupar pela direita `10 - (3 - 2)`.
3. **Estruturas de Controle e Aninhamento:** Verifique que o `if`, `while` e `for` geram nós específicos na árvore, contendo uma `Condicao` (com operadores relacionais como `<` ou `>`) e um nó de `Bloco` abrigando os comandos internos. No laço `for`, observe a divisão clara e funcional na AST entre `Inicializacao`, `Condicao`, `Incremento` e o `Bloco` de execução.
4. **Teste de Erros (Fail-Fast):** Você pode editar o arquivo `programa.min` e forçar um erro de sintaxe (ex: apagar um `;` ou não fechar uma chave `{`). Ao rodar novamente, o programa deve abortar imediatamente a criação da árvore e mostrar a linha e coluna exatas do erro capturado pelo sistema de diagnósticos.

---

## Decisões de Arquitetura e Justificativas

* **Parser Descendente Recursivo (Top-Down):** A leitura dos tokens é feita de cima para baixo, partindo da regra mais geral (`programa()`) até a mais específica (`fator()`). É a implementação mais direta e legível para gramáticas LL(1).
* **Uso Obrigatório de Blocos (`{ }`) nas Estruturas de Controle:** Comandos como `if/else`, `while` e `for` exigem a abertura e fechamento explícito de blocos de chaves. Esta restrição gramatical resolve automaticamente a ambiguidade clássica do "Dangling Else" (else pendente).
* **Isolamento de Operadores Relacionais (`Condicao`):** Criamos um nó específico (`Condicao`) na AST estritamente para operadores como `<`, `>`, `==`, etc. Isso impede que comparações lógicas se misturem diretamente com a matemática pura.
* **Desmembramento do Laço `for` na AST:** A implementação do comando `for` reaproveita as regras gramaticais de `atribuicao` e `condicao`, dividindo o laço em três etapas lógicas fisicamente separadas na árvore para facilitar a semântica posterior.
* **Camadas de Precedência Matemática:** As operações matemáticas não foram validadas em uma única função. O código foi dividido em `expressao()` (somas/subtrações) e `termo()` (multiplicações/divisões) para forçar as multiplicações a ficarem mais profundas na árvore.
* **Associatividade à Esquerda usando Laços (`while`):** Em vez de usar recursividade do lado direito para resolver contas sequenciais como `10 - 3 - 2`, as funções usam laços de repetição, preservando a lógica matemática correta.
* **Estratégia "Fail-Fast" para Erros:** O parser utiliza uma exceção personalizada (`ParseError`) que interrompe a execução completa do programa assim que encontra qualquer símbolo inesperado, evitando relatórios de erros em cascata.