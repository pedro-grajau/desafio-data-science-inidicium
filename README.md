# Cinema em dados · do catálogo IMDb à decisão de um estúdio

Projeto de ciência de dados desenvolvido a partir do desafio Lighthouse da Indicium. A PProductions quer orientar sua próxima produção. O estudo usa 999 filmes para investigar desempenho comercial, recomendar um título a um espectador desconhecido e estimar a nota IMDb após o lançamento.

**Aventura merece investigação comercial.** Entre as aventuras com ano e receita conhecidos, 57,4% chegaram ao quarto superior de bilheteria de sua década. Nos demais filmes, foram 17,3%. A base reúne filmes muito bem avaliados, e faltam dados sobre orçamento e distribuição. O resultado orienta a seleção de projetos para análise financeira.

| Pergunta | Resultado observado |
|---|---|
| Qual filme indicar sem conhecer o gosto da pessoa? | *The Godfather* ficou em primeiro ao combinar nota e volume de votos. |
| O que a sinopse revela? | O texto identificou temas e gêneros. O Jaccard médio por filme foi de 39,5%, ante 36,6% ao sugerir sempre drama. |
| Qual a precisão da estimativa de nota? | Em 200 filmes, a floresta aleatória teve erro absoluto médio de 0,154 ponto, ante 0,207 da referência. |
| Qual a previsão para o exemplo do desafio? | **8,7** para *The Shawshank Redemption*. |

O [relatório de decisões e resultados](relatorios/relatorio.md) percorre os pontos 1 a 5 e discute os limites de cada conclusão. As [tabelas reproduzíveis](relatorios/evidencias.md) detalham todas as décadas, comparações e métricas.

## Instalar e prever

Ambiente usado: Python 3.13.5, Windows de 64 bits. Execute na raiz do repositório com PowerShell.

```powershell
python -m venv .venv
& .venv/Scripts/python.exe -m pip install -r requirements.txt
& .venv/Scripts/python.exe scripts/prever.py exemplos/shawshank.json
```

A saída esperada é **8.7** (8.7361 antes do arredondamento). O [modelo treinado](modelos/modelo_imdb.pkl) acompanha o projeto. A previsão funciona sem o CSV de treinamento. Mantenha [entradas.py](scripts/entradas.py) junto ao [programa de inferência](scripts/prever.py), pois o pipeline usa a função de transformação desse módulo. Para outro filme, forneça um JSON com os cinco campos do [exemplo](exemplos/shawshank.json). O título serve apenas para identificação.

## Reproduzir as análises e o treinamento

Use uma cópia autorizada de `desafio_indicium_imdb.csv`. O CSV bruto e o enunciado original ficam fora da distribuição. SHA-256 da base usada: `fff1a7372358bfa14d0632db924d3063dd4cfcd02190334f1c992296f9b0668b`.

```powershell
$dados = 'C:/caminho/para/desafio_indicium_imdb.csv'
& .venv/Scripts/python.exe scripts/analisar.py $dados
& .venv/Scripts/python.exe scripts/treinar.py $dados
& .venv/Scripts/python.exe scripts/prever.py exemplos/shawshank.json
```

[Analisar](scripts/analisar.py) regenera as tabelas de evidências. [Treinar](scripts/treinar.py) compara os modelos, imprime as métricas e grava o pipeline da avaliação em formato pickle. A execução verifica se o pipeline serializado reproduz as previsões dos 200 filmes de teste. As versões das dependências estão em [requirements.txt](requirements.txt).
